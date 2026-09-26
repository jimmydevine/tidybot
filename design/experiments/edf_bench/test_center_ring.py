"""FreeCAD regression checks using SYNTHETIC ring dimensions, never export data.

Run with freecadcmd. The 76 x 2 mm test ring at 31 mm is not an owner measurement.
"""
import copy
import json
import os
import sys
from pathlib import Path

import FreeCAD as App

HERE = Path(os.environ.get("TIDYBOT_PROJECT_ROOT", Path.cwd())) / "design/experiments/edf_bench"
sys.path.insert(0, str(HERE))
from geometry import center_ring_geometry
from retaining_mount import cradle_shape, nominal_fan_shapes

actual = json.loads((HERE / "config.json").read_text())
missing = copy.deepcopy(actual)
missing["housing_profile"]["center_ring"]["outside_diameter_mm"] = None
try:
    cradle_shape(missing)
except ValueError as exc:
    assert "measurements required" in str(exc)
else:
    raise AssertionError("Missing ring dimensions must not silently produce a printable part")

synthetic = copy.deepcopy(actual)
synthetic["housing_profile"]["center_ring"].update(
    outside_diameter_mm=76.0, axial_width_mm=2.0, intake_edge_from_intake_face_mm=31.0)
ring = center_ring_geometry(synthetic)
assert ring["start_x_mm"] == -6.0
assert ring["relief_start_x_mm"] == -6.5
assert ring["relief_width_mm"] == 3.0 and ring["relief_diameter_mm"] == 76.6
plain = cradle_shape(synthetic, relieve_center_ring=False)
revised = cradle_shape(synthetic)
assert revised.isValid() and len(revised.Solids) == 1
raised = next(s for n, s in nominal_fan_shapes(synthetic) if n == "Measured raised center ring")
assert raised.common(plain).Volume > 1.0, "Regression must expose the omitted-ring collision"
assert raised.common(revised).Volume < 1e-5
for lift in (0, .25, 1, 5, 15, 40):
    moved = raised.copy(); moved.translate(App.Vector(0, 0, lift))
    assert moved.common(revised).Volume < 1e-5, "Ring must also enter the open groove vertically"
misplaced = raised.copy(); misplaced.translate(App.Vector(3, 0, 0))
assert misplaced.common(revised).Volume > 1.0, "Wrong groove position must remain detectable"
# Geometry away from the groove is unchanged, preserving the body-bearing bore.
import Part
away = Part.makeBox(8, 120, 60, App.Vector(3, -60, -55))
assert abs(plain.common(away).Volume - revised.common(away).Volume) < 1e-5
print("PASS: missing-data gate, independent ring collision, local relief, placement and unchanged remote geometry. Synthetic dimensions only; no files exported.")
