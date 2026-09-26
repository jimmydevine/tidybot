"""Validate and publish the selected-component placement. No fabrication geometry.

Uses only Python's standard library. All dimensions/provenance live in config.
The box checks deliberately do not certify structure, airflow, or mechanism fit.
"""
import html
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/ground/output'
COLORS = {'head':'#c58429', 'traction':'#287c91', 'air':'#478469',
          'bottom':'#9471b1', 'core':'#507cc0', 'interface':'#9b6379', 'cap':'#586275'}


def high(p):
    return [a+b for a,b in zip(p['min'],p['size'])]


def overlaps(a,b):
    return all(min(x,y)-max(u,v)>1e-6 for x,y,u,v in zip(high(a),high(b),a['min'],b['min']))


def contains(a,b):
    return all(u-1e-6<=v and y<=x+1e-6 for u,v,x,y in zip(a['min'],b['min'],high(a),high(b)))


def swept(p,delta):
    return {**p,'min':[a+min(0,d) for a,d in zip(p['min'],delta)],
            'size':[s+abs(d) for s,d in zip(p['size'],delta)]}


def validate(c):
    parts=c['parts']; lookup={p['id']:p for p in parts}; roots=[p for p in parts if not p.get('parent')]
    errors=[]; limits={'min':[0,0,0],'size':c['body_limit_mm']}
    if len(lookup)!=len(parts): errors.append('Duplicate component ID')
    for p in parts:
        if any(s<=0 for s in p['size']): errors.append(f"Nonpositive size: {p['id']}")
        if not contains(limits,p): errors.append(f"Outside robot envelope: {p['id']}")
        if p.get('parent') and not contains(lookup[p['parent']],p): errors.append(f"Outside parent: {p['id']}")
        if p.get('reference_motion') and not contains(lookup[p['parent']],swept(p,p['reference_motion'])):
            errors.append(f"Articulated reference outside support reservation: {p['id']}")
    for a,b in itertools.combinations(roots,2):
        if overlaps(a,b): errors.append(f"Static reservation interference: {a['id']} / {b['id']}")
    # Simultaneous independent motion: compare full occupied sweeps, not just endpoints.
    moving=[swept(p,p.get('motion',[0,0,0])) for p in roots]
    for a,b in itertools.combinations(moving,2):
        # Parts rigidly attached to the same moving cassette keep their separation.
        if a.get('motion_group') and a.get('motion_group')==b.get('motion_group'):
            if a.get('motion')!=b.get('motion'):
                errors.append(f"Inconsistent coupled travel: {a['id']} / {b['id']}")
            continue
        if overlaps(a,b) and not overlaps(lookup[a['id']],lookup[b['id']]):
            errors.append(f"Travel reservation interference: {a['id']} / {b['id']}")
    for p in moving:
        if not contains(limits,p): errors.append(f"Travel outside envelope: {p['id']}")
    services=[]
    for s in c['service_groups']:
        hits=[]
        if sum(bool(v) for v in s['delta'])!=1: errors.append(f"Service must be axis aligned: {s['id']}")
        for member in s['members']:
            path=swept(lookup[member],s['delta'])
            for other in roots:
                if other['id'] not in s['members']+s['released'] and overlaps(path,other):
                    hits.append(f"{member} / {other['id']}")
        services.append({'id':s['id'],'interferences':hits,'condition':s['condition']})
        errors.extend(f"Service {s['id']}: {h}" for h in hits)
    bottom=[p for p in roots if p['group'] in ('head','traction','air','bottom')]
    protrusion=max(0,max(high(p)[2] for p in bottom)-c['bottom_mate_z_mm'])
    core=[p for p in roots if p['group']=='core']
    core_projection=max(0,c['bottom_mate_z_mm']-min(p['min'][2] for p in core))
    # Conservative horizontal-transfer clearance: the whole bottom must pass
    # below the lowest core bay, even when their assembled x/y footprints differ.
    separation=c['station']['relative_bottom_drop_mm']-protrusion-core_projection
    if separation<c['station']['minimum_separation_mm']: errors.append('Station relative drop insufficient')
    if c['station']['tray_top_start_mm']-c['station']['tray_top_end_mm']!=c['station']['relative_bottom_drop_mm']:
        errors.append('Station platform heights inconsistent')
    w=c['wheel_stack']
    if abs(w['shaft_length_mm']-w['motor_face_to_hub_back_mm']-w['shaft_engagement_mm'])>1e-6:
        errors.append('Wheel shaft engagement arithmetic inconsistent')
    if w['shaft_engagement_mm']<w['hub_body_mm']: errors.append('Shaft does not span hub body')
    caster=c['caster_reference']; bay=lookup[caster['parent']]
    radius=caster['sweep_radius_mm']; x,y=caster['pivot_xy_mm']
    envelope={'min':[x-radius,y-radius,0],'size':[2*radius,2*radius,caster['overall_height_mm']]}
    if not contains(bay,envelope): errors.append('Caster full swivel sweep outside bay')
    if any(abs(a-b)>1e-6 for field in ('min','size') for a,b in zip(envelope[field],lookup[caster['part']][field])):
        errors.append('Caster displayed sweep disagrees with manufacturer reference')
    clearance=min(x-radius-bay['min'][0],y-radius-bay['min'][1],high(bay)[0]-x-radius,high(bay)[1]-y-radius)
    if clearance+1e-6<caster['minimum_radial_clearance_mm']: errors.append('Caster radial clearance insufficient')
    stack=c['converter_stack']
    board,case,pad,sink,fan,bay=(lookup[stack[k]] for k in ('board','case','thermal_pad','heatsink','fan','parent'))
    pin_protrusion=board['min'][2]-(case['min'][2]-stack['minimum_pin_length_mm'])
    if pin_protrusion+1e-6<stack['minimum_pin_protrusion_below_pcb_mm']:
        errors.append('Converter pins do not reach through carrier PCB')
    if case['min'][2]<high(board)[2]: errors.append('Converter case intersects carrier PCB')
    if board['min'][2]-bay['min'][2]+1e-6<stack['minimum_board_bottom_clearance_mm']:
        errors.append('Converter carrier bottom clearance insufficient')
    for a,b in ((case,pad),(pad,sink)):
        if abs(high(a)[2]-b['min'][2])>1e-6: errors.append('Converter thermal stack has gap or interference')
    if fan['min'][2]-high(sink)[2]+1e-6<stack['minimum_fan_to_heatsink_mm']:
        errors.append('Converter fan-to-heatsink clearance insufficient')
    if high(bay)[2]-high(fan)[2]+1e-6<stack['minimum_fan_inlet_clearance_mm']:
        errors.append('Converter fan inlet clearance insufficient')
    suspension=c['wheel_suspension']
    arm=suspension['arm_length_mm']; travel=suspension['upward_travel_mm']
    if not 0<=travel<arm:
        errors.append('Wheel travel must be less than the trailing arm length')
    else:
        shift=arm-math.sqrt(arm*arm-travel*travel)
        for p in parts:
            if p.get('reference_motion') and any(abs(a-b)>1e-6 for a,b in zip(p['reference_motion'],[0,shift,travel])):
                errors.append(f"Wheel arc and reference travel disagree: {p['id']}")
    return {'errors':errors,'root_reservations':len(roots),'reference_children':len(parts)-len(roots),
            'services':services,'bottom_projection_above_mate_mm':protrusion,
            'core_projection_below_mate_mm':core_projection,
            'station_vertical_separation_mm':separation,
            'caster_radial_clearance_mm':clearance,'converter_pin_protrusion_mm':round(pin_protrusion,6),
            'scope':'Axis-aligned reserved spaces only. Touching faces allowed. Structure, clearances inside bays, deformation, cables and mechanism paths need separate verification.'}


def metrics(c):
    b=next(p for p in c['parts'] if p['id']=='bin'); wall=3
    return {'height_mm':max(high(p)[2] for p in c['parts']),
            'tire_outer_width_mm':c['wheel_stack']['tire_outer_width_mm'],
            'bin_outer_l':b['size'][0]*b['size'][1]*b['size'][2]/1e6,
            'bin_simple_inner_l':(b['size'][0]-2*wall)*(b['size'][1]-2*wall)*(b['size'][2]-2*wall)/1e6,
            'bin_wall_assumption_mm':wall,'bin_usable_target_l':[0.5,0.6],
            'head_upward_allowance_mm':10,'wheel_upward_allowance_mm':10}


def svg(c,view):
    axes=(0,1) if view=='top' else (1,2)
    a,b=axes; scale=2.5; ox,oy=60,75
    height=850 if view=='top' else 600
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="850" height="{height}" viewBox="0 0 850 {height}">',
         '<rect width="100%" height="100%" fill="#f7f8fa"/>',
         '<g font-family="sans-serif" fill="#182536">',
         f'<text x="30" y="28" font-size="20">Vacuum integration · {view} projection</text>',
         '<text x="30" y="50" font-size="12">Reserved spaces, not printable parts. Dimensions in mm. See interactive view for heights.</text>']
    # Side view is rear to right, floor down; top view front at top.
    def point(v): return ox+v[a]*scale, oy+((180-v[b]) if view!='top' else v[b])*scale
    x,y=point([0,0,180] if view!='top' else [0,0,0])
    out.append(f'<rect x="{x}" y="{y}" width="{275*scale}" height="{c["body_limit_mm"][b]*scale}" fill="none" stroke="#182536" stroke-dasharray="6 5"/>')
    for p in sorted(c['parts'],key=lambda p: (bool(p.get('parent')),p['min'][2])):
        lo=p['min']; hi=high(p); v=lo.copy()
        if view!='top': v[b]=hi[b]
        x,y=point(v); w=p['size'][a]*scale; h=p['size'][b]*scale
        color=COLORS[p['group']]; ref=bool(p.get('parent'))
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{color}" fill-opacity="{0.13 if ref else 0.07}" stroke="{color}" stroke-width="{1 if ref else 1.5}" {"" if ref else "stroke-dasharray=\"5 3\""}><title>{html.escape(p["label"]+"; "+p["basis"])}</title></rect>')
        if not ref and w>65 and h>23:
            out.append(f'<text x="{x+4:.2f}" y="{y+14:.2f}" font-size="10">{html.escape(p["id"])}</text>')
    out.append(f'<text x="60" y="{height-30}" font-size="13">275 mm rigid limit · 178 mm scanner top · dashed outlines are allocations</text></g></svg>')
    return '\n'.join(out)


def report(c,result,m):
    rows=['# Selected-component integration check','',f'Date: {c["date"]}. **Placement only; not a fabrication release.**','',
          f'{result["root_reservations"]} root reservations, {result["reference_children"]} nested references. Numerical conflicts: {len(result["errors"])}.',
          '',result['scope'],'',f'- Scanner top: {m["height_mm"]} mm; rigid limit: 275 × 275 × 180 mm.',
          f'- Tire outer width: {m["tire_outer_width_mm"]} mm. Body margin: 2 mm per side.',
          f'- Bin: {m["bin_outer_l"]:.3f} L gross; {m["bin_simple_inner_l"]:.3f} L with 3 mm walls alone. Usable target 0.5–0.6 L remains unverified.',
          f'- Bottom projects {result["bottom_projection_above_mate_mm"]} mm above its {c["bottom_mate_z_mm"]} mm mating plane; core projects {result["core_projection_below_mate_mm"]} mm below it. A {c["station"]["relative_bottom_drop_mm"]} mm station drop leaves {result["station_vertical_separation_mm"]} mm conservative vertical separation.',
          f'- Caster reference has {result["caster_radial_clearance_mm"]} mm radial space inside its bay; final caster not selected.',
          f'- Converter minimum-length pins project {result["converter_pin_protrusion_mm"]} mm through the proposed PCB. Cooling and electrical layout are not qualified by this geometry check.',
          '', '## Conditional service paths','', '| Path | Conflicts | Preconditions |','|---|---:|---|']
    for s in result['services']: rows.append(f'| {s["id"]} | {len(s["interferences"])} | {s["condition"]} |')
    rows += ['', '## Coordinates and evidence','', '| ID | Min x/y/z | Size x/y/z | Dimension basis |','|---|---|---|---|']
    for p in c['parts']: rows.append(f'| {p["id"]} | {p["min"]} | {p["size"]} | {p["basis"]} |')
    rows += ['', '## Open design work','']+['- '+s for s in c['unresolved']]
    if result['errors']: rows+=['','## Errors','']+['- '+e for e in result['errors']]
    return '\n'.join(rows)+'\n'


def main():
    c=json.loads((ROOT/'config/vacuum_integration.json').read_text())
    result=validate(c); m=metrics(c); data={**c,'checks':result,'metrics':m}
    OUT.mkdir(exist_ok=True)
    (OUT/'vacuum_integration.json').write_text(json.dumps(data,indent=2)+'\n')
    for view in ('top','side'): (OUT/f'vacuum_integration_{view}.svg').write_text(svg(c,view))
    (OUT/'vacuum_integration_report.md').write_text(report(c,result,m))
    template=(ROOT/'design/ground/integration_viewer.html').read_text()
    (OUT/'vacuum_integration.html').write_text(template.replace('__DATA__',json.dumps(data).replace('</','<\\/')).replace('__COLORS__',json.dumps(COLORS)))
    print(json.dumps({'checks':result,'metrics':m},indent=2))
    if result['errors']: raise SystemExit(1)


if __name__=='__main__': main()
