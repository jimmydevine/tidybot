import copy
import json
import math
import unittest
import integrated_head as R


class IntegratedHeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cad=json.loads((R.OUT/'integrated_head_cad_checks.json').read_text())
        cls.d=R.read()

    def test_whole_scope_replacement_retains_automation_and_plumbing(self):
        m=R.account(self.d,self.cad['mass_rows'])
        self.assertEqual(m['prior_scope_g'],170)
        self.assertAlmostEqual(m['candidate_scope_g'],m['modeled_material_g']+m['reference_g']+m['allowance_g'])
        self.assertAlmostEqual(m['hypothetical_transfer_g'],m['current_transfer_g']-170+m['candidate_scope_g'])
        self.assertEqual(m['booked_reduction_g'],0)
        self.assertEqual((m['powered_lift_retained_g'],m['carrier_retained_g'],m['plumbing_retained_g']),(62,70,75))
        ids=[v['id'] for v in m['rows']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertFalse(any('dock_set_capture' in id for id in ids))
        # Additional physical hardware must increase the estimate one-for-one.
        rows=copy.deepcopy(self.cad['mass_rows']);rows[0]['mass_g']+=20
        heavier=R.account(self.d,rows)
        self.assertAlmostEqual(heavier['hypothetical_transfer_g']-m['hypothetical_transfer_g'],20)

    def test_flex_cannot_be_approved_from_nominal_gap(self):
        q=R.Q.read()
        level=R.Q.pose(q,[0,0,1],0,0)
        raised=R.Q.pose(q,[0,0,1],0,16)
        r=R.flex_motion([level,raised])
        self.assertAlmostEqual(r['rows'][0]['minimum_centreline_reach_mm'],25)
        self.assertAlmostEqual(r['rows'][1]['minimum_centreline_reach_mm'],math.hypot(25,16))
        self.assertGreater(r['rows'][1]['minimum_centreline_reach_mm'],25)
        self.assertEqual(r['maximum_end_angle_deg'],0)

    def test_modelled_parts_clear_protected_components_and_withdraw(self):
        c=self.cad
        self.assertEqual(c['source_fingerprint'],R.P.source_fingerprint(),'Regenerate R/P/Q CAD after model source changes')
        self.assertTrue(all(c['valid_solids'].values()))
        self.assertEqual(c['intersections'],[])
        self.assertEqual(c['withdrawal_intersections'],[])
        self.assertEqual(c['pose_count'],105)
        self.assertEqual(c['withdrawal_samples'],121)
        self.assertGreater(c['minimum_roller_clearance_mm'],.49)
        self.assertGreater(c['minimum_guide_clearance_mm'],1)
        self.assertFalse(c['fabrication_release'])

    def test_pitch_stops_block_motion_outside_working_range(self):
        controls=self.cad['pitch_stop_controls']
        self.assertEqual(len(controls),4)
        for v in controls:self.assertGreater(v['interference_mm3'],.01,v)


if __name__=='__main__':unittest.main()
