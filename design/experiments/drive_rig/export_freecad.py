"""Generate rolling-rig fit prototypes. Run with freecadcmd from repo root.

Motor/caster patterns start from owner measurements. The selected 8.5 mm motor
pitch fits one mounted motor with free rotation; see PREPARATION.md for progress.
"""
import json
import sys
from pathlib import Path

import FreeCAD as App
import Part
import MeshPart

HERE = Path(__file__).resolve().parent
C = json.loads((HERE / "config.json").read_text())
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
V = App.Vector


def box(x, y, z, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x, y, z))


def hole(x, y, z, r, length, axis=(0, 0, 1)):
    return Part.makeCylinder(r, length, V(x, y, z), V(*axis))


def merged(shapes):
    result = shapes[0]
    for item in shapes[1:]:
        result = result.fuse(item)
    return result.removeSplitter()


def cuts(shape, tools):
    for tool in tools:
        shape = shape.cut(tool)
    return shape.removeSplitter()


def moved(shape, delta):
    result = shape.copy()
    result.translate(V(*delta))
    return result


def deck():
    # Flat underside at z=0: no support required. Stiffening ribs face upward.
    w, length = C['deck']['width'], C['deck']['length']
    t, rh = C['deck']['thickness'], C['deck']['rib_height']
    shape = merged([box(-w/2, 0, 0, w, length, t),
        box(-w/2, 0, t, 4, length, rh), box(w/2-4, 0, t, 4, length, rh),
        box(-w/2, 0, t, w, 4, rh), box(-w/2, length-4, t, w, 4, rh),
        box(-w/2, 40, t, w, 8, rh), box(-w/2, 82, t, w, 8, rh)])
    tools = []
    # Motor feet bolt through the transverse ribs using M3 x 25 plus washers.
    for sign in (-1, 1):
        for x in (66, 82):
            for y in (45, 85):
                tools.append(hole(sign*x, y, -1, 1.7, 16))
        for y in (60, 70):
            tools.append(hole(sign*74, y, -1, 1.7, 16))
    # Battery straps, two 15 mm-wide straps around the crosswise pack.
    for x in (-45, 45):
        for y in (92, 148):
            tools.append(box(x-8, y-1.5, -1, 16, 3, 16))
    # Tray support columns, outside the 140 mm battery allowance.
    for x in (-78, 78):
        for y in (72, 128):
            tools.append(hole(x, y, -1, 1.7, 16))
    # Rear caster riser: four holes, clear of the Pi and driver carriers.
    for x in (-22, 22):
        for y in (195, 225):
            tools.append(hole(x, y, -1, 1.7, 16))
    # Raspberry Pi official bare-board mounting pitch; M2.5 clearance.
    for x in (-96.5, -38.5):
        for y in (163.5, 212.5):
            tools.append(hole(x, y, -1, 1.4, 16))
    # Two separate electronics carriers for 30 x 41 controller boards.
    for x in (15, 55, 63, 103):
        for y in (153, 199):
            tools.append(hole(x, y, -1, 1.7, 16))
    # Rear supply/stop switch mounting and wiring tie points; no fixed PCB pattern.
    for x in (40, 65, 90):
        for y in (218, 230):
            tools.append(box(x-6, y-1.5, -1, 12, 3, 16))
    return cuts(shape, tools)


def bracket():
    # Measured 13 mm motor ends at wheel inner face X=114.
    y = C['wheel']['axle_y']
    z = C['wheel']['diameter']/2
    face_x = 114 - C['motor']['actual_length_mm']
    back_x = face_x - 4
    plate = box(back_x, y-25, 10, 4, 50, 40)
    foot = box(60, y-25, 46, face_x-60, 50, 4)
    gussets = []
    for gy in (y-25, y+21):
        points = [V(60, gy, 46), V(back_x, gy, 14), V(back_x, gy, 46), V(60, gy, 46)]
        gussets.append(Part.Face(Part.makePolygon(points)).extrude(V(0, 4, 0)))
    shape = merged([plate, foot] + gussets)
    tools = [hole(back_x-1, y, z, 2.3, 6, (1, 0, 0))]
    py, pz = C['motor']['stationary_hole_pattern_mm']
    for sy in (-1, 1):
        for sz in (-1, 1):
            tools.append(hole(back_x-1, y+sy*py/2, z+sz*pz/2, 1.15, 6, (1, 0, 0)))
    for x in (66, 82):
        for yy in (45, 85):
            tools.append(hole(x, yy, 42, 1.7, 10))
    for yy in (60, 70):
        tools.append(hole(74, yy, 42, 1.7, 10))
    # Nut/bolt access channels through the gussets under each foot fastener.
    for x in (66, 82):
        for yy in (45, 85):
            tools.append(hole(x, yy, 9, 3.5, 37))
    result = cuts(shape, tools)
    centers = {(round(e.Curve.Center.y, 6), round(e.Curve.Center.z, 6))
               for e in result.Edges
               if isinstance(e.Curve, Part.Circle) and abs(e.Curve.Radius-1.15) < 1e-6}
    assert centers == {(round(y+sy*py/2, 6), round(z+sz*pz/2, 6))
                       for sy in (-1, 1) for sz in (-1, 1)}, centers
    return result


def caster_riser():
    # 37 mm total drop from deck underside z=50 to provisional caster datum z=13.
    # Two 4 mm flanges + four 29 mm columns; owner-measured 34 mm caster pitch.
    shape = merged([box(-28, 190, 13, 56, 40, 4), box(-28, 190, 46, 56, 40, 4)] +
                   [box(x-4, y-4, 17, 8, 8, 29) for x in (-22, 22) for y in (195, 225)])
    tools = [hole(x, y, 12, 1.7, 40) for x in (-22, 22) for y in (195, 225)]
    for sign in (-1, 1):
        tools.append(hole(sign*C['caster']['mount_hole_spacing_mm']/2, 210, 12, 1.85, 6))
    return cuts(shape, tools)


def tray():
    shape = merged([box(-84, 65, 96, 168, 70, 4),
        box(-84, 65, 100, 168, 3, 10), box(-84, 132, 100, 168, 3, 10),
        box(-84, 65, 100, 3, 70, 10), box(81, 65, 100, 3, 70, 10)])
    tools = [hole(x, y, 95, 1.7, 8) for x in (-78, 78) for y in (72, 128)]
    for x in (-40, 40):
        for y in (70, 130):
            tools.append(box(x-8, y-1.5, 95, 16, 3, 8))
    return cuts(shape, tools)


def column():
    # 42 mm between deck top and ballast tray underside; M3 x 60 through bolt.
    return hole(0, 0, 0, 5, 42).cut(hole(0, 0, -1, 1.7, 44))


def carrier():
    # Flat generic carrier; strap across a COMPONENT-FREE board edge only.
    shape = box(-24, -27, 0, 48, 54, 3)
    tools = [hole(x, y, -1, 1.7, 5) for x in (-20, 20) for y in (-23, 23)]
    for y in (-19, 19):
        for x in (-20, 20):
            tools.append(box(x-1.5, y-3, -1, 3, 6, 5))
    return cuts(shape, tools)


def motor_coupon(pitch_mm=None, notches=0):
    # The default coupon and full bracket share the selected pitch. Explicit
    # comparison pitches are retained as fit references with the same screw stack.
    px, py = C['motor']['stationary_hole_pattern_mm'] if pitch_mm is None else (pitch_mm, pitch_mm)
    shape = box(-10, -10, 0, 20, 20, 4)
    tools = [hole(0, 0, -1, 2.3, 6)]
    for x in (-px/2, px/2):
        for y in (-py/2, py/2):
            tools.append(hole(x, y, -1, 1.15, 6))
    # Edge notches identify printed coupons without changing motor contact faces.
    for i in range(notches):
        x = (i-(notches-1)/2)*3
        tools.append(box(x-0.75, 8.5, -1, 1.5, 2.5, 6))
    result = cuts(shape, tools)
    # Inspect the finished BRep: four complete mounting bores at the trial pitch.
    centers = {(round(e.Curve.Center.x, 6), round(e.Curve.Center.y, 6))
               for e in result.Edges
               if isinstance(e.Curve, Part.Circle) and abs(e.Curve.Radius-1.15) < 1e-6}
    assert centers == {(round(x, 6), round(y, 6))
                       for x in (-px/2, px/2) for y in (-py/2, py/2)}, centers
    return result


def encoder_carrier():
    # Owner-measured HiLetgo board: 23 x 23 mm, 16 x 16 mm pitch, 4 mm holes.
    # Preserve the entire mounting foot while revising only the PCB bores.
    # M3 screws use 3.4 mm carrier clearance; PCB holes allow final centering.
    shape = merged([box(78.5, 49, 17, 3, 32, 29), box(68, 49, 42, 13.5, 32, 4)])
    tools = [hole(74, y, 41, 1.7, 6) for y in (60, 70)]
    py, pz = C['encoder']['hole_pitch_mm']
    radius = C['encoder']['carrier_design']['mount_clearance_hole_diameter_mm']/2
    for sy in (-1, 1):
        for sz in (-1, 1):
            tools.append(hole(77.5, 65+sy*py/2, 30+sz*pz/2, radius, 5, (1, 0, 0)))
    result = cuts(shape, tools)
    # Inspect finished horizontal bores; distinguish vertical deck-foot holes.
    centers = {(round(e.Curve.Center.y, 6), round(e.Curve.Center.z, 6))
               for e in result.Edges if isinstance(e.Curve, Part.Circle)
               and abs(e.Curve.Radius-radius) < 1e-6
               and abs(e.Curve.Axis.x) > .99}
    assert centers == {(65+sy*py/2, 30+sz*pz/2)
                       for sy in (-1, 1) for sz in (-1, 1)}, centers
    return result


def magnet_geometry(cup_front_x_mm=None):
    e = C['encoder']
    d = e['magnet_carrier_design']
    diameter, thickness = e['magnet_mm']
    pocket_d = diameter+d['pocket_diameter_allowance_mm']
    pocket_depth = thickness+d['pocket_depth_allowance_mm']
    front = d['cup_front_x_mm'] if cup_front_x_mm is None else cup_front_x_mm
    floor = front+pocket_depth
    back = floor+d['cup_floor_mm']
    stem_start = 114-C['motor']['actual_length_mm']
    return {'pocket_diameter_mm': pocket_d, 'pocket_depth_mm': pocket_depth,
            'cup_front_x_mm': front, 'pocket_floor_x_mm': floor,
            'cup_back_x_mm': back, 'magnet_front_x_mm': floor-thickness,
            'cup_outer_diameter_mm': pocket_d+2*d['cup_wall_mm'],
            'stem_start_x_mm': stem_start}


def magnet_carrier(cup_front_x_mm=None, shaft_diameter_mm=None):
    # Cup opens inward, away from motor. A 3 mm locating stem enters the rotating
    # bore. Use the selected trial diameter; gauge fit does not qualify the holder.
    g = magnet_geometry(cup_front_x_mm)
    e = C['encoder']
    neck_d = e['magnet_carrier_design']['neck_diameter_mm']
    stem_d, stem_length = e['magnet_carrier_stem_mm']
    if shaft_diameter_mm is not None:
        neck_d = stem_d = shaft_diameter_mm
    chamfer = e['magnet_carrier_design']['tip_chamfer_length_mm']
    radial = e['magnet_carrier_design']['tip_chamfer_radial_mm']
    assert 0 < chamfer < stem_length and 0 < radial < stem_d/2
    front, back, stem = (g[k] for k in ('cup_front_x_mm', 'cup_back_x_mm', 'stem_start_x_mm'))
    assert front < back < stem and 0 < neck_d < 4.6 and 0 < stem_d < 4
    cup = hole(front, 65, 30, g['cup_outer_diameter_mm']/2, back-front, (1, 0, 0)).cut(
          hole(front-.1, 65, 30, g['pocket_diameter_mm']/2, g['pocket_depth_mm']+.1, (1, 0, 0)))
    result = merged([cup, hole(back, 65, 30, neck_d/2, stem-back, (1, 0, 0)),
                     hole(stem, 65, 30, stem_d/2, stem_length-chamfer, (1, 0, 0)),
                     Part.makeCone(stem_d/2, stem_d/2-radial, chamfer,
                                   V(stem+stem_length-chamfer, 65, 30), V(1, 0, 0))])
    # Verify the finished pocket opening and floor from circular BRep edges.
    pocket_edges = {round(edge.Curve.Center.x, 6) for edge in result.Edges
                    if isinstance(edge.Curve, Part.Circle)
                    and abs(edge.Curve.Radius-g['pocket_diameter_mm']/2) < 1e-6}
    assert pocket_edges == {round(front, 6), round(g['pocket_floor_x_mm'], 6)}, pocket_edges
    return result


def magnet_stem_gauge(diameter, notches):
    # Preserve already-printed gauges when the full holder's reach changes.
    g = magnet_geometry(C['encoder']['magnet_stem_fit']['gauge_reference_cup_front_x_mm'])
    trial = C['encoder']['magnet_stem_fit']
    base_t = g['cup_back_x_mm']-g['cup_front_x_mm']
    neck_length = g['stem_start_x_mm']-g['cup_back_x_mm']
    neck_d = C['encoder']['magnet_carrier_design']['neck_diameter_mm']
    stem_z = base_t+neck_length
    length = trial['insertion_length_mm']
    chamfer = trial['tip_chamfer_length_mm']
    radial = trial['tip_chamfer_radial_mm']
    assert 0 < chamfer < length and 0 < radial < diameter/2
    base = cuts(box(0, 0, 0, 12, 18, base_t),
                [hole(2+2*i, 18, -1, .65, base_t+2) for i in range(notches)])
    result = merged([base, hole(6, 5, base_t, neck_d/2, neck_length),
                     hole(6, 5, stem_z, diameter/2, length-chamfer),
                     Part.makeCone(diameter/2, diameter/2-radial, chamfer,
                                   V(6, 5, stem_z+length-chamfer), V(0, 0, 1))])
    # Verify the finished full-diameter measuring land, not only the tip.
    z_edges = {round(edge.Curve.Center.z, 6) for edge in result.Edges
               if isinstance(edge.Curve, Part.Circle)
               and abs(edge.Curve.Radius-diameter/2) < 1e-6}
    assert round(stem_z+length-chamfer, 6) in z_edges, z_edges
    return result


def print_orientation(shape, kind):
    result = shape.copy()
    if kind in ('motor_bracket', 'encoder_carrier'):
        # Plate against bed, gussets printed as continuous layers into the foot.
        result.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    if kind.startswith('magnet_carrier'):
        # Cup opening on bed, stem up: bridge the configured pocket (4.4 mm).
        result.rotate(V(0, 0, 0), V(0, 1, 0), -90)
    if kind == 'caster_riser':
        # On its side: avoid a 29 mm vertical unsupported upper flange.
        result.rotate(V(0, 0, 0), V(1, 0, 0), 90)
    bb = result.BoundBox
    result.translate(V(-bb.XMin, -bb.YMin, -bb.ZMin))
    return result


def add(doc, name, shape, scope):
    assert shape.isValid() and not shape.isNull(), name
    obj = doc.addObject('PartDesign::Feature', 'P'+str(len(doc.Objects)))
    obj.Label, obj.Shape = name, shape
    obj.addProperty('App::PropertyString', 'Scope').Scope = scope
    return obj


parts = {'deck': (deck(), 1), 'motor_bracket': (bracket(), 2),
         'caster_riser': (caster_riser(), 1), 'ballast_tray': (tray(), 1),
         'tray_column': (column(), 4), 'electronics_carrier': (carrier(), 2),
         'motor_mount_coupon': (motor_coupon(), 1),
         'encoder_carrier': (encoder_carrier(), 2), 'magnet_carrier': (magnet_carrier(), 2)}
tape_trial = C['encoder']['tape_wrap_trial']
tape_name = Path(tape_trial['file']).stem
parts[tape_name] = (magnet_carrier(tape_trial['cup_front_x_mm'], tape_trial['shaft_diameter_mm']), 1)
trials = []
for pitch, notches in zip(C['motor']['mount_fit']['comparison_square_pitches_mm'],
                          C['motor']['mount_fit']['comparison_edge_notches']):
    name = 'motor_mount_coupon_' + f'{pitch:.2f}'.replace('.', 'p') + 'mm'
    parts[name] = (motor_coupon(pitch, notches), 1)
    trials.append({'name': name, 'adjacent_hole_pitch_mm': [pitch, pitch],
                   'edge_notches': notches, 'mounting_hole_diameter_mm': 2.3})
stem_trials = []
stem_fit = C['encoder']['magnet_stem_fit']
for diameter, notches in zip(stem_fit['diameter_trials_mm'], stem_fit['trial_edge_notches']):
    name = 'magnet_stem_gauge_' + f'{diameter:.1f}'.replace('.', 'p') + 'mm'
    parts[name] = (magnet_stem_gauge(diameter, notches), 1)
    stem_trials.append({'name': name, 'diameter_mm': diameter, 'edge_notches': notches,
                        'insertion_length_mm': stem_fit['insertion_length_mm'],
                        'tip_chamfer_length_mm': stem_fit['tip_chamfer_length_mm']})
report = {'revision': C['revision'], 'status': C['status'], 'parts': [],
          'encoder_retention_failure': C['encoder']['retention_failure'],
          'encoder_retention_redesign': C['encoder']['retention_redesign'],
          'encoder_tape_wrap_trial': tape_trial,
          'encoder_metal_rod_proposal': C['encoder']['metal_rod_proposal'],
          'assembly_scope': 'Historical inboard encoder arrangement; bore-plug retention failed physically; nominal geometry checks do not establish fit',
          'magnet_stem_fit': stem_fit, 'magnet_stem_trials': stem_trials,
          'motor_mount_comparison': trials,
          'motor_bracket_square_pitch_mm': C['motor']['stationary_hole_pattern_mm'],
          'confirmed_coupon_pitch_mm': C['motor']['mount_fit']['confirmed_print_pitch_mm'],
          'not_verified': ['actual component fit', 'print strength/load capacity',
                           'motor bearing capacity', 'sensor magnetic field/actual gap', 'powered operation']}
# Compare the finished full-holder tip with the selected gauge, in common
# assembly coordinates. This includes the cylindrical land and entry chamfer.
selected = next(t for t in stem_trials if t['diameter_mm'] == stem_fit['selected_stem_diameter_mm'])
gauge = parts[selected['name']][0].copy()
gauge.rotate(V(0, 0, 0), V(0, 1, 0), 90)
mg = magnet_geometry()
gauge.translate(V(stem_fit['gauge_reference_cup_front_x_mm'], 60, 36))
tip_region = hole(mg['stem_start_x_mm'], 65, 30, 3,
                  stem_fit['insertion_length_mm'], (1, 0, 0))
gauge_tip = gauge.common(tip_region)
holder_tip = parts['magnet_carrier'][0].common(tip_region)
assert gauge_tip.Volume > 0 and holder_tip.Volume > 0
assert gauge_tip.cut(holder_tip).Volume < 1e-6
assert holder_tip.cut(gauge_tip).Volume < 1e-6
report['carrier_stem_matches_selected_gauge'] = True
doc = App.newDocument('DriveRigPrintableParts')
for name, (shape, qty) in parts.items():
    assert len(shape.Solids) == 1 and shape.isValid(), name
    printed = print_orientation(shape, name)
    bb = printed.BoundBox
    assert bb.XLength <= 275 and bb.YLength <= 275 and bb.ZLength <= 250, name
    mesh = MeshPart.meshFromShape(Shape=printed, LinearDeflection=0.12,
                                  AngularDeflection=0.25, Relative=False)
    assert mesh.isSolid() and mesh.CountFacets > 0, name
    mesh.write(str(OUT / (name + '.stl')))
    if name == 'magnet_carrier':
        magnet_filename = C['encoder']['magnet_carrier_design']['file']
        mesh.write(str(OUT / magnet_filename))
        for alias in C['encoder']['magnet_carrier_design']['compatibility_files']:
            mesh.write(str(OUT / alias))
        report['magnet_carrier_versioned_file'] = magnet_filename
    if name == 'encoder_carrier':
        encoder_filename = C['encoder']['carrier_design']['file']
        mesh.write(str(OUT / encoder_filename))
        report['encoder_carrier_versioned_file'] = encoder_filename
    if name == 'motor_bracket':
        py, pz = C['motor']['stationary_hole_pattern_mm']
        assert py == pz, 'Use a two-axis filename for a non-square bracket pattern'
        pitch_label = f'{py:.2f}'.replace('.', 'p')
        bracket_filename = f'motor_bracket_{pitch_label}mm.stl'
        mesh.write(str(OUT / bracket_filename))
        report['motor_bracket_versioned_file'] = bracket_filename
    add(doc, name, printed, C['status'])
    report['parts'].append({'name': name, 'quantity': qty,
        'print_extent_mm': [round(bb.XLength, 2), round(bb.YLength, 2), round(bb.ZLength, 2)],
        'closed_mesh': True, 'valid_single_solid': True,
        'solid_volume_cm3': round(shape.Volume/1000, 2)})
    if name == tape_name:
        assert abs(bb.ZLength-tape_trial['overall_length_mm']) < 1e-6
        # Confirm this trial changes the whole shaft and preserves the cup/pocket.
        tg = magnet_geometry(tape_trial['cup_front_x_mm'])
        shaft_start = tg['cup_back_x_mm']
        shaft_end = tg['stem_start_x_mm']+C['encoder']['magnet_carrier_stem_mm'][1]
        shaft = shape.common(hole(shaft_start+.01, 65, 30, 4, shaft_end-shaft_start-.02, (1, 0, 0)))
        assert abs(shaft.BoundBox.YLength-tape_trial['shaft_diameter_mm']) < 1e-6
        assert abs(shaft.BoundBox.ZLength-tape_trial['shaft_diameter_mm']) < 1e-6
        tape_a, tape_b = tape_trial['tape_band_distance_from_tip_mm']
        assert 0 < tape_a < tape_b < tape_trial['entry_trial_depth_mm']
        report['parts'][-1].update(
            print_ready=tape_trial['print_ready'], physical_fit_confirmed=False, powered_use_released=False,
            shaft_diameter_mm=tape_trial['shaft_diameter_mm'],
            pocket_diameter_mm=tg['pocket_diameter_mm'], pocket_depth_mm=tg['pocket_depth_mm'],
            scope='Retired tape trial: enters bore but wobbles and lacks reach; see ENCODER_METAL_ROD.md')
    if name == 'magnet_carrier' or name.startswith('magnet_stem_gauge_'):
        report['parts'][-1].update(
            print_ready=False,
            scope='Retired bore-plug prototype / reference gauge; no further fit prints; see ENCODER_RETENTION.md')
    elif name == 'encoder_carrier':
        report['parts'][-1].update(
            print_ready=False,
            scope='Existing inboard board support; hold duplicate prints pending retention redesign')

# One convenient print file, with the two individually valid coupons 4 mm apart.
comparison = Part.makeCompound([moved(print_orientation(parts[t['name']][0], t['name']),
                                     (i*24, 0, 0)) for i, t in enumerate(trials)])
assert comparison.isValid() and len(comparison.Solids) == len(trials)
comparison_mesh = MeshPart.meshFromShape(Shape=comparison, LinearDeflection=0.12,
                                         AngularDeflection=0.25, Relative=False)
assert comparison_mesh.isSolid()
comparison_mesh.write(str(OUT / 'motor_mount_coupon_comparison.stl'))
report['motor_mount_comparison_print'] = {
    'file': 'motor_mount_coupon_comparison.stl', 'separate_solids': len(trials),
    'closed_mesh': True,
    'print_extent_mm': [round(v, 2) for v in (comparison.BoundBox.XLength,
                         comparison.BoundBox.YLength, comparison.BoundBox.ZLength)]}
stem_comparison = Part.makeCompound([
    moved(parts[t['name']][0], (i*16, 0, 0)) for i, t in enumerate(stem_trials)])
assert stem_comparison.isValid() and len(stem_comparison.Solids) == len(stem_trials)
stem_mesh = MeshPart.meshFromShape(Shape=stem_comparison, LinearDeflection=0.12,
                                  AngularDeflection=0.25, Relative=False)
assert stem_mesh.isSolid()
stem_mesh.write(str(OUT / stem_fit['gauge_file']))
add(doc, 'Magnet stem fit gauges (combined print)', stem_comparison,
    'Unpowered fit tools, not installed robot parts; one through five edge notches identify ascending sizes')
report['magnet_stem_comparison_print'] = {
    'file': stem_fit['gauge_file'], 'separate_solids': len(stem_trials), 'closed_mesh': True,
    'print_extent_mm': [round(v, 2) for v in (stem_comparison.BoundBox.XLength,
                         stem_comparison.BoundBox.YLength, stem_comparison.BoundBox.ZLength)]}
doc.recompute()
doc.saveAs(str(OUT / 'print_parts.FCStd'))
App.closeDocument(doc.Name)

doc = App.newDocument('DriveRigAssembly')
assembly = []
def assembled(label, shape, scope='Printed fit prototype'):
    add(doc, label, shape, scope)
    assembly.append((label, shape, scope))

assembled('Deck', moved(parts['deck'][0], (0, 0, 50)))
assembled('Right motor bracket', parts['motor_bracket'][0])
left = parts['motor_bracket'][0].mirror(V(0, 0, 0), V(1, 0, 0))
assembled('Left motor bracket', left)
assembled('Caster riser', parts['caster_riser'][0])
assembled('Ballast tray', parts['ballast_tray'][0])
for x in (-78, 78):
    for y in (72, 128):
        assembled('Tray column '+str((x, y)), moved(parts['tray_column'][0], (x, y, 54)))
for x in (35, 83):
    assembled('Controller carrier '+str(x), moved(parts['electronics_carrier'][0], (x, 176, 64)))
# The owner's measured gap supersedes the old assumed seating. Keep the PCB
# reference stack, infer a holder pose consistent with the baseline 4 mm gap,
# then apply the longer part at that same pose. This does NOT measure insertion.
ed = C['encoder']['carrier_design']
reference_chip_face_x = (81.5+ed['spacer_height_mm']+
                        ed['pcb_thickness_allowance_mm']+ed['chip_projection_allowance_mm'])
adjustment = C['encoder']['gap_adjustment']
baseline_mg = magnet_geometry(C['encoder']['magnet_carrier_design']['baseline_cup_front_x_mm'])
holder_pose_shift = (reference_chip_face_x+adjustment['measured_chip_face_to_magnet_gap_mm']-
                     baseline_mg['magnet_front_x_mm'])
assert abs(baseline_mg['cup_front_x_mm']-mg['cup_front_x_mm']-
           adjustment['requested_neck_extension_mm']) < 1e-6
report['measured_gap_adjustment'] = dict(adjustment,
    inferred_holder_translation_x_mm=round(holder_pose_shift, 3),
    unadjusted_reference_gap_mm=round(mg['magnet_front_x_mm']-reference_chip_face_x, 3),
    insertion_depth_verified=False)
for s in (-1, 1):
    assembled('Owned wheel '+str(s), hole(s*114, 65, 30, 30, 8, (s, 0, 0)), 'Owned 60 x 8 mm reference')
    motor = hole(s*101, 65, 30, 14, 13, (s, 0, 0)).cut(hole(s*100, 65, 30, 2, 15, (s, 0, 0)))
    assembled('Owned motor '+str(s), motor,
              'Owner measured 28 diameter x 13 mm; wires and screw heads not represented')
    for name in ('encoder_carrier', 'magnet_carrier'):
        shape = parts[name][0]
        if name == 'magnet_carrier':
            shape = moved(shape, (holder_pose_shift, 0, 0))
        if s < 0:
            shape = shape.mirror(V(0, 0, 0), V(1, 0, 0))
        assembled(name+' '+str(s), shape,
                  'Gap-based illustrative pose; actual insertion depth unknown' if name == 'magnet_carrier'
                  else 'Printed fit prototype')
    ed = C['encoder']['carrier_design']
    by, bz, _ = C['encoder']['board_mm']
    py, pz = C['encoder']['hole_pitch_mm']
    pcb_x = 81.5+ed['spacer_height_mm']
    pcb_t = ed['pcb_thickness_allowance_mm']
    pcb = box(pcb_x, 65-by/2, 30-bz/2, pcb_t, by, bz)
    for sy in (-1, 1):
        for sz in (-1, 1):
            cy, cz = 65+sy*py/2, 30+sz*pz/2
            pcb = pcb.cut(hole(pcb_x-1, cy, cz, C['encoder']['mount_hole_diameter_mm']/2, pcb_t+2, (1, 0, 0)))
            spacer = hole(81.5, cy, cz, ed['spacer_outer_diameter_mm']/2, ed['spacer_height_mm'], (1, 0, 0)).cut(
                     hole(81.4, cy, cz, 1.7, ed['spacer_height_mm']+.2, (1, 0, 0)))
            if s < 0:
                spacer = spacer.mirror(V(0, 0, 0), V(1, 0, 0))
            assembled('Encoder spacer '+str((s, sy, sz)), spacer, '3 mm spacer reference; actual fit/gap to check')
    chip_y, chip_z = ed['chip_plan_allowance_mm']
    chip = box(pcb_x+pcb_t, 65-chip_y/2, 30-chip_z/2,
               ed['chip_projection_allowance_mm'], chip_y, chip_z)
    if s < 0:
        pcb = pcb.mirror(V(0, 0, 0), V(1, 0, 0))
        chip = chip.mirror(V(0, 0, 0), V(1, 0, 0))
    assembled('HiLetgo AS5600 PCB '+str(s), pcb, 'Owner outline/hole pattern; 1.6 mm thickness allowance, other components/wires omitted')
    assembled('Sensor package allowance '+str(s), chip, '8 x 8 mm plan, 1.8 mm projection allowance; not a measured package')
    mg = magnet_geometry()
    magnet_d, magnet_t = C['encoder']['magnet_mm']
    assembled('Included encoder magnet '+str(s),
              hole(s*(mg['magnet_front_x_mm']+holder_pose_shift), 65, 30, magnet_d/2, magnet_t, (s, 0, 0)),
              'Owner-reported 4 x 2 mm; gap-based illustrative pose; field and insertion depth unverified')
chip_face_x = pcb_x+pcb_t+ed['chip_projection_allowance_mm']
gap = round(mg['magnet_front_x_mm']+holder_pose_shift-chip_face_x, 3)
assert gap == C['encoder']['nominal_chip_to_magnet_gap_mm'] and gap > 0
assert gap == adjustment['expected_gap_same_seating_mm']
report['magnet_mount'] = dict(mg, magnet_mm=C['encoder']['magnet_mm'],
    nominal_chip_face_to_cup_edge_mm=round(mg['cup_front_x_mm']+holder_pose_shift-chip_face_x, 3),
    inferred_holder_translation_x_mm=round(holder_pose_shift, 3),
    stem_mm=C['encoder']['magnet_carrier_stem_mm'], magnetic_qualification=False,
    tip_chamfer_length_mm=C['encoder']['magnet_carrier_design']['tip_chamfer_length_mm'],
    tip_chamfer_radial_mm=C['encoder']['magnet_carrier_design']['tip_chamfer_radial_mm'],
    physical_fit_confirmed=False, print_ready=False,
    scope='Retired bore-plug prototype: reported retention failure and drag. Historical gap calculation with inferred pose; actual insertion, PCB stack and field unverified')
report['encoder_mount'] = {
    'board_outline_mm': C['encoder']['board_mm'][:2],
    'pcb_hole_pitch_mm': C['encoder']['hole_pitch_mm'],
    'pcb_hole_diameter_mm': C['encoder']['mount_hole_diameter_mm'],
    'carrier_hole_diameter_mm': ed['mount_clearance_hole_diameter_mm'],
    'deck_attachment': C['deck']['encoder_carrier_attachment'],
    'nominal_chip_face_to_magnet_mm': gap,
    'pcb_edge_to_carrier_foot_z_gap_mm': 42-(30+bz/2),
    'physical_fit_confirmed': False,
    'scope': 'Measured baseline gap, illustrative holder pose and provisional PCB stack; actual insertion, spacers and field unverified'
}
assembled('Caster flange reference', box(-22.5, 196, 10, 45, 28, 3), 'Owned envelope; holes unknown')
assembled('Caster contact illustrative', Part.makeSphere(5, V(0, 210, 5)), 'Illustrative ball; actual diameter unknown')
bl, bw, bh = C['payload']['battery_body_mm']
ml, mw, mh = C['payload']['wattmeter_body_mm']
assert all(body <= allowance for body, allowance in
           zip((bl, bw, bh), C['payload']['battery_allowance_mm']))
tray_l, tray_w, _ = C['payload']['ballast_tray_mm']
wall = C['payload']['ballast_tray_wall_thickness_mm']
assert ml < tray_l-2*wall and mw < tray_w-2*wall
assembled('Owned battery body', box(-bl/2, C['payload']['battery_center_y']-bw/2, 54, bl, bw, bh),
          'Owner dimensions; 135 mm across deck, cable end toward +X; pad, leads and connectors omitted')
assembled('Owned wattmeter body', box(-ml/2, C['payload']['wattmeter_center_y']-mw/2, 100, ml, mw, mh),
          'Owner dimensions; 86 mm across tray, two cables at each end; leads and connectors omitted')
report['payload_body_fit'] = {
    'battery_body_mm': [bl, bw, bh],
    'battery_allowance_mm': C['payload']['battery_allowance_mm'],
    'battery_total_allowance_remaining_mm': [a-b for a, b in zip(C['payload']['battery_allowance_mm'], (bl, bw, bh))],
    'battery_to_tray_underside_mm_before_padding': C['payload']['ballast_tray_bottom_z']-(54+bh),
    'wattmeter_body_mm': [ml, mw, mh],
    'tray_clear_inside_mm': [tray_l-2*wall, tray_w-2*wall],
    'wattmeter_end_clearance_mm_each': (tray_l-2*wall-ml)/2,
    'wattmeter_side_clearance_mm_each': (tray_w-2*wall-mw)/2,
    'scope': 'Nominal rigid body fit only; physical cable bends, plugs, padding and straps still to check'
}
assembled('Pi 4 board reference', box(-100, 160, 64, 85, 56, 1.6), 'Bare board only; reserve connectors/cooler to Z=105')
for x in (20, 68):
    assembled('Controller reference '+str(x), box(x, 155.5, 72, 30, 41, 12),
              'ST B-G431B-ESC1 PCB outline plus provisional 12 mm thickness')

# Check nominal placements; touch surfaces are allowed, penetration is not.
overlaps = []
for i, (a, ashape, _) in enumerate(assembly):
    for b, bshape, _ in assembly[i+1:]:
        vol = ashape.common(bshape).Volume
        if vol > 0.01:
            overlaps.append({'a': a, 'b': b, 'volume_mm3': round(vol, 3)})
report['nominal_overlap_failures'] = overlaps
assert not overlaps, overlaps
bb = Part.makeCompound([s for _, s, _ in assembly]).BoundBox
report['modeled_assembly_extent_mm'] = [round(bb.XLength, 2), round(bb.YLength, 2), round(bb.ZLength, 2)]
assert bb.XLength <= 275 and bb.YLength <= 275 and bb.ZMax <= 180
doc.recompute()
doc.saveAs(str(OUT / 'drive_rig_assembly.FCStd'))
Part.export(list(doc.Objects), str(OUT / 'drive_rig_assembly.step'))
App.closeDocument(doc.Name)
(OUT / 'geometry_report.json').write_text(json.dumps(report, indent=2)+'\n')
# Reuse the existing generic CAD depth-buffer renderer; no EDF geometry imported.
sys.path.insert(0, str(HERE.parent / 'edf_bench'))
from cad_preview import preview_svg
bracket_preview = preview_svg(
    [(print_orientation(parts['motor_bracket'][0], 'motor_bracket'), (72, 148, 151))],
    'Motor bracket in printing orientation',
    'Model geometry only; slicer supports and adhesion structures are not included.')
bracket_preview = bracket_preview.replace(
    'Unpowered assembly prototype. Use the separate cradle STL for printing.',
    'Motor face plate, perpendicular mounting foot and two reinforcing ribs.')
(OUT / (Path(report['motor_bracket_versioned_file']).stem + '_preview.svg')).write_text(bracket_preview)
encoder_preview = preview_svg(
    [(print_orientation(parts['encoder_carrier'][0], 'encoder_carrier'), (72, 148, 151))],
    'HiLetgo encoder carrier - 16 mm square pitch',
    'Existing inboard board support; hold duplicate prints pending retention redesign.')
encoder_preview = encoder_preview.replace(
    'Unpowered assembly prototype. Use the separate cradle STL for printing.',
    '23 x 23 mm PCB on separate 3 mm spacers. Actual sensor gap remains to check.')
(OUT / (Path(report['encoder_carrier_versioned_file']).stem + '_preview.svg')).write_text(encoder_preview)
magnet_preview = preview_svg(
    [(print_orientation(parts['magnet_carrier'][0], 'magnet_carrier'), (72, 148, 151))],
    'Retired bore-plug magnet carrier',
    'Failed retention and added wheel drag. Historical geometry; do not print/use.')
magnet_preview = magnet_preview.replace(
    'Unpowered assembly prototype. Use the separate cradle STL for printing.',
    'Rigid and tape holders retired. Metal-rod proposal: see ENCODER_METAL_ROD.md.')
(OUT / (Path(report['magnet_carrier_versioned_file']).stem + '_preview.svg')).write_text(magnet_preview)
for alias in C['encoder']['magnet_carrier_design']['compatibility_files']:
    (OUT / (Path(alias).stem + '_preview.svg')).write_text(magnet_preview)
stem_preview = preview_svg(
    [(stem_comparison, (72, 148, 151))],
    'Magnet stem fit gauges - five separate parts',
    'Historical reference only. No further stem trials; bore-plug retention failed.')
stem_preview = stem_preview.replace(
    'Unpowered assembly prototype. Use the separate cradle STL for printing.',
    'See ENCODER_RETENTION.md for the mechanical attachment redesign.')
(OUT / 'magnet_stem_fit_gauges_preview.svg').write_text(stem_preview)
tape_preview = preview_svg(
    [(print_orientation(parts[tape_name][0], tape_name), (72, 148, 151))],
    'Retired tape-wrap magnet carrier',
    'Enters motor bore but wobbles and lacks reach. Historical geometry; do not print/use.')
tape_preview = tape_preview.replace(
    'Unpowered assembly prototype. Use the separate cradle STL for printing.',
    'Metal-rod approach under review before relocating sensor. See ENCODER_METAL_ROD.md.')
(OUT / (tape_name+'_preview.svg')).write_text(tape_preview)
scene = []
for label, shape, scope in assembly:
    color = (121, 142, 155)
    if 'wheel' in label.lower(): color = (47, 55, 62)
    elif 'motor' in label.lower() and 'bracket' not in label.lower(): color = (69, 149, 151)
    elif 'battery' in label.lower(): color = (225, 164, 70)
    elif 'board' in label.lower() or 'PCB' in label or 'Controller reference' in label: color = (77, 151, 105)
    elif 'Ballast' in label: color = (191, 119, 83)
    scene.append((shape, color))
svg = preview_svg(scene, 'Rolling drive rig — historical encoder layout',
    '220 x 240 mm deck; 244 mm across wheels; ballast tray rim at 110 mm. Wires and fasteners omitted.')
svg = svg.replace('Unpowered assembly prototype. Use the separate cradle STL for printing.',
                  'Old holders failed. Metal rod under review; no new geometry released. See ENCODER_METAL_ROD.md.')
(OUT / 'assembly.svg').write_text(svg)
print(json.dumps(report, indent=2))
