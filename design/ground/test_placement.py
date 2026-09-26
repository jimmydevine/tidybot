"""Regression checks for changes that could make a serviceable layout unbuildable."""
import copy
import unittest

from place_modules import build_layout, validate


class PlacementChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.layout = build_layout()

    def test_current_layout_and_vertical_separation(self):
        self.assertEqual(self.layout["checks"]["errors"], [])
        # Wheel driver and dirt duct overlap in plan; their height separation matters.
        p = {p["id"]:p for p in self.layout["parts"]}
        self.assertGreater(p["wheel_driver_bay"]["min"][2],p["dirty_duct"]["min"][2]+p["dirty_duct"]["size"][2])

    def test_obstruction_between_service_endpoints(self):
        data=copy.deepcopy(self.layout)
        data["parts"].append(dict(id="blocking_post",label="Test obstruction",module="core",
                                 min=[13,150,75],size=[8,20,10],bom=[]))
        errors=validate(data)["errors"]
        self.assertTrue(any("Service sweep blocked: battery_tray by blocking_post" in e for e in errors))
        self.assertFalse(any("Reservation collision" in e for e in errors))

    def test_taller_blower_is_not_silently_accepted(self):
        data=copy.deepcopy(self.layout)
        p=next(p for p in data["parts"] if p["id"]=="blower")
        p["size"][2]+=20
        self.assertIn("Reference exceeds parent reservation: blower",validate(data)["errors"])

    def test_station_drop_must_clear_mating_projection(self):
        data=copy.deepcopy(self.layout)
        data["config"]["station"]["docked_tray_top_z_mm"]=50
        self.assertIn("Bottom separation cannot clear proposed mating projection",validate(data)["errors"])

    def test_cap_aperture_must_clear_whole_scanner(self):
        data=copy.deepcopy(self.layout)
        data["config"]["cap_aperture_mm"][2]=80
        self.assertIn("Cap aperture cannot pass over scanner",validate(data)["errors"])

    def test_bin_seal_must_release(self):
        data=copy.deepcopy(self.layout)
        next(p for p in data["parts"] if p["id"]=="clean_plenum").pop("service_min")
        self.assertIn("Bin seal release must provide at least 3 mm clearance before extraction",validate(data)["errors"])

    def test_long_roller_pair_exceeds_owner_width(self):
        config=copy.deepcopy(self.layout["config"])
        config["head_roller_set"]="long_10in"
        self.assertTrue(any("head" in e and ("limit" in e or "envelope" in e) for e in build_layout(config)["checks"]["errors"]))

    def test_height_limit_includes_scanner(self):
        data=copy.deepcopy(self.layout)
        next(p for p in data["parts"] if p["id"]=="lidar")["min"][2]+=3
        self.assertIn("Rigid component exceeds owner limit: lidar",validate(data)["errors"])

    def test_core_cannot_fill_tool_openings(self):
        data=copy.deepcopy(self.layout)
        data["parts"].append(dict(id="blocking_core_tray",label="Test obstruction",module="core",
                                 min=[196,170,76],size=[20,20,10],bom=[]))
        self.assertTrue(any("Core pocket obstructed" in e and "blocking_core_tray" in e for e in validate(data)["errors"]))

    def test_upper_filter_removal_path_is_checked(self):
        data=copy.deepcopy(self.layout)
        data["parts"].append(dict(id="rear_lip",label="Test rear lip",module="core",
                                 min=[172,274,87],size=[20,1,10],bom=[]))
        self.assertTrue(any("Service sweep blocked: bin_drawer" in e and "rear_lip" in e for e in validate(data)["errors"]))


if __name__=="__main__":
    unittest.main()
