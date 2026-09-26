#!/usr/bin/env python3
"""Retained dual-roller study; does not model the current single-roller choice."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/ground/output'
OUT.mkdir(exist_ok=True)

study = {
    'created_date': '2026-09-13',
    'status': 'SUPERSEDED_DUAL_ROLLER_STUDY_NOT_FOR_FABRICATION',
    'superseded_by': 'docs/VACUUM_RECOMMENDATION_REVIEW.md',
    'body_limit_mm': [275, 275, 180],
    'reported_threshold_range_mm': [4, 10],
    'wheel_centers_xy_mm': [[-123.5, -5], [123.5, -5]],
    'wheel_diameter_mm': 72,
    'wheel_width_mm': 24,
    'motor_body_length_mm': 69,
    'motor_body_diameter_mm': 25,
    'motor_face_x_mm': [-111.5, 111.5],
    'roller_reference_length_mm': 184.15,
    'roller_reference_diameter_mm': 28,
    'component_selection_record': 'config/vacuum_selection.json',
    'roller_selection_note': 'Earlier iRobot pair proposal; owner reference dimensions do not specify current Roborock single roller',
    'filter_selection_note': 'Earlier s-series proposal; does not place the current washable-filter candidate',
    'blower_selection_note': 'BIQU Universal Turbo Kit 1060000677 preferred; 71x70x37.5 bare blower, separate driver/adapter, placement open',
    'roller_centers_y_mm': [69, 99],
    'head_width_mm': 184.15 + 2 * (2 + 10 + 3),
    'head_depth_mm': 72,
    'head_rear_y_mm': 48,
    'drive_bay_strategy': 'Move the former 40 mm lateral drive allowance above one roller end; unselected transmission',
    'bin_outer_reservation_mm': [192, 80, 60],
    'bin_rear_y_mm': -122,
    'bin_volume_note': 'Outer reservation only; subtract walls, caster well, ducts, seals and freeboard',
    'rear_support_zone_mm': [50, 50],
    'rear_support_center_xy_mm': [0, -106],
    'rear_support_note': 'Proposed caster and swivel space; vertical intrusion into bin must be deducted',
    'brush_axis_xy_mm': [120, 125],
    'brush_bristle_radius_mm': 45,
    'brush_note': 'Illustrative axis and bristle sweep; motor and hub not selected',
    'air_path': ['roller intake', 'central duct between motors', 'rear collection bin', 'sealed filter', 'blower above/rear of bin', 'diffused exhaust'],
}
study['head_width_saved_mm'] = 254.15 - study['head_width_mm']
study['outer_wheel_width_mm'] = 2 * (123.5 + 24 / 2)
study['wheel_to_head_plan_gap_mm'] = 48 - (-5 + 72 / 2)
study['central_motor_body_gap_mm'] = 2 * (111.5 - 69)
study['bin_outer_volume_l'] = math.prod(study['bin_outer_reservation_mm']) / 1e6

# Sensitivity calculations, not measured pickup performance or selected targets.
study['airflow_scenarios'] = []
for flow_lps in (3, 5, 8):
    q = flow_lps / 1000
    area = .18415 * .004
    study['airflow_scenarios'].append({
        'flow_lps': flow_lps,
        'illustrative_open_slot_mm': [184.15, 4],
        'mean_slot_speed_mps': round(q / area, 2),
        'assumed_system_pressure_pa': 2000,
        'air_power_w': round(q * 2000, 2),
        'assumed_combined_efficiency': .25,
        'illustrative_electrical_power_w': round(q * 2000 / .25, 2),
    })

# Static sharp-step moment about wheel/step contact; no impact assistance.
r, h, mass, drive_weight_share = .036, .010, 5.0, .8
study['threshold_scenario'] = {
    'assumed_total_mass_kg': mass,
    'assumed_total_drive_wheel_weight_fraction': drive_weight_share,
    'step_mm': h * 1000,
    'wheel_radius_mm': r * 1000,
    'static_wheel_torque_nm_each': round(mass * 9.80665 * drive_weight_share / 2 * math.sqrt(2*r*h-h*h), 3),
    'formula': 'T_each = m*g*drive_weight_share/2 * sqrt(2*r*h-h*h)',
    'limits': 'Illustration only; instantaneous load redistribution, caster climb, grip and current/thermal duty remain open',
}
assert study['outer_wheel_width_mm'] <= 275
assert study['wheel_to_head_plan_gap_mm'] > 0
assert study['central_motor_body_gap_mm'] > 0
(OUT / 'next_vacuum_study.json').write_text(json.dumps(study, indent=2) + '\n')

svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="810" viewBox="0 0 1000 810">',
       '<style>text{font-family:Arial,sans-serif;fill:#1d2939}.small{font-size:14px}.label{font-size:15px}.heading{font-size:23px;font-weight:bold}</style>',
       '<rect width="1000" height="810" fill="#f8fafc"/>',
       '<text x="28" y="35" class="heading">Everyday vacuum: superseded dual-roller study</text>',
       '<text x="28" y="60" class="small">Retained reference • does not place current single-roller/filter candidates • not printable parts</text>']
scale, cx, cy = 1.8, 300, 395
def rect(x, y, w, d, fill, stroke='#344054', dash=''):
    svg.append(f'<rect x="{cx+scale*x:.2f}" y="{cy-scale*(y+d):.2f}" width="{scale*w:.2f}" height="{scale*d:.2f}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-dasharray="{dash}"/>')
def label(x, y, text, color='#1d2939'):
    svg.append(f'<text x="{cx+scale*x:.2f}" y="{cy-scale*y:.2f}" text-anchor="middle" class="label" style="fill:{color}">{text}</text>')
rect(-137.5,-137.5,275,275,'#ffffff')
for x in (-123.5,123.5):
    rect(x-12,-41,24,72,'#667085')
for x in (-111.5,42.5):
    rect(x,-17.5,69,25,'#bed9f7')
rect(-study['head_width_mm']/2,48,study['head_width_mm'],72,'#e3f3e8')
for y in (69,99):
    rect(-92.075,y-14,184.15,28,'#94d3a7')
label(0,68,'184 mm roller reference')
label(0,101,'paired rubber rollers')
rect(70,50,40,62,'none','#915fc0','5 4')
rect(-96,-122,192,80,'#fff0c2')
label(0,-66,'Rear bin reservation')
label(0,-79,'192 × 80 × 60')
rect(-25,-131,50,50,'none','#a15c1d','6 5')
label(0,-107,'Caster well')
rect(-16,-42,32,90,'#e5edf5')
label(0,22,'Duct')
bx,by = study['brush_axis_xy_mm']
svg.append(f'<circle cx="{cx+scale*bx}" cy="{cy-scale*by}" r="{scale*45}" fill="none" stroke="#ba6b22" stroke-width="2" stroke-dasharray="5 5"/>')
svg.append(f'<circle cx="{cx+scale*bx}" cy="{cy-scale*by}" r="5" fill="#ba6b22"/>')
svg.append('<text x="55" y="685" class="label">275 mm rigid outline; wheel pair occupies 271 mm</text>')
notes = [
    ('Changed from the old layout', True),
    ('72 × 24 mm tires and ordered 25D motors.', False),
    ('Side brush feeds the main pickup path.', False),
    ('Roller drive bay moves above an end support.', False),
    ('Duct passes through the 85 mm motor gap.', False),
    ('s-series filter choice is superseded.', False),
    ('Current candidates require new 3D fitting.', False),
    ('', False),
    ('Clearances calculated in this proposal', True),
    ('17 mm between tires and head in plan.', False),
    ('40 mm narrower head reservation: 214 mm.', False),
    ('0.922 L bin outer envelope before deductions.', False),
    ('Caster intrusion reduces collection volume.', False),
    ('', False),
    ('Still to resolve', True),
    ('Motor brackets, hubs and suspension travel.', False),
    ('Roller ends, transmission and contact depth.', False),
    ('Brush hub/motor and actual bristle sweep.', False),
    ('Bin extraction and automatic emptying.', False),
    ('Full height and core/latch clearance.', False),
]
for i,(text,bold) in enumerate(notes):
    weight = 'font-weight:bold' if bold else ''
    svg.append(f'<text x="610" y="{120+i*26}" class="small" style="{weight}">{text}</text>')
svg.append('<text x="28" y="750" class="label">Threshold requirement: approximately 4–10 mm. Head compliance and caster size need to accommodate it.</text>')
svg.append('<text x="28" y="778" class="small">This drawing does not establish complete 3D fit, cleaning performance, structural strength or a finished hardware list.</text>')
svg.append('</svg>')
(OUT / 'next_vacuum_study.svg').write_text('\n'.join(svg) + '\n')
print(json.dumps({k:study[k] for k in ('outer_wheel_width_mm','head_width_mm','wheel_to_head_plan_gap_mm','central_motor_body_gap_mm','bin_outer_volume_l','threshold_scenario')}, indent=2))
