"""FreeCAD geometry for the EDF cradle with measured central-ring relief.

Local x follows airflow, origin is at the ear-hole plane on the fan axis.
The two ears face +/-y and their screws follow z. Dimensions are millimetres.
"""
import math

import FreeCAD as App
import Part

from geometry import ear_geometry, center_ring_geometry


def mount_dimensions(config):
    c, m = config["confirmed"], config["retaining_mount"]
    ears = ear_geometry(config)
    bore = c["fan_minimum_housing_od_mm"] + config["layout"]["coupon_diametral_clearance_mm"]
    z_bottom = -m["axis_above_base_bottom_mm"]
    shelf_top = -c["fan_ear_thickness_along_fastener_mm"] / 2
    shelf_bottom = shelf_top - m["ear_shelf_thickness_mm"]
    assert z_bottom + m["base_thickness_mm"] < -bore / 2
    assert m["fan_slot_width_mm"] > m["fan_screw_diameter_mm"]
    assert m["base_length_mm"] > m["body_axial_length_mm"]
    assert m["fan_washer_od_mm"] < c["fan_ear_width_reported_mm"]
    stack = (c["fan_ear_thickness_along_fastener_mm"] + m["ear_shelf_thickness_mm"]
             + 2 * m["fan_washer_thickness_mm"] + m["fan_nut_height_mm"])
    assert m["fan_screw_length_mm"] > stack
    ring = center_ring_geometry(config)
    if z_bottom + m["base_thickness_mm"] >= -ring["relief_diameter_mm"] / 2:
        raise ValueError("Ring relief reaches the base; revise cradle structure before export")
    return {
        "bore_mm": bore,
        "base_bottom_z_mm": z_bottom,
        "shelf_top_z_mm": shelf_top,
        "shelf_bottom_z_mm": shelf_bottom,
        "print_height_mm": shelf_top - z_bottom,
        "hole_y_mm": ears["hole_center_lateral_offset_mm"],
        "fan_screw_stack_mm": stack,
        "fan_screw_projection_beyond_nut_mm": m["fan_screw_length_mm"] - stack,
    }


def box_centered(x_length, y_width, z_low, z_high):
    return Part.makeBox(x_length, y_width, z_high - z_low,
                        App.Vector(-x_length / 2, -y_width / 2, z_low))


def slot_z(x, y, width, travel, z_low, z_high):
    """Capsule slot along y; travel is end-circle center separation."""
    r = width / 2
    shape = Part.makeCylinder(r, z_high - z_low, App.Vector(x, y - travel / 2, z_low))
    shape = shape.fuse(Part.makeCylinder(r, z_high - z_low, App.Vector(x, y + travel / 2, z_low)))
    if travel:
        shape = shape.fuse(Part.makeBox(width, travel, z_high - z_low,
                                       App.Vector(x - r, y - travel / 2, z_low)))
    return shape


def cradle_shape(config, *, relieve_center_ring=True):
    m, d = config["retaining_mount"], mount_dimensions(config)
    bottom, top = d["base_bottom_z_mm"], d["shelf_top_z_mm"]
    body = box_centered(m["body_axial_length_mm"], m["body_width_mm"], bottom, top)
    base = box_centered(m["base_length_mm"], m["base_width_mm"], bottom, bottom + m["base_thickness_mm"])
    shape = body.fuse(base)
    bore = Part.makeCylinder(d["bore_mm"] / 2, m["base_length_mm"] + 2,
                             App.Vector(-m["base_length_mm"] / 2 - 1, 0, 0), App.Vector(1, 0, 0))
    shape = shape.cut(bore)
    if relieve_center_ring:
        ring = center_ring_geometry(config)
        relief = Part.makeCylinder(ring["relief_diameter_mm"] / 2, ring["relief_width_mm"],
                                   App.Vector(ring["relief_start_x_mm"], 0, 0), App.Vector(1, 0, 0))
        shape = shape.cut(relief)
    for sign in (-1, 1):
        y_low = m["nut_window_inner_y_mm"] if sign > 0 else -m["nut_window_outer_y_mm"]
        window = Part.makeBox(m["body_axial_length_mm"] + 2,
                              m["nut_window_outer_y_mm"] - m["nut_window_inner_y_mm"],
                              m["nut_window_depth_mm"],
                              App.Vector(-m["body_axial_length_mm"] / 2 - 1, y_low,
                                         d["shelf_bottom_z_mm"] - m["nut_window_depth_mm"]))
        shape = shape.cut(window)
        shape = shape.cut(slot_z(0, sign * d["hole_y_mm"], m["fan_slot_width_mm"],
                                 m["fan_slot_center_travel_mm"], d["shelf_bottom_z_mm"] - .1, top + 1))
    for x in (-m["base_hole_spacing_x_mm"] / 2, m["base_hole_spacing_x_mm"] / 2):
        for y in (-m["base_hole_spacing_y_mm"] / 2, m["base_hole_spacing_y_mm"] / 2):
            shape = shape.cut(Part.makeCylinder(m["base_hole_diameter_mm"] / 2,
                                                m["base_thickness_mm"] + 2,
                                                App.Vector(x, y, bottom - 1)))
    shape = shape.removeSplitter()
    assert shape.isValid() and len(shape.Solids) == 1
    return shape


def mounting_board_shape(config):
    m, d = config["retaining_mount"], mount_dimensions(config)
    length, width, thickness = m["mounting_board_mm"]
    top = d["base_bottom_z_mm"]
    shape = box_centered(length, width, top - thickness, top)
    for x in (-m["base_hole_spacing_x_mm"] / 2, m["base_hole_spacing_x_mm"] / 2):
        for y in (-m["base_hole_spacing_y_mm"] / 2, m["base_hole_spacing_y_mm"] / 2):
            shape = shape.cut(Part.makeCylinder(m["base_hole_diameter_mm"] / 2, thickness + 2,
                                                App.Vector(x, y, top - thickness - 1)))
    return shape


def nominal_fan_shapes(config):
    """Existing interfaces: minimum-OD body, measured center ring, ears and inlet."""
    c, ears = config["confirmed"], ear_geometry(config)
    inlet_x = -ears["hole_center_from_inlet_mm"]
    body = Part.makeCylinder(c["fan_minimum_housing_od_mm"] / 2,
                             c["fan_duct_length_excluding_motor_mm"],
                             App.Vector(inlet_x, 0, 0), App.Vector(1, 0, 0))
    result = [("Nominal 74 mm body; actual taper and motor not modeled", body)]
    ring = center_ring_geometry(config)
    raised = Part.makeCylinder(ring["outside_diameter_mm"] / 2, ring["axial_width_mm"],
                                App.Vector(ring["start_x_mm"], 0, 0), App.Vector(1, 0, 0))
    result.append(("Measured raised center ring", raised.cut(body)))
    for sign in (-1, 1):
        y = sign * ears["hole_center_lateral_offset_mm"]
        h, w, t = c["fan_ear_height_along_duct_mm"], c["fan_ear_width_reported_mm"], c["fan_ear_thickness_along_fastener_mm"]
        tab = Part.makeBox(h, w, t, App.Vector(-h / 2, y - w / 2, -t / 2))
        hole = Part.makeCylinder(c["fan_ear_hole_diameter_mm"] / 2, t + 2, App.Vector(0, y, -t / 2 - 1))
        result.append((f"Existing ear {sign:+d}", tab.cut(hole)))
    circle = Part.makeCircle(c["fan_lip_od_mm"] / 2, App.Vector(inlet_x, 0, 0), App.Vector(1, 0, 0))
    result.append(("Inlet lip outline; axial lip profile unmeasured", Part.makeCompound([circle])))
    return result


def fan_fastener_shapes(config):
    c, m, d = config["confirmed"], config["retaining_mount"], mount_dimensions(config)
    washer_t = m["fan_washer_thickness_mm"]
    for sign in (-1, 1):
        y = sign * d["hole_y_mm"]
        top_ear = c["fan_ear_thickness_along_fastener_mm"] / 2
        head_bottom = top_ear + washer_t
        shaft = Part.makeCylinder(m["fan_screw_diameter_mm"] / 2, m["fan_screw_length_mm"],
                                  App.Vector(0, y, head_bottom - m["fan_screw_length_mm"]))
        head = Part.makeCylinder(2.75, 3, App.Vector(0, y, head_bottom))
        yield f"M3 x 20 screw {sign:+d}; thread/socket simplified", shaft.fuse(head)
        for label, z in (("upper", top_ear), ("lower", d["shelf_bottom_z_mm"] - washer_t)):
            outer = Part.makeCylinder(m["fan_washer_od_mm"] / 2, washer_t, App.Vector(0, y, z))
            inner = Part.makeCylinder(m["fan_washer_id_mm"] / 2, washer_t + 2, App.Vector(0, y, z - 1))
            yield f"M3 {label} washer {sign:+d}", outer.cut(inner)
        nut_top = d["shelf_bottom_z_mm"] - washer_t
        radius = m["fan_nut_across_flats_mm"] / math.sqrt(3)
        vertices = [App.Vector(radius * math.cos(i * math.pi / 3), y + radius * math.sin(i * math.pi / 3),
                               nut_top - m["fan_nut_height_mm"]) for i in range(6)]
        nut = Part.Face(Part.makePolygon(vertices + vertices[:1])).extrude(App.Vector(0, 0, m["fan_nut_height_mm"]))
        nut = nut.cut(Part.makeCylinder(m["fan_screw_diameter_mm"] / 2, m["fan_nut_height_mm"] + 2,
                                       App.Vector(0, y, nut_top - m["fan_nut_height_mm"] - 1)))
        yield f"M3 locknut {sign:+d}; thread/insert simplified", nut
