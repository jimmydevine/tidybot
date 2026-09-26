#!/usr/bin/env python3
"""Generate the ground head clearance study from inventory and proposed allowances."""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent / "output"


def number(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")


def build_study():
    inventory = json.loads((ROOT / "config/owned_parts.json").read_text())
    config = json.loads((ROOT / "config/vacuum_head_layout.json").read_text())
    owned = next(p for p in inventory["owned_parts"] if p["id"] == config["inventory_id"])
    known = owned["known"]
    a = config["proposed_allowances_mm"]
    if any(not isinstance(v, (int, float)) or v < 0 for v in a.values()):
        raise ValueError("Allowances must be nonnegative numbers")
    variants = []
    for rollers in known["roller_sets"]:
        diameters = list(rollers["max_uncompressed_fin_diameter_mm_by_style"].values())
        if len(diameters) != 2 or any(d is None or d <= 0 for d in diameters):
            raise ValueError("Both roller diameters are required")
        if diameters[0] != diameters[1]:
            raise ValueError("This first study assumes equal diameters; revise placement for unequal rollers")
        diameter = diameters[0]
        spacing = a["roller_center_distance"]
        if spacing < diameter:
            raise ValueError("This clearance study excludes overlapping maximum fin envelopes")
        length = rollers["converted_length_mm"]
        wall = a["outer_wall"]
        roller_x = wall + a["end_support_bay_each_end"] + a["axial_clearance_each_end"]
        first_y = wall + a["front_rear_fin_clearance"] + diameter / 2
        width = length + 2 * roller_x + a["drive_bay_width"]
        depth = diameter + spacing + 2 * (wall + a["front_rear_fin_clearance"])
        roof_height = diameter + a["top_fin_clearance"] + a["roof_thickness"]
        if a["housing_ground_clearance"] >= diameter:
            raise ValueError("Housing ground clearance must be below roller top")
        variants.append({
            "id": rollers["id"],
            "label": f'{number(rollers["reported_length_in"])} inch pair',
            "roller_length_mm": length,
            "roller_diameter_mm": diameter,
            "roller_x_mm": roller_x,
            "roller_center_y_mm": [first_y, first_y + spacing],
            "roller_axis_height_mm": diameter / 2,
            "max_fin_envelope_gap_mm": spacing - diameter,
            "cassette_study_width_mm": width,
            "cassette_study_depth_mm": depth,
            "roof_reference_height_mm": roof_height,
            "whole_piece_possible": width <= config["whole_piece_width_limit_mm"],
            "panel_span_with_overlap_mm": width if width <= config["whole_piece_width_limit_mm"] else width / 2 + a["split_joint_overlap"],
        })
    if config["default_roller_set"] not in {v["id"] for v in variants}:
        raise ValueError("Default roller set is missing")
    return {
        "status": config["status"],
        "scope": config["scope"],
        "measurement_date": known["measurement_date"],
        "measurement_source": "config/owned_parts.json",
        "allowance_source": "config/vacuum_head_layout.json",
        "default_roller_set": config["default_roller_set"],
        "proposed_allowances_mm": a,
        "filter": known["filter"],
        "filter_approximate_local_depth_mm": known["filter"]["reported_body_envelope_mm"][2] + known["filter"]["pull_tab"]["reported_approximate_rise_mm"],
        "variants": variants,
        "notes": config["notes"],
    }


def drawing(study, v):
    a = study["proposed_allowances_mm"]
    n = number
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 780" role="img">',
        f'<title>Vacuum head clearance study: {html.escape(v["label"])}</title>',
        '<desc>Dimensioned top and side views of measured roller envelopes with proposed housing allowances. Filter shown separately. Not for fabrication.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#526079"/></marker></defs>',
        '<style>text{font-family:Arial,sans-serif;fill:#22334c} .dim{stroke:#526079;stroke-width:1;marker-start:url(#arrow);marker-end:url(#arrow)} .small{font-size:12px} .label{font-size:14px}</style>',
        '<rect width="900" height="780" fill="white"/>',
    ]

    def text(x, y, content, size=14, anchor="start", extra=""):
        elements.append(f'<text x="{x:g}" y="{y:g}" font-size="{size}" text-anchor="{anchor}" {extra}>{html.escape(content)}</text>')

    def rect(x, y, w, h, fill, stroke="#65758b", extra=""):
        elements.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{stroke}" {extra}/>')

    def line(x1, y1, x2, y2, extra='stroke="#65758b"'):
        elements.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" {extra}/>')

    def dh(x1, x2, y, label):
        line(x1, y, x2, y, 'class="dim"')
        text((x1 + x2) / 2, y - 8, label, 13, "middle")

    def dv(x, y1, y2, label):
        line(x, y1, x, y2, 'class="dim"')
        text(x + 15, (y1 + y2) / 2, label, 13, "middle", f'transform="rotate(-90 {x + 15:g} {(y1 + y2) / 2:g})"')

    text(40, 36, f'Everyday vacuum head · {v["label"]}', 24)
    text(40, 62, 'CLEARANCE STUDY · Blue/green: measured roller envelopes. Grey/amber: proposed reservations.', 13)
    text(70, 99, 'TOP VIEW · front at top', 15)
    scale, ox, oy = 2.15, 70, 155
    width = v["cassette_study_width_mm"]
    depth = v["cassette_study_depth_mm"]
    diameter = v["roller_diameter_mm"]
    length = v["roller_length_mm"]
    wall = a["outer_wall"]
    rect(ox, oy, width * scale, depth * scale, "#f1f4f8")
    drive_x = width - wall - a["drive_bay_width"]
    rect(ox + drive_x * scale, oy + wall * scale, a["drive_bay_width"] * scale,
         (depth - 2 * wall) * scale, "#fff0cb")
    for sx in [wall, v["roller_x_mm"] + length + a["axial_clearance_each_end"]]:
        rect(ox + sx * scale, oy + wall * scale, a["end_support_bay_each_end"] * scale,
             (depth - 2 * wall) * scale, "#d4dce7")
    for style, cy, color in zip(["A", "B"], v["roller_center_y_mm"], ["#acd4f4", "#a8e0d2"]):
        rx, ry = ox + v["roller_x_mm"] * scale, oy + (cy - diameter / 2) * scale
        rect(rx, ry, length * scale, diameter * scale, color)
        line(rx, oy + cy * scale, rx + length * scale, oy + cy * scale,
             'stroke="#436584" stroke-dasharray="5 4"')
        text(rx + length * scale / 2, ry + diameter * scale / 2 - 8,
             f'Style {style} · {n(length)} × Ø{n(diameter)} mm', 13, "middle")
    text(ox + (drive_x + a["drive_bay_width"] / 2) * scale, oy + depth * scale / 2 - 10, "Drive", 13, "middle")
    text(ox + (drive_x + a["drive_bay_width"] / 2) * scale, oy + depth * scale / 2 + 10, "reserved", 11, "middle")
    if not v["whole_piece_possible"]:
        split_x = ox + width * scale / 2
        strip = (wall + a["front_rear_fin_clearance"]) * scale
        line(split_x, oy, split_x, oy + strip, 'stroke="#c66a17" stroke-width="2" stroke-dasharray="4 3"')
        line(split_x, oy + depth * scale - strip, split_x, oy + depth * scale,
             'stroke="#c66a17" stroke-width="2" stroke-dasharray="4 3"')
    dh(ox, ox + width * scale, 125, f'{n(width)} mm proposed width')
    dv(ox + width * scale + 25, oy, oy + depth * scale, f'{n(depth)} mm proposed depth')
    dh(ox + v["roller_x_mm"] * scale, ox + (v["roller_x_mm"] + length) * scale,
       oy + depth * scale + 34, f'{n(length)} mm reported overall roller length')
    text(70, 380, f'End bays: {n(a["end_support_bay_each_end"])} mm each; axial clearance: {n(a["axial_clearance_each_end"])} mm each; drive reservation: {n(a["drive_bay_width"])} mm.', 13)
    text(70, 402, 'Whole cassette print proposed. Working lengths and end fittings are not modeled.' if v['whole_piece_possible'] else 'Orange marks suggest a panel join. Assembled width exceeds the 275 mm robot limit.', 13)

    text(78, 440, 'SIDE VIEW · looking along the roller axes', 14)
    ss, sx, floor = 3, 78, 570
    roof_y = floor - v["roof_reference_height_mm"] * ss
    rect(sx, roof_y, depth * ss, a["roof_thickness"] * ss, "#d4dce7")
    side_h = (v["roof_reference_height_mm"] - a["housing_ground_clearance"]) * ss
    for x in [sx, sx + (depth - wall) * ss]:
        rect(x, roof_y, wall * ss, side_h, "#d4dce7")
    for cy, color in zip(v["roller_center_y_mm"], ["#acd4f4", "#a8e0d2"]):
        cx, cz, radius = sx + cy * ss, floor - diameter / 2 * ss, diameter / 2 * ss
        elements.append(f'<circle cx="{cx:g}" cy="{cz:g}" r="{radius:g}" fill="{color}" stroke="#65758b"/>')
        line(cx - 5, cz, cx + 5, cz)
        line(cx, cz - 5, cx, cz + 5)
    line(sx - 18, floor, sx + depth * ss + 18, floor, 'stroke="#22334c" stroke-width="2"')
    text(sx + depth * ss + 23, floor + 4, 'Floor', 12)
    dv(43, roof_y, floor, f'{n(v["roof_reference_height_mm"])} mm roof reference')
    dh(sx + v["roller_center_y_mm"][0] * ss, sx + v["roller_center_y_mm"][1] * ss,
       608, f'{n(a["roller_center_distance"])} mm centers')
    text(78, 639, f'Outer-envelope gap: {n(v["max_fin_envelope_gap_mm"])} mm. Contact setting unverified.', 12)
    text(78, 659, 'Roof height excludes duct, plenum and drive protrusions.', 12)

    fx, fy, fs = 500, 478, 1.8
    fl, fw, ft = study["filter"]["reported_body_envelope_mm"]
    text(fx, 429, 'FILTER · see full robot for placement', 14)
    rect(fx, fy, fl * fs, fw * fs, "#e4f0fb")
    text(fx + fl * fs / 2, fy + fw * fs / 2 - 5, 'Outside frame envelope', 13, "middle")
    text(fx + fl * fs / 2, fy + fw * fs / 2 + 17, 'Pull-tab position not drawn', 12, "middle")
    dh(fx, fx + fl * fs, 463, f'{n(fl)} mm')
    dv(fx + fl * fs + 22, fy, fy + fw * fs, f'{n(fw)} mm')
    text(fx, 639, f'Body thickness: {n(ft)} mm; local tab depth ≈{n(study["filter_approximate_local_depth_mm"])} mm.', 12)
    tab = study["filter"]["pull_tab"]
    tab_l, tab_w = tab["reported_footprint_mm"]
    text(fx, 659, f'Tab: {n(tab_l)} × {n(tab_w)} mm, raised ≈{n(tab["reported_approximate_rise_mm"])} mm; grip access additional.', 12)
    text(40, 710, 'Measured dimensions set the part envelopes. Center spacing, walls and support/drive bays are design proposals.', 13)
    text(40, 733, 'The completed powered head may be larger. No bearing seats, couplers, gears, latches or fastener holes are released.', 13)
    text(40, 756, 'For layout review only · dimensions in millimeters · not a printable part or a low-clearance-head design.', 13)
    elements.append('</svg>')
    return "\n".join(elements)


def main():
    study = build_study()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "vacuum_head_layout.json").write_text(json.dumps(study, indent=2) + "\n")
    figures, options = [], []
    report = ["# Vacuum-head clearance study", "", "**Layout only; not for fabrication.**", "",
              "Source measurements: `config/owned_parts.json`. Proposed allowances: `config/vacuum_head_layout.json`.", "",
              "| Roller pair | Study width | Study depth | Roof reference | Fin-envelope gap | Panel span (whole short / split long) |",
              "|---|---:|---:|---:|---:|---:|"]
    for v in study["variants"]:
        svg = drawing(study, v)
        filename = f'vacuum_head_{v["id"]}.svg'
        (OUTPUT / filename).write_text(svg + "\n")
        selected = v["id"] == study["default_roller_set"]
        options.append(f'<option value="{v["id"]}" {"selected" if selected else ""}>{html.escape(v["label"])}</option>')
        metrics = f'{number(v["cassette_study_width_mm"])} × {number(v["cassette_study_depth_mm"])} mm proposed footprint; {number(v["roof_reference_height_mm"])} mm roof reference'
        figures.append(f'<section class="variant" id="{v["id"]}" {"" if selected else "hidden"}><p class="metrics">{metrics}</p><img src="{filename}" alt="Dimensioned top and side clearance views for {html.escape(v["label"])}"><p><a href="{filename}">Open standalone SVG drawing</a></p></section>')
        keys = ["cassette_study_width_mm", "cassette_study_depth_mm", "roof_reference_height_mm", "max_fin_envelope_gap_mm", "panel_span_with_overlap_mm"]
        report.append("| " + " | ".join([v["label"]] + [number(v[k]) + " mm" for k in keys]) + " |")
    allowances = study["proposed_allowances_mm"]
    report.extend(["", f'All footprint dimensions include a provisional {number(allowances["drive_bay_width"])} mm drive bay. Motor/transmission selection may change its dimensions.', "",
                   "Width = roller length + 2 × (wall + end-support bay + axial clearance) + drive bay.",
                   "Depth = roller diameter + center distance + 2 × (wall + front/rear clearance).",
                   "Roof reference = roller diameter + top clearance + roof thickness, with fin envelopes tangent to the floor.", ""])
    report.extend("- " + note for note in study["notes"])
    body_text = " × ".join(number(v) for v in study["filter"]["reported_body_envelope_mm"])
    report.extend(["", f'The short cassette targets a whole print. The long comparison uses a midpoint split with {number(allowances["split_joint_overlap"])} mm overlap; that does not reduce its assembled width or establish joint strength.', "",
                   f'The separate filter body is {body_text} mm. Its approximate {number(study["filter_approximate_local_depth_mm"])} mm local depth assumes the tab rise is additional to the body; exact placement and grip/extraction clearance remain open.', "",
                   "No new owner question is needed for this envelope study. Detailed end fittings, drive selection and airflow remain work to do. The full placement and service paths are in [the ground viewer](ground_layout.html)."])
    (OUTPUT / "report.md").write_text("\n".join(report) + "\n")
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TidyBot vacuum-head layout</title><style>
body{margin:0;background:#eef2f7;color:#22334c;font:16px/1.5 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:24px}
h1{font-size:28px;margin-bottom:8px}p{max-width:900px}.tag{font-weight:700;color:#815008}label{font-weight:600}
select{font:inherit;padding:8px;margin:8px;background:white;border:1px solid #8695a9;border-radius:6px}
.variant{background:white;padding:16px;border-radius:10px;margin-top:16px}.variant[hidden]{display:none}img{width:100%;height:auto}
.metrics{font-weight:600;margin:0 0 8px}a{color:#195ca5}:focus-visible{outline:3px solid #236fb3}details{margin-top:20px}
@media print{body{background:white}main{padding:0}select,details{display:none}img{max-height:75vh;object-fit:contain}}
</style><main><h1>First vacuum-head layout</h1><p class="tag">Clearance study · not for fabrication</p>
<p>Compare the two owned roller lengths using the dimensions recorded in the inventory. The short pair is the current reference for the 275 mm body. Its cassette targets a whole print; the long comparison exceeds the body limit. The filter is shown separately here and placed in the <a href="ground_layout.html">full robot layout</a>.</p>
<label for="variant">Roller pair</label><select id="variant">OPTIONS</select>
FIGURES
<p>The center spacing and resulting gap shown in the drawing describe a proposed clearance setting. Pickup, roller contact and the actual end supports still need development. The reserved drive bay has no selected motor or transmission.</p>
<details><summary>Inputs, calculation and design notes</summary><p><a href="../../../config/vacuum_head_layout.json">Proposed allowances</a> · <a href="../../../config/owned_parts.json">Owner measurements</a> · <a href="report.md">Calculation report</a> · <a href="../../../docs/VACUUM_HEAD.md">Vacuum-head design notes</a></p><p>Edit the allowance file and run <code>python3 design/ground/generate.py</code> to regenerate. These files use no external scripts or network services.</p></details>
</main><script>const picker=document.getElementById('variant');function showVariant(){for(const section of document.querySelectorAll('.variant'))section.hidden=section.id!==picker.value;}picker.addEventListener('change',showVariant);showVariant();</script></html>
'''.replace("OPTIONS", "".join(options)).replace("FIGURES", "\n".join(figures))
    (OUTPUT / "vacuum_head_layout.html").write_text(page)
    print(f"Generated {len(study['variants'])} dimensioned variants in {OUTPUT}")


if __name__ == "__main__":
    main()
