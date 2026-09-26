"""Generate a dimensioned bench layout and static force-budget report.

All geometry beyond owner measurements is provisional. Uses standard Python.
"""
import html
import json
from pathlib import Path

from geometry import ear_geometry, center_ring_geometry

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def calculate(config):
    c, g, s = config["confirmed"], config["layout"], config["screening"]
    h = g["thrust_height_above_pivot_mm"]
    length = g["scale_contact_left_of_pivot_mm"]
    assert h > 0 and length > 0
    assert 0 <= s["example_static_scale_preload_g"] < s["gross_scale_working_stop_g"] < c["scale_capacity_g"]
    assert 0 < s["initial_current_ceiling_a"] <= s["later_operator_current_stop_a"] < c["meter_continuous_a"]
    ratio = length / h
    hover = s["reference_robot_mass_g"] / s["fan_count"]
    target = hover * s["reference_thrust_weight_target"]
    return {
        "status": config["status"],
        "mount_revision": config["retaining_mount"]["revision"],
        "mount_status": config["retaining_mount"]["status"],
        "thrust_to_incremental_scale_ratio": ratio,
        "single_fan_hover_requirement_gf": hover,
        "single_fan_available_thrust_target_gf": target,
        "hover_incremental_scale_g": hover / ratio,
        "target_incremental_scale_g": target / ratio,
        "advertised_thrust_incremental_scale_g": s["advertised_single_fan_thrust_gf"] / ratio,
        "advertised_thrust_example_gross_scale_g": s["example_static_scale_preload_g"] + s["advertised_single_fan_thrust_gf"] / ratio,
        "example_thrust_at_gross_working_stop_gf": (s["gross_scale_working_stop_g"] - s["example_static_scale_preload_g"]) * ratio,
        "display_resolution_equivalent_gf": c["scale_readability_g"] * ratio,
        "coupon_bore_mm": c["fan_minimum_housing_od_mm"] + g["coupon_diametral_clearance_mm"],
        **ear_geometry(config),
        **{"center_ring_" + key: value for key, value in center_ring_geometry(config).items()},
    }


def layout_svg(config):
    c = config["confirmed"]
    m = config["retaining_mount"]
    ears = ear_geometry(config)
    ring = center_ring_geometry(config)
    g = config["layout"]
    px, pz = g["pivot_x_mm"], g["pivot_z_above_base_mm"]
    height, length = g["thrust_height_above_pivot_mm"], g["scale_contact_left_of_pivot_mm"]
    sx, fz = px - length, pz + height
    ear_x = px - c["fan_duct_length_excluding_motor_mm"] / 2 + ears["hole_center_from_inlet_mm"]
    board_top = fz - m["axis_above_base_bottom_mm"]
    board_bottom = board_top - m["mounting_board_mm"][2]
    x = lambda v: 70 + 1.3 * v
    z = lambda v: 515 - 1.1 * v
    items = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="850" viewBox="0 0 1100 850">',
             '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#1e3a5f"/></marker></defs>',
             '<rect width="1100" height="850" fill="#f6f8fb"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#15243a} .small{font-size:14px}.label{font-size:17px}.dim{font-size:15px;fill:#1e3a5f}</style>']

    def text(xp, yp, value, cls="label"):
        items.append(f'<text x="{xp}" y="{yp}" class="{cls}">{html.escape(value)}</text>')

    def line(x1, y1, x2, y2, color="#1e3a5f", width=2, arrow=False, dash=False):
        attrs = (' marker-end="url(#arr)"' if arrow else '') + (' stroke-dasharray="6 5"' if dash else '')
        items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{attrs}/>')

    def rect(xp, yp, w, h, fill, stroke="#1e3a5f"):
        items.append(f'<rect x="{xp}" y="{yp}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}"/>')

    text(45, 42, "EDF bench: horizontal fan / 2:1 force lever")
    if m["status"] == "AWAITING_CENTER_RING_MEASUREMENTS":
        text(45, 68, "V1 FIT FAILED — uncorrected layout shown; v2 center-ring groove awaits measurements", "small")
    else:
        text(45, 68, f"LAYOUT DRAFT — cradle {m['revision']}; complete stand not validated for powered testing", "small")
    text(45, 95, "Side view. Dimensions in mm; drawing schematic. Shielding, bearings, joints and stops require detail design.", "small")
    # Fixed base/support, then moving lever. All heights measured from base top.
    rect(x(0), z(0), 1.3 * g["base_mm"][0], 20, "#d4bd9a")
    rect(x(px - 45), z(pz - 15), 117, (pz - 15) * 1.1, "#dfe5ed")
    text(x(px + 55), z(65), "Fixed twin supports", "small")
    line(x(px), z(pz), x(sx), z(pz), "#d57825", 14)
    line(x(px), z(pz), x(px), z(board_bottom), "#d57825", 14)
    line(x(sx + 40), z(pz), x(px), z(board_bottom), "#d57825", 5)
    rect(x(ear_x - m["mounting_board_mm"][0] / 2), z(board_top),
         1.3 * m["mounting_board_mm"][0], 1.1 * m["mounting_board_mm"][2], "#d4bd9a")
    rect(x(ear_x - m["base_length_mm"] / 2), z(board_top + m["base_thickness_mm"]),
         1.3 * m["base_length_mm"], 1.1 * m["base_thickness_mm"], "#d57825")
    shelf_top = fz - c["fan_ear_thickness_along_fastener_mm"] / 2
    rect(x(ear_x - m["body_axial_length_mm"] / 2), z(shelf_top),
         1.3 * m["body_axial_length_mm"], 1.1 * (shelf_top - board_top), "#d57825")
    items.append(f'<circle cx="{x(px)}" cy="{z(pz)}" r="11" fill="white" stroke="#15243a" stroke-width="3"/>')
    text(x(px + 15), z(pz) - 15, "Pivot, axis across bench", "small")
    scale_h = g["scale_body_envelope_mm"][2]
    rect(x(sx - 66), z(scale_h), 1.3 * 132, scale_h * 1.1, "#c5dbef")
    line(x(sx), z(pz - 7), x(sx), z(scale_h + 6), "#d57825", 5)
    rect(x(sx - 10), z(scale_h + 6), 26, 6.6, "#d57825")
    text(x(sx - 65), 569, "AWS SC-2kg, centered pad", "small")
    text(x(sx - 65), 591, "100 × 100 measured platform", "small")
    line(x(sx + 18), z(100), x(sx + 18), z(40), arrow=True)
    text(x(sx + 28), z(85), "Force onto scale", "small")
    # Measured duct bounding envelope, with separate full-package allowance.
    # The lip diameter bounds the duct; this does not define its actual profile.
    duct_length = c["fan_duct_length_excluding_motor_mm"]
    lip_diameter = c["fan_lip_od_mm"]
    inlet_x = px - duct_length / 2
    rect(x(inlet_x), z(fz + g["fan_max_od_allowance_mm"] / 2),
         1.3 * g["fan_length_allowance_mm"], 1.1 * g["fan_max_od_allowance_mm"], "none", "#a1afb9")
    rect(x(inlet_x), z(fz + lip_diameter / 2), 1.3 * duct_length, 1.1 * lip_diameter, "#b8d7cb")
    rect(x(inlet_x + ring["start_from_inlet_mm"]), z(fz + ring["outside_diameter_mm"] / 2),
         1.3 * ring["axial_width_mm"], 1.1 * ring["outside_diameter_mm"], "#52675d")
    line(x(inlet_x), z(fz), x(inlet_x + g["fan_length_allowance_mm"]), z(fz), dash=True)
    text(x(inlet_x + 7), z(fz) - 10, "Duct", "small")
    line(x(px - 65), z(fz), x(px - 155), z(fz), arrow=True)
    text(x(px - 220), z(fz) - 13, "Thrust left", "label")
    line(x(px + 80), z(fz), x(px + 175), z(fz), arrow=True)
    text(x(px + 80), z(fz) - 13, "Exhaust right", "label")
    text(720, 235, f"Duct {duct_length:g} long; lip Ø{lip_diameter:g}", "small")
    text(720, 257, f"Body Ø{c['fan_minimum_housing_od_mm']:g}; ear span {c['fan_overall_span_across_ears_mm']:g}", "small")
    text(720, 279, f"Holes Ø{c['fan_ear_hole_diameter_mm']:g}, spacing ~{c['fan_ear_hole_center_spacing_mm']:g}", "small")
    text(720, 301, f"Hole centers {ears['hole_center_from_inlet_mm']:g} from inlet face", "small")
    text(720, 323, "Outer outline: 100 × 95 allowance", "small")
    text(720, 345, "Motor protrusion remains unmeasured", "small")
    text(720, 367, f"Center ring Ø{ring['outside_diameter_mm']:g} × {ring['axial_width_mm']:g}; aligned with holes", "small")
    # Dimension lines and calibration point.
    line(x(sx), z(pz) + 38, x(px), z(pz) + 38)
    for a in (sx, px):
        line(x(a), z(pz) + 30, x(a), z(pz) + 46)
    text(x(sx) + 80, z(pz) + 61, f"L = {length:g} to scale pad", "dim")
    line(x(px) + 82, z(pz), x(px) + 82, z(fz))
    for a in (pz, fz):
        line(x(px) + 74, z(a), x(px) + 90, z(a))
    text(x(px) + 95, z(pz + height / 2), f"h = {height:g}", "dim")
    cx = px - height
    items.append(f'<circle cx="{x(cx)}" cy="{z(pz)}" r="5" fill="#15243a"/>')
    text(85, 266, "Calibration point: 120 left of pivot", "small")
    line(210, 273, x(cx), z(pz) - 7, dash=True)
    text(45, 640, "Thrust (g-force) = (gross scale g − baseline g) × L / h")
    text(45, 674, "Here: thrust = 2 × change in scale reading. Example: +500 g on scale means 1,000 g-force thrust.", "small")
    text(45, 709, "Record gross baseline before taring. Proposed working stop: 1,800 g gross; scale capacity: 2,000 g.", "small")
    text(45, 744, "Calibrate the complete mechanism and check return-to-zero. Friction, cable forces and vibration can bias it.", "small")
    text(45, 779, "The moving lever and fan mount contact the fixed structure only through the pivot and scale pad.", "small")
    text(45, 814, "Base allowance: 600 × 320 × 18. Use bolted timber/metal sections, bought bearings/shaft, and fitted adapters.", "small")
    items.append("</svg>")
    return "\n".join(items)


def mount_measurement_svg(config):
    """Show the resolved inlet and motor-side mounting coordinates."""
    duct_length = config["confirmed"]["fan_duct_length_excluding_motor_mm"]
    ears = ear_geometry(config)
    ring = center_ring_geometry(config)
    scale = 290 / duct_length
    hole_y = 425 - ears["hole_center_from_inlet_mm"] * scale
    ear_top_y = 425 - ears["ear_end_from_inlet_mm"] * scale
    ear_height_px = config["confirmed"]["fan_ear_height_along_duct_mm"] * scale
    ring_top_y = 425 - ring["end_from_inlet_mm"] * scale
    ring_width_px = 160 * ring["outside_diameter_mm"] / config["confirmed"]["fan_minimum_housing_od_mm"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="620" viewBox="0 0 820 620">
<defs><marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#215a8e"/></marker></defs>
<rect width="820" height="620" fill="#f6f8fb"/>
<style>text{{font-family:Arial,sans-serif;fill:#15243a;font-size:17px}} .note{{font-size:14px}} .dim{{stroke:#215a8e;stroke-width:2;marker-start:url(#tip);marker-end:url(#tip)}} .guide{{stroke:#215a8e;stroke-width:1.5;stroke-dasharray:5 4}}</style>
<text x="35" y="32" font-weight="bold">Mounting holes and raised center ring: owner measurements</text>
<text x="35" y="57" class="note">Purple motor up, intake lip on the table. The motor-side datum is the duct end, excluding the motor.</text>
<rect x="320" y="135" width="160" height="282" rx="4" fill="#c7ddd3" stroke="#52675d" stroke-width="2"/>
<rect x="{400 - ring_width_px / 2}" y="{ring_top_y}" width="{ring_width_px}" height="{ring['axial_width_mm'] * scale}" fill="#52675d"/>
<rect x="307" y="417" width="186" height="8" fill="#52675d"/>
<rect x="370" y="85" width="60" height="50" rx="5" fill="#ac538f" stroke="#68345d"/>
<text x="456" y="111" class="note">Purple motor</text>
<text x="345" y="305">Fan housing</text>
<rect x="480" y="{ear_top_y}" width="36" height="{ear_height_px}" fill="#c7ddd3" stroke="#52675d" stroke-width="2"/>
<circle cx="498" cy="{hole_y}" r="7" fill="white" stroke="#215a8e" stroke-width="2"/>
<text x="343" y="{hole_y - 21}">Hole center</text>
<line x1="444" y1="{hole_y - 16}" x2="487" y2="{hole_y - 3}" stroke="#215a8e" stroke-width="2" marker-end="url(#tip)"/>
<line x1="498" y1="{hole_y}" x2="590" y2="{hole_y}" class="guide"/>
<line x1="480" y1="135" x2="590" y2="135" class="guide"/>
<line x1="580" y1="135" x2="580" y2="{hole_y}" class="dim"/>
<text x="600" y="191">{ears['hole_center_from_motor_side_duct_end_mm']:g} mm from</text>
<text x="600" y="214">motor-side duct end</text>
<line x1="580" y1="{hole_y}" x2="580" y2="425" class="dim"/>
<text x="600" y="344">D = {ears['hole_center_from_inlet_mm']:g} mm</text>
<text x="600" y="368">from intake face</text>
<line x1="315" y1="135" x2="249" y2="135" class="guide"/>
<line x1="260" y1="135" x2="260" y2="425" class="dim"/>
<text x="120" y="280">{duct_length:g} mm duct</text>
<text x="120" y="301" class="note">Motor excluded</text>
<rect x="100" y="425" width="610" height="20" fill="#d4bd9a" stroke="#88704e"/>
<text x="110" y="470">Tabletop</text>
<text x="319" y="470" class="note">Intake lip rests here</text>
<text x="35" y="508">Ear spans {ears['ear_start_from_inlet_mm']:g}–{ears['ear_end_from_inlet_mm']:g} mm from intake; hole centered at {ears['hole_center_from_inlet_mm']:g} mm.</text>
<text x="35" y="535">Dark ring: Ø{ring['outside_diameter_mm']:g} × {ring['axial_width_mm']:g} mm; center {ring['center_from_inlet_mm']:g} mm from intake.</text>
<text x="35" y="562" class="note">Ring edges: {ring['start_from_inlet_mm']:g}–{ring['end_from_inlet_mm']:g} mm. Cradle groove: Ø{ring['relief_diameter_mm']:g} × {ring['relief_width_mm']:g} mm, same center.</text>
<text x="35" y="595" class="note">Coordinates use the owner measurements. Remaining body profile, motor size and ear corners are schematic.</text>
</svg>'''


def mounting_board_template_svg(config):
    m = config["retaining_mount"]
    length, width, _ = m["mounting_board_mm"]
    rows = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{length:g}mm" height="{width:g}mm" viewBox="{-length/2:g} {-width/2:g} {length:g} {width:g}">',
            '<style>text{font-family:Arial,sans-serif;font-size:3.2px;text-anchor:middle}</style>',
            f'<rect x="{-length/2+.3:g}" y="{-width/2+.3:g}" width="{length-.6:g}" height="{width-.6:g}" fill="white" stroke="black" stroke-width=".3"/>',
            '<text x="0" y="-64">Mounting board: top view, dimensions in mm</text>',
            f'<text x="0" y="-59">4 holes Ø{m["base_hole_diameter_mm"]:g}; {m["base_hole_spacing_x_mm"]:g} × {m["base_hole_spacing_y_mm"]:g} center pattern</text>',
            f'<rect x="{-m["base_length_mm"]/2:g}" y="{-m["base_width_mm"]/2:g}" width="{m["base_length_mm"]:g}" height="{m["base_width_mm"]:g}" fill="none" stroke="#999" stroke-width=".3" stroke-dasharray="2 1"/>']
    for x in (-m["base_hole_spacing_x_mm"] / 2, m["base_hole_spacing_x_mm"] / 2):
        for y in (-m["base_hole_spacing_y_mm"] / 2, m["base_hole_spacing_y_mm"] / 2):
            rows.append(f'<circle cx="{x:g}" cy="{y:g}" r="{m["base_hole_diameter_mm"]/2:g}" fill="none" stroke="black" stroke-width=".3"/>')
            rows.append(f'<path d="M{x-4:g} {y:g}h8 M{x:g} {y-4:g}v8" stroke="black" stroke-width=".2"/>')
    rows += ['<path d="M-40 0H40 l-3 -2 M40 0l-3 2" fill="none" stroke="black" stroke-width=".4"/>',
             '<text x="0" y="-4">Airflow direction / fan axis</text>',
             '<text x="0" y="8">Dashed outline: cradle footprint</text>',
             '<path d="M-25 61v3 M-25 62.5H25 M25 61v3" fill="none" stroke="black" stroke-width=".4"/>',
             '<text x="0" y="68">Check this bar is 50 mm before marking holes</text>', '</svg>']
    return '\n'.join(rows)


def mounting_orientation_svg(config):
    """End-view assembly diagram. Cable curves show routing, not measured shape."""
    c, m = config["confirmed"], config["retaining_mount"]
    scale, cx, cy = 4, 350, 290
    radius = c["fan_minimum_housing_od_mm"] * scale / 2
    bore = (c["fan_minimum_housing_od_mm"] + config["layout"]["coupon_diametral_clearance_mm"]) * scale / 2
    bottom = cy + m["axis_above_base_bottom_mm"] * scale
    top = cy + c["fan_ear_thickness_along_fastener_mm"] * scale / 2
    rows = ['<svg xmlns="http://www.w3.org/2000/svg" width="950" height="630" viewBox="0 0 950 630">',
            '<rect width="950" height="630" fill="#f6f8fb"/>',
            '<style>text{font-family:Arial,sans-serif;font-size:17px;fill:#15243a}.note{font-size:14px}</style>',
            '<text x="35" y="32" font-size="23" font-weight="bold">V2 assembly: one cradle below, cables above</text>',
            '<text x="35" y="57" class="note">End view. Roll the fan about its axis to put the cable exit at the top; keep both ears horizontal.</text>',
            f'<rect x="{cx-m["base_width_mm"]*scale/2}" y="{bottom-m["base_thickness_mm"]*scale}" width="{m["base_width_mm"]*scale}" height="{m["base_thickness_mm"]*scale}" fill="#d1994f"/>',
            f'<rect x="{cx-m["body_width_mm"]*scale/2}" y="{top}" width="{m["body_width_mm"]*scale}" height="{bottom-top}" fill="#d1994f"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{bore}" fill="#f6f8fb"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#c7ddd3" stroke="#52675d" stroke-width="2"/>']
    for sign in (-1, 1):
        ex = cx + sign * c["fan_ear_hole_center_spacing_mm"] * scale / 2
        rows += [f'<rect x="{ex-c["fan_ear_width_reported_mm"]*scale/2}" y="{cy-c["fan_ear_thickness_along_fastener_mm"]*scale/2}" width="{c["fan_ear_width_reported_mm"]*scale}" height="{c["fan_ear_thickness_along_fastener_mm"]*scale}" fill="#c7ddd3" stroke="#52675d"/>',
                 f'<line x1="{ex}" y1="{cy-12}" x2="{ex}" y2="{top+34}" stroke="#748ca4" stroke-width="6"/>']
    for offset, color in ((-9, '#386fa4'), (0, '#424952'), (9, '#777f88')):
        rows.append(f'<path d="M{cx+offset} {cy-radius+2} C{cx+offset} 115 {cx+offset+45} 100 {cx+offset+70} 88" fill="none" stroke="{color}" stroke-width="6"/>')
    rows += ['<text x="610" y="130">Three cables exit above the cradle</text>',
             '<text x="610" y="157" class="note">Exit is on the motor side of the ring.</text>',
             '<path d="M600 137 L467 137 L420 99" fill="none" stroke="#52675d" stroke-width="1.5"/>',
             '<text x="610" y="289">Ears sit on the two shelves</text>',
             '<path d="M600 295 H540" fill="none" stroke="#52675d" stroke-width="1.5"/>',
             '<text x="610" y="437">One printed cradle</text>',
             '<text x="610" y="464" class="note">The upper half stays open.</text>',
             '<path d="M600 443 H565" fill="none" stroke="#52675d" stroke-width="1.5"/>',
             '<text x="290" y="280">Existing fan</text>',
             '<text x="280" y="307" class="note">Internals omitted</text>',
             '<text x="35" y="553">Fit screws and washers with power disconnected; check seating and cable clearance.</text>',
             '<text x="35" y="582" class="note">Cable curves are schematic. Route actual leads clear of inlet/exhaust, with a flexible loop at the moving-to-fixed transition.</text>',
             '<text x="35" y="610" class="note">Owner-reported 6 × 11 mm exit area is recorded; dimension axes, protrusion and exact axial position are unconfirmed.</text>', '</svg>']
    return '\n'.join(rows)


def main():
    config = json.loads((HERE / "config.json").read_text())
    result = calculate(config)
    OUT.mkdir(exist_ok=True)
    (OUT / "layout.svg").write_text(layout_svg(config))
    (OUT / "mount_measurement.svg").write_text(mount_measurement_svg(config))
    (OUT / "mounting_board_template.svg").write_text(mounting_board_template_svg(config))
    (OUT / "mounting_orientation.svg").write_text(mounting_orientation_svg(config))
    (OUT / "calculations.json").write_text(json.dumps(result, indent=2) + "\n")
    rows = "\n".join(f"| {key} | {value:.3f} |" for key, value in result.items() if isinstance(value, (int, float)))
    (OUT / "calculations.md").write_text(
        "# Static lever calculations\n\nLAYOUT_DRAFT_NOT_READY_FOR_POWERED_TEST\n\n"
        "Calculated values use nominal geometry and an example baseline, not measured rig performance.\n\n"
        "| Quantity (units in name) | Value |\n|---|---:|\n" + rows + "\n\n"
        "Use the actual baseline and measured lever arms. Display resolution is not measurement accuracy.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
