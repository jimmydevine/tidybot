"""N: a complete local fixed-mount mass scope, with explicit terrain limits.

No baseline is modified. Stock volume is conservative (holes not deducted).
The support-plane model samples adjacent horizontal levels, not step impact,
tire deformation, caster swivel dynamics or a continuous collision-free path.
"""
import csv
import itertools
import json
import math
from pathlib import Path
import build as B
import floating_heads as M
import suspension_springs as L

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/fixed_drive.json').read_text())


def stock_rows(d):
    a=d['angle'];b=d['beam'];c=d['cleat'];rho=d['material']['aluminum_g_mm3']
    w,t,r=a['width'],a['wall'],a['inside_radius'];dy=a['y_back']-a['y_front'];dz=a['z_top']-a['z_bottom']
    av=w*(t*(dy+dz-t)+r*r*(1-math.pi/4))
    length,by,bz=b['size'];t=b['wall'];bv=length*(by*bz-(by-2*t)*(bz-2*t))
    cv=c['length']*(2*c['leg']*c['wall']-c['wall']**2+c['inside_radius']**2*(1-math.pi/4))
    rows=[]
    def add(id,qty,m,xyz,basis):rows.append(dict(id=id,qty=qty,each_g=m,mass_g=qty*m,cg_mm=xyz,basis=basis))
    add('motor_support_angles',2,av*rho,[137.5,119,37],'6061 angle volume including inside radius; holes/end radii not deducted')
    add('common_crossmember',1,bv*rho,[137.5,136.35,58.65],'6063 square tube volume; holes not deducted')
    add('rail_cleats',2,cv*rho,[137.5,141,69],'Small-angle section; actual corner radius and SKU pending')
    add('Pololu_2676_brackets',2,8.5,[137.5,105,29],'Catalog mass, preserved motor/shaft position')
    # Conservative complete fastener budgets, not CAD screw-thread volumes.
    for id,qty,m,xyz in [
        ('motor_M3x6_flush_screws',4,.55,[137.5,105,36]),
        ('foot_M3x12_screw_washer_locknut_sets',8,1.9,[137.5,105,21.5]),
        ('support_M4x25_screw_washers_locknut_sets',4,4.2,[137.5,136,58.65]),
        ('beam_M4x25_screw_washers_locknut_sets',2,4,[137.5,136.35,63]),
        ('rail_M4x12_screw_washers_locknut_sets',4,2.7,[137.5,141,74.5])]:
        add(id,qty,m,xyz,'Installed fastener allowance including washer(s) and locking nut; verify selected SKU mass/grip')
    sleeve_area=math.pi/4*(6**2-4.3**2)
    add('beam_horizontal_compression_sleeves',4,sleeve_area*(by-2*t)*d['material']['steel_g_mm3'],[137.5,136.35,58.65],'Steel OD6/ID4.3 tube, inner beam width; nominal length 9.4996 mm')
    add('beam_vertical_compression_sleeves',2,sleeve_area*(bz-2*t)*d['material']['steel_g_mm3'],[137.5,136.35,58.65],'Steel OD6/ID4.3 tube, inner beam height; nominal length 9.4996 mm')
    add('completion_reserve',1,d['completion_reserve_g'],[137.5,130,50],'Local finish/tolerance/retention contingency; not an extra head budget')
    return rows


def rigid_plane(heights,caster,radius=36):
    """Gravity/floor-up vector in body coordinates and plane constant.

    Wheel supports are spherical-radius approximations at [14/261,105,36].
    Their world contact heights are n.dot(axis)-radius-c. The rear caster's
    nominal contact is body z=0. Solve the normalized normal rather than
    incorrectly treating three wheel axle centres as equal-height contacts.
    """
    hl,hr,hc=heights;cx,cy=caster[:2];nx=(hr-hl)/247
    ny=0.
    for _ in range(30):
        nz=math.sqrt(1-nx*nx-ny*ny)
        f=nx*(14-cx)+ny*(105-cy)+radius*nz-radius-hl+hc
        delta=f/((105-cy)-radius*ny/nz)
        ny-=delta
        if abs(delta)<1e-13:break
    else:raise ValueError('Support plane failed to converge')
    nz=math.sqrt(1-nx*nx-ny*ny)
    return [nx,ny,nz],nx*cx+ny*cy-hc


def sharp_step_lever(radius,height):
    if not 0<=height<radius:raise ValueError('Step model needs 0 <= h < radius')
    return math.sqrt(2*radius*height-height*height)


def head_pose(reference,normal,c,ground_height):
    nx,ny,nz=normal;x,y,_=reference
    return dict(q_mm=(ground_height+c-nx*x-ny*y)/nz,
        pitch_deg=math.degrees(math.atan2(ny,nz)),roll_deg=math.degrees(math.atan2(nx,nz)))


def beam_bending(span,positions,forces,ei,couples=None):
    """Simply supported beam, exact point loads; downward deflection negative."""
    couples=couples or [0]*len(positions)
    right=(sum(p*f for p,f in zip(positions,forces))+sum(couples))/span
    left=sum(forces)-right
    def displacement_numerator(x):return left*x**3/6-sum(f*max(0,x-p)**3/6 for p,f in zip(positions,forces))+sum(c*max(0,x-p)**2/2 for p,c in zip(positions,couples))
    c1=-displacement_numerator(span)/span
    samples=[i*span/1000 for i in range(1001)]
    def moment(x):return left*x-sum(f*max(0,x-p) for p,f in zip(positions,forces))+sum(c for p,c in zip(positions,couples) if x>=p)
    return dict(reactions_n=[left,right],max_moment_nmm=max(abs(moment(x)) for x in [0,span,*positions,*[p-1e-8 for p in positions]]),
        max_deflection_mm=max(abs((displacement_numerator(x)+c1*x)/ei) for x in samples))


def beam_torsion(span,positions,torques,gj):
    """Both end rotations fixed; no claim that the candidate joints achieve it."""
    reaction=-sum(t*(span-p) for t,p in zip(torques,positions))/span
    stops=[0,*positions,span]
    internal=[reaction+sum(t for t,p in zip(torques,positions) if p<(x+y)/2) for x,y in zip(stops,stops[1:])]
    angles=[(reaction*x+sum(t*max(0,x-p) for t,p in zip(torques,positions)))/gj for x in stops]
    return dict(max_torque_nmm=max(abs(v) for v in internal),max_twist_deg=math.degrees(max(abs(v) for v in angles)),end_rotations_rad=[angles[0],angles[-1]])


def structural_screen(d):
    a=d['angle'];b=d['beam'];l=d['loads'];mat=d['material']
    f=l['vertical_n'];fy=l['fore_aft_n'];t=a['wall'];lever=a['y_back']-t-105
    moment=f*lever+fy*(58.65-36)
    # Wheel is outboard of the two foot-bolt X columns. Preserve this couple;
    # applying only 150 N at the bracket centroid hides its larger local load.
    outer=f*(65.25-14)/(65.25-39.85)
    inner=f-outer
    section=(a['width']/2)*t*t/6*l['section_hole_factor']
    local_moment=outer*lever+(outer/f)*fy*(58.65-36)
    sigma=local_moment/section
    length,by,bz=b['size'];t=b['wall'];k=l['section_hole_factor']
    iy=(by*bz**3-(by-2*t)*(bz-2*t)**3)/12*k
    iz=(bz*by**3-(bz-2*t)*(by-2*t)**3)/12*k
    bm,hm=by-t,bz-t;j=4*(bm*hm)**2/(2*(bm+hm)/t)*k
    # Use actual mount locations. Loading the centre of this beam describes
    # neither wheel. Include either/both wheels and both fore-aft directions.
    span=238.5-36.5;positions=[55.5-36.5,219.5-36.5]
    vertical=[beam_bending(span,positions,loads,mat['e_mpa']*iy,[-41.5*loads[0],41.5*loads[1]]) for loads in [(f,0),(0,f),(f,f)]]
    horizontal=[beam_bending(span,positions,loads,mat['e_mpa']*iz,[-41.5*loads[0],41.5*loads[1]]) for loads in [(fy,fy),(fy,-fy),(-fy,fy)]]
    torsion=[beam_torsion(span,positions,loads,mat['g_mpa']*j) for loads in [(moment,0),(0,moment),(moment,moment),(moment,-moment)]]
    bending=max(v['max_moment_nmm'] for v in vertical)*bz/2/iy+max(v['max_moment_nmm'] for v in horizontal)*by/2/iz
    torque=max(v['max_torque_nmm'] for v in torsion)
    shear=torque/(2*bm*hm*t*k)
    vm=math.sqrt(bending*bending+3*shear*shear)
    deflection=max(v['max_deflection_mm'] for v in vertical)
    twist=max(v['max_twist_deg'] for v in torsion)
    area=a['width']*bz;zface=a['width']*bz*bz/6
    clamp=2*l['bolt_preload_n_each'];pmin=clamp/area-moment/zface
    return dict(local_angle_moment_nmm=local_moment,foot_column_reactions_n=[outer,inner],angle_stress_mpa=sigma,
        angle_screen_mpa=mat['angle_bending_screen_mpa'],angle_screen_pass=sigma<mat['angle_bending_screen_mpa'],
        beam_I_vertical_mm4=iy,beam_J_mm4=j,beam_combined_stress_mpa=vm,
        beam_screen_mpa=mat['tube_bending_screen_mpa'],beam_screen_pass=vm<mat['tube_bending_screen_mpa'],
        beam_deflection_bound_mm=deflection,beam_twist_bound_deg=twist,
        support_joint_min_face_pressure_mpa=pmin,
        support_joint_friction_margin_n=clamp*l['friction_assumption']-math.hypot(f,fy),
        scope='Factored 150 N vertical and +/-25 N fore-aft per wheel, as H/K. Beam load application X55.5/219.5 plus couples from the 41.5 mm outboard wheel offset, supports X36.5/238.5; 25% section reduction for holes. Torsion assumes both ends rotationally restrained, which the cleat/rail joints still need to demonstrate. Local bracket strip and tube screens only; no motor-bearing rating, fatigue or complete joint qualification. Clamp/friction values are assumptions, not torque instructions.')


def nominal_mass(bottom,d):
    p=M.prepare(bottom);items=[p['fixed'],*p['moving'],*p['head_items']]
    old=[]
    for row in B.assembly(p['layout'],bottom,payload=False)['rows']:
        if row['hardware_id']=='pod':old.append((row['mass_g'][1],row['cg_mm']))
    rows=stock_rows(d);items.extend((-m,pos) for m,pos in old)
    items.extend((r['mass_g'],r['cg_mm']) for r in rows)
    loads=p['config']['contents'][bottom][p['config']['calibration_contents_index'][bottom]]['loads']
    fixed,water=M.split_contents(p,loads)
    items.extend((v[0],v[1:]) for v in [*fixed,*water])
    mass,cg=L.weighted(items)
    baseline=p['dry_mass_g']+sum(v[0] for v in loads)
    assert abs(mass-(baseline-sum(m for m,pos in old)+sum(r['mass_g'] for r in rows)))<1e-7
    return p,dict(mass_g=mass,cg_mm=cg,M_mass_g=baseline,removed_pods_g=sum(m for m,pos in old),
        replacement_g=sum(r['mass_g'] for r in rows),potential_saving_g=baseline-mass)


def terrain(bottom,p,a,d):
    rows=[];t=p['layout']['traction'];ref=p['M']['modules'][bottom]['reference_mm']
    points=[[14,105,36],[261,105,36]]
    loads=p['config']['contents'][bottom][p['config']['calibration_contents_index'][bottom]]['loads']
    _,water=M.split_contents(p,loads)
    head_nominal=[*p['head_items'],*[(v[0],v[1:]) for v in water]]
    # Plausible limiting support states plus isolated head/threshold contact.
    # Mixed terrain under the finite-sized head itself still needs a sweep.
    for h in [0,*d['terrain_heights_mm']]:
        states=[('level',[0,0,0],0)] if h==0 else [
            ('head meets step',[0,0,0],h),
            ('both drive wheels up',[h,h,0],h if bottom=='vacuum' else 0),
            ('left wheel up',[h,0,0],0),('right wheel up',[0,h,0],0),
            ('rear caster up',[0,0,h],0),('all up',[h,h,h],h)]
        for heading in d['caster_headings_deg']:
            ang=math.radians(heading);caster=[137.5+t['caster_trail_mm']*math.cos(ang),232+t['caster_trail_mm']*math.sin(ang),0]
            for name,heights,hh in states:
                n,c=rigid_plane(heights,caster);hp=head_pose(ref,n,c,hh)
                contact=p['M']['modules'][bottom]['target_contact_n']
                tool=[ref[0],ref[1],hp['q_mm']]
                moved=M.place_head(p,hp['q_mm'],n,water)
                _,cg=L.weighted([(a['mass_g'],a['cg_mm']),*[(-m,pos) for m,pos in head_nominal],*moved])
                forces=L.reactions([*points,caster],cg,a['mass_g']/1000*B.G,n,contact,tool)
                old=p['M'];compatible=old['working_travel_mm'][0]<=hp['q_mm']<=old['working_travel_mm'][1] and max(abs(hp['pitch_deg']),abs(hp['roll_deg']))<=old['tilt_limit_deg']
                rows.append(dict(bottom=bottom,state=name,step_mm=h,heading_deg=heading,
                    heights_mm=heights,head_ground_mm=hh,normal=n,plane_constant=c,**hp,
                    cg_mm=cg,support_n=forces,M_head_motion_compatible=compatible))
    return rows


def traction(bottom,p,a,d):
    t=p['layout']['traction'];weight=a['mass_g']/1000*B.G
    currents=t['stall_torque_nm']*(t['current_limit_a']-t['no_load_current_a'])/(t['stall_current_a']-t['no_load_current_a'])
    continuous=min(4*B.G/100, t['stall_torque_nm']*(.25*t['stall_current_a']-t['no_load_current_a'])/(t['stall_current_a']-t['no_load_current_a']))
    out=[]
    # Raised tool is the conservative load case for getting across an edge.
    for h in (4,10):
        for heading in d['caster_headings_deg']:
            angle=math.radians(heading);caster=[137.5+15.5*math.cos(angle),232+15.5*math.sin(angle),0]
            forces=L.reactions([[14,105,36],[261,105,36],caster],a['cg_mm'],weight,[0,0,1])
            torque=max(forces[:2])*sharp_step_lever(36,h)/1000
            push=forces[2]*sharp_step_lever(25,h)/(25-h)
            mu=(push+weight*t['rolling_coefficient'])/sum(forces[:2])
            out.append(dict(step_mm=h,heading_deg=heading,wheel_torque_nm=torque,
                caster_push_n=push,minimum_mu_during_caster_climb=mu))
    drag=t['mop_drag_n'] if bottom=='mop' else 1.5
    ft=weight*t['rolling_coefficient']+a['mass_g']/1000*t['acceleration_m_s2']+drag
    # CG target is a sensitivity requirement, not a new tank design. Take
    # shortest wheel-to-caster distance over headings and keep the head raised.
    sensitivity=[]
    for mu in t['wet_friction_sensitivity']:
        fc=(mu-t['rolling_coefficient'])/(sharp_step_lever(25,10)/(25-10)+mu)
        sensitivity.append(dict(mu=mu,max_caster_weight_fraction=fc,
            max_cg_y_mm=105+fc*(232-15.5-105),
            required_forward_cg_shift_mm=max(0,a['cg_mm'][1]-(105+fc*(232-15.5-105)))))
    return dict(continuous_torque_screen_nm=continuous,intermittent_gearbox_screen_nm=8*B.G/100,
        current_limited_torque_nm=currents,flat_torque_nm_each=ft*.036/2,
        thresholds=out,cg_targets=sensitivity,scope='Quasistatic initiation at a sharp edge from level ground with head raised. Uses worst individual wheel load, not an assumed equal split. No impact, tire compliance or edge-friction model. Caster-climb mu is a requirement, not a measured tire property; 0.2/0.35/0.5 remain sensitivity cases.')


def study():
    d=read();out=dict(config=d,stock=stock_rows(d),structure=structural_screen(d),modules={})
    for b in ('vacuum','mop'):
        p,a=nominal_mass(b,d);poses=terrain(b,p,a,d)
        a.update(terrain=poses,traction=traction(b,p,a,d),
            q_range_mm=[min(v['q_mm'] for v in poses),max(v['q_mm'] for v in poses)],
            max_pitch_deg=max(abs(v['pitch_deg']) for v in poses),
            max_roll_deg=max(abs(v['roll_deg']) for v in poses),
            min_support_n=min(min(v['support_n']) for v in poses),
            head_motion_fail_count=sum(not v['M_head_motion_compatible'] for v in poses))
        out['modules'][b]=a
    return out


def report(r):
    rows=['# Fixed drive-mount comparison — N','','This is a lighter construction candidate, not an adopted drivetrain. Removing independent wheel suspension transfers floor-following requirements to the cleaning head. M cannot be carried forward unchanged.','',
        '| Complete carried assembly | M | N comparison | Potential reduction |','|---|---:|---:|---:|']
    for b,a in r['modules'].items():rows.append(f"| {b} | {a['M_mass_g']/1000:.3f} kg | {a['mass_g']/1000:.3f} kg | {a['potential_saving_g']:.1f} g |")
    rows+=['','Same battery, contents, cap, motors, wheels, caster, head mechanisms and frame budgets. The cap is included; the lift top is not. No head-mechanism savings or overlap credits are taken. The potential reduction remains conditional on head redesign and complete joint checks.','',
        '| Local replacement item | Count | Total |','|---|---:|---:|']
    for v in r['stock']:rows.append(f"| {v['id'].replace('_',' ')} | {v['qty']} | {v['mass_g']:.1f} g |")
    rows+=['','The 225 g bottom-frame budget remains. Nominal stock mass counts full sections, including the large-angle inside radius, without deducting holes. Fastener sets, compression sleeves and a 20 g completion reserve are explicit. Mass coordinates for stock/fasteners are approximate; CG is a planning value.','',
        '## Terrain consequence','','| Module | Required head translation in sampled states | Pitch | Roll | Minimum support reaction |','|---|---:|---:|---:|---:|']
    for b,a in r['modules'].items():rows.append(f"| {b} | {a['q_range_mm'][0]:.1f} to {a['q_range_mm'][1]:.1f} mm | {a['max_pitch_deg']:.2f}° | {a['max_roll_deg']:.2f}° | {a['min_support_n']:.1f} N |")
    rows+=['','M allows -2 to +10 mm translation and ±1.5° tilt. Its motion envelope fails the rigid-chassis comparison. These samples represent 4/10 mm horizontal levels and eight caster headings. A finite head straddling a vertical edge, backing down a step, body clearance, impact, wet traction and changing head spring/contact forces are not validated by positive support reactions.','',
        '## Drive and structure screens','']
    for b,a in r['modules'].items():
        tr=a['traction'];ten=[v for v in tr['thresholds'] if v['step_mm']==10]
        rows.append(f"- {b}: flat demand {tr['flat_torque_nm_each']:.3f} N·m per motor; conservative continuous screen {tr['continuous_torque_screen_nm']:.3f} N·m. At a 10 mm sharp edge, worst driven-wheel initiation torque {max(v['wheel_torque_nm'] for v in ten):.3f} N·m; caster-climb friction coefficient requirement up to {max(v['minimum_mu_during_caster_climb'] for v in ten):.2f}. Current-limited screen {tr['current_limited_torque_nm']:.3f} N·m; intermittent gearbox screen {tr['intermittent_gearbox_screen_nm']:.3f} N·m.")
    s=r['structure'];rows+=['',f"The retained 150 N vertical and ±25 N fore-aft per-wheel structural cases give {s['angle_stress_mpa']:.1f} MPa at the angle strip (120 MPa screen), and {s['beam_combined_stress_mpa']:.1f} MPa for the crossmember bound (55 MPa screen). Beam deflection bound {s['beam_deflection_bound_mm']:.3f} mm; twist bound {s['beam_twist_bound_deg']:.2f}°. These are local section checks, not complete mechanical qualification.",'',
        'The motor-to-beam joint screen assumes two 1,250 N bolt preloads and friction coefficient 0.15. It is not a tightening instruction. Beam bending includes the couples from the outboard wheel positions; torsion assumes rotational restraint at the ends. Cleats/rails, washer seating, tube-hole net sections, load transfer into the full chassis, motor radial loading, tolerances and fatigue remain to resolve.','',
        '## Decision and next work','','Continue with a passive, retained vacuum cassette sized for the calculated head motion, and compare its complete installed mass against M. Keep the rigid-mount option conditional until that cassette fits and wet 10 mm crossings have a credible traction margin. The current candidate reduces mass by about 230 g; it does not solve the whole-robot weight problem. Retain the previous suspension geometry as the fallback.','',
        f"The mop's nominal CG is Y={r['modules']['mop']['cg_mm'][1]:.1f} mm. At the illustrative wet friction coefficient 0.35, the caster-climb calculation requires Y ≤ {r['modules']['mop']['traction']['cg_targets'][1]['max_cg_y_mm']:.1f} mm: approximately {r['modules']['mop']['traction']['cg_targets'][1]['required_forward_cg_shift_mm']:.1f} mm forward. Investigate front-mounted water storage or a mop-specific axle location. This is a placement target, not a credited mass reduction or an assertion that those parts fit. Suspension alone does not remove a rear-heavy caster's climb load.",'',
        'No new order or print follows from this comparison. The metal pieces require cut stock, trimmed angle legs, drilled holes and deburring; precision compression spacers or supplier-cut spacers are needed. No mill/lathe is assumed. Confirm cutting capability or use supplier processing before fabrication.','',
        '## Sources','']
    for label,url in r['config']['sources'].items():rows.append(f'- [{label.replace("_"," ")}]({url})')
    rows+=['','[Geometry and limitations](../../../docs/FIXED_DRIVE_COMPARISON.md) · [Mass correction](../../../docs/MASS_OPTIMIZATION_REVIEW.md)']
    return '\n'.join(rows)+'\n'


def main():
    r=study();OUT.mkdir(exist_ok=True)
    (OUT/'fixed_drive.json').write_text(json.dumps(r,indent=2)+'\n')
    (OUT/'fixed_drive.md').write_text(report(r))
    template=ROOT/'design/system/fixed_drive_viewer.html'
    if template.exists():(OUT/'fixed_drive.html').write_text(template.read_text().replace('__MODEL__',json.dumps(r)))
    with (OUT/'fixed_drive_mass.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r['stock'][0]));w.writeheader();w.writerows(r['stock'])
    for b,a in r['modules'].items():print(b,round(a['mass_g'],1),'g; potential saving',round(a['potential_saving_g'],1),'g; head range',a['q_range_mm'],'pitch',a['max_pitch_deg'])
    print('structure',r['structure'])


if __name__=='__main__':main()
