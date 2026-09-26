import copy
import json
import unittest
import core_support as S


class CoreSupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=S.study()

    def test_material_union_and_hole_count_once(self):
        boxes=[[0,0,0,2,2,2],[1,0,0,2,2,2]]
        v,c=S.volume_and_centre(boxes,[[1,0,0,1,1,2]])
        self.assertAlmostEqual(v,10)
        self.assertAlmostEqual(c[0],1.5)
        self.assertAlmostEqual(c[1],1.1)

    def test_scope_does_not_remove_battery_or_electrical_functions(self):
        r=self.r;m=r['mass'];d=r['config']
        self.assertEqual(set(d['replace_hardware_ids']),{'core_prints','battery_receiver'})
        self.assertEqual(m['before_g'],210)
        self.assertEqual(sum(d['retained'][k] for k in ('cartridge_shell_and_restraint_g','cartridge_monitor_id_g','cartridge_fuse_contacts_wiring_g')),140)
        self.assertAlmostEqual(m['same_capacity_wh'],115.44)
        self.assertAlmostEqual(m['candidate_g'],m['material_g']+m['unfinished_g'])
        self.assertEqual(m['booked_saving_g'],0)
        for c in r['cases']:
            self.assertAlmostEqual(c['before_g']-c['candidate_g'],m['conditional_saving_g'])
            self.assertFalse(c['measured_compliance'])
        self.assertIn('mass projection only',r['cases'][-1]['layout_scope'])

    def test_unfinished_hardware_growth_is_visible(self):
        d=copy.deepcopy(self.r['config']);d['remaining_parts'][0]['mass_g']+=75
        changed=S.study(d)
        self.assertAlmostEqual(changed['mass']['candidate_g']-self.r['mass']['candidate_g'],75)
        self.assertLess(changed['mass']['conditional_saving_g'],0)

    def test_bridge_stiffness_failure_is_visible(self):
        self.assertTrue(self.r['beam_screen']['passes'])
        d=copy.deepcopy(self.r['config']);d['bridge']['height']/=2
        weak=S.study(d)
        self.assertFalse(weak['beam_screen']['passes'])
        self.assertAlmostEqual(weak['beam_screen']['deflection_mm']/self.r['beam_screen']['deflection_mm'],8)

    def test_cad_fit_exchange_and_positive_retention_controls(self):
        c=json.loads((S.OUT/'core_support_cad_checks.json').read_text())
        self.assertEqual(c['source_fingerprint'],S.P.source_fingerprint(),'Regenerate S and P/Q/R CAD')
        self.assertTrue(all(c['valid_solids'].values()))
        for v in c['volume_differences_mm3'].values():self.assertLess(abs(v),1e-5)
        for key in ('internal_intersections','component_intersections','protected_reservation_intersections','core_upward_intersections','battery_downward_intersections'):
            self.assertEqual(c[key],[],key)
        for row in c['closed_latch_negative_controls']:self.assertGreater(row['interference_mm3'],0)
        self.assertEqual(c['downward_steps'],101)
        for size in c['printed_part_bounds_mm'].values():self.assertLessEqual(max(size),275)
        self.assertFalse(c['fabrication_release'])


if __name__=='__main__':unittest.main()
