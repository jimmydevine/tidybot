import math
import unittest
import fixed_drive as N


class FixedDriveTests(unittest.TestCase):
    def test_three_contact_heights(self):
        for heights in ([0,0,0],[10,0,0],[0,10,0],[10,10,0],[0,0,10]):
            caster=[142,220,0];n,c=N.rigid_plane(heights,caster)
            self.assertAlmostEqual(sum(x*x for x in n),1,places=10)
            got=[sum(v*w for v,w in zip(n,[x,105,36]))-36-c for x in (14,261)]
            got.append(sum(v*w for v,w in zip(n,caster))-c)
            for a,b in zip(got,heights):self.assertAlmostEqual(a,b,places=9)

    def test_uniform_floor_offset_does_not_move_head(self):
        for h in (0,4,10,100):
            n,c=N.rigid_plane([h,h,h],[137.5,232,0])
            self.assertAlmostEqual(N.head_pose([137.5,36,0],n,c,h)['q_mm'],0)

    def test_mirrored_terrain_reverses_roll(self):
        a,_=N.rigid_plane([10,0,0],[137.5,232,0]);b,_=N.rigid_plane([0,10,0],[137.5,232,0])
        self.assertAlmostEqual(a[0],-b[0]);self.assertAlmostEqual(a[1],b[1])

    def test_sharp_step_domain_and_zero(self):
        self.assertEqual(N.sharp_step_lever(36,0),0)
        self.assertAlmostEqual(N.sharp_step_lever(36,10),math.sqrt(620))
        with self.assertRaises(ValueError):N.sharp_step_lever(36,36)

    def test_beam_known_centre_load(self):
        r=N.beam_bending(100,[50],[10],1000)
        self.assertEqual(r['reactions_n'],[5,5])
        self.assertEqual(r['max_moment_nmm'],250)
        self.assertAlmostEqual(r['max_deflection_mm'],10*100**3/(48*1000))

    def test_outboard_couple_preserves_force_application(self):
        r=N.beam_bending(202,[19],[150],1000,[-41.5*150])
        self.assertAlmostEqual(sum(r['reactions_n']),150)
        self.assertAlmostEqual(r['reactions_n'][1]*202,150*(-22.5))
        self.assertLess(r['reactions_n'][1],0)  # opposite mount must resist uplift

    def test_torsion_boundary_conditions(self):
        r=N.beam_torsion(100,[25,75],[10,10],1000)
        self.assertAlmostEqual(r['max_torque_nmm'],10)
        self.assertAlmostEqual(r['end_rotations_rad'][1],0)
        self.assertAlmostEqual(r['max_twist_deg'],math.degrees(.25))

    def test_mass_conservation_and_motion_failure_not_hidden(self):
        r=N.study()
        for a in r['modules'].values():
            self.assertAlmostEqual(a['M_mass_g']-a['mass_g'],a['removed_pods_g']-sum(v['mass_g'] for v in r['stock']))
            self.assertGreater(a['head_motion_fail_count'],0)
            self.assertGreater(a['max_pitch_deg'],5)
            for pose in a['terrain']:
                tool=3 if pose['bottom']=='vacuum' else 8
                self.assertAlmostEqual(sum(pose['support_n'])+tool,a['mass_g']/1000*N.B.G)


if __name__=='__main__':unittest.main()
