"""Model tests cover accounting and meaningful failure cases, not real hardware."""
import copy
import itertools
import math
import unittest
import build as model

class SystemDesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=model.read();cls.r=model.build(cls.c)

    def test_all_ground_allocations_clear(self):
        for k,v in self.r['checks'].items():self.assertEqual(v['errors'],[],k)

    def test_overlap_checker_catches_bad_placement(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['parts'])
        next(p for p in parts if p['id']=='lidar')['min']=[30,170,100]
        self.assertTrue(any('lidar / filter_bay' in s for s in model.allocation_checks(self.c,parts,'vacuum')['errors']))

    def test_nested_component_outside_carrier_is_error(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['parts'])
        next(p for p in parts if p['id']=='pi_reference')['min'][0]=280
        self.assertTrue(any('Reference outside bay: pi_reference' in s for s in model.allocation_checks(self.c,parts,'vacuum')['errors']))

    def test_sibling_references_cannot_share_space(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['parts'])
        next(p for p in parts if p['id']=='sink_reference')['min'][2]=91
        self.assertTrue(any('Nested reference overlap:' in s for s in model.allocation_checks(self.c,parts,'vacuum')['errors']))

    def test_lift_camera_cannot_intrude_into_blower(self):
        a=copy.deepcopy(self.r['flights']['vacuum_octo10']['assembly'])
        next(p for p in a['parts'] if p['id']=='flight_camera_down')['min']=[200,180,80]
        self.assertTrue(any('flight_camera_down / blower_bay' in s for s in model.lift_metrics(self.c,a,'octo10')['geometry_errors']))

    def test_all_mass_rows_have_basis_and_ordered_positive_bounds(self):
        for k,h in self.c['hardware'].items():
            self.assertTrue(h['mass_basis'],k)
            self.assertGreater(h['mass_g'][0],0,k)
            self.assertEqual(h['mass_g'],sorted(h['mass_g']),k)
            self.assertIsNone(h['measured_mass_g'],k)

    def test_complete_module_sum(self):
        for bottom,a in self.r['ground'].items():
            expected=sum(self.r['module_masses'][k][1] for k in ['core','cap',bottom])+self.c['batteries']['design_6s']['mass_g'][1]+self.c['bottoms'][bottom]['payload_g']
            self.assertAlmostEqual(a['mass_g'][1],expected)

    def test_lift_replaces_cap_instead_of_adding_it(self):
        for bottom in self.c['bottoms']:
            for variant in self.c['lift']['variants']:
                a=self.r['flights'][bottom+'_'+variant]['assembly']
                expected=self.r['ground'][bottom]['mass_g'][1]-self.r['module_masses']['cap'][1]+self.r['module_masses'][variant][1]
                self.assertAlmostEqual(a['mass_g'][1],expected)
                self.assertFalse(any(r['module']=='cap' for r in a['rows']))

    def test_battery_and_drive_count(self):
        for a in self.r['ground'].values():
            self.assertEqual(sum(r['qty'] for r in a['rows'] if r['instance']=='battery'),1)
            self.assertEqual(sum(r['qty'] for r in a['rows'] if r['hardware_id']=='drive_motor'),2)
            self.assertEqual(sum(r['qty'] for r in a['rows'] if r['hardware_id']=='roboclaw'),1)

    def test_cg_interval_against_exhaustive_small_case(self):
        rows=[{'mass_g':[1,2,3],'cg_mm':[0,0,0]},{'mass_g':[2,4,7],'cg_mm':[12,20,5]},{'mass_g':[1,3,5],'cg_mm':[7,15,9]}]
        calc=model.mass_and_cg(rows)
        for axis in range(3):
            possible=[sum(w*r['cg_mm'][axis] for w,r in zip(weights,rows))/sum(weights) for weights in itertools.product(*[[r['mass_g'][0],r['mass_g'][2]] for r in rows])]
            self.assertAlmostEqual(calc['cg_bounds_mm'][axis][0],min(possible))
            self.assertAlmostEqual(calc['cg_bounds_mm'][axis][1],max(possible))

    def test_support_uncertainty_remains_visible(self):
        self.assertLess(self.r['traction']['vacuum']['support']['mass_and_position_bound_margin_mm'],0)
        for t in self.r['traction'].values():
            self.assertGreater(t['support']['minimum_nominal_margin_mm'],0)
            self.assertGreater(t['support']['backup_contact_hull_bound_margin_mm'],0)

    def test_runtime_energy_balance_and_rails(self):
        for p in self.r['power'].values():
            self.assertEqual(p['allocation_errors'],[])
            self.assertAlmostEqual(sum(v['normal_w'] for v in p['rails'].values())+p['conversion_loss_w'],p['normal_w'])
            for key,minutes in p['runtimes_min'].items():
                b=self.c['batteries'][key]
                self.assertAlmostEqual(p['normal_w']*minutes/60,b['capacity_ah']*b['nominal_v']*.8)

    def test_motor_current_limit_is_not_stall_torque(self):
        t=self.r['traction']['vacuum']
        self.assertLess(t['current_limited_torque_nm'],self.c['traction']['stall_torque_nm'])
        self.assertLess(t['required_torque_nm_each'],t['continuous_torque_screen_nm'])

    def test_wet_caster_issue_is_not_hidden(self):
        self.assertGreater(self.r['traction']['mop']['thresholds'][1]['floor_mu_needed_during_caster_climb'],.5)

    def test_extension_reach_and_raise(self):
        e=self.r['extension'];self.assertEqual(e['travel_mm'],1000)
        self.assertGreater(e['useful_sofa_depth_mm'],self.c['limits']['sofa_depth_mm'])
        self.assertEqual(e['one_way_time_s'],20)
        for bottom in ['low','dust']:
            transit={p['id']:p for p in model.reference_parts(self.c,bottom)}
            work={p['id']:p for p in model.reference_parts(self.c,bottom,'extended')}
            self.assertGreater(transit['extension_flex']['size'][2],0)
            self.assertLessEqual(model.hi(work['extension'])[2],40)
            self.assertEqual(transit['extension']['min'][2]-work['extension']['min'][2],12)

    def test_extended_cg_moves_and_mass_is_conserved(self):
        for key in ['low','dust']:
            a=self.r['ground'][key];ex=self.r['extended'][key]['assembly']
            self.assertEqual(a['mass_g'],ex['mass_g'])
            self.assertLess(ex['cg_mm'][1],a['cg_mm'][1]-30)

    def test_air_loss_rises_with_flow(self):
        c=copy.deepcopy(self.c);c['extension']['airflow_l_s']*=2
        self.assertAlmostEqual(model.extension_metrics(c)['total_added_loss_pa'],4*self.r['extension']['total_added_loss_pa'])

    def test_curve_endpoints_and_no_extrapolation(self):
        curve=self.c['lift']['curve_thrust_g_power_w']
        for x,y in curve:self.assertAlmostEqual(model.interpolate(curve,x),y)
        self.assertIsNone(model.interpolate(curve,curve[-1][0]+1))
        self.assertIsNone(model.interpolate(curve,curve[0][0]-1))

    def test_8s_fits_rotated_but_not_the_propulsion_voltage(self):
        fit=self.r['battery_fit']['design_8s']
        self.assertTrue(fit['any_orientation_bare_fit'])
        self.assertLess(fit['body_clearance_mm'][2],0)
        a=model.assembly(self.c,'vacuum','octo10','design_8s')
        with self.assertRaisesRegex(ValueError,'outside'):model.lift_metrics(self.c,a,'octo10')

    def test_guards_cost_thrust_and_power(self):
        a=self.r['flights']['vacuum_octo10']['assembly'];c=copy.deepcopy(self.c)
        normal=model.lift_metrics(c,a,'octo10');c['lift']['guard_factor']=.65
        worse=model.lift_metrics(c,a,'octo10')
        self.assertLess(worse['thrust_weight_nominal'],normal['thrust_weight_nominal'])
        self.assertGreater(worse['hover_w'],normal['hover_w'])

    def test_no_geometry_or_voltage_claim_implies_flight_qualification(self):
        for f in self.r['flights'].values():
            self.assertFalse(f['screen']['flight_qualified'])
            self.assertEqual(f['screen']['geometry_errors'],[])

    def test_stair_yaw_and_energy_reserve(self):
        f=self.r['flights']['vacuum_octo10']['screen']
        self.assertGreater(f['occupied_stair_width_mm'],f['envelope_mm'][0]+50)
        self.assertAlmostEqual(f['departure_energy_wh'],(f['transfer_wh']+f['landing_reserve_wh'])*1.2)
        self.assertGreater(f['stair_body_origin_above_local_plane_mm'],400)

    def test_station_reserves_arrival_vacancy(self):
        self.assertEqual(self.r['station']['bottom_positions'],5)
        self.assertEqual(self.r['station']['washes_per_floor'],10)
        self.assertGreater(self.r['station']['empty_station_mass_kg'],30)
        self.assertTrue(all(r['module']!='station' for a in self.r['ground'].values() for r in a['rows']))

    def test_station_spares_do_not_increase_carried_mass(self):
        c=copy.deepcopy(self.c)
        c['battery_exchange']['spare_packs_per_station']=20
        self.assertEqual(model.assembly(c,'vacuum')['mass_g'],self.r['ground']['vacuum']['mass_g'])
        for a in self.r['ground'].values():
            self.assertEqual(sum(r['qty'] for r in a['rows'] if r['hardware_id']=='battery_cartridge'),1)
        e=self.r['battery_exchange']
        self.assertEqual(e['total_fleet_packs'],5)
        self.assertAlmostEqual(e['spare_cartridge_mass_kg_per_station'],2*(753+140)/1000)

    def test_battery_exchange_vacancy_is_not_a_pack(self):
        self.assertEqual(self.r['battery_exchange']['geometry_errors'],[])
        c=copy.deepcopy(self.c);c['battery_exchange']['rack_bays_per_station']=3
        self.assertIn('Battery rack lacks receiving/recovery vacancies',model.battery_exchange_metrics(c)['geometry_errors'])

    def test_battery_extraction_requires_clear_fixed_core(self):
        c=copy.deepcopy(self.c)
        next(p for p in c['parts'] if p['id']=='dock_logic_power')['min']=[50,90,50]
        self.assertIn('Battery withdrawal intersects fixed core: dock_logic_power',model.battery_exchange_metrics(c)['geometry_errors'])

    def test_battery_rack_must_not_overlap_water_tank(self):
        c=copy.deepcopy(self.c);c['battery_exchange']['rack_allocation']['min']=[880,1030,0]
        self.assertIn('Battery rack intersects station allocation: clean_tank',model.battery_exchange_metrics(c)['geometry_errors'])

    def test_charge_throughput_and_pack_recovery_are_separate_limits(self):
        e=self.r['battery_exchange'];case=e['floor_cases']['vacuum']
        self.assertAlmostEqual(e['average_charge_to_cells_w'],180*.9*.8)
        self.assertEqual([v['minimum_local_pack_count'] for v in case['recovery_scenarios']],[3,3,4])
        self.assertFalse(case['recovery_scenarios'][-1]['configured_pack_count_sufficient'])
        c=copy.deepcopy(self.c);c['station']['charger_allocation_w']=90
        c['battery_exchange']['spare_packs_per_station']=10
        limited=model.battery_exchange_metrics(c)['floor_cases']['vacuum']
        self.assertLess(limited['average_charge_margin_w'],0)
        self.assertTrue(all(v['configured_pack_count_sufficient'] for v in limited['recovery_scenarios']))

if __name__=='__main__':unittest.main()
