from copy import deepcopy
import math
import unittest
import build as B
import floor_support as H
import suspension_springs as L


class SpringEquilibrium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=L.read();cls.c=next(c for c in cls.d['candidates'] if c['id']==cls.d['preferred_candidate'])
        cls.p=L.prepare('vacuum',cls.d)

    def test_support_forces_preserve_force_and_moments_with_tool_contact(self):
        n=[.03,-.02,math.sqrt(1-.03**2-.02**2)]
        points=[[14,105,36],[261,105,36],[137,232,0]];cg=[120,132,80];tool=[137,36,0]
        f=L.reactions(points,cg,50,n,4,tool)
        self.assertAlmostEqual(sum(f)+4,50)
        for axis in (0,1):
            project=lambda p:p[axis]-p[2]*n[axis]/n[2]
            self.assertAlmostEqual(sum(force*project(p) for force,p in zip(f,points))+4*project(tool),50*project(cg))

    def test_moving_mass_is_subtracted_from_fixed_mass_once(self):
        p=self.p
        self.assertAlmostEqual(p['fixed'][0]+sum(m for m,cg in p['moving']),p['dry_mass_g'])
        r=L.evaluate(p,self.c,[3,3],[4,-1],loads=[[123,85,212,52]])
        self.assertAlmostEqual(r['mass_g'],p['dry_mass_g']+123)
        self.assertAlmostEqual(sum(r['support_n']),r['mass_g']/1000*B.G)
        self.assertAlmostEqual(p['moving'][0][1][0]+p['moving'][1][1][0],275)

    def test_nominal_pod_moment_includes_own_weight(self):
        p=self.p;r=L.evaluate(p,self.c,[3,3],[0,0]);m,cg=p['moving'][0]
        expected=m/1000*B.G*(145-cg[1])
        self.assertAlmostEqual(r['moving_gravity_moment_nmm'][0],expected)
        spring=r['springs'][0]['force_n']*16
        self.assertAlmostEqual(r['residual_nmm'][0],spring+expected-r['support_n'][0]*40)

    def test_solver_balances_free_suspension(self):
        cal=L.calibrate(self.p,self.c);loads=self.d['contents']['vacuum'][1]['loads']
        r=L.solve(self.p,self.c,cal['shims_mm'],loads=loads,heading=90)
        self.assertEqual(r['stops'],[None,None])
        self.assertLess(max(map(abs,r['residual_nmm'])),1e-5)
        self.assertTrue(r['supports_positive'])
        self.assertTrue(all(2<t<4 for t in r['travel_mm']))

    def test_bump_stop_has_correct_reaction_sign_under_overload(self):
        r=L.solve(self.p,self.c,[3,3],loads=[[10000,137.5,110,60]])
        self.assertEqual(r['stops'],['bump','bump'])
        self.assertTrue(all(f<0 for f in r['residual_nmm']))

    def test_high_preload_reaches_droop_with_opposite_reaction_sign(self):
        c=deepcopy(self.c);c['free_length_mm']=40
        r=L.solve(self.p,c,[6,6])
        self.assertEqual(r['stops'],['droop','droop'])
        self.assertTrue(all(f>0 for f in r['residual_nmm']))

    def test_front_tool_contact_reduces_drive_normal_load(self):
        cal=L.calibrate(self.p,self.c)
        raised=L.solve(self.p,self.c,cal['shims_mm']);lowered=L.solve(self.p,self.c,cal['shims_mm'],contact_n=6)
        self.assertLess(sum(lowered['support_n'][:2]),sum(raised['support_n'][:2]))
        self.assertLess(sum(lowered['travel_mm']),sum(raised['travel_mm']))

    def test_solid_clearance_does_not_override_working_length(self):
        r=L.installed_screen(self.p,self.c,[5,5],.25)
        self.assertGreater(r['solid_gap_after_uncertainty_mm'],0)
        self.assertLess(r['working_length_margin_after_reserve_mm'],0)
        self.assertFalse(r['passes'])

    def test_short_spring_and_wide_spring_are_rejected(self):
        c=deepcopy(self.c);c['free_length_mm']=20
        self.assertFalse(L.installed_screen(self.p,c,[3,3])['passes'])
        c=deepcopy(self.c);c['od_mm']=14
        self.assertFalse(L.installed_screen(self.p,c,[3,3])['fits_radially'])
        # Actual free-length variation participates in seating-force checks.
        nominal=L.installed_screen(self.p,self.c,[2,2],.25)
        short=L.installed_screen(self.p,self.c,[2,2],.25,free_offsets=(-.5,-.5))
        self.assertGreater(nominal['min_spring_force_n'],short['min_spring_force_n'])

    def test_nominal_modules_fit_but_tolerance_corner_is_not_hidden(self):
        for bottom in ('vacuum','mop','low'):
            p=L.prepare(bottom,self.d);cal=L.calibrate(p,self.c)
            self.assertTrue(L.installed_screen(p,self.c,cal['shims_mm'],.25)['passes'])
        p=L.prepare('low',self.d);cal=L.calibrate(p,self.c,rate_factors=(.9,.9),free_offsets=(-.5,-.5))
        self.assertFalse(L.installed_screen(p,self.c,cal['shims_mm'],.25,rate_factors=(.9,.9),free_offsets=(-.5,-.5))['passes'])

    def test_new_resting_position_requires_raised_anti_tip_rollers(self):
        cal=L.calibrate(self.p,self.c)
        row=L.solve(self.p,self.c,cal['shims_mm'],loads=self.d['contents']['vacuum'][1]['loads'])
        height=L.height_and_head(self.p,[row])
        self.assertLess(height['old_anti_tip_min_clearance_mm'],0)
        self.assertGreater(height['raised_anti_tip_min_clearance_mm'],0)
        d=deepcopy(self.d);d['anti_tip_raise_mm']=0
        unchanged=L.prepare('vacuum',d)
        self.assertLess(L.height_and_head(unchanged,[row])['raised_anti_tip_min_clearance_mm'],0)


if __name__=='__main__':unittest.main()
