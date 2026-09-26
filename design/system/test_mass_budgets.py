import unittest
import mass_budgets as Q


class MassBudgetTests(unittest.TestCase):
    def test_scope_keeps_core_battery_and_load_but_removes_swapped_top(self):
        rows=[dict(module=m,mass_g=[w,w,w]) for m,w in [('core',1200),('battery',800),('vacuum',1900),('payload',300),('cap',70),('lift',2500)]]
        self.assertEqual(Q.included_mass(rows),4200)
        self.assertEqual(Q.included_mass(rows,cap_removed=False),4270)

    def test_budget_boundary_and_class(self):
        d=Q.read()
        for name,limit in [('vacuum',4500),('air_dust',3500)]:
            a=Q.comparison('id','name',name,limit-10,limit,None,0,10,0,'test',d)
            self.assertTrue(a['nominal_hardware_with_max_contents_within_budget'])
            b=Q.comparison('id','name',name,limit,limit+1,None,0,1,0,'test',d)
            self.assertFalse(b['nominal_hardware_with_max_contents_within_budget'])
            self.assertEqual(b['reduction_needed_g'],1)
            self.assertIsNone(b['upper_estimate_within_budget'])
            self.assertFalse(b['measured_compliance'])

    def test_load_changes_do_not_change_hardware(self):
        for c in Q.study()['cases']:
            self.assertAlmostEqual(c['max_contents_mass_g']-c['usual_mass_g'],c['max_modeled_contents_g']-c['usual_contents_g'])
            self.assertAlmostEqual(c['headroom_g'],c['budget_g']-c['max_contents_mass_g'])

    def test_N_mass_matches_existing_candidate_after_physical_cap_removal(self):
        r=Q.study()
        for bottom in ('vacuum','mop'):
            _,n=Q.N.nominal_mass(bottom,Q.N.read())
            c=next(v for v in r['cases'] if v['id']=='N_'+bottom)
            self.assertAlmostEqual(c['usual_mass_g'],n['mass_g']-c['removed_cap_nominal_g'])
            self.assertIsNone(c['upper_hardware_and_max_contents_g'])

    def test_duster_uses_shared_updated_core_without_floor_drive(self):
        d=Q.E.read();a=Q.E.air_assembly(Q.E.configured(Q.H.baseline(),d),d)
        self.assertFalse(any(r['module']=='drive' for r in a['rows']))
        c=next(v for v in Q.study()['cases'] if v['bottom']=='air_dust')
        self.assertAlmostEqual(c['usual_mass_g'],Q.included_mass(a['rows']))
        self.assertAlmostEqual(c['upper_hardware_and_max_contents_g'],Q.included_mass(a['rows'],2))

    def test_resident_sofa_mission_uses_ordinary_vacuum_flight_mass(self):
        r=Q.study();om=Q.O.study()['mass']
        c=next(v for v in r['cases'] if v['id']=='O_vacuum')
        self.assertAlmostEqual(c['max_contents_mass_g'],om['transfer_max_contents_g'])
        self.assertIn('O_vacuum',r['primary_case_ids'])
        self.assertNotIn('K_low',r['primary_case_ids'])
        self.assertTrue(any(v['id']=='K_low' for v in r['cases']))


if __name__=='__main__':unittest.main()
