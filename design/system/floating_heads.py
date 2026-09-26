"""M motion envelopes and coupled ideal head/chassis equilibrium.

Does not prescribe a realizable guide mechanism. It calculates the space, mass,
force and travel that a detailed compliant mount must supply.
"""
from copy import deepcopy
import hashlib
import itertools
import json
import math
from pathlib import Path
import build as B
import suspension_springs as L
import height_mounting as I

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read(): return json.loads((ROOT/'config/floating_heads.json').read_text())


def corners(p):
    return list(itertools.product(*[(v,v+s) for v,s in zip(p['min'],p['size'])]))


def rotation(normal):
    """Minimal rotation carrying local Z into the floor normal in body axes."""
    x,y,z=normal
    return [[1-x*x/(1+z),-x*y/(1+z),x],[-x*y/(1+z),1-y*y/(1+z),y],[-x,-y,z]]


def transform(point,reference,q,normal=(0,0,1),oscillation=0):
    r=rotation(normal);v=[point[i]-reference[i] for i in range(3)];v[0]+=oscillation
    return [reference[i]+sum(r[i][j]*v[j] for j in range(3))+(q if i==2 else 0) for i in range(3)]


def envelope(p,reference,q,normal=(0,0,1),oscillation=0):
    pts=[transform(v,reference,q,normal,oscillation) for v in corners(p)]
    lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
    return dict(id=p['id'],min=lo,size=[hi[i]-lo[i] for i in range(3)])


def geometry(p,d,revised=True):
    c,h=I.configured(p['layout'],p['h'],I.read())
    parts=I.body_parts(c,h,I.read(),p['bottom'])
    for v in parts:
        if v['id'].startswith('anti_tip'):v['min'][2]+=p['config']['anti_tip_raise_mm']
        if not revised:continue
        v['min'][2]+=d['shared_shifts_z_mm'].get(v['id'],0)
        if p['bottom']=='vacuum':v['min'][2]+=d['vacuum_shifts_z_mm'].get(v['id'],0)
        if v['id']=='I_cap_height_bound':v['min'][2]+=d['cap_roof_raise_mm']
        if v['id']=='mop_tank':v['min'][2]+=d['mop_tank_raise_mm']
        if v['id']=='mop_lift':v['min'][2]+=d['mop_lift_raise_mm']
        if v['id']=='mop_drive':v.update(min=d['mop_drive_min_mm'][:],size=d['mop_drive_size_mm'][:])
        if v['id']=='vac_head_drive':
            v['size'][2]=d['vacuum_drive_height_mm'];v['min'][0]=d['vacuum_drive_x_mm'];v['size'][0]=d['vacuum_drive_width_mm']
        if v['id']=='vac_head':v['size'][2]=d['vacuum_head_height_mm']
        if v['id']=='near_1':v['min'][0]=250
    return parts


def prepare(bottom,d=None,index=1):
    d=d or read();p=L.prepare(bottom,mass_index=index);md=d['modules'][bottom]
    before={v['id']:v for v in geometry(p,d,False)}
    after={v['id']:v for v in geometry(p,d)}
    fixed=[p['fixed']];head=[]
    for row in B.assembly(p['layout'],bottom,payload=False)['rows']:
        mass=row['mass_g'][index];xyz=row['cg_mm'];id=row['part']
        # L already raises anti-tip hardware; no second move here.
        if id.startswith('anti_tip'):continue
        if id in md['moving_parts']:
            fixed.append((-mass,xyz))
            v=after[id];head.append((mass,[v['min'][i]+v['size'][i]/2 for i in range(3)]))
        elif id in after:
            # Some source rows aggregate smaller functional reservations, so
            # their exact CG remains an allowance when no matching ID exists.
            delta=[after[id]['min'][i]-before[id]['min'][i] for i in range(3)]
            fixed.extend([(-mass,xyz),(mass,[xyz[i]+delta[i] for i in range(3)])])
    moving=md['mount_moving_g'][index];mount=md['mount_allowance_g'][index]
    head.append((moving,md['mount_cg_mm']))
    fixed.append((mount-moving,md['mount_cg_mm']))
    for key,pos in [('lift_addition_g','lift_cg_mm'),('riser_addition_g','riser_cg_mm')]:
        fixed.append((md[key][index],md[pos]))
    p['fixed']=L.weighted(fixed);p['head_items']=head;p['head_mass_g']=sum(m for m,xyz in head)
    p['dry_mass_g']+=mount+md['lift_addition_g'][index]+md['riser_addition_g'][index]
    p['M']=d;p['parts']=list(after.values())
    # Calibrate once per physical cassette at its reference head mass. Added
    # pad water is deliberately NOT recalibrated as it changes during use.
    p['downward_preload_n']=md['target_contact_n']-(p['head_mass_g']+md.get('calibration_pad_water_g',0))/1000*B.G
    return p


def split_contents(p,loads):
    fixed=[];head=[]
    for row in loads:
        q=list(row)
        if p['bottom']=='mop':
            if abs(q[1]-137.5)<1e-6 and abs(q[2]-171)<1e-6:head.append(q);continue
            q[1]=60.5;q[3]+=p['M']['mop_tank_raise_mm']
        fixed.append(q)
    return fixed,head


def place_head(p,q,normal,head_loads=()):
    ref=p['M']['modules'][p['bottom']]['reference_mm']
    return [(m,transform(xyz,ref,q,normal)) for m,xyz in p['head_items']]+[
        (v[0],transform(v[1:],ref,q,normal)) for v in head_loads]


def contact_force(p,q,n,water_g=0,rate_factor=1,parasitic=0,suction=0):
    md=p['M']['modules'][p['bottom']]
    down=p['downward_preload_n']+md['total_spring_rate_n_mm']*rate_factor*(q-md['spring_reference_q_mm'])
    # Virtual work in the body-Z slide: N*nz = W*nz + downward spring force.
    net=(p['head_mass_g']+water_g)/1000*B.G+down/n[2]+parasitic
    # Pressure suction adds downward aerodynamic load AND upward floor contact.
    # At coincident resultants it increases scrub load, not chassis unloading.
    return dict(net_n=net,gross_contact_n=net+suction,downward_spring_n=down)


def solve(p,candidate,shims,loads=(),heading=0,raised=False,rate_factor=1,parasitic=0,suction=0):
    md=p['M']['modules'][p['bottom']];fixed,water=split_contents(p,loads)
    q=p['M']['raised_travel_mm'] if raised else md['spring_reference_q_mm'];normal=[0,0,1];pp=deepcopy(p)
    ref=md['reference_mm'];head_force=0
    for iteration in range(60):
        moved=place_head(p,q,normal,water)
        pp['fixed']=L.weighted([p['fixed'],*moved])
        force=contact_force(p,q,normal,sum(v[0] for v in water),rate_factor,parasitic,suction)
        head_force=0 if raised else force['net_n']
        if head_force<0:raise ValueError('Head loses contact; this ideal floor-following solution is invalid')
        pp['config']['tool_contact'][p['bottom']]['at_mm']=[ref[0],ref[1],q]
        r=L.solve(pp,candidate,shims,loads=fixed,heading=heading,contact_n=head_force)
        if raised:break
        n=r['normal'];caster=r['caster_mm']
        nq=-(n[0]*(ref[0]-caster[0])+n[1]*(ref[1]-caster[1]))/n[2]
        err=max(abs(nq-q),*(abs(n[i]-normal[i]) for i in range(3)))
        if err<1e-8:break
        q=(q+nq)/2;normal=[(normal[i]+n[i])/2 for i in range(3)]
        mag=math.sqrt(sum(v*v for v in normal));normal=[v/mag for v in normal]
    else:raise RuntimeError('Head/chassis iteration failed')
    r.update(q_mm=q,head_normal=normal,head_net_n=head_force,
        head_gross_n=0 if raised else force['gross_contact_n'],spring_down_n=force['downward_spring_n'],
        raised=raised,head_iterations=iteration+1,heading_deg=heading,parasitic_n=parasitic,
        rate_factor=rate_factor,suction_n=suction,head_mass_g=p['head_mass_g']+sum(v[0] for v in water))
    parts=[envelope(v,ref,q,normal,0) if v['id'] in md['moving_parts'] else v for v in p['parts']]
    n=r['normal'];cx,cy,_=r['caster_mm']
    r['height_with_reserve_mm']=max(n[0]*(pt[0]-cx)+n[1]*(pt[1]-cy)+n[2]*pt[2] for v in parts for pt in corners(v))+2
    pad=next(v for v in parts if v['id']==md['moving_parts'][0])
    # Exact transformed floor corners rather than AABB corners for this check.
    raw=next(v for v in p['parts'] if v['id']==md['moving_parts'][0])
    pts=[transform(pt,ref,q,normal) for pt in corners(raw) if pt[2]==raw['min'][2]]
    r['head_floor_clearance_mm']=min(n[0]*(pt[0]-cx)+n[1]*(pt[1]-cy)+n[2]*pt[2] for pt in pts)
    r['anti_tip_clearance_mm']=min(n[0]*(pt[0]-cx)+n[1]*(pt[1]-cy)+n[2]*pt[2] for v in parts if v['id'].startswith('anti_tip') for pt in corners(v))
    r['tilt_deg']=math.degrees(math.acos(max(-1,min(1,normal[2]))))
    r['motion_pass']=raised or (p['M']['working_travel_mm'][0]<=q<=p['M']['working_travel_mm'][1] and
        abs(math.degrees(math.atan2(normal[0],normal[2])))<=p['M']['tilt_limit_deg'] and
        abs(math.degrees(math.atan2(normal[1],normal[2])))<=p['M']['tilt_limit_deg'])
    return r


def calibrate(p,candidate):
    md=p['M']['modules'][p['bottom']];pp=deepcopy(p)
    pp['fixed']=L.weighted([p['fixed'],*place_head(p,p['M']['raised_travel_mm'],[0,0,1])])
    # Lifted tool calibration also raises pad water and relocates tank water.
    for case in pp['config']['contents'][p['bottom']]:
        fixed,water=split_contents(p,case['loads'])
        case['loads']=fixed+[[v[0],*transform(v[1:],md['reference_mm'],p['M']['raised_travel_mm'])] for v in water]
    return L.calibrate(pp,candidate)


def clearance_audit(p,revised=True):
    d=p['M'];md=d['modules'][p['bottom']];parts=geometry(p,d,revised)
    moving=[v for v in parts if v['id'] in md['moving_parts']]
    # Duct flex is intentionally compliant; empty cap bound is height-only.
    fixed=[v for v in parts if v['id'] not in md['moving_parts'] and v['id'] not in ('vac_flex','I_cap_height_bound')]
    issues=[];poses=[];bounds=[]
    tilt=d['tilt_limit_deg']
    for q,ax,ay in itertools.product([d['working_travel_mm'][0],4,d['working_travel_mm'][1]],[-tilt,0,tilt],[-tilt,0,tilt]):
        n=[math.tan(math.radians(ax)),math.tan(math.radians(ay)),1];mag=math.sqrt(sum(x*x for x in n));n=[x/mag for x in n]
        poses.append((q,n))
    poses.append((d['raised_travel_mm'],[0,0,1]))
    for q,n in poses:
        for v in moving:
            # Oscillation belongs to the pad, not the complete mop drive.
            oscillations=[-1.5,1.5] if v['id']=='mop_pad' else [0]
            for osc in oscillations:
                a=envelope(v,md['reference_mm'],q,n,osc);bounds.append(a)
                for b in fixed:
                    if B.overlap(a,b):issues.append(dict(moving=a['id'],fixed=b['id'],q_mm=q,normal=n,oscillation_mm=osc))
    # Check changed static allocations against all other static allocations.
    changed=set(d['shared_shifts_z_mm'])|{'near_1'}|set(d['vacuum_shifts_z_mm'] if p['bottom']=='vacuum' else ['mop_tank','mop_lift'])
    static=[]
    for a,b in itertools.combinations(fixed,2):
        if (a['id'] in changed or b['id'] in changed) and B.overlap(a,b):static.append([a['id'],b['id']])
    return dict(poses=len(poses),interferences=issues,pairs=sorted({(v['moving'],v['fixed']) for v in issues}),
        changed_static_interferences=static,
        xy_within_limit=all(v['min'][i]>=0 and B.hi(v)[i]<=275 for v in bounds for i in (0,1)),
        scope='Conservative transformed AABBs of functional allocations, including H stock. K exact moving pod solids, fasteners, new guides/lift/risers, service paths and the deforming air joint are absent. An overlap is a packaging conflict, not proof actual solids collide.')


def summarize(rows):
    span=lambda key:[min(r[key] for r in rows),max(r[key] for r in rows)]
    return dict(cases=len(rows),q_mm=span('q_mm'),head_net_n=span('head_net_n'),head_gross_n=span('head_gross_n'),
        total_drive_n=[min(sum(r['support_n'][:2]) for r in rows),max(sum(r['support_n'][:2]) for r in rows)],
        max_height_with_reserve_mm=max(r['height_with_reserve_mm'] for r in rows),
        min_head_clearance_mm=min(r['head_floor_clearance_mm'] for r in rows),
        max_head_clearance_mm=max(r['head_floor_clearance_mm'] for r in rows),
        min_anti_tip_clearance_mm=min(r['anti_tip_clearance_mm'] for r in rows),
        motion_failures=sum(not r['motion_pass'] for r in rows),stop_cases=sum(any(r['stops']) for r in rows),
        negative_support_cases=sum(not r['supports_positive'] for r in rows),
        max_residual_nmm=max(abs(v) for r in rows for v in r['residual_nmm']))


def report(r):
    lines=['# M — floating-head integration','',r['config']['status'],'',
        'The previous static layout does not reserve working head movement. M adds an ideal floor-following model, separate moving-head mass and a revised clearance proposal. This is the space/load contract for the next detailed mount, not a finished suspension.','',
        '| Module | Nominal loaded planning mass | Wheel shims L / R | Working retraction | Net head force | Drive-wheel normal load |','|---|---:|---:|---:|---:|---:|']
    fmt=lambda v:'–'.join(f'{x:.2f}' for x in v)
    for b,v in r['modules'].items():
        s=v['operation'];lines.append(f"| {b} | {v['nominal_loaded_mass_g']/1000:.3f} kg | {fmt(v['calibration']['shims_mm'])} mm | {fmt(s['q_mm'])} mm | {fmt(s['head_net_n'])} N | {fmt(s['total_drive_n'])} N |")
    lines+=['','Each module is calibrated once with its head raised and reference contents. Work sweeps use all L contents, 24 caster headings, three head-spring rate cases and ±1 N parasitic-load cases. Nominal K hardware and nominal wheel springs are used; this does not resolve L spring manufacturing sensitivity.','',
        '| Module | Old moving/fixed conflict pairs | Proposed conflict pairs | Static conflicts | Raised minimum clearance | Max height + 2 mm |','|---|---:|---:|---:|---:|---:|']
    for b,v in r['modules'].items():
        a=v['proposed_clearance'];lines.append(f"| {b} | {len(v['previous_clearance']['pairs'])} | {len(a['pairs'])} | {len(a['changed_static_interferences'])} | {v['raised']['min_head_clearance_mm']:.2f} mm | {max(v['operation']['max_height_with_reserve_mm'],v['raised']['max_height_with_reserve_mm']):.2f} mm |")
    for b,v in r['modules'].items():
        lines+=['',f'## {b} conflicts and mass','',f"Earlier pairs: {v['previous_clearance']['pairs']}",f"Proposed pairs: {v['proposed_clearance']['pairs']}",f"Changed static pairs: {v['proposed_clearance']['changed_static_interferences']}",
                f"Moving dry head: {v['moving_head_g']:.1f} g. Added mount/lift/riser allowance: {v['added_mass_g']:.1f} g; original allowances retained, no speculative saving. Signed preload at reference height: {v['preload_n']:.2f} N (negative means counterbalance upward)."]
    lines+=['','## Interpretation','',
        'The whole vacuum cassette and its motor move together. Its dead weight already exceeds the 3 N trial contact target, so use adjustable upward counterbalance, not extra downward preload. The complete mop pad/drive float together while only the pad oscillates. Its 8 N trial target needs downward preload. Neither target establishes hair pickup, wet cleaning or traction performance.',
        '', 'A separately listed 0–5 N suction-force sensitivity increases gross brush/skid contact and possible drag. It does not automatically remove that same force from the wheels: with coincident pressure/contact resultants those external forces cancel in whole-robot vertical balance. The parasitic hose/guide load is modeled separately. Actual pressure footprint, moments, friction, head support reactions and brush deformation remain unknown.',
        '', 'M reserves −2…+10 mm working translation with ±1.5° pitch/roll, then a level 16 mm raised stop. The raised-clearance calculation is flat-floor only; it does not prove traversal of a 10 mm step. The working sweep is not every combination of wheel spring tolerances or obstacle contacts.',
        '', 'The layout requires elevated vacuum electronics and power shelf, a higher shared Pi/camera mounting position, an 18 mm higher mop tank and a 15 mm higher mop lift. The vacuum head is reduced to a 48 mm height reservation and its drive to 71 × 60 × 29 mm. The mop drive becomes 32 × 27 × 83 mm, farther rearward. These tightened allocations still require actual roller/motor/mount/belt/connector CAD; trimming an envelope does not prove the hardware fits it. The cap roof reservation rises 6 mm; the lidar remains the tallest part.',
        '', 'Guide, gimbal, equalizer, lift latch and riser geometry are not included in the clearance pass. Their mass allowances are included. The ideal floor-following model does not demonstrate that a particular guide supplies its motion without binding. Retain the L 10 mm raised anti-tip requirement. No STL is released.',
        '', '[Design and mechanism requirements](../../../docs/FLOATING_HEAD_DESIGN.md) · [Interactive review](floating_heads.html) · [Input data](../../../config/floating_heads.json)']
    return '\n'.join(lines)+'\n'


def write_viewer(result):
    template=ROOT/'design/system/floating_heads_viewer.html'
    compact=deepcopy(result)
    for v in compact['modules'].values():
        v.pop('samples',None);v['raised_samples']=v['raised_samples'][:1]
        v.pop('previous_clearance',None);v.pop('proposed_clearance',None)
    (OUT/'floating_heads.html').write_text(template.read_text().replace('__MODEL__',json.dumps(compact)))


def main():
    d=read();ld=L.read();candidate=next(v for v in ld['candidates'] if v['id']==ld['preferred_candidate'])
    result=dict(config=d,modules={},fabrication_release=False,
        input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config/floating_heads.json',ROOT/'config/suspension_springs.json',ROOT/'config/height_mounting.json',OUT/'pod_joints_cad_checks.json']})
    for b in d['modules']:
        p=prepare(b,d);cal=calibrate(p,candidate);rows=[];raised=[]
        for contents,heading in itertools.product(p['config']['contents'][b],range(0,360,15)):
            raised.append(solve(p,candidate,cal['shims_mm'],loads=contents['loads'],heading=heading,raised=True))
            for rate,force in itertools.product(d['head_spring_rate_factor_cases'],d['parasitic_normal_force_n']):
                row=solve(p,candidate,cal['shims_mm'],loads=contents['loads'],heading=heading,rate_factor=rate,parasitic=force)
                row['contents']=contents['label'];rows.append(row)
        mass=p['dry_mass_g']+sum(v[0] for v in p['config']['contents'][b][p['config']['calibration_contents_index'][b]]['loads'])
        nominal=next(v for v in rows if v['heading_deg']==0 and v['rate_factor']==1 and v['parasitic_n']==0 and v['contents']==p['config']['contents'][b][p['config']['calibration_contents_index'][b]]['label'])
        result['modules'][b]=dict(nominal_loaded_mass_g=mass,added_mass_g=p['dry_mass_g']-L.prepare(b)['dry_mass_g'],
            moving_head_g=p['head_mass_g'],preload_n=p['downward_preload_n'],calibration=cal,
            operation=summarize(rows),raised=summarize(raised),samples=rows,raised_samples=raised,
            nominal=nominal,parts=p['parts'],previous_clearance=clearance_audit(p,False),proposed_clearance=clearance_audit(p),
            wheel_spring_installed=L.installed_screen(p,candidate,cal['shims_mm'],ld['seat_error_mm']))
        print(b,'mass',round(mass,1),'working',result['modules'][b]['operation'],'conflicts',result['modules'][b]['proposed_clearance']['pairs'],result['modules'][b]['proposed_clearance']['changed_static_interferences'])
    result['modules']['vacuum']['gross_contact_suction_sensitivity_n']=[result['modules']['vacuum']['operation']['head_net_n'][0],result['modules']['vacuum']['operation']['head_net_n'][1]+max(d['vacuum_suction_force_n'])]
    (OUT/'floating_heads.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'floating_heads.md').write_text(report(result))
    template=ROOT/'design/system/floating_heads_viewer.html'
    if template.exists():write_viewer(result)


if __name__=='__main__':main()
