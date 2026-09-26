"""Check mass conservation, withdrawal interference and F configuration scope."""
import copy
import unittest

import build as base
import airborne_study as air
import core_partition as partition


class CorePartition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=base.read();cls.d=partition.read();cls.ad=air.read()
        cls.new=partition.configured(cls.c,cls.d)
        cls.r=partition.study(cls.c,cls.d,cls.ad)

    def test_baseline_inputs_are_not_mutated(self):
        c=copy.deepcopy(self.c);d=copy.deepcopy(self.d)
        partition.configured(c,d)
        self.assertEqual(c,self.c);self.assertEqual(d,self.d)

    def test_only_applicable_modules_carry_converters(self):
        for bottom, expected in [('vacuum',{'tool_converter','motor_buck','regen_clamp'}),
                ('low',{'tool_converter','motor_buck','regen_clamp'}),
                ('mop',{'motor_buck','regen_clamp'})]:
            a=self.r['ground'][bottom]['assembly']
            actual={r['hardware_id'] for r in a['rows']} & {'tool_converter','motor_buck','regen_clamp'}
            self.assertEqual(actual,expected)
            self.assertTrue(all(r['module']!='core' for r in a['rows'] if r['hardware_id'] in expected))
            for id in expected:self.assertEqual(sum(r['qty'] for r in a['rows'] if r['hardware_id']==id),1)
        a=self.r['airborne_after']['cases']['quad10']['assembly']
        self.assertFalse({r['hardware_id'] for r in a['rows']} & {'tool_converter','motor_buck','regen_clamp'})
        self.assertEqual(sum(r['qty'] for r in a['rows'] if r['hardware_id']=='logic_buck'),1)

    def test_whole_stack_mass_includes_added_hardware(self):
        added=self.r['carrier_installed_g']+self.d['floor_interface_allowance_g'][1]+self.d['core_interface_allowance_g'][1]
        for bottom,g in self.r['ground'].items():
            expected=added-(self.c['hardware']['tool_converter']['mass_g'][1] if bottom=='mop' else 0)
            self.assertAlmostEqual(g['delta_g'],expected)
            self.assertAlmostEqual(self.r['transfers'][bottom]['delta_g'],expected)
        before=self.r['airborne_before']['cases']['quad10']['assembly']
        after=self.r['airborne_after']['cases']['quad10']['assembly']
        self.assertAlmostEqual(before['mass_g'][1]-after['mass_g'][1],254-8)

    def test_payload_sensors_cell_energy_and_cleaning_loads_preserved(self):
        for bottom in ('vacuum','mop','low'):
            old=base.assembly(self.c,bottom);new=self.r['ground'][bottom]['assembly']
            ids={'battery_cartridge','design_6s','payload','pi','lidar','depth_camera','drive_motor','drive_wheel','blower','filter','mop_pump'}
            def retained(a):return sorted((r['hardware_id'],r['qty'],r['mass_g']) for r in a['rows'] if r['hardware_id'] in ids)
            self.assertEqual(retained(old),retained(new))
            self.assertEqual(base.power_metrics(self.c,bottom),base.power_metrics(self.new,bottom))
        self.assertEqual(self.c['batteries'],self.new['batteries'])
        self.assertEqual(self.r['airborne_before']['config']['missions'],self.r['airborne_after']['config']['missions'])

    def test_floor_layouts_and_removal_sweeps_clear_new_hardware(self):
        for g in self.r['ground'].values():
            self.assertEqual(g['allocation']['errors'],[])
            self.assertEqual(g['withdrawal_errors'],[])
        for v in self.r['airborne_after']['cases'].values():self.assertEqual(v['screen']['geometry_errors'],[])

    def test_old_capacitor_position_would_trap_core_camera(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['assembly']['parts'])
        next(p for p in parts if p['id']=='brake_cap_reference')['min']=[112,15,90]
        errors=partition.withdrawal_errors(parts)
        self.assertIn('front_camera / brake_cap_reference',errors)

    def test_filling_shelf_notch_would_trap_core_camera(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['assembly']['parts'])
        p=next(p for p in parts if p['id']=='floor_shelf_right')
        p['min'][1]=13;p['size'][1]=70
        self.assertIn('front_camera / floor_shelf_right',partition.withdrawal_errors(parts))

    def test_new_core_board_keeps_body_height_limit(self):
        a=self.r['ground']['vacuum']['assembly']
        bay=next(p for p in a['parts'] if p['id']=='core_logic_power_F')
        board=next(p for p in a['parts'] if p['id']=='logic_buck_reference')
        self.assertTrue(base.contains(bay,board))
        self.assertLess(base.hi(bay)[2],180)

    def test_sheet_and_tube_mass_is_not_a_percentage_of_old_core(self):
        # Explicit stock shape volumes, with aluminum tube and steel rod in posts.
        shelf=next(p for p in partition.carrier_parts(self.d) if p['id']=='shelf_left')
        self.assertAlmostEqual(shelf['stock_mass_g'],81*70*1*0.0027)
        self.assertGreater(self.r['carrier_installed_g'],self.r['carrier_stock_g'])

    def test_current_screen_does_not_qualify_hardware(self):
        self.assertAlmostEqual(self.r['raw_branch_current_a'],240/18)
        self.assertGreater(self.d['interface']['contact_continuous_requirement_a'],self.r['raw_branch_current_a'])
        self.assertFalse(self.r['qualified'])
        self.assertFalse(self.r['airborne_after']['limits']['flight_qualified'])


if __name__=='__main__':unittest.main()
