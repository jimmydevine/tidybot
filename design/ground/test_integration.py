"""Regression checks for meaningful placement failures before a print release."""
import copy
import json
from pathlib import Path
import unittest
from integrate_vacuum import validate

BASE=json.loads((Path(__file__).resolve().parents[2]/'config/vacuum_integration.json').read_text())


class IntegrationChecks(unittest.TestCase):
    def setUp(self):
        self.c=copy.deepcopy(BASE)
        self.parts={p['id']:p for p in self.c['parts']}

    def errors(self): return validate(self.c)['errors']

    def test_current_reservations_and_conditional_services(self):
        self.assertEqual(self.errors(),[])

    def test_filter_must_fit_allocation(self):
        self.parts['filter_allocation']['size'][0]=155
        self.assertTrue(any('Outside parent: filter_allocation' in e for e in self.errors()))

    def test_extra_scanner_height_is_rejected(self):
        self.parts['lidar']['size'][2]+=3
        self.assertTrue(any('Outside robot envelope: lidar' in e for e in self.errors()))

    def test_head_drive_moves_with_head(self):
        self.parts['roller_drive']['motion']=[0,0,0]
        self.assertTrue(any('Inconsistent coupled travel' in e for e in self.errors()))

    def test_wheel_arc_requires_rearward_clearance(self):
        self.parts['wheel_left']['size'][1]=72
        self.assertTrue(any('Articulated reference outside' in e for e in self.errors()))

    def test_service_obstruction_after_clear_start(self):
        self.c['parts'].append({'id':'obstruction','label':'test obstacle','group':'interface','min':[4,113,92],'size':[3,20,10],'basis':'test'})
        errors=self.errors()
        self.assertFalse(any('Static reservation' in e for e in errors))
        self.assertTrue(any('Service battery_service' in e for e in errors))

    def test_short_station_drop_cannot_clear_towers(self):
        self.c['station']['relative_bottom_drop_mm']=40
        self.c['station']['tray_top_end_mm']=20
        self.assertTrue(any('Station relative drop insufficient' in e for e in self.errors()))

    def test_drop_includes_core_power_bay_below_mate(self):
        # 50 mm used to clear the rear towers, but cannot clear the new core bay.
        self.c['station'].update(relative_bottom_drop_mm=50,tray_top_start_mm=60)
        result=validate(self.c)
        self.assertEqual(result['core_projection_below_mate_mm'],16)
        self.assertEqual(result['station_vertical_separation_mm'],0)
        self.assertIn('Station relative drop insufficient',result['errors'])

    def test_caster_requires_swivel_sweep_not_only_wheel_diameter(self):
        self.parts['caster']['size'][1]=65
        self.assertIn('Caster full swivel sweep outside bay',self.errors())

    def test_converter_pins_must_reach_carrier(self):
        self.parts['converter_carrier']['min'][2]-=1
        self.assertIn('Converter pins do not reach through carrier PCB',self.errors())

    def test_converter_thermal_contact_is_not_a_free_air_gap(self):
        self.parts['converter_pad']['min'][2]+=0.5
        self.assertIn('Converter thermal stack has gap or interference',self.errors())

    def test_fan_and_guard_need_space_above_heat_sink(self):
        self.parts['converter_fan']['size'][2]+=2
        self.assertIn('Converter fan inlet clearance insufficient',self.errors())


if __name__=='__main__': unittest.main()
