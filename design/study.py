"""Reproducible envelope screening, not flight certification or fabrication geometry.

Robot frame: x forward/upstairs, y left, z up; ground contact plane z=0.
The site JSON uses metres; all geometry here is millimetres. Stdlib only.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs(root=ROOT):
    config = json.loads((root / 'config/concept.json').read_text())
    site = json.loads((root / config['site_profile']).read_text())
    with (root / 'config/components.csv').open(newline='') as stream:
        ledger = list(csv.DictReader(stream))
    for row in ledger:
        for key in ('qty', 'unit_mass_g', 'ground_w', 'flight_w', 'cost_low_usd', 'cost_high_usd'):
            row[key] = float(row[key])
    validate(config, site, ledger)
    return config, site, ledger


def validate(c, site, ledger):
    if site['length_unit'] != 'm':
        raise ValueError('Site length_unit must be m')
    for group, keys in ((c['body'], ['length_mm','width_mm','bottom_height_mm','core_height_mm']),
                        (c['station'], ['width_mm','depth_mm','height_mm'])):
        if any(not math.isfinite(group[k]) or group[k] <= 0 for k in keys):
            raise ValueError('Geometry must be positive and finite')
    if not 0 < c['screening']['guard_thrust_factor'] <= 1:
        raise ValueError('Invalid guard factor')
    if not 0 < c['screening']['usable_energy_fraction'] <= 1:
        raise ValueError('Invalid energy fraction')
    for row in ledger:
        if any(not math.isfinite(row[k]) or row[k] < 0 for k in
               ('qty','unit_mass_g','ground_w','flight_w','cost_low_usd','cost_high_usd')):
            raise ValueError(f'Invalid ledger row {row["id"]}')
    for p in c['propulsion'].values():
        curve = p['curve_thrust_g_power_w']
        if p['bench_voltage'] <= 0 or p['prop_diameter_mm'] <= 0:
            raise ValueError('Invalid propulsion reference')
        if any(t <= 0 or w <= 0 for t,w in curve) or any(
            b[0] <= a[0] or b[1] <= a[1] for a,b in zip(curve,curve[1:])):
            raise ValueError('Thrust/power curve must increase')


def box(name, group, center, size, color):
    return dict(name=name, group=group, center=list(center), size=list(size), color=color)


def packaging(c):
    """Purchasable component bounding boxes plus mounting allowances.

    Centers are editable in this source; body/variant dimensions live in JSON.
    Shells are keepouts, not solid plastic and are excluded from pair checks.
    """
    b = c['body']; z = b['bottom_height_mm']
    parts = [
        box('Battery + connector clearance','core',(0,-95,z+43),(175,55,57),'#f1b34b'),
        box('Compute + cooler','core',(-45,0,z+43),(95,70,35),'#5cbf9b'),
        box('Power electronics','core',(55,0,z+43),(80,55,35),'#e48b66'),
        box('LiDAR mounting envelope','core',(-55,95,z+51),(60,60,45),'#bd99e1'),
        box('Depth camera allowance','core',(45,95,z+60),(90,35,30),'#8fa9ef'),
        box('Bin/filter gross envelope','bottom',(0,0,65),(90,110,45),'#65accb'),
        box('Blower + hose allowance','bottom',(0,-98,60),(75,75,45),'#ecb86b'),
        box('Blower controller','bottom',(0,100,60),(50,35,15),'#d6a85d'),
        box('Roller envelope','bottom',(75,0,25),(45,200,45),'#67c2ad'),
        box('Roller motor','bottom',(75,115,40),(35,25,25),'#a1ceb8'),
        box('Floor control allowance','bottom',(-75,0,65),(35,90,15),'#899ec6'),
    ]
    for sign in (-1,1):
        parts.append(box(f'Drive motor {sign:+}','bottom',
                         (b['drive_x_mm'],sign*85,35),(25,82,25),'#98b1c1'))
    return parts


def bounds(part):
    return [(p-s/2,p+s/2) for p,s in zip(part['center'],part['size'])]


def overlap(a,b):
    """Positive-volume AABB overlap only; touching faces are not overlap."""
    return all(min(x[1],y[1])-max(x[0],y[0]) > 1e-7
               for x,y in zip(bounds(a),bounds(b)))


def packaging_checks(c):
    parts=packaging(c); b=c['body']; issues=[]
    for a,p in itertools.combinations(parts,2):
        if overlap(a,p): issues.append(f'{a["name"]} intersects {p["name"]}')
    for p in parts:
        limits=[(-b['length_mm']/2,b['length_mm']/2),(-b['width_mm']/2,b['width_mm']/2),
                (b['bottom_height_mm'],b['bottom_height_mm']+b['core_height_mm'])
                if p['group']=='core' else (0,b['bottom_height_mm'])]
        if any(lo < lim[0]-1e-7 or hi > lim[1]+1e-7 for (lo,hi),lim in zip(bounds(p),limits)):
            issues.append(f'{p["name"]} outside {p["group"]} envelope')
    return issues


def rotation(point,yaw=0,pitch=0,roll=0,pivot_z=0):
    x,y,z=point; z-=pivot_z
    a,b,d=map(math.radians,(roll,pitch,yaw))
    y,z=y*math.cos(a)-z*math.sin(a),y*math.sin(a)+z*math.cos(a)
    x,z=x*math.cos(b)+z*math.sin(b),-x*math.sin(b)+z*math.cos(b)
    x,y=x*math.cos(d)-y*math.sin(d),x*math.sin(d)+y*math.cos(d)
    return x,y,z+pivot_z


def body_points(c):
    b=c['body']
    points=list(itertools.product((-b['length_mm']/2,b['length_mm']/2),
               (-b['width_mm']/2,b['width_mm']/2),(10,b['bottom_height_mm']+b['core_height_mm'])))
    for side in (-1,1):
        for a in range(0,360,10):
            r=b['wheel_diameter_mm']/2
            for dy in (-b['wheel_width_mm']/2,b['wheel_width_mm']/2):
                points.append((b['drive_x_mm']+r*math.cos(math.radians(a)),
                               side*b['drive_track_mm']/2+dy,r+r*math.sin(math.radians(a))))
    return points


def rotor_points(c,v):
    r=c['propulsion'][v['propulsion']]['prop_diameter_mm']/2+c['screening']['guard_radial_allowance_mm']
    h=c['screening']['guard_half_height_mm']
    pts=[]
    # Closed, filled-cylinder envelope; center points capture top/bottom disks.
    # Angular discretization underestimation is bounded by r*(1-cos(2.5deg)).
    for sx,sy in itertools.product((-1,1),repeat=2):
        for dz in (-h,h):
            pts.append((sx*v['rotor_x_mm'],sy*v['rotor_y_mm'],v['rotor_plane_mm']+dz))
            for a in range(0,360,5):
                pts.append((sx*v['rotor_x_mm']+r*math.cos(math.radians(a)),
                            sy*v['rotor_y_mm']+r*math.sin(math.radians(a)),v['rotor_plane_mm']+dz))
    # Include horizontal arm/motor envelopes. In-body vertical supports are drawn
    # in the scene generator but are not separately collision-tested here.
    # Their construction and stiffness are not specified by these occupied volumes.
    for sx,sy in itertools.product((-1,1),repeat=2):
        for t in (i/20 for i in range(21)):
            for dx,dy,dz in itertools.product((-8,8),repeat=3):
                pts.append((sx*v['rotor_x_mm']*t+dx,sy*v['rotor_y_mm']*t+dy,v['rotor_plane_mm']-35+dz))
        for dx,dy,dz in itertools.product((-20,20),(-20,20),(-43,0)):
            pts.append((sx*v['rotor_x_mm']+dx,sy*v['rotor_y_mm']+dy,v['rotor_plane_mm']+dz))
    return pts


def stair_height(x,tread,rise):
    """Infinite interior straight flight, current tread centered at x=0,z=0.

    Treat a riser boundary as the higher tread. Used for interior-step screening;
    finite top/bottom transitions remain unknown site checks.
    """
    return math.floor((x+tread/2)/tread+1e-10)*rise


def curve_power(curve,thrust):
    if not curve[0][0] <= thrust <= curve[-1][0]:
        return None  # No extrapolation or invented hover point.
    for a,b in zip(curve,curve[1:]):
        if a[0] <= thrust <= b[0]:
            t=(thrust-a[0])/(b[0]-a[0])
            return a[1]+t*(b[1]-a[1])
    return curve[-1][1]


def mass_budget(c,ledger,v):
    by_group={}; high=0; low=0; total=0; zsum=0
    group_z={'core':c['body']['bottom_height_mm']+c['body']['core_height_mm']/2,
             'bottom':45,'lift':v['rotor_plane_mm']-20}
    for row in ledger:
        if row['section'] not in group_z: continue
        mass=row['qty']*(c['propulsion'][v['propulsion']]['motor_mass_g']
                         if row['id']=='lift_motors' else row['unit_mass_g'])
        total+=mass; by_group[row['section']]=by_group.get(row['section'],0)+mass
        # Sensitivity bounds, not statistical confidence intervals.
        frac=0.3 if row['mass_basis']=='estimate' else 0.05
        low+=mass*(1-frac); high+=mass*(1+frac); zsum+=mass*group_z[row['section']]
    return dict(total_g=total,low_g=low,high_g=high,by_group_g=by_group,cg_height_mm=zsum/total)


def support_margin(c,x=0,y=0):
    b=c['body']
    # CCW convex contact polygon: rear support, right drive, front support, left drive.
    poly=[(b['support_x_mm'][0],0),(b['drive_x_mm'],-b['drive_track_mm']/2),
          (b['support_x_mm'][1],0),(b['drive_x_mm'],b['drive_track_mm']/2)]
    return min(((q[0]-p[0])*(y-p[1])-(q[1]-p[1])*(x-p[0]))/math.dist(p,q)
               for p,q in zip(poly,poly[1:]+poly[:1]))


def screen_variant(c,site,ledger,v):
    s=c['screening']; b=c['body']; p=c['propulsion'][v['propulsion']]
    tread=site['staircase']['tread_depth']*1000; rise=site['staircase']['approx_riser_height']*1000
    r=p['prop_diameter_mm']/2+s['guard_radial_allowance_mm']; sample_error=r*(1-math.cos(math.radians(2.5)))
    mass=mass_budget(c,ledger,v); cg=mass['cg_height_mm']
    raw=rotor_points(c,v); body=body_points(c)
    yaw=s['yaw_error_deg']; tilt=s['pitch_roll_error_deg']; offset=s['landing_error_mm']
    maxwidth=0; maxlength=0; minclear=math.inf; minbodyedge=math.inf
    # Sample yaw/pitch/roll at 0 and both assumed bounds. This is NOT a swept-volume
    # proof between samples. A future CAD/trajectory checker must handle that.
    for ya,pi,ro in itertools.product((-yaw,0,yaw),(-tilt,0,tilt),(-tilt,0,tilt)):
        points=[rotation(q,ya,pi,ro,cg) for q in raw]
        # Symmetric route corridor about the body origin, so attitude-induced
        # lateral shifts of a high rotor plane are not silently recentered away.
        maxwidth=max(maxwidth,2*max(abs(q[1]) for q in points)+2*sample_error)
        maxlength=max(maxlength,2*max(abs(q[0]) for q in points)+2*sample_error)
        for dx in (-offset,0,offset):
            minclear=min(minclear,min(q[2]-stair_height(q[0]+dx+sample_error,tread,rise) for q in points)-sample_error)
    # Wheels must be level at contact. Check yaw/position errors independently of
    # the airborne rotor tilt envelope; claiming a landed five-degree roll is invalid.
    for ya in (-yaw,0,yaw):
        minbodyedge=min(minbodyedge,tread/2-max(abs(rotation(q,ya)[0]) for q in body)-offset)
    combined_width=site['staircase']['tread_width']*1000-sum(o['inward_projection']*1000 for o in site['staircase']['side_obstacles'])
    projection_gap=math.hypot(max(v['rotor_x_mm']-b['length_mm']/2,0),
                              max(v['rotor_y_mm']-b['width_mm']/2,0))-r
    rotor_gap=min(2*v['rotor_x_mm'],2*v['rotor_y_mm'])-2*r
    contactedge=tread/2-max(abs(x) for x in [*b['support_x_mm'],b['drive_x_mm']])-offset-b['contact_patch_radius_mm']
    cg_margin=support_margin(c)-s['cg_horizontal_uncertainty_mm']-cg*math.tan(math.radians(tilt))
    factor=s['guard_thrust_factor']; maxt=p['curve_thrust_g_power_w'][-1][0]*4
    vfactor=min(1,(s['minimum_flight_voltage_assumption']/p['bench_voltage'])**2)
    bench_ratio=maxt*factor/mass['total_g']; sensitive_ratio=bench_ratio*vfactor
    hpower=curve_power(p['curve_thrust_g_power_w'],mass['total_g']/(4*factor))
    shared=sum(row['qty']*row['flight_w'] for row in ledger if row['section'] in ('core','bottom','lift'))
    hover=None if hpower is None else 4*hpower+shared
    energy=c['battery']['capacity_ah']*c['battery']['nominal_voltage']
    reserved=None if hover is None else hover*s['reserved_flight_seconds']/3600
    ground=sum(row['qty']*row['ground_w'] for row in ledger if row['section'] in ('core','bottom','cap'))
    floor_runtime=None if reserved is None else max(0,energy*s['usable_energy_fraction']-reserved)/ground*60
    st=c['station']; length=2*(v['rotor_x_mm']+r); width=2*(v['rotor_y_mm']+r)
    interface=b['bottom_height_mm']+b['core_height_mm']
    park_top=st['top_park_interface_z_mm']+v['rotor_plane_mm']+s['guard_half_height_mm']-interface
    checks=[]
    def add(name,margin,detail):
        checks.append(dict(name=name,status='PASS_MODEL' if margin>=0 else 'FAIL_MODEL',margin_mm=round(margin,2),detail=detail))
    add('Component boxes',0 if not packaging_checks(c) else -1,'; '.join(packaging_checks(c)) or 'No modeled component-box overlaps; no cables/duct routing or mounting design proof.')
    add('Guard-to-guard separation',rotor_gap,'Level rotor cylinders; complete guard construction remains unresolved.')
    add('Guard clear of core projection',projection_gap,'Plan-view separation only; does not estimate aerodynamic interference.')
    add('Lift arm height above core',v['rotor_plane_mm']-35-8-interface,'Lowest horizontal arm envelope above core; low layouts may intrude into electronics.')
    add('Landed body/tire tread edges',minbodyedge-s['collision_margin_mm'],'Level contact with sampled yaw and +/- landing offset; includes wheel outline.')
    add('Support contacts on tread',contactedge,'Fore-aft bounds only; compliant support engagement must be demonstrated.')
    add('CG inside contact polygon',cg_margin,'Centered CG with assumed horizontal uncertainty and tilt sensitivity; heights are group estimates.')
    add('Rotors above uphill steps',minclear-s['collision_margin_mm'],'27 attitude samples and position offsets; guards, motors and arms; interior steps only.')
    add('Combined rail projection screen',combined_width-maxwidth-2*s['lateral_margin_each_mm'],'Conservative width gate; actual rail cross-sections/heights are not modeled as obstacles.')
    add('Station straight entry/parking width',st['width_mm']-2*st['structure_allowance_mm']-width-2*st['tool_handling_margin_mm'],'Level, aligned entry; external doorway approach remains unknown.')
    add('Station straight entry/parking depth',min(st['dock_x_mm']-length/2-st['structure_allowance_mm'],st['depth_mm']-st['structure_allowance_mm']-st['dock_x_mm']-length/2)-st['tool_handling_margin_mm'],'Both front and rear ends contained during aligned vertical top removal.')
    add('Parked lift top below station roof',st['height_mm']-st['structure_allowance_mm']-park_top-st['tool_handling_margin_mm'],'Vertical top lift only; carriage thickness is part of the allowance.')
    add('Bottom exchange vertical gap',st['raised_core_bottom_z_mm']-(st['bottom_tray_z_mm']+b['bottom_height_mm'])-st['tool_handling_margin_mm'],'Core elevated before tool tray moves; actuator selection/recovery unresolved.')
    add('Cap shuttle lateral storage',st['width_mm']/2-st['structure_allowance_mm']-st['cap_shelf_y_mm']-b['width_mm']/2-st['tool_handling_margin_mm'],'Cap shelf lies below parked lift top; static lateral extent with handling allowance.')
    checks.append(dict(name='Thrust reserve sensitivity',status='PASS_ASSUMPTION' if sensitive_ratio>=s['thrust_to_weight_target'] else 'FAIL_ASSUMPTION',margin_mm=None,detail=f'{sensitive_ratio:.2f}:1 at assumed lower voltage and guard factor; not measured. Bench guarded estimate {bench_ratio:.2f}:1.'))
    for name in ('Headroom and complete landing geometry','Station doorway and approach routes','Guard access/impact protection and dogs','Minimum-voltage thrust and thermal endurance','Structural retention and station actuation','Cleaning coverage on a tread','Automatic battery balance charging'):
        checks.append(dict(name=name,status='UNKNOWN',margin_mm=None,detail='Requires measurement, design or physical validation; no overall feasibility pass.'))
    return dict(id=v['id'],label=v['label'],geometry=dict(length_mm=length,width_mm=width,height_mm=v['rotor_plane_mm']+s['guard_half_height_mm'],sampled_width_mm=maxwidth,sampled_length_mm=maxlength,rotor_step_clearance_mm=minclear,body_edge_clearance_mm=minbodyedge,combined_rail_width_mm=combined_width),
                mass=mass,checks=checks,power=dict(ideal_hover_w=(mass['total_g']/1000*9.81)**1.5/math.sqrt(2*1.225*4*math.pi*(p['prop_diameter_mm']/2000)**2),bench_equivalent_hover_w=hover,ground_w=ground,nominal_battery_wh=energy,flight_reserve_wh=reserved,ground_minutes_after_reserve=floor_runtime,bench_guarded_thrust_ratio=bench_ratio,voltage_sensitivity_thrust_ratio=sensitive_ratio,high_mass_thrust_ratio=sensitive_ratio*mass['total_g']/mass['high_g'],target_mass_headroom_g=maxt*factor*vfactor/s['thrust_to_weight_target']-mass['total_g'],assumed_low_voltage_current_a=None if hover is None else hover/s['minimum_flight_voltage_assumption']),overall='NOT_VALIDATED')


def evaluate(c,site,ledger):
    return [screen_variant(c,site,ledger,v) for v in c['variants']]


def write_report(c,site,ledger,results,path):
    default=next(r for r in results if r['id']==c['default_variant'])
    text=['# Concept screening results','',
          'Generated by `python3 design/generate.py` from the editable concept, home profile and component ledger.',
          '**All configurations remain NOT_VALIDATED. A model pass is only a pass of the stated simplified check.**','',
          '| Configuration | Guarded L × W × H (mm) | Mass (kg) | Geometry failures | Thrust ratio sensitivity |',
          '|---|---|---:|---:|---:|']
    for r in results:
        g=r['geometry']; failures=sum(ch['status']=='FAIL_MODEL' for ch in r['checks'])
        text.append(f'| {r["label"]} | {g["length_mm"]:.0f} × {g["width_mm"]:.0f} × {g["height_mm"]:.0f} | {r["mass"]["total_g"]/1000:.2f} | {failures} | {r["power"]["voltage_sensitivity_thrust_ratio"]:.2f}:1 |')
    for r in results:
        text.extend(['',f'## {r["label"]}','', '| Check | Result | Margin (mm) | Scope |','|---|---|---:|---|'])
        for ch in r['checks']:
            margin='—' if ch['margin_mm'] is None else str(ch['margin_mm'])
            text.append(f'| {ch["name"]} | {ch["status"]} | {margin} | {ch["detail"]} |')
    p=default['power']; m=default['mass']
    text.extend(['','## Default mass and energy sensitivity','',
        f'Loaded mass: {m["total_g"]/1000:.2f} kg. Sensitivity range: {m["low_g"]/1000:.2f}–{m["high_g"]/1000:.2f} kg, using ±30% on estimated masses and ±5% on manufacturer masses. These are not confidence intervals.',
        f'Core {m["by_group_g"]["core"]/1000:.2f} kg; loaded vacuum bottom {m["by_group_g"]["bottom"]/1000:.2f} kg; lift top {m["by_group_g"]["lift"]/1000:.2f} kg. Cap and stations are excluded from airborne mass.',
        f'Ground power allowance: {p["ground_w"]:.0f} W. Nominal battery energy: {p["nominal_battery_wh"]:.1f} Wh.'])
    text.append(f'Only {p["target_mass_headroom_g"]:.0f} g of mass headroom remains against the assumed thrust target. At the upper mass sensitivity, thrust/weight falls to {p["high_mass_thrust_ratio"]:.2f}:1. The nominal pass does not close the mass/propulsion budget.')
    if p['bench_equivalent_hover_w'] is not None:
        text.extend([f'Bench-equivalent hover estimate including an assumed guard loss and shared electronics: {p["bench_equivalent_hover_w"]:.0f} W. At the assumed minimum bus voltage this implies {p["assumed_low_voltage_current_a"]:.0f} A if that power holds.',
                     f'A {c["screening"]["reserved_flight_seconds"]} s flight-energy allowance consumes {p["flight_reserve_wh"]:.1f} Wh. With {c["screening"]["usable_energy_fraction"]*100:.0f}% usable pack energy, estimated ground runtime after that allowance is {p["ground_minutes_after_reserve"]:.0f} minutes. Neither reserve adequacy nor runtime is validated.'])
    robot=[row for row in ledger if row['section'] in ('core','bottom','lift','cap')]
    station=[row for row in ledger if row['section']=='station']
    cost=lambda rows,key: sum(row['qty']*row[key] for row in rows)
    text.extend(['','## Purchase allowances','',
        f'One reference robot with vacuum bottom, lift top and one cap: ${cost(robot,"cost_low_usd"):,.0f}–${cost(robot,"cost_high_usd"):,.0f}. Each complete station: ${cost(station,"cost_low_usd"):,.0f}–${cost(station,"cost_high_usd"):,.0f}.',
        'These are mixed listed references and planning allowances in USD, before tax/shipping/tools. Extra bottoms, the second cap, replacement inventory and household modifications are additional. Station masses and power are not estimated by zero-valued airborne ledger fields. Alternative variants only substitute motor mass; their frame/guard/prop masses and costs must be re-estimated before comparison is final.',
        '', '## Method limits','',
        '- Propulsion interpolation uses only the manufacturer curve range. It never extrapolates a missing hover point.',
        '- The low-voltage thrust sensitivity uses `(V_assumed / V_bench)^2` and an independent guard factor. Neither is measured; it is not a battery/propeller model. Full-throttle bench points are short-duration reserve references, not continuous lift ratings.',
        '- Stair geometry is an infinite interior straight flight. Rotor cylinders are sampled every 5 degrees with a radial discretization allowance; 27 attitude combinations are tested. This is not a continuous swept-volume guarantee. The body tread check is level at contact with yaw/position error.',
        '- Component boxes omit cable bends, fasteners, cooling/air passages and shell thickness. Positive-volume box intersection is checked, not assembly manufacturability.',
        '- Station checks cover explicit static bounds and aligned vertical exchanges. They do not prove a designed actuator, complete motion sequence or unattended recovery.',
        '- The example home retains unknown headroom, landings, rail thicknesses, doorways and bookcase position. No site survey or pet behavior is synthesized.',
        '', '## Sources',''])
    for key,p in c['propulsion'].items(): text.append(f'- [{p["candidate"]}]({p["source"]})')
    text.append('- Component sources and replacement notes are in [the CSV ledger](../../config/components.csv).')
    path.write_text('\n'.join(text)+'\n')
