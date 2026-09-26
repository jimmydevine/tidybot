"""Independent limits and adverse geometry cases for J."""
from copy import deepcopy
import math
import unittest
import floor_support as support
import wheel_pod as design


class WheelPod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h=support.read();cls.d=design.read();cls.g=support.baseline()
        cls.j=design.configured(cls.h,cls.d);cls.r=design.study(cls.h,cls.d,cls.g)

    def test_previous_layout_and_mass_are_preserved(self):
        h,g=deepcopy(self.h),deepcopy(self.g)
        design.study(self.h,self.d,self.g)
        self.assertEqual(self.h,h);self.assertEqual(self.g,g)
        for key in ('axle_yz_mm','pivot_yz_mm','bump_mm','droop_candidate_mm'):
            self.assertEqual(self.j['wheel'][key],h['wheel'][key])
        self.assertFalse(self.r['fabrication_release'])

    def test_nominal_seat_force_has_expected_moment(self):
        p=design.spring_pose(self.j,self.d,0,0)
        self.assertEqual(p['length_mm'],26)
        self.assertEqual(p['force_n'],32.5)
        self.assertAlmostEqual(p['equivalent_wheel_force_n'],13)
        self.assertAlmostEqual(design.spring_pose(self.j,self.d,0,6)['equivalent_wheel_force_n'],25)

    def test_guide_and_coil_clearance_detect_impossible_parts(self):
        self.assertTrue(self.r['spring']['passes'])
        for field,value in [('guide_length_mm',16),('guide_length_mm',12),('solid_height_limit_mm',16),('upper_guide_id_mm',2.9),('id_min_mm',6)]:
            d=deepcopy(self.d);d['spring'][field]=value
            self.assertFalse(design.spring_screen(self.j,d)['passes'],(field,value))

    def test_preload_does_not_hide_sofa_shortfall(self):
        self.assertTrue(self.r['preload']['vacuum']['within_adjuster_range'])
        self.assertTrue(self.r['preload']['mop']['within_adjuster_range'])
        self.assertFalse(self.r['preload']['low']['within_adjuster_range'])
        self.assertGreater(self.r['preload']['low']['required_shim_ranges_mm'][0][1],6)
        with self.assertRaises(ValueError):design.spring_pose(self.j,self.d,0,6.1)

    def test_bump_stop_target_resolves_full_pose(self):
        st=self.r['stops'];y,z=st['bump_contact_yz_mm']
        self.assertAlmostEqual(z,62)
        self.assertLess(145-y,32)  # Vertical offset also moves the contact forward/back.
        self.assertAlmostEqual(self.r['pivot']['stop_lever_at_bump_mm'],145-y)
        self.assertFalse(st['hardware_complete'])

    def test_impact_moments_balance_with_actual_spring_direction(self):
        p=self.r['pivot'];w=self.j['wheel'];ax=support.pose(self.j,10)
        for row in p['cases']:
            spring=design.spring_pose(self.j,self.d,10,row['shim_mm'])
            external=150*(145-ax['axle_y_mm'])+row['fore_aft_force_n']*36
            reacted=row['stop_force_n']*p['stop_lever_at_bump_mm']+spring['force_n']*spring['moment_arm_mm']
            self.assertAlmostEqual(external,reacted)
        self.assertGreater(p['max_hard_stop_force_n'],support.pivot_screen(self.h)['hard_stop_force_n'])
        self.assertFalse(p['screens'][0]['passes']);self.assertTrue(p['screens'][1]['passes'])
        self.assertAlmostEqual(p['screens'][0]['bending_mpa']/p['screens'][1]['bending_mpa'],(8/6)**3)

    def test_motor_boss_thread_and_shaft_stack(self):
        a=self.r['axial']
        self.assertEqual(a['wheel_x_mm'],[2,26]);self.assertEqual(a['motor_plate_x_mm'],[24,26])
        self.assertEqual(a['boss_to_hub_back_mm'],1.5)
        self.assertEqual(a['shaft_hub_overlap_mm'],8.5)
        self.assertLessEqual(a['motor_thread_insertion_mm'],6)
        d=deepcopy(self.d);d['hub']['back_x_mm']=24
        self.assertLess(design.axial_stack(d)['boss_to_hub_back_mm'],0)
        d=deepcopy(self.d);d['bracket']['motor_screw_length_mm']=10
        self.assertGreater(design.axial_stack(d)['motor_thread_insertion_mm'],6)


if __name__=='__main__':unittest.main()
