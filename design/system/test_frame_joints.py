"""Unit consistency and mechanical allocation regressions for G."""
import copy
import unittest
import build as base
import airborne_study as air
import core_partition as partition
import frame_joints as frame


class FrameJoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=partition.configured(base.read(),partition.read());cls.d=frame.read()
        cls.r=frame.study(cls.f,cls.d,air.read());cls.g=cls.r['model_config']

    def test_previous_model_not_mutated(self):
        f=copy.deepcopy(self.f);frame.configured(f,self.d);self.assertEqual(f,self.f)

    def test_flange_formula_matches_known_rectangular_beam(self):
        s=frame.flange_screen(100,10,20,2,100000)
        self.assertAlmostEqual(s['second_moment_mm4'],20/3)
        self.assertAlmostEqual(s['stress_mpa'],75)
        self.assertAlmostEqual(s['deflection_mm'],0.025)

    def test_thin_sections_fail_unequal_load_screen(self):
        rows=[s for s in self.r['flange_screens'] if s['anchors_sharing']==2]
        self.assertTrue(all(not s['passes_stress_screen'] for s in rows[:-1]))
        self.assertTrue(rows[-1]['passes_stress_screen'])
        self.assertEqual(rows[-1]['force_n'],300)
        self.assertFalse(self.r['fabrication_release'])

    def test_load_paths_are_not_double_factored(self):
        self.assertEqual(self.d['loads']['factored_axial_n'],600)
        self.assertEqual({s['force_n'] for s in self.r['flange_screens']},{150,300})
        self.assertTrue(self.r['rail_screen']['passes'])

    def test_bearing_pads_are_needed_for_radius_clearance_under_load(self):
        self.assertTrue(self.r['corner_radius_screen']['passes'])
        d=copy.deepcopy(self.d);d['corner']['bearing_pad_mm'][2]=0
        self.assertFalse(frame.corner_radius_screen(d)['passes'])
        d=copy.deepcopy(self.d);d['corner']['inside_radius_screen_mm']=4
        self.assertFalse(frame.corner_radius_screen(d)['passes'])

    def test_added_mass_flows_into_every_assembly(self):
        delta=self.r['installed_frame_mass_g']-self.r['old_frame_mass_g']
        self.assertGreater(delta,0)
        for g in self.r['ground'].values():self.assertAlmostEqual(g['after']['mass_g'][1]-g['before']['mass_g'][1],delta)
        for variant,case in self.r['airborne_after']['cases'].items():
            self.assertAlmostEqual(case['assembly']['mass_g'][1]-self.r['airborne_before']['cases'][variant]['assembly']['mass_g'][1],delta)

    def test_locks_and_floor_carrier_not_double_counted_or_deleted(self):
        before=base.assembly(self.f,'vacuum');after=self.r['ground']['vacuum']['assembly']
        for id in ('core_locks','core_prints','bottom_frame','floor_carrier_fasteners','floor_post_0','floor_post_1','floor_post_2'):
            self.assertEqual(sum(r['mass_g'][1] for r in before['rows'] if r['hardware_id']==id),sum(r['mass_g'][1] for r in after['rows'] if r['hardware_id']==id))
        self.assertEqual(sum(r['qty'] for r in after['rows'] if r['hardware_id']=='core_locks'),1)

    def test_locked_pose_and_service_paths_clear_allocations(self):
        for g in self.r['ground'].values():
            self.assertEqual(g['checks']['errors'],[]);self.assertEqual(g['withdrawal_errors'],[])
            self.assertEqual(g['slider_sweep_errors'],[])
        self.assertEqual(self.r['battery_exchange_errors'],[])
        for a in self.r['airborne_after']['cases'].values():self.assertEqual(a['screen']['geometry_errors'],[])

    def test_height_and_service_envelope_reported_separately(self):
        self.assertAlmostEqual(self.r['ground_height_mm'],179.1)
        self.assertLessEqual(self.r['ground_height_mm'],180)
        self.assertEqual(self.r['unlocked_slider_x_envelope_mm'],[0,275])
        self.assertAlmostEqual(self.r['new_top_seat_mm'],124.1)

    def test_existing_protection_bay_would_hit_new_rail(self):
        parts=copy.deepcopy(self.r['ground']['vacuum']['assembly']['parts'])
        next(p for p in parts if p['id']=='pack_protection')['min'][0]=230
        self.assertTrue(any('pack_protection / G_rail_right' in e for e in base.allocation_checks(self.g,parts,'vacuum')['errors']))

    def test_capacity_targets_and_real_filter_size_preserved(self):
        self.assertTrue(all(b['target_screen_pass'] for b in self.r['bins'].values()))
        self.assertTrue(all(not b['usable_capacity_qualified'] for b in self.r['bins'].values()))
        def element(c):return next(p['size'] for p in c['parts'] if p['id']=='filter_reference')
        self.assertEqual(element(self.f),element(self.g))
        self.assertEqual(self.f['bottoms'],self.g['bottoms'])
        self.assertEqual(self.f['batteries'],self.g['batteries'])
        self.assertEqual(self.f['power'],self.g['power'])

    def test_bridge_is_not_adopted_despite_known_interference(self):
        self.assertIn('drive_control',self.r['ground']['vacuum']['bridge_conflicts_before'])
        self.assertIn('extension_drive',self.r['ground']['low']['bridge_conflicts_before'])
        self.assertTrue(all(not g['bridge_conflicts'] for g in self.r['ground'].values()))
        self.assertFalse(any(p['id']=='G_floor_bridge' for p in self.g['parts']))
        for id in ('roboclaw_reference','bottom_mcu_reference','extension_drive'):
            self.assertEqual(next(p['size'] for p in self.f['parts'] if p['id']==id),next(p['size'] for p in self.g['parts'] if p['id']==id))


if __name__=='__main__':unittest.main()
