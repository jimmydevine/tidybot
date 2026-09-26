import copy
import json
import math
import unittest
import passive_head as Q


class PassiveHeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=Q.study()

    def test_pose_closes_rails_and_floor_constraints(self):
        d=self.r['config']
        for p in self.r['poses']:
            for i,row in enumerate(p['R']):
                for j,other in enumerate(p['R']):self.assertAlmostEqual(Q.dot(row,other),1 if i==j else 0)
            left=Q.move(d['pivot_left_mm'],p)
            right=Q.move([d['pivot_right_x_mm'],*d['pivot_left_mm'][1:]],p)
            self.assertAlmostEqual(left[0],d['pivot_left_mm'][0])
            self.assertAlmostEqual(left[1],d['pivot_left_mm'][1]);self.assertAlmostEqual(right[1],left[1])
            self.assertAlmostEqual(d['pivot_right_x_mm']-right[0],p['right_float_used_mm'])
            for pt in ([22.5,6,0],[252.5,66,0]):
                self.assertAlmostEqual(Q.dot(p['normal'],Q.move(pt,p)),p['plane_constant']+p['ground_height_mm'])

    def test_travel_reserves_cut_and_placement_tolerance(self):
        v=self.r['motion'];self.assertGreater(v['minimum_travel_margin_mm'],1)
        self.assertGreater(v['remaining_float_margin_mm'],0)
        self.assertLess(v['maximum_pitch_deg'],self.r['config']['pitch_stop_deg'])
        for z in v['raised_carriage_z_mm']:
            self.assertLess(z,v['tolerance_adjusted_limits_mm'][1])
        self.assertEqual(self.r['raised']['ground_height_mm'],0)
        self.assertAlmostEqual(Q.move([137.5,36,0],self.r['raised'])[2],16)
        d=copy.deepcopy(self.r['config']);d['rail_end_tolerance_mm']+=3
        self.assertGreater(Q.rail_limits(d)[0],v['carriage_range_mm'][0])

    def test_counterbalance_accounts_for_motor_side_mass(self):
        c=self.r['calibration'];d=self.r['config'];left,right=c['upward_preload_n']
        self.assertGreater(left,right);self.assertGreater(right,0)
        self.assertAlmostEqual(c['weight_n']-left-right,d['target_contact_n'])
        x0=d['pivot_left_mm'][0];x1=d['pivot_right_x_mm'];cx=(x0+x1)/2
        self.assertAlmostEqual(c['weight_n']*c['cg_mm'][0]-left*x0-right*x1,d['target_contact_n']*cx)

    def test_spring_can_go_slack_but_not_push_down(self):
        p=copy.deepcopy(self.r['poses'][0]);p['carriage_z_mm']=[200,200]
        f=Q.force_case(self.r['config'],self.r['calibration'],p)
        self.assertEqual(f['springs_n'],[0,0])

    def test_low_pivot_reduces_drag_tipping(self):
        d=self.r['config'];c=self.r['calibration']
        low=Q.flat_pitch_screen(d,c,d['target_contact_n'],1.5)
        high=copy.deepcopy(d);high['pivot_left_mm'][2]+=20
        high=Q.flat_pitch_screen(high,c,d['target_contact_n'],1.5)
        self.assertTrue(low['supported_without_pitch_stop'])
        self.assertFalse(high['supported_without_pitch_stop'])

    def test_guide_friction_does_not_hide_invalid_floor_following(self):
        self.assertGreater(self.r['extended_contact']['nonpositive_cases'],0)
        self.assertLess(self.r['extended_contact']['net_range_n'][0],0)
        d=self.r['config'];self.assertGreater(Q.guide_resistance(d,.3)['combined_parasitic_bound_n'],Q.guide_resistance(d,.05)['combined_parasitic_bound_n'])
        with self.assertRaisesRegex(ValueError,'self-locking'):Q.guide_resistance(d,1)

    def test_mass_comparison_is_whole_scope_and_not_booked(self):
        r=self.r;m=r['mass'];g=r['gravity_comparison']
        self.assertAlmostEqual(sum(v['total_g'] for v in r['mass_rows']),m['candidate_mechanism_g'])
        self.assertAlmostEqual(m['catalog_reference_g']+m['unfinished_allowance_g'],m['candidate_mechanism_g'])
        self.assertEqual(m['prior_compliance_and_lift_g'],97)
        self.assertAlmostEqual(m['current_transfer_g']-m['conditional_reduction_g'],m['hypothetical_transfer_g'])
        self.assertEqual(m['booked_reduction_g'],0)
        self.assertEqual(m['candidate_mechanism_g']-g['mechanism_g'],3)

    def test_cad_reports_frame_rework_instead_of_hiding_it(self):
        q=json.loads((Q.OUT/'passive_head_cad_checks.json').read_text())
        self.assertEqual(q['source_fingerprint'],Q.P.source_fingerprint(),'Regenerate Q CAD')
        self.assertTrue(all(q['valid_shapes'].values()))
        for k in ('guide_context_intersections','moving_reference_intersections','head_P_N_intersections'):self.assertEqual(q[k],[],k)
        self.assertGreater(len(q['head_frame_rework_required']),0)
        self.assertFalse(q['fabrication_release'])


if __name__=='__main__':unittest.main()
