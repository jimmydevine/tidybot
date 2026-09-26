"""FreeCAD bench export, fit gauge and physical cradle prototype.

Run from the repository root with freecadcmd. Cradle is for unpowered assembly.
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
from geometry import ear_geometry, center_ring_geometry
from retaining_mount import cradle_shape, mount_dimensions, mounting_board_shape, nominal_fan_shapes, fan_fastener_shapes
from cad_preview import preview_svg

OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
CONFIG = json.loads((HERE / "config.json").read_text())
C = CONFIG["confirmed"]
G = CONFIG["layout"]
EAR = ear_geometry(CONFIG)
M = CONFIG["retaining_mount"]
MD = mount_dimensions(CONFIG)
REV = M["revision"]
CRADLE_NAME = "retaining_cradle_" + REV
ASSEMBLY_NAME = "retaining_mount_assembly_" + REV
RING = center_ring_geometry(CONFIG)  # Runs before opening/saving any document.


def add(doc, name, shape, scope="LAYOUT ENVELOPE; not fabrication geometry"):
    assert not shape.isNull() and shape.isValid(), name
    feature = doc.addObject("PartDesign::Feature", "Part" + str(len(doc.Objects)))
    feature.Label = name
    feature.Shape = shape
    feature.addProperty("App::PropertyString", "Scope").Scope = scope
    return feature


def box(doc, name, center, size, wire=False):
    low = [c - s / 2 for c, s in zip(center, size)]
    solid = Part.makeBox(*size, App.Vector(*low))
    return add(doc, name, Part.makeCompound(solid.Edges) if wire else solid)


def cylinder(doc, name, center, radius, length, axis):
    vector = App.Vector(*axis)
    return add(doc, name, Part.makeCylinder(radius, length, App.Vector(*center) - vector * length / 2, vector))


def save(doc, name):
    doc.recompute()
    doc.saveAs(str(OUT / (name + ".FCStd")))
    Part.export(list(doc.Objects), str(OUT / (name + ".step")))
    print(f"EXPORTED {name}: {len(doc.Objects)} valid features")


doc = App.newDocument("EDFBenchLayout")
base_x, base_y, base_z = G["base_mm"]
px = G["pivot_x_mm"]
pz = base_z + G["pivot_z_above_base_mm"]
fz = pz + G["thrust_height_above_pivot_mm"]
sx = px - G["scale_contact_left_of_pivot_mm"]
ear_x = px - C["fan_duct_length_excluding_motor_mm"] / 2 + EAR["hole_center_from_inlet_mm"]
board_bottom = fz + MD["base_bottom_z_mm"] - M["mounting_board_mm"][2]
box(doc, "Fixed base 600 x 320 x 18 allowance", [base_x / 2, 0, base_z / 2], G["base_mm"])
for y in G["bearing_y_mm"]:
    foot_z = pz - CONFIG["procurement"]["bearing_axis_above_foot_mm"]
    box(doc, "Fixed support plus cap envelope; joints pending", [px, y, (foot_z + base_z) / 2], [100, 18, foot_z - base_z])
    box(doc, "Selected 1602-0032-0008; clearance envelope only", [px, y, foot_z + 25], [60, 32, 50], wire=True)
cylinder(doc, "Selected 8 x 200 round shaft; hub joints pending", [px, 0, pz], G["shaft_diameter_mm"] / 2, G["shaft_length_mm"], [0, 1, 0])
box(doc, "Moving scale arm", [(px + sx) / 2, 0, pz], [px - sx + 24, 35, 18])
box(doc, "Moving upright / fan support; joint details pending", [px, 0, (pz + board_bottom) / 2], [35, 35, board_bottom - pz])
brace_start = App.Vector(sx + 40, 0, pz)
brace_end = App.Vector(px, 0, board_bottom)
brace_axis = brace_end - brace_start
add(doc, "Diagonal brace allowance; joints not detailed", Part.makeCylinder(5, brace_axis.Length, brace_start, brace_axis))
board = mounting_board_shape(CONFIG)
board.translate(App.Vector(ear_x, 0, fz))
add(doc, "120 x 140 x 18 mounting board; joint to lever still to detail", board)
cradle = cradle_shape(CONFIG)
cradle.translate(App.Vector(ear_x, 0, fz))
add(doc, f"Cradle {REV} prototype; unpowered assembly only", cradle,
    "Printable prototype. Load, thermal, fastener and complete-fixture validation pending.")
duct_length = C["fan_duct_length_excluding_motor_mm"]
lip_diameter = C["fan_lip_od_mm"]
cylinder(doc, "Nominal minimum-OD body: 66 long, OD 74; actual taper unmeasured", [px, 0, fz], C["fan_minimum_housing_od_mm"] / 2, duct_length, [1, 0, 0])
ring_shape = next(shape for label, shape in nominal_fan_shapes(CONFIG) if label == "Measured raised center ring")
ring_shape.translate(App.Vector(ear_x, 0, fz))
add(doc, "Measured raised center ring", ring_shape)
add(doc, "Measured inlet lip outline; axial lip profile unmeasured",
    Part.makeCompound([Part.makeCircle(lip_diameter / 2, App.Vector(px - duct_length / 2, 0, fz), App.Vector(1, 0, 0))]))
ear_height = C["fan_ear_height_along_duct_mm"]
ear_width = C["fan_ear_width_reported_mm"]
ear_thickness = C["fan_ear_thickness_along_fastener_mm"]
for sign in (-1, 1):
    ey = sign * EAR["hole_center_lateral_offset_mm"]
    ear = Part.makeBox(ear_height, ear_width, ear_thickness,
                       App.Vector(ear_x - ear_height / 2, ey - ear_width / 2, fz - ear_thickness / 2))
    hole = Part.makeCylinder(C["fan_ear_hole_diameter_mm"] / 2, ear_thickness + 2,
                             App.Vector(ear_x, ey, fz - ear_thickness / 2 - 1))
    feature = add(doc, f"Measured ear {sign:+d}: 20 x 8 x 3, hole 4; center 37 from inlet", ear.cut(hole),
                  "Nominal measured ear model; corners and root fillets omitted. Not a printable replacement ear or retaining bracket.")
    feature.addProperty("App::PropertyLength", "HoleCenterFromInlet").HoleCenterFromInlet = EAR["hole_center_from_inlet_mm"]
box(doc, "Measured ear-span clearance 91; nominal ear geometry spans 90.5", [ear_x, 0, fz],
    [ear_height, C["fan_overall_span_across_ears_mm"], ear_thickness], wire=True)
package_center_x = px + (G["fan_length_allowance_mm"] - duct_length) / 2
box(doc, "Full-package clearance allowance; motor protrusion unmeasured", [package_center_x, 0, fz], [G["fan_length_allowance_mm"], G["fan_max_od_allowance_mm"], G["fan_max_od_allowance_mm"]], wire=True)
scale_h = G["scale_body_envelope_mm"][2]
box(doc, "AWS case clearance allowance; platform center is contact datum", [sx, 0, base_z + scale_h / 2], G["scale_body_envelope_mm"], wire=True)
box(doc, "Owner-measured platform outline", [sx, 0, base_z + scale_h], [100, 100, 0.2], wire=True)
pad_z = base_z + scale_h + 3
cylinder(doc, "Rounded contact pad allowance; must not constrain scale laterally", [sx, 0, pad_z], 10, 6, [0, 0, 1])
rod_low, rod_high = pad_z + 3, pz - 9
cylinder(doc, "Adjustable compression contact rod", [sx, 0, (rod_low + rod_high) / 2], 4, rod_high - rod_low, [0, 0, 1])
box(doc, "Calibration position 120 mm left of pivot", [px - G["thrust_height_above_pivot_mm"], 0, pz + 10], [12, 35, 2], wire=True)
save(doc, "bench_layout")
App.closeDocument(doc.Name)

# A separate printable document keeps existing fan/fixture hardware out of STL.
doc = App.newDocument("RetainingCradle" + REV)
print_shape = cradle_shape(CONFIG)
print_shape.translate(App.Vector(M["base_length_mm"] / 2, M["base_width_mm"] / 2, -MD["base_bottom_z_mm"]))
add(doc, f"Cradle {REV}; print base flat; unpowered assembly prototype", print_shape,
    "PRINTABLE PROTOTYPE; not released for powered testing")
save(doc, CRADLE_NAME)
Mesh.export(list(doc.Objects), str(OUT / (CRADLE_NAME + ".stl")))
mesh = Mesh.Mesh(str(OUT / (CRADLE_NAME + ".stl")))
assert mesh.isSolid() and mesh.CountFacets > 0
print(f"CRADLE STL: {mesh.CountFacets} facets; closed mesh; extent {mesh.BoundBox}")
App.closeDocument(doc.Name)

doc = App.newDocument("RetainingMountAssembly" + REV)
add(doc, f"Cradle {REV} prototype", cradle_shape(CONFIG), "Unpowered assembly prototype; use separate cradle STL for printing")
add(doc, "Mounting board 120 x 140 x 18; four 4.5 mm through holes", mounting_board_shape(CONFIG))
for label, shape in nominal_fan_shapes(CONFIG):
    add(doc, label, shape, "Existing fan interface model; do not print")
for label, shape in fan_fastener_shapes(CONFIG):
    add(doc, label, shape, "Purchased metal hardware; verify actual dimensions and thread engagement")
save(doc, ASSEMBLY_NAME)
App.closeDocument(doc.Name)

(OUT / (CRADLE_NAME + "_preview.svg")).write_text(preview_svg(
    [(cradle_shape(CONFIG), (209, 153, 79))],
    f"Retaining cradle {REV} — one printable part", "48 x 112 mm footprint; 52.5 mm high. Includes the measured center-ring relief."))
scene = [(mounting_board_shape(CONFIG), (204, 179, 139)), (cradle_shape(CONFIG), (209, 153, 79))]
scene += [(shape, (177, 194, 190)) for _, shape in nominal_fan_shapes(CONFIG)]
scene += [(shape, (116, 140, 164)) for _, shape in fan_fastener_shapes(CONFIG)]
(OUT / (ASSEMBLY_NAME + "_preview.svg")).write_text(preview_svg(
    scene, f"Retaining mount {REV} — nominal assembly", "Fan interfaces and center ring in grey; M3 hardware in blue. Motor/wires/board bolts omitted."))

# Two loose semicircular pieces can be held around the housing without snapping
# a ring over the inlet lip. Their clearance is a print trial, not a clamp fit.
doc = App.newDocument("UnpoweredFitGauge")
bore = CONFIG["confirmed"]["fan_minimum_housing_od_mm"] + G["coupon_diametral_clearance_mm"]
outer = bore / 2 + G["coupon_radial_wall_mm"]
height = G["coupon_axial_height_mm"]
ring = Part.makeCylinder(outer, height).cut(Part.makeCylinder(bore / 2, height))
half = ring.common(Part.makeBox(2 * outer + 2, outer + 1, height + 2, App.Vector(-outer - 1, 0, -1)))
for index in range(2):
    shape = half.copy()
    shape.translate(App.Vector(outer + index * (2 * outer + 8), 0, 0))
    add(doc, f"Loose half gauge {index + 1}; bore {bore:g} mm", shape,
        "UNPOWERED FIT CHECK ONLY; no retention, stiffness or containment rating")
save(doc, "unpowered_fit_gauge")
Mesh.export(list(doc.Objects), str(OUT / "unpowered_fit_gauge.stl"))
mesh = Mesh.Mesh(str(OUT / "unpowered_fit_gauge.stl"))
assert mesh.CountFacets > 0
assert mesh.isSolid(), "Gauge mesh must be closed"
print(f"GAUGE STL: {mesh.CountFacets} facets; closed mesh")
App.closeDocument(doc.Name)
