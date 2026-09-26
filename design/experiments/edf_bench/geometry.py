"""Mounting coordinates derived from owner measurements, all in millimetres."""
import math


def center_ring_geometry(config):
    """Require measured ring geometry before building the corrected mount."""
    ring = config["housing_profile"]["center_ring"]
    keys = ("outside_diameter_mm", "axial_width_mm", "intake_edge_from_intake_face_mm")
    missing = [key for key in keys if ring.get(key) is None]
    if missing:
        raise ValueError("Central housing ring measurements required: " + ", ".join(missing))
    diameter, width, start = (ring[key] for key in keys)
    if not all(isinstance(v, (float, int)) and math.isfinite(v) for v in (diameter, width, start)):
        raise ValueError("Central housing ring dimensions must be finite numbers")
    c = config["confirmed"]
    if diameter <= c["fan_minimum_housing_od_mm"] or width <= 0 or start < 0 or start + width > c["fan_duct_length_excluding_motor_mm"]:
        raise ValueError("Central housing ring dimensions do not fit the reported duct envelope")
    relief = config["retaining_mount"]["center_ring_relief"]
    radial, axial = relief["radial_clearance_mm"], relief["axial_clearance_each_side_mm"]
    if not all(isinstance(v, (float, int)) and math.isfinite(v) and v > 0 for v in (radial, axial)):
        raise ValueError("Central ring relief clearances must be positive finite numbers")
    ear_plane = ear_geometry(config)["hole_center_from_inlet_mm"]
    return {
        "outside_diameter_mm": diameter,
        "axial_width_mm": width,
        "start_from_inlet_mm": start,
        "center_from_inlet_mm": start + width / 2,
        "end_from_inlet_mm": start + width,
        "start_x_mm": start - ear_plane,
        "relief_start_from_inlet_mm": start - axial,
        "relief_start_x_mm": start - ear_plane - axial,
        "relief_width_mm": width + 2 * axial,
        "relief_diameter_mm": diameter + 2 * radial,
    }


def ear_geometry(config):
    c = config["confirmed"]
    duct = c["fan_duct_length_excluding_motor_mm"]
    height = c["fan_ear_height_along_duct_mm"]
    end_from_motor = c["fan_ear_intake_end_from_motor_side_duct_end_mm"]
    start = duct - end_from_motor
    end = start + height
    center = (start + end) / 2
    width = c["fan_ear_width_reported_mm"]
    hole = c["fan_ear_hole_diameter_mm"]
    spacing = c["fan_ear_hole_center_spacing_mm"]
    assert 0 <= start < center < end <= duct
    assert 0 < hole < min(width, height)
    return {
        "ear_start_from_inlet_mm": start,
        "ear_end_from_inlet_mm": end,
        "hole_center_from_inlet_mm": center,
        "hole_center_from_motor_side_duct_end_mm": duct - center,
        "hole_center_lateral_offset_mm": spacing / 2,
        "nominal_ear_outer_span_mm": spacing + width,
        "measured_span_minus_nominal_mm": c["fan_overall_span_across_ears_mm"] - (spacing + width),
    }
