"""L: coupled chassis/pod equilibrium and catalog spring comparison.

Standard library only. Positive wheel travel is bump. Wheel reactions support
both sprung and moving mass; only the remaining pivot moment loads the spring.
"""
from copy import deepcopy
import hashlib
import itertools
import json
import math
from pathlib import Path
import build as B
import floor_support as H
import height_mounting as I
import wheel_pod as J
import pod_joints as K

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read(): return json.loads((ROOT/'config/suspension_springs.json').read_text())


def weighted(items):
    mass=sum(m for m,p in items)
    return mass,[sum(m*p[i] for m,p in items)/mass for i in range(3)]


def prepare(bottom, d=None, mass_index=1):
    d=d or read();cad=json.loads((OUT/'pod_joints_cad_checks.json').read_text())
    for filename,digest in cad['config_hashes'].items():
        if hashlib.sha256((ROOT/'config'/filename).read_bytes()).hexdigest()!=digest:
            raise ValueError('Stale K CAD input: '+filename)
    c=K.replaced_layout(H.baseline(),cad['mass']['per_pod_interval_g'],cad['mass']['cg_mm'])
    h=J.configured(H.read(),J.read());a=B.assembly(c,bottom,payload=False)
    # Explicitly classify moving K solids. The 5 g spring/bushing allowance is
    # split as 1 g bushings + half the 4 g spring moving, remainder body-fixed.
    moving=[(r['mass_g'],r['cg_mm']) for r in cad['mass']['items']
            if any(r['id'].startswith(p) for p in d['moving_pod_prefixes'])]
    moving.append((d['moving_spring_bushing_allowance_g'],d['moving_allowance_at_mm']))
    pm,pcg=weighted(moving)
    fixed=[];groups=[[],[]]
    for r in a['rows']:
        m=r['mass_g'][mass_index];xyz=r['cg_mm'][:]
        if r['part'].startswith('anti_tip'):xyz[2]+=d['anti_tip_raise_mm']
        if r['hardware_id'] in ('drive_wheel','wheel_hub','drive_motor'):
            side=0 if xyz[0]<137.5 else 1
            xyz[1:]=[105,36];groups[side].append((m,xyz))
        elif r['hardware_id']=='pod':
            side=0 if xyz[0]<137.5 else 1
            # Scale the moving subset consistently for the global mass-bound
            # scenarios. These scenarios are correlated bounds, not all mixed
            # independent component extremes or manufacturer tolerances.
            factor=m/cad['mass']['per_pod_interval_g'][1]
            point=[pcg[0] if side==0 else 275-pcg[0],*pcg[1:]]
            groups[side].append((pm*factor,point))
            fixed.append((m,xyz));fixed.append((-pm*factor,point))
        else: fixed.append((m,xyz))
    return dict(bottom=bottom,config=d,h=h,layout=c,dry_mass_g=a['mass_g'][mass_index],
                fixed=weighted(fixed),moving=[weighted(g) for g in groups],mass_index=mass_index)


def spring_definition(candidate, rate_factor=1, free_offset=0):
    j=J.read();s=j['spring']
    s.update(free_length_mm=candidate['free_length_mm']+free_offset,
             rate_n_mm=candidate['rate_n_mm']*rate_factor,
             solid_height_limit_mm=candidate['solid_height_mm'])
    return j


def reactions(points,cg,weight,normal,contact_n=0,contact_at=(0,0,0)):
    """Three parallel normal forces; project along gravity onto z=0.

    This retains gravity-induced load transfer when the chassis rolls/pitches.
    Using wheel centres or spherical contact points gives the same moment.
    """
    nx,ny,nz=normal
    def project(p):return p[0]-p[2]*nx/nz,p[1]-p[2]*ny/nz
    a,b,c=map(project,points);g=project(cg);tool=project(contact_at)
    force=weight-contact_n
    mx=weight*g[0]-contact_n*tool[0]-force*c[0]
    my=weight*g[1]-contact_n*tool[1]-force*c[1]
    ax,ay=a[0]-c[0],a[1]-c[1];bx,by=b[0]-c[0],b[1]-c[1]
    det=ax*by-bx*ay
    left=(mx*by-bx*my)/det;right=(ax*my-mx*ay)/det
    return [left,right,force-left-right]


def evaluate(p, candidate, shims, travel, loads=(), heading=0, contact_n=0,
             rate_factors=(1,1),free_offsets=(0,0),seat_errors=(0,0)):
    h=p['h'];b=p['bottom'];d=p['config']
    angle=math.radians(heading);cx,cy=h['caster']['centres_xy_mm'][b]
    trail=p['layout']['traction']['caster_trail_mm']
    caster=[cx+trail*math.cos(angle),cy+trail*math.sin(angle),0]
    n=H.support_plane(h,*travel,caster[:2]);moving=[];points=[]
    for side,t in enumerate(travel):
        m,xyz=p['moving'][side];moving.append((m,[xyz[0],*H.rotate_yz(h,*xyz[1:],t)]))
        wheel=H.pose(h,t);points.append([14 if side==0 else 261,wheel['axle_y_mm'],wheel['axle_z_mm']])
    mass,cg=weighted([p['fixed'],*moving,*[(r[0],list(r[1:])) for r in loads]])
    forces=reactions([*points,caster],cg,mass/1000*B.G,n,contact_n,d['tool_contact'][b]['at_mm'])
    springs=[];residuals=[];gravity=[]
    for side,t in enumerate(travel):
        definition=spring_definition(candidate,rate_factors[side],free_offsets[side])
        # Seat error changes actual spring span at a fixed installed setting.
        definition['spring']['upper_pivot_yz_mm'][1]+=seat_errors[side]
        sp=J.spring_pose(h,definition,t,shims[side]);springs.append(sp)
        py,pz=h['wheel']['pivot_yz_mm'];m,xyz=moving[side]
        own_moment=m/1000*B.G*((py-xyz[1])*n[2]+(xyz[2]-pz)*n[1])
        lever=(py-points[side][1])*n[2]+(points[side][2]-pz)*n[1]
        gravity.append(own_moment)
        residuals.append(sp['force_n']*sp['moment_arm_mm']+own_moment-forces[side]*lever)
    return dict(travel_mm=list(travel),normal=n,caster_mm=caster,mass_g=mass,cg_mm=cg,
        support_n=forces,springs=springs,residual_nmm=residuals,moving_gravity_moment_nmm=gravity)


def solve(p,candidate,shims,**kwargs):
    """Projected Newton solve with positive stop reactions at active limits."""
    lo=-p['h']['wheel']['droop_candidate_mm'];hi=p['h']['wheel']['bump_mm'];t=[0.,0.]
    for iteration in range(45):
        r=evaluate(p,candidate,shims,t,**kwargs);f=r['residual_nmm']
        active=[(t[i]<=lo+1e-8 and f[i]>=0) or (t[i]>=hi-1e-8 and f[i]<=0) for i in range(2)]
        if all(active[i] or abs(f[i])<1e-6 for i in range(2)):break
        jac=[]
        for i in range(2):
            q=t[:];q[i]+=.001
            ff=evaluate(p,candidate,shims,q,**kwargs)['residual_nmm']
            jac.append([(ff[k]-f[k])/.001 for k in range(2)])
        if all(active):break
        if any(active):
            i=0 if not active[0] else 1;step=[0.,0.];step[i]=-f[i]/jac[i][i]
        else:
            a,c=jac[0];b,d=jac[1];det=a*d-b*c
            step=[(-f[0]*d+b*f[1])/det,(c*f[0]-a*f[1])/det]
        t=[min(hi,max(lo,t[i]+max(-4,min(4,step[i])))) for i in range(2)]
    else:raise RuntimeError('Equilibrium failed to converge')
    r['stops']=['droop' if t[i]<=lo+1e-7 else 'bump' if t[i]>=hi-1e-7 else None for i in range(2)]
    r['iterations']=iteration+1;r['supports_positive']=min(r['support_n'])>0
    return r


def calibrate(p,candidate,rate_factors=(1,1),free_offsets=(0,0),target=None):
    """Set each module once at its stated contents, tool raised, caster heading 0."""
    d=p['config'];target=d.get('target_by_module_mm',{}).get(p['bottom'],d['target_travel_mm']) if target is None else target
    loads=d['contents'][p['bottom']][d['calibration_contents_index'][p['bottom']]]['loads']
    values=[];clipped=[]
    for side in range(2):
        args=dict(loads=loads,rate_factors=rate_factors,free_offsets=free_offsets)
        f0=evaluate(p,candidate,[0,0],[target,target],**args)['residual_nmm'][side]
        f6=evaluate(p,candidate,[6,6],[target,target],**args)['residual_nmm'][side]
        if f0>0:value=0;clipped.append(True)
        elif f6<0:value=6;clipped.append(True)
        else:
            lo=0;hi=6
            for _ in range(35):
                mid=(lo+hi)/2
                f=evaluate(p,candidate,[mid,mid],[target,target],**args)['residual_nmm'][side]
                if f>0:hi=mid
                else:lo=mid
            value=(lo+hi)/2;clipped.append(False)
        step=d['shim_step_mm'];values.append(round(value/step)*step)
    return dict(shims_mm=values,clipped=clipped,target_travel_mm=target)


def installed_screen(p,candidate,shims,seat_error=0,rate_factors=(1,1),free_offsets=(0,0)):
    d=p['config'];h=p['h'];samples=[]
    for t in [-2.5+i*.1 for i in range(126)]:
        for side,shim in enumerate(shims):
            for error in (-seat_error,seat_error):
                j=spring_definition(candidate,rate_factors[side],free_offsets[side]);j['spring']['upper_pivot_yz_mm'][1]+=error
                samples.append(J.spring_pose(h,j,t,shim))
    shortest=min(r['length_mm'] for r in samples);longest=max(r['length_mm'] for r in samples)
    solid=shortest-candidate['solid_height_mm']-d['solid_height_extra_mm']
    working=None if candidate['load_length_mm'] is None else shortest-candidate['load_length_mm']-d['working_length_margin_mm']
    guide=min(r['guide_end_gap_mm'] for r in samples);overlap=min(r['guide_overlap_mm'] for r in samples)
    fits=candidate['od_mm']<=d['spring_envelope_od_mm'] and candidate['id_mm']>=d['spring_envelope_id_mm']
    return dict(min_length_mm=shortest,max_length_mm=longest,solid_gap_after_uncertainty_mm=solid,
        working_length_margin_after_reserve_mm=working,min_guide_end_gap_mm=guide,min_guide_overlap_mm=overlap,
        max_spring_force_n=max(r['force_n'] for r in samples),min_spring_force_n=min(r['force_n'] for r in samples),
        fits_radially=fits,passes=fits and solid>=2 and working is not None and working>=0 and guide>=1 and overlap>=1.5
        and min(r['force_n'] for r in samples)>0)


def nominal_comparison(d):
    rows=[]
    for candidate in d['candidates']:
        modules={}
        for bottom in ('vacuum','mop','low'):
            p=prepare(bottom,d);cal=calibrate(p,candidate);s=installed_screen(p,candidate,cal['shims_mm'],d['seat_error_mm'])
            modules[bottom]=dict(calibration=cal,installed=s)
        rows.append(dict(candidate=candidate,modules=modules,all_pass=all(v['installed']['passes'] and not any(v['calibration']['clipped']) for v in modules.values())))
    return rows


def summary(rows):
    return dict(samples=len(rows),travel_ranges_mm=[[min(r['travel_mm'][i] for r in rows),max(r['travel_mm'][i] for r in rows)] for i in range(2)],
        support_ranges_n=[[min(r['support_n'][i] for r in rows),max(r['support_n'][i] for r in rows)] for i in range(3)],
        stop_cases=sum(any(r['stops']) for r in rows),negative_support_cases=sum(not r['supports_positive'] for r in rows),
        max_free_equilibrium_residual_nmm=max(abs(v) for r in rows for i,v in enumerate(r['residual_nmm']) if r['stops'][i] is None),
        total_drive_load_range_n=[min(sum(r['support_n'][:2]) for r in rows),max(sum(r['support_n'][:2]) for r in rows)])


def operation(p,candidate,shims,headings=None,**kwargs):
    d=p['config'];bottom=p['bottom'];rows=[]
    for contents,heading,contact in itertools.product(d['contents'][bottom],
            headings or range(0,360,d['heading_step_deg']),d['tool_contact'][bottom]['force_n']):
        r=solve(p,candidate,shims,loads=contents['loads'],heading=heading,contact_n=contact,**kwargs)
        r.update(contents=contents['label'],heading_deg=heading,contact_n=contact)
        rows.append(r)
    return rows


def height_and_head(p,rows):
    c,h=I.configured(p['layout'],p['h'],I.read());parts=I.body_parts(c,h,I.read(),p['bottom'])
    tips=[v for v in parts if v['id'].startswith('anti_tip')]
    hi=[];head=[];stowed=[];original_tip=[];raised_tip=[]
    x,y,z=p['config']['tool_contact'][p['bottom']]['at_mm']
    for r in rows:
        top,n=I.height_at(parts,h,*r['travel_mm'],r['caster_mm'][:2]);hi.append(top[0])
        for tip in tips:
            q=[tip['min'][i] if n[i]>=0 else B.hi(tip)[i] for i in range(3)]
            clearance=n[0]*(q[0]-r['caster_mm'][0])+n[1]*(q[1]-r['caster_mm'][1])+n[2]*q[2]
            original_tip.append(clearance);raised_tip.append(clearance+n[2]*p['config']['anti_tip_raise_mm'])
        height=n[0]*(x-r['caster_mm'][0])+n[1]*(y-r['caster_mm'][1])+n[2]*z
        head.append(-height/n[2])
        if p['bottom']=='low':
            part=next(v for v in B.reference_parts(c,'low') if v['id']=='low_head')
            q=[part['min'][i] if n[i]>=0 else B.hi(part)[i] for i in range(3)]
            stowed.append(n[0]*(q[0]-r['caster_mm'][0])+n[1]*(q[1]-r['caster_mm'][1])+n[2]*q[2])
    return dict(max_height_mm=max(hi),max_height_with_2mm_reserve_mm=max(hi)+2,
        required_head_retraction_range_mm=[min(head),max(head)] if p['bottom']!='low' else None,
        stowed_sofa_head_min_clearance_mm=min(stowed) if stowed else None,
        old_anti_tip_min_clearance_mm=min(original_tip),raised_anti_tip_min_clearance_mm=min(raised_tip),
        scope='I height allocations, K mass. Head value is the chassis-Z shift to put its reference point on the floor. It is not a completed floating-head linkage or a ground-clearance check of every part.')


def sensitivity(p,candidate):
    d=p['config'];rows=[];setups=[]
    # Each real module is calibrated once with its actual two springs. The
    # rate/free-length corner values are not allowed to change during a run.
    rates_at=[min(d['spring_rate_factors']),max(d['spring_rate_factors'])]
    offsets_at=[min(d['free_length_offsets_mm']),max(d['free_length_offsets_mm'])]
    for rates,offsets in itertools.product(itertools.product(rates_at,repeat=2),itertools.product(offsets_at,repeat=2)):
        cal=calibrate(p,candidate,rate_factors=rates,free_offsets=offsets)
        fit=installed_screen(p,candidate,cal['shims_mm'],d['seat_error_mm'],rates,offsets)
        setups.append(dict(rate_factors=rates,free_offsets_mm=offsets,calibration=cal,installed=fit))
        for errors in itertools.product((-d['seat_error_mm'],d['seat_error_mm']),repeat=2):
            rows.extend(operation(p,candidate,cal['shims_mm'],headings=[0,90,180,270],
                rate_factors=rates,free_offsets=offsets,seat_errors=errors))
    return dict(setups=setups,installed_failures=sum(not v['installed']['passes'] or any(v['calibration']['clipped']) for v in setups),
        operation=summary(rows),height=height_and_head(p,rows))


def structural_screen(r,candidate):
    """Reapply K's declared impact cases to the new spring force envelope."""
    cases=[];max_force=max(v['installed']['max_spring_force_n'] for v in r['preferred'].values())
    for v in r['preferred'].values():
        max_force=max(max_force,max(s['installed']['max_spring_force_n'] for s in v['sensitivity']['setups']))
    cap=math.ceil(max_force/5)*5;h=J.configured(H.read(),J.read())
    for v in r['preferred'].values():
        setups=[dict(calibration=v['calibration'],rate_factors=[1,1],free_offsets_mm=[0,0]),*v['sensitivity']['setups']]
        for setup in setups:
            for side in (0,1):
                for error in (-r['config']['seat_error_mm'],r['config']['seat_error_mm']):
                    j=spring_definition(candidate,setup['rate_factors'][side],setup['free_offsets_mm'][side])
                    j['spring']['upper_pivot_yz_mm'][1]+=error
                    cases.append(K.load_screen(h,j,K.read(),[setup['calibration']['shims_mm'][side]],cap))
    return dict(screens=len(cases),max_spring_force_n=max_force,cap_branch_bound_n=cap,
        pivot_bending_mpa=max(c['pivot_bending_mpa'] for c in cases),stop_bolt_bending_mpa=max(c['stop_bolt_bending_mpa'] for c in cases),
        max_stop_force_n=max(c['max_stop_force_n'] for c in cases),
        inner_M4_shear_mpa=max(c['inner_rail_joint']['M4_shear_mpa'] for c in cases),
        angle_edge_shear_mpa=max(c['inner_rail_joint']['angle_countersink_edge_shear_mpa'] for c in cases),
        rail_edge_shear_mpa=max(c['inner_rail_joint']['rail_rear_edge_shear_mpa'] for c in cases),
        passes=all(c['pivot_passes'] and c['stop_bolt_passes'] and c['inner_rail_joint']['M4_passes']
                   and c['inner_rail_joint']['angle_edge_passes'] and c['inner_rail_joint']['rail_rear_edge_shear_mpa']<=80 for c in cases),
        scope='K 150 N vertical/±25 N fore-aft impact screens reapplied at full bump, including spring sensitivity setups that fail length screens. Fixed cap branch bound raised to cover spring force. No full plate, cup, trunnion, fatigue, thread or motor-shaft qualification.')


def report(r):
    d=r['config'];lines=['# L — springs and loaded ride height','',d['status'],'',
        'K remains the carried-mass planning scenario. L corrects spring loading for moving wheel/pod mass, solves chassis attitude and compares catalog springs. No physical tests or spring order are implied.','',
        '## Candidate comparison','',
        'The dimensional pass below uses module-specific calibration, all −2.5…+10 mm travel, a ±0.25 mm seat error, +0.5 mm solid-height uncertainty, 2 mm coil-bind gap and a 0.5 mm reserve above catalog L1. It does not establish fatigue life. The earlier spring has no catalog L1.','',
        '| Candidate | OD | Rate | Free length | Vacuum / mop / sofa installed screen |','|---|---:|---:|---:|---|']
    for row in r['comparison']:
        c=row['candidate'];results=['pass' if v['installed']['passes'] and not any(v['calibration']['clipped']) else 'fail' for v in row['modules'].values()]
        lines.append(f"| {c['id']} | {c['od_mm']:.2f} mm | {c['rate_n_mm']:.2f} N/mm | {c['free_length_mm']:.2f} mm | {' / '.join(results)} |")
    lines+=['',f"**Preferred integration candidate: {d['preferred_candidate']}**, with an 11.2 mm OD clearance reservation in the existing 12 mm cups. This widens the earlier 10 mm spring reservation; it does not make the robot wider. Use the music-wire variant. Procurement and manufacturing tolerances are unconfirmed.",'',
        'The reference resting points are +3 mm travel for vacuum/sofa and +1 mm for mop, leaving roughly 7 and 9 mm to the bump stop at calibration. The mop uses more preload than a +3 mm setup so its spring remains seated at full droop. This is not 10 mm of remaining bump and does not demonstrate crossing a 10 mm threshold. Empty/full containers do not trigger an automatic preload adjustment. Each bottom has its own calibrated left/right settings.','',
        '| Module | Left/right shim | Operational left travel | Right travel | Max body height + reserve |','|---|---:|---:|---:|---:|']
    fmt=lambda q:'…'.join(f'{v:.2f}' for v in q)
    for b,v in r['preferred'].items():
        s=v['operation'];lines.append(f"| {b} | {' / '.join(str(x) for x in v['calibration']['shims_mm'])} mm | {fmt(s['travel_ranges_mm'][0])} mm | {fmt(s['travel_ranges_mm'][1])} mm | {v['height']['max_height_with_2mm_reserve_mm']:.2f} mm |")
    lines+=['','Operation includes nominal hardware, separate empty/design/heavy contents and the declared tool contact forces over 24 caster headings. All settings remain fixed within each module. Sofa results cover stowed transit only.','',
        '| Module | Full-bump shortest spring incl. seat error | Remaining L1 margin after reserve | Failed calibrated tolerance setups |','|---|---:|---:|---:|']
    for b,v in r['preferred'].items():
        fit=v['installed'];lines.append(f"| {b} | {fit['min_length_mm']:.2f} mm | {fit['working_length_margin_after_reserve_mm']:.2f} mm | {v['sensitivity']['installed_failures']} / 16 |")
    lines+=['','**Do not release this spring for purchase yet.** Some assumed rate/free-length tolerance corners lose either working-length margin at bump or positive seating force at droop at their calibrated settings. The sofa nominal margin is small. Obtain actual load-at-length/tolerance data, then accept a bounded spring/setpoint range or revise the seat/stop geometry. Passing nominal dimensions is insufficient.','',
        '## Moving mass, contents and tool contact','',
        'The moving wheel, hub, motor and pod subtotal is about 276 g per side. The wheels carry this mass directly as well as the chassis load. Its gravity moment is included in pod equilibrium and its position changes with travel. The K preload calculation treated the whole wheel reaction as spring-supported and therefore overstated preload. L retains the K total hardware mass, separating its moving and fixed portions without counting either twice. Wheel/hub centres move to the H/J axle location; mop water and wet-pad masses have separate positions.','',
        '| Module | Contents mass | Head retraction needed at reference point |','|---|---:|---:|']
    for b,v in r['preferred'].items():
        masses=[sum(q[0] for q in case['loads']) for case in d['contents'][b]]
        head=v['height']['required_head_retraction_range_mm']
        value=fmt(head)+' mm' if head else f"Stowed head: {v['height']['stowed_sofa_head_min_clearance_mm']:.2f} mm minimum floor clearance"
        lines.append(f"| {b} | {min(masses)}…{max(masses)} g | {value} |")
    lines+=['','The head values are required motion relative to the chassis, not evidence that the current head mechanism supplies it. Tool pressure and floating-head travel must be designed together before the resting point is adopted. Mop fluid sensitivity covers a centred wet pad and water at the allocated tank centre; slosh is unmodeled. Sofa head/hose support while extended needs a separate contact model.','',
        '## Necessary anti-tip mount change','',
        'The original front anti-tip rollers extend down to Z=2 mm. They intersect the floor in these resting poses, so the three-support calculation would not describe the unchanged robot. L is explicitly conditional on raising their mounts 10 mm (new allocation Z=12…36 mm). Their mass is retained and raised in the CG model. The raised allocation clears the sampled normal-running poses; actual brackets and tipping/threshold behavior remain unqualified.','',
        '| Module | Original minimum clearance | Raised minimum clearance |','|---|---:|---:|']
    for b,v in r['preferred'].items():
        lines.append(f"| {b} | {v['height']['old_anti_tip_min_clearance_mm']:.2f} mm | {v['height']['raised_anti_tip_min_clearance_mm']:.2f} mm |")
    lines+=['',
        '## Uncertainty and scope','',
        'The 16 calibrated tolerance setups combine independent ±10% spring rates and ±0.5 mm free lengths; operational sweeps then add ±0.25 mm seat errors. These are project sensitivities, not supplier specifications. Low/high hardware sweeps use the existing component mass intervals with nominal shim settings, preserving contents as separate loads. They are correlated all-low/all-high cases, not every mixed component/CG corner. No design-wide tolerance closure is claimed.','',
        '| Module | Low-hardware travel L/R | High-hardware travel L/R | High-mass stop cases |','|---|---|---|---:|']
    for b,v in r['preferred'].items():
        lo=v['mass_sensitivity']['low'];hi=v['mass_sensitivity']['high']
        lines.append(f"| {b} | {fmt(lo['travel_ranges_mm'][0])} / {fmt(lo['travel_ranges_mm'][1])} | {fmt(hi['travel_ranges_mm'][0])} / {fmt(hi['travel_ranges_mm'][1])} | {hi['stop_cases']} |")
    s=r['structure']
    lines+=['','The calculation assumes quasistatic motion, parallel ground-normal forces, spherical tire reach and an ideal caster. Drive torque, friction, damping, acceleration, tire deformation and obstacle-climbing dynamics are absent. Extra rigid ground contacts invalidate the three-support solution; the raised anti-tip clearance is checked separately. Stop reaction signs are checked for equilibrium at the limits. The installed spring calculations use all travel; operational height is a finite sample.','',
        f"Reapplying the K impact cases with the new spring gives at most {s['max_spring_force_n']:.1f} N spring force and uses a ±{s['cap_branch_bound_n']} N fixed-cap branch bound. Screened pivot/stop-screw bending: {s['pivot_bending_mpa']:.1f}/{s['stop_bolt_bending_mpa']:.1f} MPa; inner M4 bolt shear: {s['inner_M4_shear_mpa']:.1f} MPa; angle-edge shear: {s['angle_edge_shear_mpa']:.1f} MPa. These limited static screens {'pass' if s['passes'] else 'FAIL'}; cup/trunnion strength, retention, fatigue, thread and motor-shaft checks remain open.",'',
        'Spring mass, revised shims and any new hardware remain within an unclosed mass allowance; K totals are not presented as measured or finalized L hardware.','',
        '## Sources and artifacts','',
        f"- [ASRaymond manufacturer catalog]({d['catalog_source']}): spring dimensions, rates and load lengths; catalog music-wire values used.",
        '- [ASRaymond C0360-051-1250-M](https://www.asraymond.com/mechanical-wire-springs/compression/spec-standard-compression-springs-132415/c0360-051-1250-m-c03600511250m/) and [C0480-067-1000-M](https://www.asraymond.com/mechanical-wire-springs/compression/spec-standard-compression-springs-132415/c0480-067-1000-m-c04800671000m/): product identity/rate references; rounded solid heights differ from the catalog, so the larger catalog dimensions are retained.',
        '- [Interactive results](suspension_springs.html), [inputs](../../../config/suspension_springs.json), [calculation data](suspension_springs.json), [design record](../../../docs/SUSPENSION_SPRING_SELECTION.md).']
    return '\n'.join(lines)+'\n'


def main():
    d=read();r=dict(revision=d['revision'],config=d,comparison=nominal_comparison(d),preferred={},fabrication_release=False,
        input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config/suspension_springs.json',OUT/'pod_joints_cad_checks.json',ROOT/'config/height_mounting.json']})
    candidate=next(v for v in d['candidates'] if v['id']==d['preferred_candidate'])
    for bottom in ('vacuum','mop','low'):
        p=prepare(bottom,d);cal=calibrate(p,candidate);rows=operation(p,candidate,cal['shims_mm'])
        r['preferred'][bottom]=dict(calibration=cal,moving_mass_cg=p['moving'],operation=summary(rows),samples=rows,
            height=height_and_head(p,rows),installed=installed_screen(p,candidate,cal['shims_mm'],d['seat_error_mm']),
            sensitivity=sensitivity(p,candidate),mass_sensitivity={})
        for label,index in [('low',0),('high',2)]:
            bound=prepare(bottom,d,index);cases=operation(bound,candidate,cal['shims_mm'])
            r['preferred'][bottom]['mass_sensitivity'][label]={**summary(cases),'height':height_and_head(bound,cases)}
    r['structure']=structural_screen(r,candidate)
    (OUT/'suspension_springs.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'suspension_springs.md').write_text(report(r))
    template=ROOT/'design/system/suspension_springs_viewer.html'
    if template.exists():(OUT/'suspension_springs.html').write_text(template.read_text().replace('__MODEL__',json.dumps(r)))
    print('L spring/ride study written; nominal cases',sum(v['operation']['samples'] for v in r['preferred'].values()),
          'tolerance cases',sum(v['sensitivity']['operation']['samples'] for v in r['preferred'].values()))


if __name__=='__main__':main()
