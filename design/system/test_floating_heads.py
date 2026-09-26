from copy import deepcopy
import math
import unittest
import build as B
import floating_heads as M
import suspension_springs as L


class FloatingHeads(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=M.read();ld=L.read();cls.c=next(v for v in ld['candidates'] if v['id']==ld['preferred_candidate'])
        cls.p={b:M.prepare(b,cls.d) for b in ('vacuum','mop')}
        cls.cal={b:M.calibrate(p,cls.c) for b,p in cls.p.items()}

    def test_head_partition_preserves_total_mass(self):
        for p in self.p.values():
            self.assertAlmostEqual(p['fixed'][0]+p['head_mass_g']+sum(m for m,cg in p['moving']),p['dry_mass_g'])
            md=p['M']['modules'][p['bottom']]
            old=L.prepare(p['bottom'])
            self.assertAlmostEqual(p['dry_mass_g']-old['dry_mass_g'],sum(md[k][1] for k in ('mount_allowance_g','lift_addition_g','riser_addition_g')))

    def test_plane_following_rotation_preserves_distance_and_normal(self):
        n=[.01,-.02,math.sqrt(1-.01**2-.02**2)];ref=[137.5,36,0];q=3
        a=M.transform([22.5,6,0],ref,q,n);b=M.transform([252.5,6,0],ref,q,n)
        self.assertAlmostEqual(sum((a[i]-b[i])**2 for i in range(3)),230**2)
        for v in (a,b):self.assertAlmostEqual(sum(n[i]*(v[i]-[137.5,36,3][i]) for i in range(3)),0)

    def test_spring_force_uses_slide_virtual_work(self):
        p=self.p['vacuum'];n=[.2,0,math.sqrt(.96)]
        f=M.contact_force(p,4,n)
        self.assertAlmostEqual(f['net_n']*n[2],p['head_mass_g']/1000*B.G*n[2]+p['downward_preload_n'])
        self.assertLess(f['downward_spring_n'],0)
        self.assertGreater(self.p['mop']['downward_preload_n'],0)

    def test_pad_water_moves_with_head_and_tank_water_is_raised(self):
        p=self.p['mop'];loads=[[350,59,209.5,63],[50,137.5,171,11]]
        fixed,wet=M.split_contents(p,loads)
        self.assertEqual(fixed,[[350,60.5,209.5,81]])
        self.assertEqual(wet,[[50,137.5,171,11]])
        f0=M.contact_force(p,1,[0,0,1]);f1=M.contact_force(p,1,[0,0,1],water_g=50)
        self.assertAlmostEqual(f1['net_n']-f0['net_n'],.05*B.G)
        self.assertAlmostEqual(f1['net_n'],8)
        self.assertEqual(loads[0],[350,59,209.5,63])

    def test_coupled_contact_conserves_whole_robot_load_and_follows_floor(self):
        for b,p in self.p.items():
            loads=p['config']['contents'][b][1]['loads']
            r=M.solve(p,self.c,self.cal[b]['shims_mm'],loads=loads,heading=90)
            self.assertAlmostEqual(r['mass_g'],p['dry_mass_g']+sum(v[0] for v in loads))
            self.assertAlmostEqual(sum(r['support_n'])+r['head_net_n'],r['mass_g']/1000*B.G)
            self.assertLess(abs(r['head_floor_clearance_mm']),1e-6)
            self.assertLess(max(map(abs,r['residual_nmm'])),1e-5)
            self.assertTrue(r['motion_pass']);self.assertTrue(r['supports_positive'])

    def test_pressure_load_increases_contact_without_double_unloading_wheels(self):
        p=self.p['vacuum'];shims=self.cal['vacuum']['shims_mm']
        a=M.solve(p,self.c,shims,suction=0);b=M.solve(p,self.c,shims,suction=5)
        self.assertAlmostEqual(b['head_gross_n']-a['head_gross_n'],5)
        self.assertEqual(a['support_n'],b['support_n'])

    def test_raised_head_is_carried_without_floor_reaction(self):
        p=self.p['mop'];r=M.solve(p,self.c,self.cal['mop']['shims_mm'],raised=True)
        self.assertEqual(r['head_net_n'],0)
        self.assertEqual(r['head_normal'],[0,0,1])
        self.assertGreater(r['head_floor_clearance_mm'],10)
        self.assertAlmostEqual(sum(r['support_n']),r['mass_g']/1000*B.G)

    def test_old_envelopes_conflict_and_proposal_clears_sampled_allocations(self):
        for p in self.p.values():
            self.assertTrue(M.clearance_audit(p,False)['interferences'])
            a=M.clearance_audit(p)
            self.assertFalse(a['interferences']);self.assertFalse(a['changed_static_interferences'])
            self.assertTrue(a['xy_within_limit'])

    def test_lifting_the_tank_is_necessary(self):
        d=deepcopy(self.d);d['mop_tank_raise_mm']=0
        a=M.clearance_audit(M.prepare('mop',d))
        self.assertIn(('mop_pad','mop_tank'),a['pairs'])


if __name__=='__main__':unittest.main()
