"""Check fabrication exports and nominal assembly paths with FreeCAD.

Run after export_freecad.py. These are geometric checks, not load certification.
"""
import json
import os
import sys
from pathlib import Path

import FreeCAD as App
import Part
import Mesh

ROOT = Path(os.environ.get("TIDYBOT_PROJECT_ROOT", Path.cwd())).resolve()
HERE = ROOT / "design/experiments/edf_bench"
sys.path.insert(0, str(HERE))
from retaining_mount import cradle_shape, mount_dimensions, nominal_fan_shapes, fan_fastener_shapes, mounting_board_shape
from geometry import center_ring_geometry

config = json.loads((HERE / "config.json").read_text())
m, d = config["retaining_mount"], mount_dimensions(config)
mount = cradle_shape(config)
fan = nominal_fan_shapes(config)
fasteners = list(fan_fastener_shapes(config))
revision = m["revision"]
ring_shape = next(shape for name, shape in fan if name == "Measured raised center ring")
old_mount = cradle_shape(config, relieve_center_ring=False)
old_ring_overlap = ring_shape.common(old_mount).Volume
assert old_ring_overlap > 1e-5, "Measured ring must reproduce the reported v1 interference; recheck profile/position before printing"
# Also reproduce the collision against the saved solid for the part actually
# printed, independently of the current cradle builder's unrelieved variant.
old_doc = App.openDocument(str(HERE / "output/retaining_cradle_v1.FCStd"))
printed_v1 = old_doc.Objects[0].Shape.copy()
App.closeDocument(old_doc.Name)
printed_v1.translate(App.Vector(-m["base_length_mm"] / 2, -m["base_width_mm"] / 2, d["base_bottom_z_mm"]))
saved_v1_overlap = ring_shape.common(printed_v1).Volume
assert saved_v1_overlap > 1e-5, "Measured ring must also collide with the preserved v1 print geometry"
assert abs(saved_v1_overlap - old_ring_overlap) < 1e-5
ring = center_ring_geometry(config)
washer_ring_clearance = []
shifted_washer_ring_clearance = []


def clear_of_mount(name, shape):
    overlap = shape.common(mount).Volume
    assert overlap < 1e-5, f"{name}: mount interference {overlap} mm^3"


for name, shape in fan:
    clear_of_mount(name, shape)
    if shape.Solids:
        for height in (.25, 1, 5, 15, 40, 80):
            moved = shape.copy()
            moved.translate(App.Vector(0, 0, height))
            clear_of_mount(name + " during vertical placement", moved)
for name, shape in fasteners:
    clear_of_mount(name, shape)
    if "upper washer" in name:
        washer_ring_clearance.append(shape.distToShape(ring_shape)[0])
    for label, part in fan:
        assert shape.common(part).Volume < 1e-5, (name, label)
    for dy in (-m["fan_slot_center_travel_mm"] / 2, m["fan_slot_center_travel_mm"] / 2):
        shifted = shape.copy()
        shifted.translate(App.Vector(0, dy, 0))
        clear_of_mount(name + " at slot endpoint", shifted)
        if "upper washer" in name:
            shifted_washer_ring_clearance.append(shifted.distToShape(ring_shape)[0])
        for label, part in fan:
            assert shifted.common(part).Volume < 1e-5, (name, label, dy)

# Board matches all four base holes; 9 mm-OD head/washer access clears the cradle.
board = mounting_board_shape(config)
assert board.common(mount).Volume < 1e-5
for x in (-m["base_hole_spacing_x_mm"] / 2, m["base_hole_spacing_x_mm"] / 2):
    for y in (-m["base_hole_spacing_y_mm"] / 2, m["base_hole_spacing_y_mm"] / 2):
        bolt = Part.makeCylinder(2, 28, App.Vector(x, y, d["base_bottom_z_mm"] - 19))
        clear_of_mount("M4 board bolt", bolt)
        assert bolt.common(board).Volume < 1e-5
        washer_access = Part.makeCylinder(4.5, 5, App.Vector(x, y, d["base_bottom_z_mm"] + m["base_thickness_mm"]))
        clear_of_mount("Base washer/head clearance", washer_access)

for name in ("bench_layout", "retaining_cradle_" + revision, "retaining_mount_assembly_" + revision, "unpowered_fit_gauge"):
    doc = App.openDocument(str(HERE / "output" / (name + ".FCStd")))
    assert all(not o.Shape.isNull() and o.Shape.isValid() for o in doc.Objects), name
    App.closeDocument(doc.Name)
    step = Part.read(str(HERE / "output" / (name + ".step")))
    assert not step.isNull() and step.isValid(), name
mesh = Mesh.Mesh(str(HERE / "output" / ("retaining_cradle_" + revision + ".stl")))
assert mesh.isSolid()
b = mesh.BoundBox
assert abs(b.XLength - m["base_length_mm"]) < .01
assert abs(b.YLength - m["base_width_mm"]) < .01
assert abs(b.ZLength - d["print_height_mm"]) < .01
assert b.ZMin == 0

report = {
    "status": "NOMINAL_GEOMETRY_CHECKS_PASSED_NOT_LOAD_VALIDATED",
    "revision": revision,
    "v1_interference_with_measured_ring_mm3": old_ring_overlap,
    "preserved_v1_interference_with_measured_ring_mm3": saved_v1_overlap,
    "v2_interference_with_measured_ring_mm3": ring_shape.common(mount).Volume,
    "center_ring_geometry": ring,
    "material_above_base_under_groove_mm": -ring["relief_diameter_mm"] / 2 - (d["base_bottom_z_mm"] + m["base_thickness_mm"]),
    "upper_washer_to_ring_nominal_gap_mm": min(washer_ring_clearance),
    "upper_washer_to_ring_gap_at_sampled_slot_endpoints_mm": min(shifted_washer_ring_clearance),
    "physical_fit_status": config["physical_checks"].get("cradle_" + revision, {"status": "NOT_YET_TESTED"})["status"],
    "physical_fit_observation": config["physical_checks"].get("cradle_" + revision, {}).get("observation"),
    "physical_fit_scope": config["physical_checks"].get("cradle_" + revision, {}).get("scope"),
    "body_ring_fit_observation": config["physical_checks"].get("cradle_" + revision, {}).get("body_ring_fit_observation"),
    "cradle_solid_volume_mm3": mount.Volume,
    "cradle_stl_facets": mesh.CountFacets,
    "print_extent_mm": [b.XLength, b.YLength, b.ZLength],
    "fan_hardware_stack_mm": d["fan_screw_stack_mm"],
    "screw_projection_beyond_nominal_nut_mm": d["fan_screw_projection_beyond_nut_mm"],
    "checks": ["Measured ring collides with both regenerated and preserved v1 solid; clears the revised groove", "Nominal fan interfaces clear cradle", "Sampled vertical placement clear",
               "M3 hardware clear at nominal and slot endpoints", "Four board holes and base washer access clear",
               "Four CAD/STEP exports reopened", "Single-solid CAD and closed cradle STL"],
    "limits": ["Actual fan taper, root fillets, wiring and motor protrusion not measured",
               "Inward screw positions leave little washer-to-ring margin; center the screws/washers in the ears and verify the actual gap. Washer float and manufacturing tolerances are not modeled.",
               "Physical results are recorded separately; no load, thermal, vibration or powered fixture validation",
               "Hardware models use nominal dimensions; verify purchased parts"],
}
(HERE / "output/mount_verification.json").write_text(json.dumps(report, indent=2) + "\n")
(HERE / "output" / ("mount_verification_" + revision + ".json")).write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
