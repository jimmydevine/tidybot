import copy
import json
import unittest
import head_coupling as P


class HeadCouplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=P.study()

    def test_scope_partition_conserves_existing_mass(self):
        m=self.r['mass']
        self.assertAlmostEqual(m['before_combined_budget_g'],m['after_combined_budget_g'])
        self.assertAlmostEqual(m['detailed_body_scope_g'],m['body_budget_g'])
        self.assertAlmostEqual(sum(v['mass_g'] for v in self.r['rows'] if v['owner']=='carrier'),m['carrier_budget_g'])
        self.assertEqual(m['booked_assembly_delta_g'],0)
        self.assertGreater(m['prior_transfer_gap_g'],0)
        self.assertFalse(m['complete_mechanism_mass_verified'])

    def test_unfinished_hardware_overrun_is_visible(self):
        d=copy.deepcopy(self.r['config']);d['allowances_g']['carrier_completion']+=20
        m=P.study(d)['mass']
        self.assertLess(m['carrier_remainder_g'],0)
        self.assertGreater(m['detailed_carrier_scope_g'],m['carrier_budget_g'])

    def test_key_stroke_must_clear_cheek(self):
        d=copy.deepcopy(self.r['config']);d['locks']['withdrawal_mm']=0
        self.assertLess(P.study(d)['mechanical']['released_key_clearance_mm'],0)
        self.assertAlmostEqual(self.r['mechanical']['released_key_clearance_mm'],0.5)
        self.assertAlmostEqual(self.r['mechanical']['minimum_key_engagement_with_axial_tolerance_mm'],0.5)

    def test_key_engagement_accounts_for_gap_and_axial_tolerance(self):
        d=copy.deepcopy(self.r['config']);d['locks']['axial_tolerance_mm']+=0.6
        self.assertLess(P.study(d)['mechanical']['minimum_key_engagement_with_axial_tolerance_mm'],0)

    def test_contact_stroke_uses_high_load_and_detects_bad_stack(self):
        r=self.r;e=r['config']['electrical'];q=r['mechanical']
        lo,hi=r['electrical']['compression_with_tolerance_and_high_beam_deflection_mm']
        self.assertAlmostEqual(hi-e['nominal_compression_mm'],e['stack_tolerance_mm']+q['crossmember_high_seal']['deflection_mm'])
        self.assertGreater(q['crossmember_high_seal']['deflection_mm'],q['crossmember_seal']['deflection_mm'])
        self.assertGreater(lo,0);self.assertLess(hi,e['max_stroke_mm'])
        d=copy.deepcopy(r['config']);d['electrical']['stack_tolerance_mm']=1.2
        self.assertFalse(P.study(d)['electrical']['stays_within_catalog_stroke'])

    def test_power_pair_loss_counts_supply_and_return(self):
        self.assertAlmostEqual(self.r['electrical']['power_contact_pair_loss_w'],0.64)
        d=copy.deepcopy(self.r['config']);d['electrical']['proposed_tool_current_limit_a']/=2
        self.assertAlmostEqual(P.study(d)['electrical']['power_contact_pair_loss_w'],0.16)

    def test_withdrawal_clears_rearmost_service_not_just_head(self):
        x=self.r['exchange'];d=copy.deepcopy(self.r['config'])
        self.assertAlmostEqual(x['separation_before_lateral_transfer_mm'],21.814)
        self.assertEqual(x['longitudinal_robot_and_extension_mm'],735)
        d['withdrawal_mm']=90
        self.assertLess(P.study(d)['exchange']['separation_before_lateral_transfer_mm'],0)

    def test_export_is_current_and_has_no_reported_local_intersections(self):
        path=P.OUT/'head_coupling_cad_checks.json'
        self.assertTrue(path.exists(),'Run export_head_coupling_freecad.py first')
        q=json.loads(path.read_text())
        self.assertEqual(q['source_fingerprint'],P.source_fingerprint(),'Regenerate CAD after source changes')
        self.assertTrue(all(q['valid_solids'].values()))
        for field in ('context_intersections','internal_intersections','head_motion_intersections','withdrawal_intersections'):
            self.assertEqual(q[field],[],field)
        row=next(row for row in self.r['rows'] if row['id']=='slotted_cheeks')
        self.assertAlmostEqual(q['cheek_cad_mass_g'],row['mass_g'])
        self.assertGreater(q['minimum_sampled_head_gap_mm'],1)
        self.assertGreater(q['minimum_carrier_wheel_gap_mm'],.5)
        self.assertEqual(q['withdrawal_samples'],self.r['config']['withdrawal_mm']+1)


if __name__=='__main__':unittest.main()
