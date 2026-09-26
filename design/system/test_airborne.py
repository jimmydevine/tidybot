"""Check new architecture accounting, mission energy and collision regressions."""
import copy
import unittest
import build as base
import airborne_study as study


class AirborneStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=base.read();cls.d=study.read();cls.r=study.study(cls.c,cls.d)

    def test_airborne_bottom_has_one_core_pack_and_no_ground_drivetrain(self):
        for case in self.r['cases'].values():
            rows=case['assembly']['rows'];ids={r['hardware_id'] for r in rows}
            self.assertFalse(ids & {'drive_motor','drive_wheel','wheel_hub','pod','caster','roboclaw','blower','extension_drive'})
            self.assertEqual(sum(r['qty'] for r in rows if r['instance']=='battery'),1)
            self.assertEqual(sum(r['qty'] for r in rows if r['hardware_id']=='battery_cartridge'),1)
            self.assertIn('air_feet',ids);self.assertIn('air_root',ids);self.assertIn('air_io',ids)
            self.assertTrue(all(r['module']!='cap' for r in rows))

    def test_mass_replacement_keeps_core_and_top_unchanged(self):
        old=base.assembly(self.c,'dust','octo10')
        new=self.r['cases']['octo10']['assembly']
        for module in ('core','battery','lift'):
            self.assertEqual(sum(r['mass_g'][1] for r in old['rows'] if r['module']==module),
                             sum(r['mass_g'][1] for r in new['rows'] if r['module']==module))
        expected=self.r['old_bottom_nominal_g']-self.r['new_bottom_mass_g'][1]+self.c['bottoms']['dust']['payload_g']-self.d['payload_g'][1]
        self.assertAlmostEqual(old['mass_g'][1]-new['mass_g'][1],expected)

    def test_mission_counts_both_legs_and_landing_reserve(self):
        m=dict(outbound_s=60,return_s=60,landing_reserve_s=60,transit_power_factor=1,
               cleaning_power_factor=1,energy_margin_fraction=0)
        self.assertAlmostEqual(study.mission(600,0,40,m)['cleaning_seconds'],60)
        m['return_s']=120
        self.assertAlmostEqual(study.mission(600,0,40,m)['cleaning_seconds'],0)
        m['return_s']=180
        self.assertFalse(study.mission(600,0,40,m)['transit_reserve_feasible'])
        self.assertIsNone(study.mission(None,0,40,m))

    def test_energy_balance_includes_contact_power_and_margin(self):
        m=self.d['missions']['local_dusting'];hover=1700;tool=2;energy=92.352
        result=study.mission(hover,tool,energy,m)
        check=study.mission(hover,tool,energy,m,result['cleaning_seconds'])
        self.assertAlmostEqual(check['required_usable_wh'],energy)

    def test_quad_static_loads_balance_force_moments_and_yaw(self):
        a=self.r['cases']['quad10']['assembly'];trim=study.quad_balance(a,self.c)
        xy=self.c['lift']['variants']['quad10']['rotors_xy_relative_mm'];f=trim['fractions']
        self.assertAlmostEqual(sum(f),1)
        for axis in (0,1):self.assertAlmostEqual(sum(w*p[axis] for w,p in zip(f,xy)),a['cg_mm'][axis]-137.5)
        self.assertAlmostEqual(f[0]-f[1]+f[2]-f[3],0)
        self.assertFalse(self.r['cases']['quad10']['screen']['static_trim']['meets_2_to_1_static_screen'])

    def test_current_tube_route_clears_lift_and_core_allocations(self):
        for key,v in self.r['cases'].items():self.assertEqual(v['screen']['geometry_errors'],[],key)

    def test_centred_boom_would_hit_hex_central_support(self):
        d=copy.deepcopy(self.d);d['boom']['root_mm'][0]=137.5
        r=study.study(self.c,d)
        self.assertTrue(any('beam_nose_1' in e for e in r['cases']['hex10']['screen']['geometry_errors']))

    def test_new_ducts_do_not_inherit_propeller_performance(self):
        for layout in self.r['layouts'][1:]:
            self.assertIsNone(layout['matched_hover_power_w'])
            self.assertIsNone(layout['installed_top_mass_g'])
            self.assertFalse(layout['flight_qualified'])
            self.assertGreaterEqual(layout['minimum_body_radial_clearance_mm'],9.99)

    def test_storage_allocation_includes_head_after_rotation(self):
        self.assertTrue(all(x>0 for x in self.r['parked_boom']['clearance_mm']))
        d=copy.deepcopy(self.d);d['station_boom_rack_mm'][1]=50
        self.assertLess(study.parked_boom(d)['clearance_mm'][1],0)

    def test_ground_design_is_not_mutated(self):
        c=copy.deepcopy(self.c);study.study(c,self.d)
        self.assertEqual(c,self.c)
        self.assertEqual(base.extension_metrics(c)['travel_mm'],1000)

    def test_rear_balance_keeps_mass_and_cameras_improves_trim(self):
        front=self.r['front_reference'];rear=self.r['cases']['quad10']
        self.assertEqual(front['mass_g'],rear['assembly']['mass_g'])
        self.assertGreater(rear['screen']['static_trim']['static_peak_thrust_weight'],front['static_peak_thrust_weight'])
        rows=rear['assembly']['rows'];parts={p['id']:p for p in rear['assembly']['parts']}
        cameras=[r for r in rows if r['module']=='lift' and r['hardware_id']=='depth_camera']
        self.assertEqual(sum(r['qty'] for r in cameras),2)
        for row in cameras:self.assertEqual(row['cg_mm'],base.centre(parts[row['part']]))
        self.assertEqual(sum(r['qty'] for r in rows if r['hardware_id']=='flight_controller'),1)

    def test_edf_replaces_all_propulsion_and_keeps_payload_mass(self):
        for fan in self.r['ducted_comparison']['candidates']:
            for i in range(3):
                self.assertAlmostEqual(fan['top_mass_g'][i],sum(row['mass_g'][i] for row in fan['ledger']))
                for bottom,case in fan['cases'].items():
                    old=self.r['cases']['quad10']['assembly'] if bottom=='air_dust' else base.assembly(self.c,bottom,'quad10')
                    carried=sum(row['mass_g'][i] for row in old['rows'] if row['module']!='lift')
                    self.assertAlmostEqual(case['mass_g'][i],carried+fan['top_mass_g'][i])

    def test_edf_unknown_hover_does_not_become_zero_energy(self):
        fan=self.r['ducted_comparison']['candidates'][1]
        for case in fan['cases'].values():
            self.assertIsNone(case['hover_w']);self.assertIsNone(case['transfer'])
            self.assertFalse(case['flight_qualified']);self.assertFalse(case['trim_and_yaw_qualified'])
        self.assertIsNone(fan['cases']['air_dust']['local_dusting'])

    def test_edf_trip_and_loss_sensitivity(self):
        fan=self.r['ducted_comparison']['candidates'][0]
        case=fan['cases']['air_dust'];tws=case['peak_tw_retention_sensitivity']
        self.assertLess(tws[0],tws[1]);self.assertLess(tws[1],tws[2])
        self.assertFalse(case['local_dusting']['transit_reserve_feasible'])
        self.assertGreater(case['local_dusting']['required_usable_wh'],self.r['usable_pack_wh'])
        transfer=fan['cases']['vacuum']['transfer']
        self.assertEqual(transfer['return_s'],0)
        self.assertAlmostEqual(transfer['required_usable_wh'],fan['cases']['vacuum']['hover_w']*(45*1.2+30)/3600*1.2)


if __name__=='__main__':unittest.main()
