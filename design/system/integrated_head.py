"""R frame accounting and air-flex motion, independent of FreeCAD.

The CAD exporter supplies material volumes; unresolved hardware stays explicit.
"""
import csv
import json
import math
from pathlib import Path
import head_coupling as P
import passive_head as Q

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'


def read():
    return json.loads((ROOT / 'config/integrated_head.json').read_text())


def flex_motion(poses):
    """Necessary straight-line reach and end angle, not a hose feasibility test."""
    rows = []
    centre = [137.5, 66, 30]
    fixed = [137.5, 91, 30]
    # The actual 32 x 22 mm bore corners expose differential wall travel.
    offsets = [(x, z) for x in (-16, 16) for z in (-11, 11)]
    for n, p in enumerate(poses):
        start = Q.move(centre, p)
        distances = []
        for x, z in offsets:
            a = Q.move([centre[0] + x, centre[1], centre[2] + z], p)
            b = [fixed[0] + x, fixed[1], fixed[2] + z]
            distances.append(math.dist(a, b))
        delta = [b-a for a,b in zip(start, fixed)]
        rows.append(dict(pose=n,centre_mm=start,delta_mm=delta,
            minimum_centreline_reach_mm=math.dist(start, fixed),
            straight_bore_edge_lengths_mm=distances,
            end_axis_angle_deg=math.degrees(math.acos(max(-1,min(1,p['R'][1][1]))))))
    return dict(rows=rows,nominal_axial_gap_mm=25,
        centreline_reach_range_mm=[min(v['minimum_centreline_reach_mm'] for v in rows),max(v['minimum_centreline_reach_mm'] for v in rows)],
        bore_edge_reach_range_mm=[min(min(v['straight_bore_edge_lengths_mm']) for v in rows),max(max(v['straight_bore_edge_lengths_mm']) for v in rows)],
        maximum_end_angle_deg=max(v['end_axis_angle_deg'] for v in rows),
        scope='Lengths are lower bounds between mating points, not bend-radius, wall-strain, restoring-force or fatigue approval. Flexible connector must retain open bore throughout motion.')


def account(d, modeled):
    rows = [dict(v,kind='CAD material') for v in modeled]
    rows += [dict(v,kind='catalog reference' if v['id'] in ('guide_rails','guide_carriages','pivot_bearings') else 'allowance') for v in d['retained_rows']]
    old = d['frame_budget_g'] + d['compliance_budget_g']
    total = sum(v['mass_g'] for v in rows)
    current = P.study()['mass']['prior_transfer_mass_g']
    return dict(rows=rows,prior_scope_g=old,candidate_scope_g=total,
        modeled_material_g=sum(v['mass_g'] for v in rows if v['kind']=='CAD material'),
        reference_g=sum(v['mass_g'] for v in rows if v['kind']=='catalog reference'),
        allowance_g=sum(v['mass_g'] for v in rows if v['kind']=='allowance'),
        conditional_reduction_g=old-total,booked_reduction_g=0,
        current_transfer_g=current,hypothetical_transfer_g=current-old+total,
        remaining_gap_if_adopted_g=current-old+total-4500,
        powered_lift_retained_g=62,carrier_retained_g=70,plumbing_retained_g=75)


def report(r):
    m=r['mass'];c=r['cad'];f=r['flex']
    lines=['# Integrated cassette ends — R candidate','',
        'The head ends combine roller-end walls, spherical-bearing seats, skid ramps and pitch-stop supports. A thin removable hood connects the ends. The existing powered lift is retained; this is not Q’s dock-only capture mechanism.','',
        '**Review geometry only.** Purchased roller ends, pivot retention, guide mounting, wear surfaces, seals and powered-lift joints are unfinished. No printing or purchase release.','',
        '## Scope and mass','',
        '| Same complete local scope | Mass |','|---|---:|',
        f"| Prior frame + remaining compliance | {m['prior_scope_g']:.1f} g |",
        f"| CAD material at solid material density | {m['modeled_material_g']:.2f} g |",
        f"| Catalog guide/bearing references | {m['reference_g']:.1f} g |",
        f"| Remaining hardware, seals and reserve | {m['allowance_g']:.1f} g |",
        f"| Candidate total | {m['candidate_scope_g']:.2f} g |",
        f"| Conditional reduction | {m['conditional_reduction_g']:.2f} g |",'',
        'P’s 70 g removable carrier, 62 g powered lift and 75 g plumbing remain. The roller, motor, transmission, driver, risers and body interface remain separate and unchanged. Do not add Q’s 72/75 g mechanism. Each item below belongs to the replacement 170 g scope once.','',
        '| Physical part or unfinished scope | Mass | Basis |','|---|---:|---|']
    lines += [f"| {v['id']} | {v['mass_g']:.2f} g | {v['kind']}: {v['basis']} |" for v in m['rows']]
    lines += ['',f"Current transfer estimate stays **{m['current_transfer_g']/1000:.3f} kg**. Substituting this candidate alone would give **{m['hypothetical_transfer_g']/1000:.3f} kg**, still **{m['remaining_gap_if_adopted_g']:.0f} g over** the 4.5 kg limit. No savings are booked.",'',
        '## Geometry checks','',
        f"{c['pose_count']} head poses and {c['withdrawal_samples']} forward-withdrawal samples checked. {len(c['intersections'])} motion intersections and {len(c['withdrawal_intersections'])} withdrawal intersections remain in the reported scope. See the CAD check JSON for exact pairs, exemptions and missing hardware.",
        f"Minimum sampled clearance to the protected roller envelope: {c['minimum_roller_clearance_mm']:.3f} mm. Minimum sampled head/guide clearance: {c['minimum_guide_clearance_mm']:.3f} mm.",
        'The roller remains a protected 200.6 × 45.1 × 45.1 mm listing envelope. No end-cap dimensions or package-to-bare-mass correction is invented. Stock and printed solids can be volume checked without claiming those purchased interfaces are resolved.',
        'The pitch-stop negative controls deliberately tilt to ±7° and find pin/slot interference on both sides; sampled working motion remains free. The nominal ±6° slot has 0.2 mm radial clearance, so it is not an exact ±6° hard limit. Pins, wear and joint capacity remain unqualified.',
        'R also corrects P’s risers and end shoes: Y79 becomes Y72.5. Risers occupy Z60–66 and shoes Z59.5–64.5, clearing the wheel and both earlier P and current Q head-motion samples. The carrier stays within its existing 70 g allocation; no separate system saving is credited.','',
        '## Air connection is a separate constraint','',
        f"The nominal 25 mm axial space requires centreline straight-line reach from **{f['centreline_reach_range_mm'][0]:.2f} to {f['centreline_reach_range_mm'][1]:.2f} mm** across the sampled motion, including the 16 mm raised state. Corresponding bore-edge distances span **{f['bore_edge_reach_range_mm'][0]:.2f}–{f['bore_edge_reach_range_mm'][1]:.2f} mm**; mating-axis angle reaches **{f['maximum_end_angle_deg']:.2f}°**.",
        'A taut 25 mm tube cannot supply this reach. A formed bellows or a longer routed flexible connector must be designed for the entire stroke, open bore and small restoring force. These distances are lower bounds, not a specification of bellows developed length. The existing 75 g plumbing allowance stays intact.','',
        '## Next decision','',
        'Close the pivot fastener stack, keyed carriage joint, rail attachment and powered-lift attachment against these actual end walls before releasing parts. Then solve the short air connection and revisit Q’s friction screen with the resulting moving mass and spring/connector forces. Thin printed walls and stop contact still need stiffness, wear and joint-load qualification. A few grams of frame saving cannot close the system’s remaining weight deficit.','']
    return '\n'.join(lines)


def main():
    d=read();cad=json.loads((OUT/'integrated_head_cad_checks.json').read_text())
    if cad['source_fingerprint']!=P.source_fingerprint():
        raise RuntimeError('Regenerate integrated-head CAD before the report')
    q=Q.study();r=dict(config=d,cad=cad,mass=account(d,cad['mass_rows']),
        flex=flex_motion([*q['poses'],q['raised']]))
    (OUT/'integrated_head.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'integrated_head.md').write_text(report(r))
    with (OUT/'integrated_head_mass.csv').open('w') as out:
        fields=['id','mass_g','moving','kind','basis'];writer=csv.DictWriter(out,fields,extrasaction='ignore');writer.writeheader();writer.writerows(r['mass']['rows'])
    print(json.dumps({k:v for k,v in r['mass'].items() if k!='rows'},indent=2))


if __name__=='__main__':main()
