"""Mechanical screens and honest failure reporting for the H study."""
from copy import deepcopy
import math
import unittest
import build as base
import floor_support as support


class FloorSupport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=support.baseline();cls.d=support.read();cls.r=support.study(cls.g,cls.d)

    def test_baseline_remains_unchanged_and_candidate_mass_is_not_installed(self):
        original=deepcopy(self.g);support.study(self.g,self.d)
        self.assertEqual(original,self.g)
        for bottom,v in self.r['ground'].items():self.assertEqual(v['mass_g'],base.assembly(self.g,bottom)['mass_g'])
        self.assertGreater(self.r['gross_candidate_stock_g'],self.r['conditional_removed_carrier_g'])
        self.assertTrue(self.r['mass_accounting']['G_retained'])

    def test_leading_arm_motion_and_arc_length(self):
        p=support.pose(self.d,10)
        self.assertAlmostEqual(p['angle_deg'],14.4775121859)
        self.assertAlmostEqual(p['axle_y_mm'],106.2701665379)
        self.assertAlmostEqual(math.hypot(p['axle_y_mm']-145,p['axle_z_mm']-36),40)
        self.assertEqual(support.rotate_yz(self.d,145,36,10),[145,36])
        with self.assertRaises(ValueError):support.pose(self.d,40)

    def test_spring_rate_uses_squared_motion_ratio(self):
        w=self.r['ground']['vacuum']['loads']
        self.assertAlmostEqual(w['lever_ratio'],0.4)
        self.assertAlmostEqual(w['spring_rate_n_mm'],5)
        self.assertAlmostEqual(w['spring_rate_n_mm']*w['lever_ratio']**2,0.8)
        self.assertGreaterEqual(self.r['poses'][-1]['spring_length_mm'],self.d['wheel']['spring_solid_height_limit_mm']+2)

    def test_motor_swept_box_clearance_and_negative_case(self):
        self.assertGreater(min(p['motor_to_cap_mm'] for p in self.r['poses']),0)
        self.assertLess(min(p['motor_to_cap_mm'] for p in self.r['poses']),1)
        # The earlier 61 mm roof would fail the conservative box sweep.
        self.assertGreater(base.hi(self.r['poses'][-1]['motor_box'])[2],61)

    def test_beam_reactions_obey_force_and_moment_balance(self):
        b=support.simply_supported_loads([5],[100],[0,10])
        self.assertEqual(b['reactions_n'],[-50,-50]);self.assertEqual(b['max_moment_nmm'],250)
        b=support.simply_supported_loads([-5],[100],[0,10])
        self.assertEqual(b['reactions_n'],[-150,50]);self.assertEqual(b['max_moment_nmm'],500)

    def test_pin_screen_includes_stop_and_rejects_four_mm(self):
        p=self.r['pivot'];self.assertGreater(p['hard_stop_force_n'],150)
        rows={r['diameter_mm']:r for r in p['screens']}
        self.assertFalse(rows[4]['passes']);self.assertTrue(rows[6]['passes'])
        self.assertAlmostEqual(rows[4]['bending_mpa']/rows[6]['bending_mpa'],(6/4)**3)
        self.assertFalse(p['motor_output_radial_load_rating_verified'])

    def test_plate_section_and_fitting_height(self):
        s=self.r['caster'];self.assertEqual(s['section']['area_mm2'],120)
        self.assertAlmostEqual(s['section']['inertia_mm4'],90)
        self.assertTrue(s['passes'])
        cases={r['fitting_height_mm']:r for r in s['fitting_cases']}
        self.assertEqual(cases[2.5]['vacuum_mop_gap_mm'],1)
        self.assertLess(cases[5]['vacuum_mop_gap_mm'],0)
        self.assertFalse(s['stem_retention_verified'])

    def test_stock_routes_clear_external_bays_and_each_other(self):
        for bottom,g in self.r['ground'].items():
            self.assertEqual(g['stock_conflicts'],[]);self.assertEqual(g['candidate_stock_overlaps'],[])
            for p in support.stock(self.d,bottom):self.assertTrue(base.contains({'min':[0,0,0],'size':[275,275,180]},p))
        d=deepcopy(self.d);d['carrier']['bridge_min_mm'][1]-=3
        self.assertTrue(support.stock_conflicts(self.g,d,'vacuum'))

    def test_support_plane_satisfies_contact_constraints(self):
        for left,right in [(-2.5,-2.5),(-2.5,10),(0,0),(10,10)]:
            caster=[230,232];n=support.support_plane(self.d,left,right,caster)
            self.assertAlmostEqual(sum(x*x for x in n),1)
            for x,t in [(14,left),(261,right)]:
                p=support.pose(self.d,t)
                self.assertAlmostEqual(n[0]*(x-caster[0])+n[1]*(p['axle_y_mm']-caster[1])+n[2]*p['axle_z_mm'],36)

    def test_nominal_height_does_not_mask_droop_failure(self):
        self.assertEqual(support.support_plane(self.d,0,0,[137.5,232]),[0,0,1])
        h=self.r['support_height_screen'];self.assertEqual(h['sampled_support_poses'],7776)
        self.assertGreater(max(c['max_height_mm'] for c in h['cases'].values()),180)
        self.assertFalse(h['droop_adopted']);self.assertFalse(h['full_pose_envelope_verified'])

    def test_gearbox_limit_supersedes_fraction_of_stall(self):
        t=self.r['torque'];self.assertAlmostEqual(t['continuous_screen_nm'],0.392266)
        self.assertLess(t['continuous_screen_nm'],t['old_fraction_screen_nm'])
        self.assertEqual(t['continuous_current_screen_a'],1.25)
        self.assertFalse(self.r['fabrication_release'])


if __name__=='__main__':unittest.main()
