import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from study import (curve_power,evaluate,load_inputs,packaging_checks,rotation,
                   screen_variant,stair_height,support_margin,validate)


class ConceptChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c,cls.site,cls.ledger=load_inputs()
        cls.results={r['id']:r for r in evaluate(cls.c,cls.site,cls.ledger)}

    def check_named(self,result,name):
        return next(x for x in result['checks'] if x['name']==name)

    def variant(self,name='nine_raised'):
        return next(v for v in self.c['variants'] if v['id']==name)

    def test_riser_boundary_is_higher_surface(self):
        self.assertEqual(stair_height(139.699,279.4,190.5),0)
        self.assertEqual(stair_height(139.7,279.4,190.5),190.5)
        self.assertEqual(stair_height(-139.701,279.4,190.5),-190.5)

    def test_interpolation_does_not_extrapolate(self):
        self.assertEqual(curve_power([[100,20],[300,80]],200),50)
        self.assertIsNone(curve_power([[100,20],[300,80]],99))
        self.assertIsNone(curve_power([[100,20],[300,80]],301))

    def test_low_lift_plane_hits_stair(self):
        r=self.results['nine_low']
        self.assertLess(r['geometry']['rotor_step_clearance_mm'],0)
        self.assertEqual(self.check_named(r,'Rotors above uphill steps')['status'],'FAIL_MODEL')

    def test_raised_configuration_retains_actual_clearance(self):
        r=self.results['nine_raised']
        self.assertGreater(r['geometry']['rotor_step_clearance_mm'],self.c['screening']['collision_margin_mm'])
        self.assertFalse(any(ch['status']=='FAIL_MODEL' for ch in r['checks']))

    def test_earlier_240mm_body_is_rejected_for_tread_error_budget(self):
        c=copy.deepcopy(self.c); c['body']['length_mm']=240
        r=screen_variant(c,self.site,self.ledger,self.variant())
        self.assertEqual(self.check_named(r,'Landed body/tire tread edges')['status'],'FAIL_MODEL')

    def test_packaging_catches_undersized_core(self):
        c=copy.deepcopy(self.c); c['body']['length_mm']=150
        self.assertTrue(any('Battery' in issue for issue in packaging_checks(c)))
        self.assertEqual(packaging_checks(self.c),[])

    def test_uncertain_high_mass_loses_thrust_target(self):
        p=self.results['nine_raised']['power']
        self.assertGreater(p['voltage_sensitivity_thrust_ratio'],2)
        self.assertLess(p['high_mass_thrust_ratio'],2)

    def test_guard_loss_can_fail_nominal_configuration(self):
        c=copy.deepcopy(self.c); c['screening']['guard_thrust_factor']=0.7
        r=screen_variant(c,self.site,self.ledger,self.variant())
        self.assertEqual(self.check_named(r,'Thrust reserve sensitivity')['status'],'FAIL_ASSUMPTION')

    def test_extra_400g_is_not_free_payload(self):
        ledger=copy.deepcopy(self.ledger)
        next(x for x in ledger if x['id']=='debris')['unit_mass_g']+=400
        r=screen_variant(self.c,self.site,ledger,self.variant())
        self.assertAlmostEqual(r['mass']['total_g']-self.results['nine_raised']['mass']['total_g'],400)
        self.assertLess(r['power']['voltage_sensitivity_thrust_ratio'],2)

    def test_station_storage_is_not_airborne_mass(self):
        ledger=copy.deepcopy(self.ledger)
        for x in ledger:
            if x['section'] in ('station','cap'): x['unit_mass_g']=100000
        r=screen_variant(self.c,self.site,ledger,self.variant())
        self.assertAlmostEqual(r['mass']['total_g'],self.results['nine_raised']['mass']['total_g'])

    def test_missing_hover_data_is_unknown_not_zero_power(self):
        self.assertIsNone(self.results['twelve_raised']['power']['bench_equivalent_hover_w'])
        self.assertIsNone(self.results['twelve_raised']['power']['ground_minutes_after_reserve'])

    def test_unknown_home_cannot_become_validated(self):
        self.assertIsNone(self.site['staircase']['minimum_headroom'])
        self.assertFalse(self.site['staircase']['flight_route_validated'])
        for r in self.results.values():
            self.assertEqual(r['overall'],'NOT_VALIDATED')
            self.assertTrue(any(ch['status']=='UNKNOWN' for ch in r['checks']))

    def test_high_rotor_plane_lateral_shift_is_preserved(self):
        self.assertGreater(self.results['nine_raised']['geometry']['sampled_width_mm'],
                           self.results['nine_low']['geometry']['sampled_width_mm'])
        self.assertAlmostEqual(rotation((0,0,200),roll=90,pivot_z=100)[1],-100)

    def test_contact_polygon_rejects_outside_cg(self):
        self.assertGreater(support_margin(self.c),0)
        self.assertLess(support_margin(self.c,x=500),0)

    def test_too_close_rotors_and_low_core_support_fail(self):
        c=copy.deepcopy(self.c); c['station']['raised_core_bottom_z_mm']=220
        v=copy.deepcopy(self.variant()); v['rotor_y_mm']=80
        r=screen_variant(c,self.site,self.ledger,v)
        for name in ('Guard-to-guard separation','Bottom exchange vertical gap'):
            self.assertEqual(self.check_named(r,name)['status'],'FAIL_MODEL')

    def test_invalid_units_and_loss_factors_are_rejected(self):
        site=copy.deepcopy(self.site); site['length_unit']='mm'
        with self.assertRaises(ValueError): validate(self.c,site,self.ledger)
        c=copy.deepcopy(self.c); c['screening']['guard_thrust_factor']=0
        with self.assertRaises(ValueError): validate(c,self.site,self.ledger)


if __name__=='__main__': unittest.main()
