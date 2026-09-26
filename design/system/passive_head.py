"""Q: realizable-DOF kinematics and force sensitivity for two independent slides.

No mechanism mass saving is booked. Catalog envelopes, not manufacturer solids.
Side guide/drop-link details require a redesigned cassette end frame.
"""
import csv
import itertools
import json
import math
from pathlib import Path
import fixed_drive as N
import head_coupling as P

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/passive_head.json').read_text())


def dot(a,b):return sum(x*y for x,y in zip(a,b))


def pose(d,normal,c,ground):
    """Head floor follows a horizontal plane; pivots share body Y.

    R = Ry(roll) Rx(pitch), not M's minimal rotation. R_yx=0 makes
    the two spherical-joint centers compatible with parallel vertical rails.
    The right pivot floats axially as the projected head width contracts.
    """
    nx,ny,nz=normal;roll=math.atan2(nx,nz);pitch=-math.asin(ny)
    cr,sr,cp,sp=math.cos(roll),math.sin(roll),math.cos(pitch),math.sin(pitch)
    R=[[cr,sr*sp,sr*cp],[0,cp,-sp],[-sr,cr*sp,cr*cp]]
    left,y,h=d['pivot_left_mm'];span=d['pivot_right_x_mm']-left
    x=left+span/2*cr;z=(c+ground+h-nx*x-ny*y)/nz
    centre=[x,y,z];ref=[(left+d['pivot_right_x_mm'])/2,y,h]
    T=[centre[i]-dot(R[i],ref) for i in range(3)]
    joint_z=[z+span/2*sr,z-span/2*sr]
    return dict(R=R,T=T,pitch_deg=math.degrees(pitch),roll_deg=math.degrees(roll),
        pivot_z_mm=joint_z,carriage_z_mm=[v+d['carriage_above_pivot_mm'] for v in joint_z],
        right_float_used_mm=span*(1-cr),normal=normal,plane_constant=c,ground_height_mm=ground)


def move(v,p):return [dot(row,v)+t for row,t in zip(p['R'],p['T'])]


def moved_box(v,p):
    pts=[move(pt,p) for pt in N.M.corners(v)]
    lo=[min(pt[i] for pt in pts) for i in range(3)]
    return dict(id=v['id'],min=lo,size=[max(pt[i] for pt in pts)-lo[i] for i in range(3)])


def rail_limits(d):
    lo=d['rail_left_min_mm'][2];hi=lo+d['rail_envelope_mm'][2]
    inset=d['carriage_length_mm']/2+d['end_stop_reserve_mm']
    tol=d['rail_end_tolerance_mm']+d['placement_tolerance_mm']
    return [lo+inset+tol,hi-inset-tol]


def head_items(p,d):
    # Remove the old generic moving mount (30 g), then include the new moving
    # rows once. All five actual cleaning-head rows remain unchanged.
    items=p['head_items'][:-1]
    ref=d['pivot_left_mm'];mid=(ref[0]+d['pivot_right_x_mm'])/2
    for row in d['parts']:
        if row['moving']:items.append((row['qty']*row['each_g'],[mid,ref[1],ref[2]+10]))
    return items


def calibrate(items,d):
    mass,cg=N.L.weighted(items);w=mass/1000*N.B.G;contact=d['target_contact_n']
    left=d['pivot_left_mm'][0];right=d['pivot_right_x_mm'];cx=(left+right)/2
    up=w-contact
    ur=(w*cg[0]-contact*cx-up*left)/(right-left)
    return dict(mass_g=mass,cg_mm=cg,weight_n=w,upward_preload_n=[up-ur,ur],
        reference_carriage_z_mm=d['pivot_left_mm'][2]+d['carriage_above_pivot_mm'])


def force_case(d,cal,p,rate_factor=1,preload_factor=1,parasitic=0,suction=0,drag=0):
    # Springs pull up and are clipped at zero tension; no invented negative
    # extension-spring force. Rates/initial tension remain design sensitivities.
    springs=[max(0,preload_factor*f-d['counterbalance_rate_each_n_mm']*rate_factor*(z-cal['reference_carriage_z_mm']))
             for f,z in zip(cal['upward_preload_n'],p['carriage_z_mm'])]
    up=sum(springs);net=cal['weight_n']-up/p['normal'][2]+parasitic;gross=net+suction
    return dict(springs_n=springs,net_n=net,gross_n=gross,rate_factor=rate_factor,
        preload_factor=preload_factor,parasitic_n=parasitic,suction_n=suction,drag_n=drag)


def flat_pitch_screen(d,cal,net,drag):
    # Whole-head free body about the transverse pivot, level body. Brush motor
    # torque is internal to that whole assembly and is not counted again.
    y=d['pivot_left_mm'][1];h=d['pivot_left_mm'][2]
    moment=cal['weight_n']*(cal['cg_mm'][1]-y)+drag*h
    cop=y+moment/net if net>0 else None
    a,b=d['support_y_mm']
    required=math.inf if cop is None else max(0,net*(a-cop),net*(cop-b))
    return dict(net_n=net,drag_n=drag,cop_y_mm=cop,stop_moment_nmm=required,
        supported_without_pitch_stop=cop is not None and a<=cop<=b)


def guide_resistance(d,mu,upward_force=0):
    """Conservative scalar guide-friction screen, including eccentric feedback.

    Assume pad reactions at an effective span, add shear and moment magnitudes,
    and solve friction's own offset moment. Not a manufacturer friction rating.
    """
    span=d['guide_effective_contact_span_mm'];off=d['guide_load_offset_mm']
    denominator=1-2*mu*off/span
    if denominator<=0:raise ValueError('Guide friction screen is self-locking')
    drag=max(abs(v) for v in d['drag_n_cases'])
    external_normal=drag+2*drag*d['carriage_above_pivot_mm']/span+2*upward_force*off/span
    service=max(abs(v) for v in d['net_parasitic_n_cases'])
    bound=(2*d['guide_breakaway_allowance_n_each']+mu*external_normal+service)/denominator
    return dict(mu=mu,feedback_denominator=denominator,combined_parasitic_bound_n=bound)


def study(d=None):
    d=d or read();base,a=N.nominal_mass('vacuum',N.read());pr=P.study()
    items=head_items(base,d);cal=calibrate(items,d);limits=rail_limits(d)
    rows=[]
    for n in N.terrain('vacuum',base,a,N.read()):
        p=pose(d,n['normal'],n['plane_constant'],n['head_ground_mm'])
        p.update(state=n['state'],step_mm=n['step_mm'],heading_deg=n['heading_deg'])
        p['travel_margin_mm']=min(min(p['carriage_z_mm'])-limits[0],limits[1]-max(p['carriage_z_mm']))
        p['pitch_margin_deg']=d['pitch_stop_deg']-abs(p['pitch_deg'])
        rows.append(p)
    # Dock supports both pivots level; raising is done at the station.
    raise_by=d['raised_pivot_z_mm']-d['pivot_left_mm'][2]
    raised=pose(d,[0,0,1],0,raise_by);raised['state']='dock captured'
    # The transform raises the tool, not the actual floor beneath it.
    raised['ground_height_mm']=0
    forces=[]
    for i,p in enumerate(rows):
        for rate,preload,para,suction in itertools.product(d['spring_rate_factors'],
                [1-d['counterbalance_force_tolerance'],1,1+d['counterbalance_force_tolerance']],
                d['net_parasitic_n_cases'],d['suction_n_cases']):
            forces.append(dict(pose=i,**force_case(d,cal,p,rate,preload,para,suction)))
    nom=[force_case(d,cal,p) for p in rows]
    pitch=[flat_pitch_screen(d,cal,f,drag) for f,drag in itertools.product(
        [d['target_contact_n'],min(v['net_n'] for v in nom),min(v['net_n'] for v in forces)],d['drag_n_cases'])]
    massrows=[dict(v,total_g=v['qty']*v['each_g']) for v in d['parts']]
    total=sum(v['total_g'] for v in massrows)
    old=pr['mass']['remaining_head_compliance_g']+pr['mass']['head_lift_retained_g']
    railmass=2*d['rail_envelope_mm'][2]*.15
    assert abs(railmass-massrows[0]['total_g'])<1e-9
    ramp=[];tan=d['ramp_rise_mm']/d['ramp_run_mm']
    for mu in d['ramp_mu_cases']:
        multiplier=(tan+mu)/(1-mu*tan)
        ramp.append(dict(mu=mu,force_ratio=multiplier,
            target_contact_push_n=multiplier*d['target_contact_n'],
            high_contact_push_n=multiplier*max(f['gross_n'] for f in forces)))
    guide=[guide_resistance(d,mu,sum(cal['upward_preload_n'])) for mu in d['guide_mu_cases']]
    extended=[];bounds=[]
    for p,rate,preload in itertools.product(rows,d['spring_rate_factors'],[1-d['counterbalance_force_tolerance'],1,1+d['counterbalance_force_tolerance']]):
        nominal=force_case(d,cal,p,rate,preload)
        bound=guide_resistance(d,max(d['guide_mu_cases']),sum(nominal['springs_n']))['combined_parasitic_bound_n']/p['normal'][2]
        bounds.append(bound)
        extended.extend([force_case(d,cal,p,rate,preload,sign*bound) for sign in (-1,1)])
    gravity_guides=[guide_resistance(d,mu) for mu in d['guide_mu_cases']]
    gravity_bound=max(v['combined_parasitic_bound_n'] for v in gravity_guides)/min(p['normal'][2] for p in rows)
    return dict(config=d,calibration=cal,poses=rows,raised=raised,mass_rows=massrows,
        mass=dict(candidate_mechanism_g=total,prior_compliance_and_lift_g=old,
            conditional_reduction_g=old-total,catalog_reference_g=sum(v['total_g'] for v in massrows if v['kind'].startswith('catalog')),
            unfinished_allowance_g=sum(v['total_g'] for v in massrows if not v['kind'].startswith('catalog')),
            current_transfer_g=pr['mass']['prior_transfer_mass_g'],hypothetical_transfer_g=pr['mass']['prior_transfer_mass_g']-old+total,
            hypothetical_gap_g=pr['mass']['prior_transfer_gap_g']-old+total,booked_reduction_g=0),
        motion=dict(carriage_range_mm=[min(min(p['carriage_z_mm']) for p in rows),max(max(p['carriage_z_mm']) for p in rows)],
            tolerance_adjusted_limits_mm=limits,minimum_travel_margin_mm=min(p['travel_margin_mm'] for p in rows),
            maximum_pitch_deg=max(abs(p['pitch_deg']) for p in rows),maximum_roll_deg=max(abs(p['roll_deg']) for p in rows),
            maximum_right_float_mm=max(p['right_float_used_mm'] for p in rows),
            remaining_float_margin_mm=d['right_axial_float_mm']-d['rail_spacing_tolerance_mm']-max(p['right_float_used_mm'] for p in rows),
            raised_carriage_z_mm=raised['carriage_z_mm'],raised_floor_clearance_mm=raise_by),
        contact=dict(nominal_range_n=[min(v['net_n'] for v in nom),max(v['net_n'] for v in nom)],
            sensitivity_net_range_n=[min(v['net_n'] for v in forces),max(v['net_n'] for v in forces)],
            sensitivity_gross_range_n=[min(v['gross_n'] for v in forces),max(v['gross_n'] for v in forces)],
            nonpositive_cases=sum(v['net_n']<=0 for v in forces),cases=len(forces)),
        pitch_screen=pitch,ramp=ramp,guide_friction=guide,
        gravity_comparison=dict(mechanism_g=total-3,conditional_reduction_g=old-total+3,
            nominal_contact_n=cal['weight_n'],guide_cases=gravity_guides,
            net_contact_range_n=[cal['weight_n']-gravity_bound,cal['weight_n']+gravity_bound],
            policy='No counterbalance springs; force set by head mass. Tiny worst-case friction margin is not validation. Dock-only capture limitations unchanged.'),
        extended_contact=dict(combined_parasitic_bound_n=max(bounds),
            net_range_n=[min(v['net_n'] for v in extended),max(v['net_n'] for v in extended)],
            nonpositive_cases=sum(v['net_n']<=0 for v in extended),cases=len(extended)),
        limitations=['Horizontal support-plane samples, not a continuous sharp-step traversal.',
            'Pitch free-body is level only; guides and springs have unmeasured friction and moments.',
            'Mass includes unfinished joints, pins, springs, capture and supports as explicit allowances.',
            'Dock-set capture requires a receiving station to release the head. Arbitrary in-flight head positioning is not supplied.'])


def report(r):
    d=r['config'];m=r['mass'];v=r['motion'];c=r['contact'];cal=r['calibration']
    lines=['# Passive vacuum head — Q comparison','',d['status'],'',
        'Two independent vertical slides carry spherical head pivots. A short drop link places each pivot 20 mm below its carriage. The left pivot locates the head laterally; the right provides 1 mm axial float. The head can translate, roll and pitch without forcing a rigid crossbar to slide crookedly.','',
        '## Motion and force results','',
        f"- Required carriage centers: {v['carriage_range_mm'][0]:.2f}–{v['carriage_range_mm'][1]:.2f} mm. Tolerance-adjusted limits: {v['tolerance_adjusted_limits_mm'][0]:.2f}–{v['tolerance_adjusted_limits_mm'][1]:.2f} mm; smallest travel margin {v['minimum_travel_margin_mm']:.2f} mm.",
        f"- Pitch {v['maximum_pitch_deg']:.2f}°, roll {v['maximum_roll_deg']:.2f}°; right-side geometric float {v['maximum_right_float_mm']:.3f} mm. After 0.5 mm spacing tolerance, {v['remaining_float_margin_mm']:.3f} mm remains from the 1 mm float allocation.",
        f"- Nominal moving head {cal['mass_g']:.1f} g. Target normal force 3.5 N needs unequal upward spring preloads: {cal['upward_preload_n'][0]:.2f} N left / {cal['upward_preload_n'][1]:.2f} N right. The motor-side mass is not centered.",
        f"- Nominal spring model: {c['nominal_range_n'][0]:.2f}–{c['nominal_range_n'][1]:.2f} N net contact. Including rate/preload variation and ±1 N parasitic force: {c['sensitivity_net_range_n'][0]:.2f}–{c['sensitivity_net_range_n'][1]:.2f} N; with 0–5 N suction: {c['sensitivity_gross_range_n'][0]:.2f}–{c['sensitivity_gross_range_n'][1]:.2f} N. These are assumptions, not measured bounds.",
        f"- Station capture uses {v['raised_floor_clearance_mm']:.0f} mm raised clearance and carriage Z{v['raised_carriage_z_mm'][0]:.0f} mm. Passive end stops alone do not provide the proposed raised flight capture.",'',
        '## Whole local replacement scope','',
        '| Item | Quantity | Total | Basis |','|---|---:|---:|---|']
    for row in r['mass_rows']:lines.append(f"| {row['id']} | {row['qty']} | {row['total_g']:.1f} g | {row['kind']} |")
    lines += ['',f"Total **{m['candidate_mechanism_g']:.1f} g**, including {m['unfinished_allowance_g']:.1f} g of unfinished allowances. Compare against **{m['prior_compliance_and_lift_g']:.0f} g** (remaining P compliance plus M lift), giving a conditional {m['conditional_reduction_g']:.1f} g reduction. The 70 g carrier, old head frame and plumbing stay counted.",'',
        f"Current transfer remains **{m['current_transfer_g']/1000:.3f} kg**. If the whole Q scope is completed at this mass and meets its functions, the hypothetical total is {m['hypothetical_transfer_g']/1000:.3f} kg, still {m['hypothetical_gap_g']:.0f} g over 4.5 kg. No reduction is booked.",'',
        '## Pitch stability and edge climbing','',
        '| Net contact | Drag | Required floor resultant Y | Stop couple needed |','|---:|---:|---:|---:|']
    for p in r['pitch_screen']:lines.append(f"| {p['net_n']:.2f} N | {p['drag_n']:.1f} N | {p['cop_y_mm']:.1f} mm | {p['stop_moment_nmm']:.1f} N·mm |")
    lines += ['', 'The ideal front/rear support interval is Y20–52 mm. A resultant outside that interval means the freely pitching head cannot maintain both support rows: a pitch stop or different force/geometry is needed. Moving the pivot upward worsens this drag moment; the drop link prevents that unnecessary penalty. This is a level-body free-body screen, not a solved contact distribution on a step.','',
        'Two end skids have proposed front/back 13.5 mm rises over 14 mm runs. At a 10 mm edge they are intended to lead the hard housing. Wedge/friction sensitivity:', '',
        '| Assumed friction | Push / normal-force ratio | Push at target contact | Push at high contact case |','|---:|---:|---:|---:|']
    for a in r['ramp']:lines.append(f"| {a['mu']:.2f} | {a['force_ratio']:.2f} | {a['target_contact_push_n']:.1f} N | {a['high_contact_push_n']:.1f} N |")
    lines += ['', 'This exposes an unresolved force cost. Guide drag, tire traction, contact transitions, edge shape and housing clearance need a coupled threshold check; the actuator cannot be deleted solely because an incline fits on paper.','',
        f"Adding guide friction, the 20 mm drop-link moment, eccentric-force feedback and ±1 N services produces up to ±{r['extended_contact']['combined_parasitic_bound_n']:.2f} N in the conservative scalar screen. It gives {r['extended_contact']['nonpositive_cases']} nonpositive-contact cases out of {r['extended_contact']['cases']}, with net contact down to {r['extended_contact']['net_range_n'][0]:.2f} N. A nonpositive result means the assumed floor-following state is not physically sustained; do not interpret it as negative floor pressure. These friction inputs are not measured limits.",'',
        f"A gravity-loaded variant removes the counterbalance springs: {r['gravity_comparison']['mechanism_g']:.0f} g local scope, nominal {r['gravity_comparison']['nominal_contact_n']:.2f} N contact and only {r['gravity_comparison']['net_contact_range_n'][0]:.2f} N residual in the high-friction screen. Its conditional {r['gravity_comparison']['conditional_reduction_g']:.0f} g saving is too small to justify deleting away-from-dock lift capability without validation. Prefer evaluating this simpler force arrangement within an integrated head-frame design, while retaining the powered-lift budget until the operating requirements close.",'',
        '## Catalog references','',
        'The guide reference uses two 62 mm NS-01-17 rails (150 g/m) and two standard NW-02-17 carriages (1.7 g each, 20 mm long, 6 mm assembled profile). The manufacturer also describes preload and fixed/floating mounting; use a standard carriage here to avoid adding unnecessary preload. Exact short-rail holes and mounting-face fit need specification. [Guide catalog](https://www.igus.com/us/pdf/drylinn.pdf) · [Current carriage](https://www.igus.com/product/drylin-nw-2-17-j?artnr=NW-02-17).','',
        'The KGLM-03 historical pivot reference has a 3 mm bore, 10 mm OD and 6 mm width. Its specified precision shaft/housing fits are not achieved merely by printing a hole. A captured split housing and smooth pin need qualification, and the current LC successor must be checked separately. [Bearing dimensions](https://www.igus.com/us/pdf/igubal.pdf) · [Historical 0.5 g mass](https://www.igus.com/contentData/Product_Files/Download/pdf/2016%20igubal%20complete.pdf).','',
        '## Boundaries and next decision','']
    lines += ['- '+s for s in r['limitations']]
    lines += ['', '[Design record](../../../docs/PASSIVE_HEAD.md) · [Interactive mechanism](passive_head.html) · [Local CAD check](passive_head_cad_checks.json) · [Mass rows](passive_head_mass.csv)']
    return '\n'.join(lines)+'\n'


def main():
    r=study();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'passive_head.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'passive_head.md').write_text(report(r))
    with (OUT/'passive_head_mass.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r['mass_rows'][0]));w.writeheader();w.writerows(r['mass_rows'])
    print(json.dumps({k:r[k] for k in ('mass','motion','contact','calibration','guide_friction')},indent=2))


if __name__=='__main__':main()
