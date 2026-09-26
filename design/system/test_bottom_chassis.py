import copy
import json
import unittest
import bottom_chassis as T


class BottomChassisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=T.study()

    def test_complete_scope_preserves_electrical_interface_and_counts_drive_once(self):
        for c in self.r['cases']:
            old={v['id']:v['mass_g'] for v in c['prior_rows']}
            self.assertNotIn('floor_interface_F',old)
            self.assertEqual(set(old)&T.F_IDS,T.F_IDS)
            self.assertEqual(old['bottom_frame'],225)
            self.assertEqual(old['caster'],112)
            ids=[v['id'] for v in c['rows']];self.assertEqual(len(ids),len(set(ids)))
            for v in c['rows']:
                if v['id'].startswith('N_'):self.assertAlmostEqual(v['mass_g'],old[v['id']])
            self.assertAlmostEqual(c['candidate_transfer_g'],c['current_transfer_g']-sum(old.values())+sum(v['mass_g'] for v in c['rows']))
            self.assertEqual(c['booked_saving_g'],0)
        vacuum=self.r['cases'][0]
        self.assertAlmostEqual(vacuum['impossible_zero_scope_transfer_g'],vacuum['current_transfer_g']-vacuum['prior_scope_g'])
        self.assertGreater(vacuum['impossible_zero_scope_transfer_g'],vacuum['budget_g'])

    def test_caster_correction_and_completion_growth_cannot_disappear(self):
        self.assertEqual(self.r['caster_correction_g'],30)
        d=copy.deepcopy(self.r['config']);d['remaining_parts'][0]['mass_g']+=50
        heavier=T.study(d)
        for a,b in zip(self.r['cases'],heavier['cases']):
            self.assertAlmostEqual(b['candidate_transfer_g']-a['candidate_transfer_g'],50)
            self.assertLess(a['conditional_saving_g'],0)

    def test_thinning_seats_exposes_bending_failure(self):
        d=copy.deepcopy(self.r['config']);d['seat_wall_mm']/=2
        weaker=T.screen(d)
        self.assertAlmostEqual(weaker['corner_seat']['stress_mpa']/self.r['screens']['corner_seat']['stress_mpa'],4)
        self.assertFalse(weaker['corner_seat']['passes'])
        self.assertFalse(self.r['screens']['whole_frame_qualified'])

    def test_rejected_geometry_is_valid_material_and_reports_obstructions(self):
        c=json.loads((T.OUT/'bottom_chassis_cad_checks.json').read_text())
        self.assertEqual(c['source_fingerprint'],T.S.P.source_fingerprint())
        self.assertTrue(all(c['valid_solids'].values()))
        self.assertEqual(c['internal_intersections'],[])
        self.assertEqual(c['core_upward_intersections'],[])
        self.assertEqual(c['vacuum_head_poses'],105)
        self.assertEqual(c['withdrawal_steps'],121)
        self.assertGreater(len(c['withdrawal_intersections']),0)
        self.assertIn('Rejected',c['decision'])
        self.assertFalse(c['fabrication_release'])
        for bb in c['bounds'].values():
            self.assertGreaterEqual(min(bb[:3]),0)
            self.assertLessEqual(max(bb[3:5]),275)
            self.assertLessEqual(bb[5],180)


if __name__=='__main__':unittest.main()
