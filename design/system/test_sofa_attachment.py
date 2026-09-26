import copy
import unittest
import sofa_attachment as O


class SofaAttachmentTests(unittest.TestCase):
    def test_second_floor_adds_inventory_not_carried_mass(self):
        d=O.read();one=copy.deepcopy(d);one['policy']['floors']=1
        a,b=O.study(one),O.study(d)
        self.assertEqual(a['mass']['transfer_max_contents_g'],b['mass']['transfer_max_contents_g'])
        self.assertEqual(a['mass']['sofa_ground_max_contents_g'],b['mass']['sofa_ground_max_contents_g'])
        self.assertEqual(2*a['mass']['all_resident_extensions_g'],b['mass']['all_resident_extensions_g'])
        self.assertEqual(b['mass']['extension_mass_in_flight_g'],0)

    def test_swapping_head_conserves_physical_mass(self):
        r=O.study();m=r['mass']
        self.assertAlmostEqual(m['ordinary_ground_max_contents_g']+m['extension_g'],
            m['sofa_ground_max_contents_g']+m['parked_normal_head_with_adapter_g'])
        self.assertAlmostEqual(m['ordinary_ground_max_contents_g']-m['removed_cap_g'],m['transfer_max_contents_g'])
        self.assertAlmostEqual(m['transfer_max_contents_g']-m['baseline_N_transfer_max_contents_g'],m['flight_interface_increment_g'])

    def test_shared_air_hardware_and_drive_not_duplicated_in_extension(self):
        r=O.study()
        removed={v['hardware_id'] for v in r['removed_head_rows']}
        self.assertEqual(removed,{'tricut','head_frame','roller_motor','roller_transmission','tool_stage'})
        ext=[v['id'] for v in r['hardware'] if v['scope']=='extension']
        for forbidden in ('low_bin','blower','filter','wheel','battery'):
            self.assertFalse(any(forbidden in id for id in ext),forbidden)
        self.assertIsNone(r['mass']['upper_complete_mass_g'])

    def test_reach_distinguishes_body_and_head_standoff(self):
        r=O.study();s=r['space']
        self.assertEqual(s['stroke_mm'],1000)
        self.assertEqual(s['head_standoff_mm'],20)
        self.assertEqual(s['body_standoff_mm'],360)
        self.assertGreaterEqual(s['reach_from_sofa_front_mm'],s['required_sofa_depth_mm'])
        self.assertLess(s['under_sofa_working_height_mm'],50)
        self.assertGreater(s['under_sofa_raised_height_mm'],50)

    def test_loss_is_zero_at_rest_and_quadratic_with_assumed_flow(self):
        r=O.study();zero,low,mid,high=r['air']
        self.assertEqual(zero['total_added_loss_pa'],0)
        self.assertAlmostEqual(high['total_added_loss_pa']/low['total_added_loss_pa'],(high['flow_l_s']/low['flow_l_s'])**2)
        self.assertEqual(mid['smallest_bore_mm'],[31,19])

    def test_old_telescope_cannot_be_reused_inside_vacuum(self):
        r=O.study()
        self.assertIn('vac_duct',r['checks']['old_internal_telescope_conflicts'])
        self.assertEqual(r['checks']['receiver_reservation_intersections'],[])

    def test_receiver_clears_sampled_motion_not_just_stationary_head(self):
        motion=O.study()['receiver_motion']
        self.assertGreater(motion['previous']['intersection_count'],0)
        self.assertEqual(motion['revised']['intersection_count'],0)
        self.assertGreater(motion['revised']['minimum_sampled_box_gap_mm'],2)
        self.assertEqual(motion['mass_delta_g'],0)

    def test_supported_withdrawal_clears_body_and_is_separate_from_room_clearance(self):
        r=O.study();motion=r['receiver_motion']
        self.assertEqual(motion['withdrawal_intersections'],[])
        self.assertGreater(motion['minimum_head_front_separation_after_withdrawal_mm'],0)
        self.assertGreater(motion['extension_tail_front_separation_after_withdrawal_mm'],0)
        self.assertGreater(motion['exchange_combination_depth_mm'],r['config']['room_clearance']['front_space_mm'])


if __name__=='__main__':unittest.main()
