"""H mechanism study. Candidate stock is never silently added to/replaces G mass."""
from copy import deepcopy
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

import build as base
import core_partition as power
import frame_joints as frame

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'


def read():
    return json.loads((ROOT / 'config/floor_support.json').read_text())


def baseline():
    return frame.configured(power.configured(base.read(), power.read()), frame.read())


def pose(d, travel):
    w = d['wheel']; py, pz = w['pivot_yz_mm']; ay, az = w['axle_yz_mm']
    length = math.hypot(py-ay, pz-az)
    if az != pz or not -length < travel < length:
        raise ValueError('This study requires a level reference arm and travel below arm length')
    theta = math.asin(travel/length)
    return dict(travel_mm=travel, angle_deg=math.degrees(theta), axle_y_mm=py-length*math.cos(theta),
                axle_z_mm=az+travel, length_mm=length, pivot_y_mm=py, pivot_z_mm=pz)


def rotate_yz(d, y, z, travel):
    p = pose(d, travel); a = math.radians(p['angle_deg']); py, pz = d['wheel']['pivot_yz_mm']
    # Rotation about -X: forward points rise on bump.
    return [py+(y-py)*math.cos(a)+(z-pz)*math.sin(a),
            pz-(y-py)*math.sin(a)+(z-pz)*math.cos(a)]


def moving_box(d, xyz, size, travel):
    corners = [rotate_yz(d,y,z,travel) for y,z in itertools.product(
        (xyz[1],xyz[1]+size[1]), (xyz[2],xyz[2]+size[2]))]
    yy, zz = zip(*corners)
    return dict(min=[xyz[0],min(yy),min(zz)],size=[size[0],max(yy)-min(yy),max(zz)-min(zz)])


def simply_supported_loads(xs, loads, supports):
    a,b = supports
    rb = -sum(f*(x-a) for x,f in zip(xs,loads))/(b-a)
    ra = -sum(loads)-rb
    events = sorted([(a,ra),(b,rb)]+list(zip(xs,loads)))
    moments = [sum(f*(x-xx) for xx,f in events if xx <= x) for x,_ in events]
    return dict(reactions_n=[ra,rb],max_moment_nmm=max(map(abs,moments)))


def pivot_screen(d):
    w=d['wheel']; length=pose(d,0)['length_mm']
    fw=w['factored_vertical_wheel_load_n']; fs=w['spring_force_at_impact_n']
    # Hard-stop force includes the adverse fore/aft ground-force moment.
    stop=(fw*length+w['horizontal_wheel_load_n']*w['axle_yz_mm'][1]-fs*w['spring_lever_mm'])/w['bump_stop_lever_mm']
    arm=simply_supported_loads([w['contact_x_mm'],w['spring_x_mm'],w['bump_stop_x_mm']],
                              [fw,-fs,-stop],w['bushing_centres_x_mm'])
    # The arm puts equal-and-opposite forces into the pin at the two bushings.
    pin=simply_supported_loads(w['bushing_centres_x_mm'],[-v for v in arm['reactions_n']],w['fixed_support_centres_x_mm'])
    horizontal_arm=simply_supported_loads([w['contact_x_mm']],[w['horizontal_wheel_load_n']],w['bushing_centres_x_mm'])
    horizontal_pin=simply_supported_loads(w['bushing_centres_x_mm'],[-v for v in horizontal_arm['reactions_n']],w['fixed_support_centres_x_mm'])
    moment=math.hypot(pin['max_moment_nmm'],horizontal_pin['max_moment_nmm'])
    resultant=max(math.hypot(v,h) for v,h in zip(arm['reactions_n'],horizontal_arm['reactions_n']))
    rows=[]
    for diameter in w['pivot_diameter_sensitivity_mm']:
        sigma=32*moment/(math.pi*diameter**3)
        # Conservative full bearing reaction on one pin section; no double-shear credit.
        tau=4*resultant/(math.pi*diameter**2)
        rows.append(dict(diameter_mm=diameter,bending_mpa=sigma,shear_mpa=tau,
            passes=sigma<=w['steel_bending_screen_mpa'] and tau<=w['steel_shear_screen_mpa']))
    return dict(arm_bearing_reactions_n=arm['reactions_n'],fixed_support_reactions_n=pin['reactions_n'],
        hard_stop_force_n=stop,spring_force_n=fs,pin_moment_bound_nmm=moment,screens=rows,
        max_projected_bushing_pressure_mpa=resultant/(w['pivot_diameter_mm']*w['bushing_length_mm']),
        motor_output_radial_load_rating_verified=False,bushing_rating_verified=False)


def plate_section(width,thickness):
    return dict(area_mm2=width*thickness,neutral_z_mm=thickness/2,
                inertia_mm4=width*thickness**3/12,c_mm=thickness/2)


def caster_screen(d):
    c=d['caster'];m=d['material']
    s=plate_section(c['saddle_width_mm'],c['plate_mm'])
    length=c['rear_attachment_y_mm']-c['centres_xy_mm']['vacuum'][1]
    f=c['factored_vertical_load_n'];moment=c['horizontal_load_n']*c['bare_height_mm'];e=m['aluminum_e_mpa'];i=s['inertia_mm4']
    stress=(f*length+moment)*s['c_mm']/i
    deflection=f*length**3/(3*e*i)+moment*length**2/(2*e*i)
    return dict(section=s,cantilever_mm=length,stress_mpa=stress,deflection_mm=deflection,
        passes=stress<=m['aluminum_bending_screen_mpa'] and deflection<=m['deflection_screen_mm'],
        rigid_root_assumed=True,stem_retention_verified=False,
        fitting_cases=[dict(fitting_height_mm=h,saddle_top_mm=c['bare_height_mm']+h+c['plate_mm']+c['retainer_allowance_mm'],
            vacuum_mop_gap_mm=62-(c['bare_height_mm']+h+c['plate_mm']+c['retainer_allowance_mm']),
            low_gap_mm=64-(c['bare_height_mm']+h+c['plate_mm']+c['retainer_allowance_mm'])) for h in c['fitting_height_sensitivity_mm']])


def stock(d,bottom='vacuum'):
    """Gross blanks; connected joints and fasteners still require detail."""
    parts=[];rho=d['material']['aluminum_density_g_mm3'];w=d['wheel'];c=d['caster'];k=d['carrier']
    def add(id,xyz,size,role,**extra):
        p=dict(id=id,min=xyz,size=size,role=role,shape='box',mass_g=math.prod(size)*rho,**extra)
        parts.append(p);return p
    for side,mirror in [('left',False),('right',True)]:
        def xval(x,width): return 275-x-width if mirror else x
        for name,x in [('outer',26),('inner',103)]:
            add('H_'+side+'_cheek_'+name,[xval(x,3),w['pivot_yz_mm'][0]-13,26],[3,22,w['cap_bottom_z_mm']-26],'pivot support',
                hole=dict(axis='x',diameter=w['pivot_diameter_mm']+0.2,y=w['pivot_yz_mm'][0],z=36))
        add('H_'+side+'_cap',[xval(26,80),w['axle_yz_mm'][0]+4,w['cap_bottom_z_mm']],[80,45,3],'pivot support')
    add('H_front_bridge',k['bridge_min_mm'],k['bridge_size_mm'],'carrier route')
    add('H_left_rail',k['left_rail_min_mm'],k['left_rail_size_mm'],'carrier route')
    add('H_right_rail',k['right_rail_min_mm'],k['right_rail_size_mm'],'carrier route')
    add('H_shelf_rib',k['right_shelf_rib_min_mm'],k['right_shelf_rib_size_mm'],'carrier route')
    for j,r in enumerate(k['inner_rails']):add('H_inner_rail_'+str(j),r['min'],r['size'],'carrier route')
    add('H_rear_bridge',k['rear_bridge_min_mm'],k['rear_bridge_size_mm'],'rear route')
    x,y=c['centres_xy_mm'][bottom];z=c['bare_height_mm']+c['reference_fitting_height_mm'];b=c['saddle_width_mm'];length=c['saddle_length_mm'];t=c['plate_mm'];front=c['saddle_front_y_mm']
    add('H_caster_base',[x-b/2,front,z],[b,length,t],'caster saddle',hole=dict(axis='z',diameter=8.5,x=x,y=y))
    # Rear tab meets the crossbar at z=65. This is a profile in one plate, not
    # a welded butt joint; export together or procure as one flat profile.
    add('H_caster_rear_tab',[x-b/2,263,z+t],[b,3,65-(z+t)],'rear route')
    return parts


def stock_conflicts(g,d,bottom):
    """External functional bays only; own pod/caster allocations are replaced.

    This intentionally reports route obstructions rather than suppressing them.
    It is not a check of all candidate-to-candidate fastening/contact surfaces.
    """
    parts=base.reference_parts(g,bottom)
    replaced=set(d['carrier']['removed_if_closed'])|{'pod_left','pod_right','caster'}
    errors=[]
    for s in stock(d,bottom):
        for p in parts:
            if p.get('parent') or p['shape']=='distributed' or p['id'] in replaced:continue
            if base.overlap(s,p):errors.append(s['id']+' / '+p['id'])
    return errors


def static_wheel_loads(g,d,bottom):
    a=base.assembly(g,bottom);cg=a['cg_mm'];w=d['wheel'];y=w['axle_yz_mm'][0]
    x1,x2=[p[0] for p in g['traction']['drive_contact_xy']];cx,cy=d['caster']['centres_xy_mm'][bottom]
    weight=a['mass_g'][1]/1000*base.G;rows=[]
    for deg in range(0,360,5):
        angle=math.radians(deg);x=cx+15.5*math.cos(angle);yy=cy+15.5*math.sin(angle)
        rc=weight*(cg[1]-y)/(yy-y)
        rr=(weight*(cg[0]-x1)-rc*(x-x1))/(x2-x1);rl=weight-rc-rr
        rows.append((rl,rr,rc))
    ratio=w['spring_lever_mm']/pose(d,0)['length_mm'];rate=w['wheel_rate_n_mm']/ratio**2
    return dict(support_force_ranges_n=[[min(r[i] for r in rows),max(r[i] for r in rows)] for i in range(3)],
        spring_rate_n_mm=rate,lever_ratio=ratio,
        spring_preload_compression_mm=[[min(r[i] for r in rows)/(ratio*rate),max(r[i] for r in rows)/(ratio*rate)] for i in (0,1)],
        scope='G nominal mass/CG and proposed y=105 contacts, 72 caster headings; excludes uncertainty, tool contact and small moving-part CG shift')


def support_plane(d, left, right, caster_xy):
    """Unit ground normal in chassis coordinates for two spherical tire proxies.

    A sphere of the tire radius bounds a tilted disk's vertical reach. The
    caster is an ideal body-fixed point selected from its trail circle.
    """
    w=d['wheel'];cx,cy=caster_xy;p=pose(d,left);q=pose(d,right)
    a=14-cx;b=p['axle_y_mm']-cy;c=261-cx;e=q['axle_y_mm']-cy
    det=a*e-b*c
    def solve(u,v):return ((u*e-b*v)/det,(a*v-u*c)/det)
    alpha=solve(w['radius_mm'],w['radius_mm'])
    beta=solve(-p['axle_z_mm'],-q['axle_z_mm'])
    aa=1+sum(x*x for x in beta);bb=2*sum(x*y for x,y in zip(alpha,beta));cc=sum(x*x for x in alpha)-1
    nz=(-bb+math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    return [alpha[0]+beta[0]*nz,alpha[1]+beta[1]*nz,nz]


def height_screen(g,d):
    w=d['wheel'];travel=[-w['droop_candidate_mm'],0,2.5,5,7.5,w['bump_mm']]
    # Heights of real functional allocations; distributed allowances have no
    # physical outer surface. Ignore extension overhang in this rigid-body limit.
    parts=[p for p in base.reference_parts(g,'vacuum') if not p.get('parent') and p['shape']!='distributed']
    result={};count=0
    for bottom,centre in d['caster']['centres_xy_mm'].items():
        worst=dict(max_height_mm=0)
        for left,right in itertools.product(travel,repeat=2):
            for heading in range(0,360,5):
                a=math.radians(heading);caster=[centre[0]+15.5*math.cos(a),centre[1]+15.5*math.sin(a)]
                n=support_plane(d,left,right,caster);count+=1
                for part in parts:
                    xyz=[(base.hi(part)[i] if n[i]>=0 else part['min'][i]) for i in range(3)]
                    height=n[0]*(xyz[0]-caster[0])+n[1]*(xyz[1]-caster[1])+n[2]*xyz[2]
                    if height>worst['max_height_mm']:
                        worst=dict(max_height_mm=height,part=part['id'],left_travel_mm=left,right_travel_mm=right,
                                   caster_heading_deg=heading,normal=n)
        result[bottom]=worst
    return dict(cases=result,sampled_support_poses=count,droop_adopted=False,full_pose_envelope_verified=False,
        scope='Sampled ideal three-support plane; spherical tire reach and ideal caster point. Not a continuous extremum proof or physical contact/suspension equilibrium. Stop access, spring loads, housing, tolerances and sensor mounts remain open.')


def study(g,d):
    w=d['wheel'];poses=[]
    for delta in (-w['droop_candidate_mm'],0,w['bump_mm']):
        p=pose(d,delta);box=moving_box(d,w['motor_reference_min_mm'],w['motor_reference_size_mm'],delta)
        sy,sz=rotate_yz(d,w['pivot_yz_mm'][0]-w['spring_lever_mm'],w['spring_seat_z_mm'],delta)
        p.update(motor_box=box,motor_to_cap_mm=w['cap_bottom_z_mm']-base.hi(box)[2],spring_length_mm=w['spring_top_z_mm']-sz,
                 spring_seat_y_mm=sy,fore_aft_shift_mm=p['axle_y_mm']-w['axle_yz_mm'][0])
        poses.append(p)
    removed=sum(g['hardware'][id]['mass_g'][1] for id in d['carrier']['removed_if_closed'])
    part_list=stock(d);subtotal=sum(p['mass_g'] for p in part_list)
    traction=g['traction'];limits=d['motor_load_guidance'];kgf_cm=base.G/100
    continuous=min(traction['stall_torque_nm']*traction['continuous_torque_fraction_of_stall'],limits['continuous_kgf_cm']*kgf_cm)
    return dict(revision=d['revision'],config=d,poses=poses,pivot=pivot_screen(d),caster=caster_screen(d),
        stock=part_list,gross_candidate_stock_g=subtotal,conditional_removed_carrier_g=removed,
        mass_accounting=dict(G_retained=True,bottom_frame_g=g['hardware']['bottom_frame']['mass_g'][1],
            pod_pair_g=2*g['hardware']['pod']['mass_g'][1],caster_installation_g=g['hardware']['caster']['mass_g'][1],
            note='Candidate stock covers only part of these assemblies; no subtraction/addition to complete G mass until joints, moving pods and retainers close.'),
        ground={bottom:dict(mass_g=base.assembly(g,bottom)['mass_g'],stock_conflicts=stock_conflicts(g,d,bottom),
            candidate_stock_overlaps=[a['id']+' / '+b['id'] for a,b in itertools.combinations(stock(d,bottom),2) if base.overlap(a,b)],
            loads=static_wheel_loads(g,d,bottom)) for bottom in ('vacuum','mop','low')},
        height=dict(G_nominal_mm=179.1,parallel_droop_probe_mm=179.1+w['droop_candidate_mm'],limit_mm=g['limits']['body_mm'][2],
            droop_adopted=False,full_pose_envelope_verified=False,
            note='Parallel lift is a clearance probe, not solved caster-constrained chassis attitude; nominal G fit cannot certify suspension travel.'),
        support_height_screen=height_screen(g,d),
        torque=dict(old_fraction_screen_nm=traction['stall_torque_nm']*traction['continuous_torque_fraction_of_stall'],
            gearbox_continuous_nm=limits['continuous_kgf_cm']*kgf_cm,continuous_screen_nm=continuous,
            gearbox_intermittent_nm=limits['intermittent_kgf_cm']*kgf_cm,
            continuous_current_screen_a=traction['stall_current_a']*limits['continuous_stall_current_fraction'],
            burst_current_setting_a=traction['current_limit_a'],
            note='2 A is a short-duration current setting, not continuous permission; apply motor temperature/duty limits as well.'),
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [ROOT/'config/system_design.json',ROOT/'config/core_partition.json',ROOT/'config/frame_joints.json',ROOT/'config/floor_support.json']},
        fabrication_release=False,flight_qualified=False)


def report(r):
    d=r['config'];w=d['wheel'];s=r['caster'];p=r['pivot'];t=r['torque']
    lines=['# H — wheel pivots and rear support','',
        '**Candidate mechanisms, with open integration gates. G remains the complete layout/mass baseline.** This pass adds load and travel checks; it does not release prints or claim a lighter robot.','',
        '## Wheel mechanism','',
        'Use a 40 mm leading arm with its pivot behind the axle. The proposed axle moves 3 mm forward to y=105; pivot y=145, z=36. This gives room for 6 mm pivot holes and rear edge material ahead of the mop drive at y=155. It corrects the earlier “trailing pod” terminology. The two motors, hubs and 72 mm wheels remain the same candidates.','',
        'Each fixed hanger has two 3 × 22 × 36 mm cheek blanks and an 80 × 45 × 3 mm roof plate at z=62–65. A smooth 6 mm pin runs through the cheeks, with two 6 mm-ID / 8 mm-OD / 8 mm-long bushings in moving ears. Retain both pin ends mechanically; threads do not run inside bushings. The roof needs both outer and inner rail support. Printed moving ears locate replaceable bushings; a metal motor-face bracket and under-motor tray carry motor loads. Their final shape, spring cups, stop fingers and attachment hardware remain to detail.','',
        'The proposed roof stays below the battery pocket. A compression spring sits 16 mm forward of the pivot, beside/behind the motor, with a pivoting lower seat. A separate compression stop acts 32 mm forward of the pivot; the spring must not be the travel stop. Two wheel-drop switches remain in the sensor budget.','',
        '| Wheel travel | Arm angle | Axle moves rearward | Motor-envelope gap below roof | Spring seat spacing |',
        '|---|---:|---:|---:|---:|']
    for x in r['poses']:lines.append(f"| {x['travel_mm']:+.1f} mm | {x['angle_deg']:+.2f}° | {x['fore_aft_shift_mm']:.3f} mm | {x['motor_to_cap_mm']:.2f} mm | {x['spring_length_mm']:.2f} mm |")
    lines += ['', 'Positive travel is bump; negative travel is droop. Rotating the full rectangular motor envelope is conservative relative to its cylindrical body, but does not include a qualified cable bend radius, bracket, screw-head or spring-seat envelope.','',
        'At a 0.4 spring-to-wheel motion ratio, the earlier 0.8 N/mm wheel rate requires approximately **5 N/mm at the spring**, not a 0.8 N/mm spring. Target OD ≤10 mm and solid height ≤18 mm, leaving at least 2 mm before coil bind at full bump in the reference geometry. Preload varies by module and must be set with its assembled load. No spring SKU is approved by this target.','',
        '| Bottom | Left normal load | Right normal load | Preload compression, left/right |', '|---|---:|---:|---|']
    for bottom,g in r['ground'].items():
        v=g['loads'];fmt=lambda values:f'{values[0]:.1f}–{values[1]:.1f}'
        lines.append(f"| {bottom} | {fmt(v['support_force_ranges_n'][0])} N | {fmt(v['support_force_ranges_n'][1])} N | {fmt(v['spring_preload_compression_mm'][0])} / {fmt(v['spring_preload_compression_mm'][1])} mm |")
    lines += ['', 'These are nominal G mass/CG calculations over caster heading, with the proposed contact position. They exclude mass uncertainty, cleaning-head support, asymmetric obstacles and the small CG change from moving the wheel assemblies. Spring procurement also needs free length, tolerances, fatigue and guided buckling checks.','',
        '## Pivot and impact load path','',
        'Wheel → motor bracket/moving tray → bushed ears and compression stop → fixed cheeks/roof → inner and outer rails → metal module-seat joints. The latter joints are not completed by this study. The motor output shaft remains another unqualified link; a stronger suspension pin does not establish the motor shaft’s radial-load capacity.','',
        f"Screen one wheel at 150 N vertical and 25 N fore/aft, with {w['spring_force_at_impact_n']} N spring force at bump. Moment balance about the suspension pivot requires **{p['hard_stop_force_n']:.1f} N** at the separate stop. Include this force when calculating pivot reactions; treating the pin as carrying only the wheel's vertical load misses the stop moment. These are engineering load cases, not a verified impact spectrum.",'',
        '| Pin diameter | Bending bound | Mean shear bound | Project screen |','|---|---:|---:|---|']
    for x in p['screens']:lines.append(f"| {x['diameter_mm']} mm | {x['bending_mpa']:.1f} MPa | {x['shear_mpa']:.1f} MPa | {'Pass' if x['passes'] else 'Fail'} |")
    lines += ['',f"The selected 6 mm pin gives a projected bushing-pressure screen of {p['max_projected_bushing_pressure_mpa']:.1f} MPa. Select an actual bushing material and rated pin grade for this pressure and oscillatory duty. The 150 MPa steel bending / 90 MPa shear limits are declared screening assumptions. Retaining hardware, fatigue, printed-ear creep, roof-plate joints and stop contact still need verification.",'',
        '## Rear caster saddle','',
        'Use a flat 40 × 44 × 3 mm aluminum plate, ending at a rear crossbar at y=266. A 40 mm-wide downward tab in that crossbar provides the rear attachment zone. Connect the plate with bolted stock angles, using flush underside screw heads; CAD shows the plate and tab, not completed angle joints. No sheet-metal brake or milled channel is required. The vacuum/mop saddle is centred at x=137.5; the sofa saddle moves to x=230. Reserve 5 mm above the plate for the stem retainer/washer/thread stack. No additional caster is added.','',
        f"For the flat plate, I={s['section']['inertia_mm4']:.1f} mm⁴. A 100 N vertical load at a 34 mm cantilever plus the adverse 25 N horizontal load applied 50.5 mm below the plate gives **{s['stress_mpa']:.1f} MPa** bending and **{s['deflection_mm']:.3f} mm** deflection. This assumes rigid attachment; it excludes stem-hole concentration, torsion, fastener slip, countersink effects and wear.",'',
        'The TENTE L51-8 is supplied with a blind fitting bore. Its separate retained fitting has to be specified; bare caster height is not installed mounting height. The manufacturer fitting table lists several stem families with different added heights. Do not substitute a generic M8 bolt or infer retention strength from the rolling load rating.','',
        '| Added fitting height | Top including 5 mm retainer reserve | Gap below vacuum/mop bin | Gap below sofa blower |','|---|---:|---:|---:|']
    for x in s['fitting_cases']:lines.append(f"| {x['fitting_height_mm']:.1f} mm | {x['saddle_top_mm']:.1f} mm | {x['vacuum_mop_gap_mm']:.1f} mm | {x['low_gap_mm']:.1f} mm |")
    lines += ['', 'The 2.5 mm case used in the reference CAD has only 1 mm beneath the vacuum/mop allocation. It is conditional on the actual fitting and fastener stack. A 5 mm fitting fails that space. Stem retention under lifting, access to its fastener and a supplier drawing are still required.','',
        '## Power shelf and frame integration','',
        'The proposed front bridge, two outer rails and two inner rails provide routes from the shelf to the fixed wheel hangers. The left rail also stiffens the shelf’s left edge; a separate 2 × 70 × 8 mm rib supports its right edge. The rear crossbar carries the caster saddle. Keep power electronics on these fixed members, with strain-relieved wiring to the moving motors.','',
        f"Candidate aluminum blanks total **{r['gross_candidate_stock_g']:.1f} g**, before their joint hardware and the rest of the chassis. The six F post/foot/tab items that could be removed total **{r['conditional_removed_carrier_g']:.1f} g**. Comparing those numbers alone is misleading: some candidates replace part of the existing 225 g bottom-frame and 112 g installed-caster allowances. The full old allowances, two 62 g pod allowances and F carrier remain in G until every replacement is accounted for. No mass saving is credited.",'',
        'External allocation audit (own old pod/caster allocations and the six replacement items excluded):','']
    for bottom,g in r['ground'].items():lines.append('- '+bottom+': '+('; '.join(g['stock_conflicts']) or 'no external stock-route overlap in this check')+'.')
    lines += ['', 'This audit is not an all-parts interference pass: contact/fastening between candidate plates, curved wheel cavity clearance, screws, moving trays and cable flex are unresolved. Close those joints and the rear/side connections to all four module studs before generating an installed H mass or deleting the F carrier.','',
        '## Two requirements corrected by this pass','',
        f"**Height:** G's 179.1 mm result is a nominal pose. The ideal three-support calculation samples {r['support_height_screen']['sampled_support_poses']} combinations of wheel travel and caster heading. Its highest case is **{max(v['max_height_mm'] for v in r['support_height_screen']['cases'].values()):.1f} mm**, above 180 mm. This already fails the screen; no physical contact model or tolerance refinement can be assumed to fix it. Keep droop unadopted until sensor/cap placement and suspension attitudes are resolved. Do not reduce suspension performance silently to preserve the old fit claim. The calculation bounds tilted wheel-disk reach with a sphere and treats the caster as an ideal support point; it is not a continuous extrema proof or equilibrium solution.",'',
        f"**Continuous drive load:** Pololu's published gearbox guidance is 4 kgf·cm continuous and 8 kgf·cm intermittent. The continuous screen is therefore **{t['continuous_screen_nm']:.3f} N·m**, below the old {t['old_fraction_screen_nm']:.3f} N·m fraction-of-stall estimate. The general motor-current guidance gives {t['continuous_current_screen_a']:.2f} A at 25% of 5 A stall; the existing 2 A setting must be treated as a bounded transient setting. Motor thermal duty and gearbox guidance both apply. Nothing in this study establishes wet-threshold performance.",'',
        '## Next detail release','',
        'Finish the moving motor tray, positive stops and roof-to-rail fasteners; obtain a dimensional drawing for the retained caster fitting; solve the full suspension height envelope. Then close the rear/side/module-seat joints and replace the old frame/carrier allowances with the complete ledger. No purchases or printing are needed for this review.','',
        '[Motor guidance]('+d['sources']['motor']+') · [Motor drawing]('+d['sources']['motor_drawing']+') · [Caster]('+d['sources']['caster']+') · [Fitting table]('+d['sources']['caster_fittings']+')','',
        '[Interactive mechanism](floor_support.html) · [Hardware blanks](floor_support_stock.csv) · [FreeCAD](floor_support.FCStd) · [Verification](floor_support_validation.md)']
    return '\n'.join(lines)+'\n'


def main():
    r=study(baseline(),read());OUT.mkdir(exist_ok=True,parents=True)
    (OUT/'floor_support.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'floor_support.md').write_text(report(r))
    template=(ROOT/'design/system/floor_support_viewer.html').read_text()
    (OUT/'floor_support.html').write_text(template.replace('__DATA__',json.dumps(r)))
    with (OUT/'floor_support_stock.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['id','role','x_mm','y_mm','z_mm','width_mm','depth_mm','height_mm','gross_mass_g','status'])
        for p in r['stock']:writer.writerow([p['id'],p['role'],*p['min'],*p['size'],round(p['mass_g'],3),'candidate blank; not an installed BOM'])
    print(json.dumps({k:r[k] for k in ('gross_candidate_stock_g','conditional_removed_carrier_g','pivot','caster','height','torque')},indent=2))


if __name__=='__main__':main()
