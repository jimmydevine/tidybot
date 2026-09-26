"""Regression and adverse cases for the I packaging overlay."""
from copy import deepcopy
import math
import unittest
import build as base
import floor_support as support
import height_mounting as design


class HeightMounting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=support.baseline();cls.h=support.read();cls.d=design.read()
        cls.r=design.study(cls.g,cls.h,cls.d)
        cls.c,cls.s=design.configured(cls.g,cls.h,cls.d)

    def test_changes_preserve_source_inputs_and_travel(self):
        g,h=deepcopy(self.g),deepcopy(self.h)
        design.configured(self.g,self.h,self.d)
        self.assertEqual(self.g,g);self.assertEqual(self.h,h)
        self.assertEqual(self.h['wheel'],self.s['wheel'])
        self.assertEqual(self.c['hardware'],self.g['hardware'])
        self.assertFalse(self.r['fabrication_release'])

    def test_a1_failure_and_c1_height_reserve(self):
        for b in design.BOTTOMS:
            self.assertGreater(self.r['height_before'][b]['max_height_mm'],180)
            self.assertTrue(self.r['height_after'][b]['passes_reserved_screen'])
            self.assertLess(self.r['height_after'][b]['reserved_height_mm'],179.5)
        self.assertFalse(self.r['continuous_envelope_proven'])

    def test_height_uses_module_specific_geometry(self):
        c=deepcopy(self.c)
        c['parts'].append(dict(id='adverse_mop_tower',module='mop',min=[130,200,180],size=[5,5,30],shape='box',hardware=[]))
        rows=design.height_screen(c,self.s,self.d)
        self.assertFalse(rows['mop']['passes_reserved_screen'])
        self.assertEqual(rows['mop']['part'],'adverse_mop_tower')
        self.assertTrue(rows['vacuum']['passes_reserved_screen'])
        self.assertTrue(rows['low']['passes_reserved_screen'])

    def test_port_rotation_preserves_volume_and_window_requires_it(self):
        old=next(p for p in self.g['parts'] if p['id']=='top_port')
        new=next(p for p in self.c['parts'] if p['id']=='top_port')
        self.assertEqual(math.prod(old['size']),math.prod(new['size']))
        self.assertEqual(self.c['interfaces'],self.g['interfaces'])
        self.assertAlmostEqual(self.r['port_to_pack_protection_gap_mm'],1.5)
        self.assertTrue(self.r['optics']['passes'])
        c=deepcopy(self.c)
        for p in c['parts']:
            if p['id']=='top_port':p.update(deepcopy(old))
        self.assertFalse(design.optics(c,self.d)['passes'])

    def test_full_thread_tip_not_nut_sets_overhead(self):
        s=self.r['caster_stack']
        self.assertAlmostEqual(s['thread_tip_mm'],71.5)
        self.assertAlmostEqual(s['nut_top_mm'],69.1)
        self.assertAlmostEqual(s['overhead_gap_mm'],2.5)
        self.assertAlmostEqual(s['thread_projection_mm'],2.4)
        self.assertFalse(s['caster_pullout_retention_verified'])
        self.assertFalse(s['stem_pairing_confirmed'])
        d=deepcopy(self.d);d['caster']['nut_height_reserve_mm']=12
        s=design.caster_stack(self.s,d)
        self.assertLess(s['thread_projection_mm'],0)
        self.assertEqual(s['hardware_top_mm'],s['nut_top_mm'])

    def test_taller_fitting_load_arm_and_changed_clearances(self):
        self.assertTrue(self.r['caster_beam']['passes'])
        self.assertGreater(self.r['caster_beam']['stress_mpa'],support.caster_screen(self.h)['stress_mpa'])
        for errors in self.r['conflicts'].values():self.assertEqual(errors,[])
        for id,bottom,lower in [('vac_bin_upper','vacuum',12),('blower_bay','low',10),('mop_pump','mop',8)]:
            c=deepcopy(self.c)
            for p in c['parts']:
                if p['id']==id:p['min'][2]-=lower
            self.assertTrue(design.changed_conflicts(c,self.s,self.d,bottom),id)

    def test_reserve_volume_and_nested_blower_follow_move(self):
        for b,row in self.r['bins'].items():self.assertTrue(row['target_screen_pass'],b)
        p={p['id']:p for p in self.c['parts']}
        self.assertTrue(base.contains(p['blower_bay'],p['blower_reference']))
        self.assertAlmostEqual(self.r['bins']['vacuum']['after_reserve_l'],.5418444)
        self.assertAlmostEqual(self.r['mass_comparison']['illustrative_net_delta_g'],-12)


if __name__=='__main__':unittest.main()
