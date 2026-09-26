from copy import deepcopy
import math
import unittest
import build as base
import floor_support as H
import wheel_pod as J
import pod_joints as K


class PodJoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k=K.read();cls.j=J.read();cls.h=J.configured(H.read(),cls.j);cls.g=H.baseline()

    def test_nominal_clearance_is_compensated_at_both_stops(self):
        s=K.slot(self.h,self.k)
        for i,t in enumerate((-2.5,10)):
            c=K.stop_contact(self.h,self.k,i)
            self.assertAlmostEqual(c['travel_mm'],t)
            self.assertAlmostEqual(c['cap_distance_mm'],.25)
            self.assertAlmostEqual(c['contact_lever_mm'],s['radius_mm']*math.cos(s['end_trim_rad']/2))
        # Without shortening the track, the pin centre reaches the cap centre,
        # leaving clearance that permits extra wheel travel.
        self.assertGreater(s['end_trim_rad'],0)

    def test_invalid_slot_is_rejected(self):
        k=deepcopy(self.k);k['stop']['slot_width_mm']=7.9
        with self.assertRaises(ValueError):K.slot(self.h,k)
        k['stop']['slot_width_mm']=30
        with self.assertRaises(ValueError):K.slot(self.h,k)

    def test_load_screens_do_not_credit_unqualified_plate_action(self):
        r=K.load_screen(self.h,self.j,self.k)
        self.assertTrue(r['pivot_passes']);self.assertTrue(r['stop_bolt_passes'])
        self.assertFalse(r['tray_strip'][0]['passes']);self.assertTrue(r['tray_strip'][1]['passes'])
        self.assertAlmostEqual(r['tray_strip'][0]['bending_mpa'],150)
        self.assertGreater(r['max_stop_force_n'],200)
        k=deepcopy(self.k);k['stop']['bolt_root_diameter_mm']=3
        self.assertFalse(K.load_screen(self.h,self.j,k)['stop_bolt_passes'])

    def test_stop_contact_normal_balances_wheel_moment(self):
        c=K.stop_contact(self.h,self.k,1);r=K.load_screen(self.h,self.j,self.k)
        for row in r['cases']:
            sp=J.spring_pose(self.h,self.j,10,row['shim_mm']);p=H.pose(self.h,10)
            applied=150*(145-p['axle_y_mm'])+row['fore_aft_n']*36
            resisted=row['stop_force_n']*c['contact_lever_mm']+sp['force_n']*sp['moment_arm_mm']
            self.assertAlmostEqual(applied,resisted)

    def test_inner_rail_bolts_and_countersink_ligament(self):
        r=K.load_screen(self.h,self.j,self.k)['inner_rail_joint']
        self.assertFalse(r['M3_passes']);self.assertTrue(r['M4_passes'])
        self.assertTrue(r['angle_edge_passes']);self.assertLess(r['rail_rear_edge_shear_mpa'],80)
        # A full-thickness straight-hole area would overstate this edge's strength.
        plain_area=2*3.175*(142-137.25-2.2)
        self.assertGreater(r['angle_countersink_edge_shear_mpa'],r['max_bolt_force_n']/plain_area)

    def test_mass_replacement_counts_motor_and_pod_once(self):
        c=K.replaced_layout(self.g,[190,200,230],[65,130,40]);g=deepcopy(self.g)
        for b in ('vacuum','mop','low'):
            before=base.assembly(self.g,b);after=base.assembly(c,b)
            self.assertAlmostEqual(after['mass_g'][1]-before['mass_g'][1],2*(200-62))
            rows=base.hardware_rows(c,base.reference_parts(c,b))
            self.assertEqual(sum(v['qty'] for v in rows if v['hardware_id']=='drive_motor'),2)
            self.assertEqual(sum(v['qty'] for v in rows if v['hardware_id']=='pod'),2)
        self.assertEqual(self.g,g)
        self.assertEqual(c['hardware']['bottom_frame'],self.g['hardware']['bottom_frame'])

    def test_mass_centres_keep_motor_separate_and_mirror_only_x(self):
        c=K.replaced_layout(self.g,[190,200,230],[65,130,40])
        rows=base.hardware_rows(c,base.reference_parts(c,'vacuum'))
        motors=[r for r in rows if r['hardware_id']=='drive_motor'];pods=[r for r in rows if r['hardware_id']=='pod']
        self.assertEqual([r['cg_mm'][1:] for r in motors],[[105,36],[105,36]])
        self.assertEqual([r['cg_mm'][1:] for r in pods],[[130,40],[130,40]])
        self.assertEqual(sum(r['cg_mm'][0] for r in pods),275)


if __name__=='__main__':unittest.main()
