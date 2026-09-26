"""Build the whole-system design report from editable, unit-labelled inputs.

Geometry is component allocation, not production CAD. Mass bounds, friction,
loads and installation factors are declared engineering cases, not test results.
"""
from copy import deepcopy
import csv
import html
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/system/output'
G = 9.80665


def read():
    return json.loads((ROOT / 'config/system_design.json').read_text())


def hi(p):
    return [x+s for x,s in zip(p['min'],p['size'])]


def overlap(a,b):
    return all(min(x,y)>max(u,v)+1e-7 for x,y,u,v in zip(hi(a),hi(b),a['min'],b['min']))


def contains(a,b):
    return all(u<=v+1e-7 and y<=x+1e-7 for u,v,x,y in zip(a['min'],b['min'],hi(a),hi(b)))


def centre(p):
    return p.get('mass_cg_mm', [x+s/2 for x,s in zip(p['min'],p['size'])])


def reference_parts(c,bottom,pose='transit'):
    groups=set(c['bottoms'][bottom]['groups']+['core','cap'])
    parts=deepcopy([p for p in c['parts'] if p['module'] in groups])
    for p in parts:
        if p['id']=='caster' and 'caster_min_override' in c['bottoms'][bottom]:
            p['min']=c['bottoms'][bottom]['caster_min_override'][:]
        if bottom in ('low','dust'):
            lift=c['bottoms'][bottom]['transit_lift_mm'] if pose=='transit' else 0
            if p['id'] in ('extension','extension_cable','extension_air_turn','low_head','dust_head'):
                p['min'][2]+=lift
                if 'mass_cg_mm' in p: p['mass_cg_mm'][2]+=lift
            if p['id']=='extension_flex':
                p['min'][2]+=lift; p['size'][2]-=lift
            if pose=='extended' and p['id'] in ('low_head','dust_head'):
                p['min'][1]-=extension_metrics(c)['travel_mm']
            if pose=='extended' and p['id']=='extension':
                # Show swept guide allocation; nested tube material is not a solid slab.
                travel=extension_metrics(c)['travel_mm']
                p['min'][1]-=travel; p['size'][1]+=travel
                p['notes']+=' Extended guide envelope, not full solid material.'
                # Six equal-length stages at offsets 0, -200, ... -1000 mm.
                # Weight tube centres by their actual thin-wall cross-sections.
                e=c['extension']; weights=[]; ys=[]
                for i in range(e['stage_count']):
                    w,h=[d-i*e['step_mm'] for d in e['outer_mm']]
                    weights.append(w*h-(w-2*e['wall_mm'])*(h-2*e['wall_mm']))
                    ys.append(e['stage_length_mm']/2-i*(e['stage_length_mm']-e['overlap_mm']))
                p['mass_cg_mm']=[133,sum(w*y for w,y in zip(weights,ys))/sum(weights),22]
            if pose=='extended' and p['id']=='extension_cable':
                p['min'][1]-=extension_metrics(c)['travel_mm']; p['size'][1]+=extension_metrics(c)['travel_mm']
                p['mass_cg_mm']=[162,-407.5,23]
    return parts


def lift_parts(c,variant):
    l=c['lift']; v=l['variants'][variant]; parts=[]
    def add(id,label,xyz,size,rows,shape='box',group='lift'):
        parts.append(dict(id=id,module='lift',label=label,min=xyz,size=size,group=group,
                          hardware=[{'id':k,'qty':q} for k,q in rows],shape=shape,notes='Design reference; not fabrication geometry.'))
    for i,(x,y) in enumerate(v['rotors_xy_relative_mm']):
        x+=137.5; y+=137.5
        add(f'rotor_{i+1}',f'Rotor {i+1}: motor / prop / ESC',[x-19,y-19,101],[38,38,60],
            [('lift_motor',1),('lift_prop',1),('lift_esc',1)],'cylinder_z')
        d=l['guard_diameter_mm']; z0,z1=l['guard_z_range_mm']
        add(f'guard_{i+1}',f'Guard {i+1}',[x-d/2,y-d/2,z0],[d,d,z1-z0],[('lift_guard',1)],'ring_z')
    xy=v['rotors_xy_relative_mm']; d=l['guard_diameter_mm']
    x0=min(x for x,y in xy)+137.5-d/2; y0=min(y for x,y in xy)+137.5-d/2
    w=max(x for x,y in xy)-min(x for x,y in xy)+d
    depth=max(y for x,y in xy)-min(y for x,y in xy)+d
    for key,qty in l['common'].items():
        if key=='lift_structure': qty*=v['structure_scale']
        add(key,c['hardware'][key]['name'],[x0,y0,79],[w,depth,57],[(key,qty)],'distributed')
    # Distinct proxies for flight electronics and two added stereo viewpoints.
    add('flight_fc_proxy','Flight controller, vibration mount and connections',[101,282,105],[74,53,32],[],'box','sensor')
    add('flight_camera_rear','Rear stereo camera',[85.5,278,43],[104,27,34],[],'box','sensor')
    add('flight_camera_down','Downward stereo camera / clear floor view',[285,112,50],[104,34,27],[],'box','sensor')
    # Route stock below motor bases and outside the fixed core. These zero-mass
    # proxies visualize stock already included in lift_structure.
    span=1200 if variant=='octo10' else 600
    for i,x in enumerate([-42.5,317.5]):
        add('beam_long_'+str(i),'20/18 mm carbon longitudinal beam',[x-10,137.5-span/2,79],[20,span,20],[],'cylinder_y')
    for i,y in enumerate([-15,290]):
        add('beam_cross_'+str(i),'20/18 mm carbon crossbeam',[-32.5,y-10,79],[340,20,20],[],'cylinder_x')
    if variant=='hex10':
        for i,y in enumerate([-452.5,300]):
            add('beam_nose_'+str(i),'Hex centre-rotor support route',[127.5,y,79],[20,427.5,20],[],'cylinder_y')
    return parts


def hardware_rows(c,parts):
    rows=[]
    for p in parts:
        for r in p['hardware']:
            h=c['hardware'][r['id']]; q=r['qty']
            rows.append(dict(instance=p['id']+':'+r['id'],hardware_id=r['id'],part=p['id'],
                             module=p['module'],name=h['name'],qty=q,
                             mass_g=[q*m for m in h['mass_g']],mass_basis=h['mass_basis'],
                             cg_mm=centre(p),source=h['source'],procurement=h['procurement'],
                             notes=h['notes'],measured_mass_g=h['measured_mass_g']))
    return rows


def mass_and_cg(rows):
    mass=[sum(r['mass_g'][i] for r in rows) for i in range(3)]
    cg=[sum(r['mass_g'][1]*r['cg_mm'][i] for r in rows)/mass[1] for i in range(3)]
    def extremum(axis,minimize):
        lo=min(r['cg_mm'][axis] for r in rows); high=max(r['cg_mm'][axis] for r in rows)
        for _ in range(70):
            mid=(lo+high)/2; moment=0
            for r in rows:
                delta=r['cg_mm'][axis]-mid
                bound=2 if ((delta<0)==minimize) else 0
                moment+=r['mass_g'][bound]*delta
            if moment>0: lo=mid
            else: high=mid
        return (lo+high)/2
    return {'mass_g':mass,'cg_mm':cg,'cg_bounds_mm':[[extremum(a,True),extremum(a,False)] for a in range(3)]}


def assembly(c,bottom,top='cap',battery='design_6s',payload=True,pose='transit'):
    parts=reference_parts(c,bottom,pose)
    if top!='cap':
        parts=[p for p in parts if p['module']!='cap']+lift_parts(c,top)
    rows=hardware_rows(c,parts)
    b=c['batteries'][battery]; bay=next(p for p in parts if p['id']=='pack_cell_pocket')
    rows.append(dict(instance='battery',hardware_id=battery,part='battery_bay',module='battery',name=b['label'],qty=1,
                     mass_g=b['mass_g'],mass_basis='Listed pack reference; no protection or harness double-counted',
                     cg_mm=centre(bay),source=c['sources'][b['source']],procurement='comparison_not_ordered',notes='',measured_mass_g=None))
    if payload:
        bot=c['bottoms'][bottom]
        rows.append(dict(instance='payload',hardware_id='payload',part='payload',module='payload',name=bot['payload_note'],qty=1,
                         mass_g=[bot['payload_g'],bot['payload_g'],bot['payload_high_g']],mass_basis='Bounded design contents',
                         cg_mm=bot['payload_at'],source='Owner task / design allowance',procurement='consumable_load',notes='',measured_mass_g=None))
    result=mass_and_cg(rows)
    result.update(bottom=bottom,top=top,battery=battery,pose=pose,parts=parts,rows=rows)
    return result


def allocation_checks(c,parts,bottom):
    errors=[]; roots=[p for p in parts if not p.get('parent') and p['shape']!='distributed']
    lookup={p['id']:p for p in parts}
    for p in parts:
        if any(s<=0 for s in p['size']): errors.append('Non-positive extent: '+p['id'])
        if p.get('parent') and not contains(lookup[p['parent']],p): errors.append('Reference outside bay: '+p['id'])
        if p['module']!='lift' and p['id'] not in ('low_head','dust_head'):
            if not contains({'min':[0,0,0],'size':c['limits']['body_mm']},p):
                errors.append('Outside fixed body allocation: '+p['id'])
    for a,b in itertools.combinations(roots,2):
        if overlap(a,b): errors.append('Allocation overlap: '+a['id']+' / '+b['id'])
    for a,b in itertools.combinations([p for p in parts if p.get('parent')],2):
        if a['parent']==b['parent'] and overlap(a,b):errors.append('Nested reference overlap: '+a['id']+' / '+b['id'])
    return {'errors':errors,'root_count':len(roots),'reference_count':len(parts)-len(roots),
            'scope':'Axis-aligned functional allocations and nested reference containment, transit pose. Distributed structure/wires are mass allowances, not collision-certified solids. Extension head overhang is intentional.'}


def power_metrics(c,bottom):
    p=c['power']; loads=p['core_loads']+p['drive_loads']+p['tools'][bottom]
    rails={rail:{'normal_w':0.,'high_w':0.} for rail in ('5v','12v','24v')}
    for load in loads:
        for k in ('normal_w','high_w'): rails[load['rail']][k]+=load[k]
    totals={k:sum(v[k]/p['rail_efficiency'][r] for r,v in rails.items()) for k in ('normal_w','high_w')}
    totals['conversion_loss_w']=totals['normal_w']-sum(v['normal_w'] for v in rails.values())
    totals['rails']=rails; totals['loads']=loads
    totals['allocation_errors']=[r for r,x in rails.items() if x['high_w']>p['rail_allocations_w'][r]]
    totals['runtimes_min']={key:(b['nominal_v']*b['capacity_ah']*p['usable_energy_fraction']/totals['normal_w']*60)
                           for key,b in c['batteries'].items()}
    bot=c['bottoms'][bottom]
    totals['coverage_m2_h']=bot['swath_m']*bot['speed_m_s']*bot['coverage_efficiency']*3600
    totals['one_floor_motion_min']=92.903/totals['coverage_m2_h']*60
    return totals


def signed_margin(point,poly):
    area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))
    sign=1 if area>0 else -1
    return min(sign*((b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0]))/math.dist(a,b)
               for a,b in zip(poly,poly[1:]+poly[:1]))


def support_metrics(c,a):
    t=c['traction']; wheels=t['drive_contact_xy']; caster=next(p for p in a['parts'] if p['id']=='caster')
    pivot=centre(caster)[:2]; trail=t['caster_trail_mm']; cg=a['cg_mm'][:2]
    e=t['cg_uncertainty_mm']; bounds=a['cg_bounds_mm']
    corners=list(itertools.product([bounds[0][0]-e,bounds[0][1]+e],[bounds[1][0]-e,bounds[1][1]+e]))
    nominal=[]; uncertain=[]; caster_fraction=[]; backup=[]
    for deg in range(0,360,5):
        r=math.radians(deg); contact=[pivot[0]+trail*math.cos(r),pivot[1]+trail*math.sin(r)]
        poly=wheels+[contact]
        nominal.append(signed_margin(cg,poly)); uncertain.extend(signed_margin(p,poly) for p in corners)
        # Clockwise convex hull of all contacts once the 2 mm backup gap closes.
        pts=sorted(set(map(tuple,poly+t.get('backup_contact_xy',[]))))
        def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
        lower=[]; upper=[]
        for p in pts:
            while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
            lower.append(p)
        for p in reversed(pts):
            while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
            upper.append(p)
        hull=lower[:-1]+upper[:-1]
        backup.extend(signed_margin(p,hull) for p in corners)
        caster_fraction.append((cg[1]-wheels[0][1])/(contact[1]-wheels[0][1]))
    return {'minimum_nominal_margin_mm':min(nominal),'mass_and_position_bound_margin_mm':min(uncertain),
            'backup_contact_hull_bound_margin_mm':min(backup),
            'backup_engagement_pitch_deg':math.degrees(math.atan2(t.get('backup_ground_gap_mm',0),wheels[0][1]-14)),
            'caster_weight_fraction_range':[min(caster_fraction),max(caster_fraction)],
            'scope':'Static level-floor, pad/head lifted, 72 caster headings; interval component masses plus 15 mm position allowance. Not dynamic stability or impact certification.'}


def traction_metrics(c,a):
    t=c['traction']; m=a['mass_g'][1]/1000; r=t['wheel_radius_m']; support=support_metrics(c,a)
    drag=t['mop_drag_n'] if a['bottom']=='mop' else 1.5
    f=m*G*t['rolling_coefficient']+m*t['acceleration_m_s2']+drag
    torque=f*r/2
    available=t['stall_torque_nm']*(t['current_limit_a']-t['no_load_current_a'])/(t['stall_current_a']-t['no_load_current_a'])
    continuous=t['stall_torque_nm']*t['continuous_torque_fraction_of_stall']
    caster_fraction=support['caster_weight_fraction_range'][1]
    wheel_normal=m*G*(1-caster_fraction)
    threshold=[]
    for h_mm in (4,10):
        h=h_mm/1000; lever=math.sqrt(2*r*h-h*h)
        wheel_step_torque=(wheel_normal/2)*lever
        cr=.025; caster_load=m*G*caster_fraction
        push=caster_load*math.sqrt(2*cr*h-h*h)/(cr-h)
        mu_needed=(push+m*G*t['rolling_coefficient'])/wheel_normal
        threshold.append({'height_mm':h_mm,'driven_wheel_torque_nm_each':wheel_step_torque,
                          'caster_push_n':push,'floor_mu_needed_during_caster_climb':mu_needed,
                          'wheel_current_limit_margin_nm':available-wheel_step_torque})
    return dict(required_torque_nm_each=torque,continuous_torque_screen_nm=continuous,
                current_limited_torque_nm=available,free_speed_m_s=2*math.pi*r*t['free_speed_rpm']/60,
                force_n=f,wet_force_bounds_n=[mu*wheel_normal for mu in t['wet_friction_sensitivity']],
                thresholds=threshold,support=support,
                scope='Quasistatic sharp-edge and DC motor approximation; no claim of proven wet-floor traction. Stall torque is not a continuous rating.')


def extension_metrics(c):
    e=c['extension']; travel=(e['stage_count']-1)*(e['stage_length_mm']-e['overlap_mm'])
    dims=[[e['outer_mm'][0]-i*e['step_mm'],e['outer_mm'][1]-i*e['step_mm']] for i in range(e['stage_count'])]
    q=e['airflow_l_s']/1000; losses=[]; rho=1.225
    for i,(w,h) in enumerate(dims):
        wi=(w-2*e['wall_mm'])/1000; he=(h-2*e['wall_mm'])/1000
        area=wi*he; dh=2*wi*he/(wi+he); vel=q/area
        length=(e['stage_length_mm'] if i==0 else e['stage_length_mm']-e['overlap_mm'])/1000
        loss=e['hose_friction_factor']*length/dh*rho*vel*vel/2
        losses.append(dict(stage=i+1,outer_mm=[w,h],inner_area_mm2=area*1e6,velocity_m_s=vel,loss_pa=loss))
    minor=e['minor_loss_k']*rho*losses[-1]['velocity_m_s']**2/2
    return dict(travel_mm=travel,extended_guide_length_mm=e['stage_length_mm']+travel,
                nose_to_leading_edge_mm=travel+e['head_length_mm'],
                useful_sofa_depth_mm=travel+e['head_length_mm']-e['sofa_standoff_mm'],
                one_way_time_s=travel/e['feed_speed_mm_s'],stages=losses,
                straight_loss_pa=sum(s['loss_pa'] for s in losses),minor_loss_pa=minor,
                total_added_loss_pa=sum(s['loss_pa'] for s in losses)+minor,
                scope='Smooth-duct estimate at assumed flow; excludes filter/head losses and seal leakage. Does not establish an operating point.')


def interpolate(curve,x):
    if x<curve[0][0] or x>curve[-1][0]: return None
    for (x0,y0),(x1,y1) in zip(curve,curve[1:]):
        if x0<=x<=x1: return y0+(y1-y0)*(x-x0)/(x1-x0)
    return None


def lift_metrics(c,a,variant):
    if not 4<=c['batteries'][a['battery']]['cells']<=6:
        raise ValueError('Battery voltage is outside the selected 4–6S motor reference; no extrapolated flight result')
    l=c['lift']; v=l['variants'][variant]; n=len(v['rotors_xy_relative_mm']); mass=a['mass_g'][1]
    factor=l['guard_factor']; voltage=l['minimum_voltage_screen_v']; curve=l['curve_thrust_g_power_w']
    voltage_factor=(voltage/l['reference_voltage_v'])**l['voltage_scaling_exponent']
    max_total=n*curve[-1][0]*factor*voltage_factor
    required=mass/(n*factor); per_motor=interpolate(curve,required)
    core_w=sum(x['normal_w']/c['power']['rail_efficiency'][x['rail']] for x in c['power']['core_loads'])
    additional_flight_electronics_w=16
    hover=None if per_motor is None else n*per_motor*l['power_overhead_factor']+core_w+additional_flight_electronics_w
    # Same-RPM/thrust approximation uses the 24 V power curve; low-voltage loss uncertainty is explicit.
    peak_per_motor=interpolate(curve,required*l['thrust_to_weight_target'])
    maneuver=None if peak_per_motor is None else n*peak_per_motor*l['power_overhead_factor']+core_w+additional_flight_electronics_w
    xy=v['rotors_xy_relative_mm']; d=l['guard_diameter_mm']
    w=max(x for x,y in xy)-min(x for x,y in xy)+d
    depth=max(y for x,y in xy)-min(y for x,y in xy)+d
    yaw=math.radians(l['yaw_uncertainty_deg'])
    occupied=w*math.cos(yaw)+depth*abs(math.sin(yaw))+2*l['lateral_margin_mm']
    clear=c['limits']['stair_clear_width_mm']-c['limits']['left_projection_mm']-c['limits']['right_projection_mm']
    collision=[]
    for i,(x,y) in enumerate(xy):
        # Distance from each rotor centre to core square; disks cannot blow through the body.
        dx=max(abs(x)-137.5,0); dy=max(abs(y)-137.5,0)
        if math.hypot(dx,dy)<d/2: collision.append(f'Guard {i+1} overlaps core plan')
        for j in range(i):
            if math.dist((x,y),xy[j])<d: collision.append(f'Guard overlap {j+1}/{i+1}')
    base=[p for p in a['parts'] if p['module']!='lift' and p['shape']!='distributed' and not p.get('parent')]
    top=[p for p in a['parts'] if p['module']=='lift' and p['shape']!='distributed']
    for p in top:
        for b in base:
            if not overlap(p,b):continue
            if p['shape']=='ring_z':
                cx,cy=centre(p)[:2];bx,by=b['min'][:2];hx,hy=hi(b)[:2]
                dx=max(bx-cx,0,cx-hx);dy=max(by-cy,0,cy-hy)
                if math.hypot(dx,dy)>=p['size'][0]/2:continue
            collision.append('Lift/base allocation overlap: '+p['id']+' / '+b['id'])
    robot_batt=c['batteries'][a['battery']]
    available_wh=robot_batt['nominal_v']*robot_batt['capacity_ah']*c['power']['usable_energy_fraction']
    transfer=None if hover is None else hover*l['maneuver_power_factor']*l['transfer_s']/3600
    landing=None if hover is None else hover*l['landing_reserve_s']/3600
    departure=None if hover is None else (transfer+landing)*(1+l['energy_margin_fraction'])
    slope=c['limits']['stair_riser_mm']/c['limits']['stair_tread_mm']
    stair_body_origin=max(100+slope*137.5,100+slope*depth/2-l['guard_z_range_mm'][0])
    extended_tool_w=0
    if a['pose']=='extended':
        extended_tool_w=sum(x['normal_w']/c['power']['rail_efficiency'][x['rail']] for x in c['power']['tools'][a['bottom']])
    return dict(rotor_count=n,envelope_mm=[w,depth,l['guard_z_range_mm'][1]],
                occupied_stair_width_mm=occupied,conservative_stair_width_mm=clear,
                lateral_margin_remaining_mm=clear-occupied,geometry_errors=collision,
                total_available_thrust_g=max_total,thrust_weight_nominal=max_total/mass,
                thrust_weight_high_mass=max_total/a['mass_g'][2],
                thrust_weight_guard_sensitivity=[max_total/factor*k/mass for k in l['guard_factor_range']],
                max_mass_at_target_g=max_total/l['thrust_to_weight_target'],
                hover_w=hover,hover_current_a=None if hover is None else hover/voltage,
                maneuver_target_w=maneuver,maneuver_current_a=None if maneuver is None else maneuver/voltage,
                maneuver_target_within_voltage_thrust_screen=max_total/mass>=l['thrust_to_weight_target'],
                published_full_throttle_total_w=n*curve[-1][1],
                transfer_wh=transfer,landing_reserve_wh=landing,departure_energy_wh=departure,
                energy_remaining_after_departure_reserve_wh=None if departure is None else available_wh-departure,
                supply_compatible=robot_batt['cells']<=6,flight_qualified=False,
                stair_slope_deg=math.degrees(math.atan(slope)),
                stair_body_origin_above_local_plane_mm=stair_body_origin,
                stair_highest_point_above_lowest_underlying_tread_mm=stair_body_origin+180+slope*depth/2,
                airborne_tool_w=extended_tool_w,
                airborne_tool_mode_w=None if hover is None else hover+extended_tool_w,
                scope='Estimated installed thrust/power using published 24 V bench data and declared loss/voltage assumptions. Not a flight capability claim. Full-throttle curve point has a 29-second limit.')


def battery_fit(c,key):
    b=c['batteries'][key]; bay=next(p for p in c['parts'] if p['id']=='pack_cell_pocket')
    clearance=[s-x for s,x in zip(bay['size'],b['body_mm'])]
    orientations=[list(d) for d in sorted(set(itertools.permutations(b['body_mm']))) if all(x<=y for x,y in zip(d,bay['size']))]
    return {'body_clearance_mm':clearance,'any_orientation_bare_fit':bool(orientations),'fitting_orientations_mm':orientations,
            'installed_cartridge_fit_qualified':False,
            'scope':'Bare pack versus the smaller cell pocket inside the cartridge. This excludes leads, padding and swelling clearance; it does not qualify an installed cartridge.'}


def battery_exchange_metrics(c):
    e=c['battery_exchange']; s=c['station']; b=c['batteries']['design_6s']
    tare=[sum(c['hardware'][key]['mass_g'][i] for key in e['cartridge_tare_hardware_ids']) for i in range(3)]
    usable_wh=b['nominal_v']*b['capacity_ah']*c['power']['usable_energy_fraction']
    available_w=s['charger_allocation_w']*e['charge_input_efficiency']*e['charge_enabled_time_fraction']
    local_packs=e['spare_packs_per_station']+e['cartridges_on_robot']
    cases={}
    for key in c['bottoms']:
        power=power_metrics(c,key); runtime=power['runtimes_min']['design_6s']
        cases[key]=dict(runtime_min=runtime,
            minimum_charge_enabled_fraction=power['normal_w']/(s['charger_allocation_w']*e['charge_input_efficiency']),
            average_charge_margin_w=available_w-power['normal_w'],
            recovery_scenarios=[dict(recovery_min=t,minimum_local_pack_count=math.ceil(t/runtime)+1,
                configured_pack_count_sufficient=local_packs>=math.ceil(t/runtime)+1)
                for t in e['recovery_time_scenarios_min']])
    errors=[]
    required=e['spare_packs_per_station']+e['minimum_free_receiving_bays']+e['recovery_bays_reserved']
    if e['rack_bays_per_station']<required: errors.append('Battery rack lacks receiving/recovery vacancies')
    if len(e['rack_slot_min_mm'])!=e['rack_bays_per_station']: errors.append('Battery rack slot count does not match allocation')
    # The old bottom is parked before withdrawal. Check the full downward
    # cartridge sweep against fixed core allocations, not against removed tools.
    moving=deepcopy(next(p for p in c['parts'] if p['id']=='battery_bay'))
    moving['min'][2]-=e['extraction_drop_mm']; moving['size'][2]+=e['extraction_drop_mm']
    for p in c['parts']:
        if p['module']=='core' and p['id']!='battery_bay' and not p.get('parent') and p['shape']!='distributed' and overlap(moving,p):
            errors.append('Battery withdrawal intersects fixed core: '+p['id'])
    rack=e['rack_allocation']; slots=[dict(min=xyz,size=e['rack_slot_size_mm']) for xyz in e['rack_slot_min_mm']]
    for i,slot in enumerate(slots):
        if not contains(rack,slot): errors.append('Battery slot outside rack: '+str(i+1))
    if any(overlap(a,b) for a,b in itertools.combinations(slots,2)): errors.append('Battery rack slots overlap')
    for p in station_parts(c):
        if p['id']!='battery_rack' and not p.get('parent') and p['shape']!='distributed' and overlap(rack,p):
            errors.append('Battery rack intersects station allocation: '+p['id'])
    return dict(total_fleet_packs=s['count']*e['spare_packs_per_station']+e['cartridges_on_robot'],
        local_cycling_pack_count=local_packs,rack_bays_per_station=e['rack_bays_per_station'],
        spare_packs_per_station=e['spare_packs_per_station'],cartridge_tare_g=tare,
        nominal_loaded_cartridge_g=b['mass_g'][1]+tare[1],
        spare_cartridge_mass_kg_per_station=e['spare_packs_per_station']*(b['mass_g'][1]+tare[1])/1000,
        reference_usable_wh=usable_wh,average_charge_to_cells_w=available_w,
        example_cc_charge_lower_bound_min=c['power']['usable_energy_fraction']/e['example_charge_c_rate']*60,
        floor_cases=cases,geometry_errors=errors,
        scope='Energy throughput and pack-count screens only. Recovery scenarios must include cooling, shared-power contention, CC/CV taper and balance time. Swap time, connector fit, thermal containment and full gantry swept volume are unverified.')


def station_metrics(c):
    s=c['station']; floor_m2=92.903
    cycles=math.ceil(floor_m2/s['mop_wash_interval_m2'])
    water={surface:floor_m2*s[key]+cycles*s['wash_water_ml'] for surface,key in [('wood','wood_water_ml_m2'),('tile','tile_water_ml_m2')]}
    area=s['cabinet_mm'][0]*(s['cabinet_mm'][1]+s['front_approach_mm'])/1e6
    return dict(reserved_area_m2_per_floor=area,washes_per_floor=cycles,water_ml_per_floor=water,
                empty_station_mass_kg=sum(x['mass_each_g']*x['qty'] for x in s['hardware'])/1000,
                bottom_positions=len(s['bottom_slot_min_mm']),
                clean_tank_floor_equivalents={k:s['clean_water_l']*1000/v for k,v in water.items()},
                minimum_dc_service_allocation_w=s['charger_allocation_w']+c['battery_exchange']['station_logic_input_w']+14,
                scope='Water/docking intervals are design recipes, not demonstrated sanitation or coverage. Mains evacuation is separate from the 24 V DC supply.')


def station_parts(c):
    """Off-robot machinery reservations; storage and swept motion are distinct."""
    s=c['station']; out=[]
    def add(id,xyz,sz,label,group='structure'):
        out.append(dict(id=id,module='station',min=xyz,size=sz,label=label,group=group,
                        hardware=[],shape='box',notes='Station space reservation, not a fabricated component.'))
    add('cabinet',[0,0,0],s['cabinet_mm'],'Cabinet and handling envelope')
    out[-1]['shape']='distributed'
    add('arrival',[450,-15,10],[300,355,180],'Robot arrival / scale', 'drive')
    for i,xyz in enumerate(s['bottom_slot_min_mm']):
        add('slot_'+str(i+1),xyz,[275,335,132],f'Bottom position {i+1}', 'tool')
    add('core_held',[462.5,287.5,376],[275,275,112],'Core raised clear of bottom transfer', 'logic')
    add('core_lift',[345,260,10],[85,350,490],'Core forks / vertical lift', 'structure')
    add('top_park',[278,308,600],[644,1444,180],'Intact eight-rotor top parking', 'lift')
    add('cap_tray',[470,1410,220],[275,275,180],'Cap / scanner-clear storage', 'logic')
    add('bottom_transfer',[25,120,220],[1150,1250,132],'Bottom picker travel plane', 'structure')
    out[-1]['shape']='distributed'
    add('top_handler',[235,200,1050],[730,1580,220],'Overhead Y/Z handler', 'structure')
    add('wash',[460,630,30],[320,330,175],'Mop wash / drain pan', 'water')
    add('clean_tank',[880,1030,0],[270,290,330],'5 L clean water + removal clearance', 'water')
    add('dirty_tank',[880,1360,0],[270,290,330],'5 L dirty water + removal clearance', 'water')
    add('vacuum_service',[30,1370,0],[340,390,430],'Vacuum appliance / 5 L debris', 'air')
    add('station_electrical',[420,1420,470],[360,320,110],'Supply / charge / station controls', 'power')
    e=c['battery_exchange']
    add('battery_rack',e['rack_allocation']['min'],e['rack_allocation']['size'],'Four battery bays / dry enclosure', 'battery')
    for i,xyz in enumerate(e['rack_slot_min_mm']):
        add('battery_slot_'+str(i+1),xyz,e['rack_slot_size_mm'],f'Battery bay {i+1}: two spares + receiving/recovery vacancies', 'battery')
        out[-1]['parent']='battery_rack'
    return out


def svg_layout(c,a,view='top'):
    parts=[p for p in a['parts'] if p['shape']!='distributed' and not p.get('parent')]
    axes=(0,1) if view=='top' else (1,2)
    mins=[min(p['min'][i] for p in parts) for i in range(3)]; maxs=[max(hi(p)[i] for p in parts) for i in range(3)]
    ax,bx=axes; scale=min(840/(maxs[ax]-mins[ax]+40),560/(maxs[bx]-mins[bx]+40))
    def xy(x,z):
        return 50+(x-mins[ax])*scale,75+((maxs[bx]-z) if view!='top' else (z-mins[bx]))*scale
    colors={'power':'#ca7e26','logic':'#466cbd','sensor':'#954ab3','battery':'#b88617','structure':'#667685','drive':'#147c88','air':'#3d8d66','tool':'#b85552','water':'#258eac','extension':'#986731','lift':'#6d63a9'}
    o=['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="720" viewBox="0 0 940 720">',
       '<rect width="100%" height="100%" fill="#f7f9fc"/>','<g font-family="sans-serif">',
       f'<text x="30" y="30" font-size="22">{html.escape(c["bottoms"][a["bottom"]]["label"])} + {a["top"]} · {view}</text>',
       '<text x="30" y="53" font-size="12">Engineering allocations in mm; see hardware worksheet for evidence and mass intervals.</text>']
    for p in sorted(parts,key=lambda p:p['min'][2]):
        color=colors[p['group']]; x,y=xy(p['min'][ax],p['min'][bx] if view=='top' else hi(p)[bx])
        w,h=p['size'][ax]*scale,p['size'][bx]*scale
        if view=='top' and p['shape'] in ('ring_z','cylinder_z'):
            o.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{color}" fill-opacity=".08" stroke="{color}"><title>{html.escape(p["label"])}</title></ellipse>')
        else:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" fill-opacity=".12" stroke="{color}"><title>{html.escape(p["label"])}</title></rect>')
        if w>65 and h>22: o.append(f'<text x="{x+3}" y="{y+13}" font-size="9">{html.escape(p["id"])}</text>')
    o.append(f'<text x="30" y="680" font-size="14">Mass {a["mass_g"][1]/1000:.2f} kg; range {a["mass_g"][0]/1000:.2f}–{a["mass_g"][2]/1000:.2f} kg, with design payload and battery.</text>')
    o.append('<text x="30" y="703" font-size="12">Front = y 0; extensions may have negative y. Distributed frames/wiring are not drawn as solid boxes.</text></g></svg>')
    return '\n'.join(o)


def report(c,result):
    r=['# Whole-system engineering budget','',f'Revision {c["revision"]}, {c["date"]}. Preliminary design, not measured performance.','',
       'All masses include the stated battery and contents. Low/high are engineering bounds, not statistical intervals. A complete bottom includes its own wheels and controls.','',
       'Revision C baseline: lift layouts and the wheeled horizontal duster below remain comparison evidence. The preferred wheel-less duster, raised boom, compact duct targets and round-trip mission budget are in the [revision D airborne supplement](airborne_dusting.md) and [interactive comparison](airborne_dusting.html). See [LIFT_LAYOUT_REVIEW.md](../../../docs/LIFT_LAYOUT_REVIEW.md) for earlier size drivers.','',
       '## Loaded floor configurations','',
       '| Bottom + core + cap | Low / nominal / high kg | Normal / high battery W | 6S example runtime min | Level-floor nominal support margin mm |','|---|---:|---:|---:|---:|']
    for key,a in result['ground'].items():
        p=result['power'][key]; t=result['traction'][key]
        r.append(f'| {c["bottoms"][key]["label"]} | '+ ' / '.join(f'{m/1000:.2f}' for m in a['mass_g'])+f' | {p["normal_w"]:.1f} / {p["high_w"]:.1f} | {p["runtimes_min"]["design_6s"]:.0f} | {t["support"]["minimum_nominal_margin_mm"]:.1f} |')
    r+=['','Runtime uses 80% nominal energy and assumed average loads, including conversion losses. A battery with adequate energy may still fail flight-current or packaging requirements.','',
        '## Module hardware masses without bare cells or contents','', '| Module | Low / nominal / high kg |','|---|---:|']
    for name,m in result['module_masses'].items(): r.append('| '+name+' | '+' / '.join(f'{x/1000:.3f}' for x in m)+' |')
    r+=['','## Lift comparisons at 21 V and assumed 75% retained thrust','',
        '| Bottom | Top | Complete nominal / high kg | Nominal / high-mass thrust:weight | Estimated hover W / A | Departure reserve Wh |','|---|---|---:|---:|---:|']
    for key,entry in result['flights'].items():
        a=entry['assembly']; f=entry['screen']
        def num(x): return 'outside curve' if x is None else f'{x:.1f}'
        r.append(f'| {a["bottom"]} | {a["top"]} | {a["mass_g"][1]/1000:.2f} / {a["mass_g"][2]/1000:.2f} | {f["thrust_weight_nominal"]:.2f} / {f["thrust_weight_high_mass"]:.2f} | {num(f["hover_w"])} / {num(f["hover_current_a"])} | {num(f["departure_energy_wh"])} |')
    r+=['','The 2:1 sizing target is provisional. Guard loss and voltage scaling are unverified. Hover power comes from interpolation at required equivalent open-rotor thrust, plus 10% installation/electrical power overhead and flight electronics. These are coupled assumptions, not a measured flight curve.',
        '','Departure reserve includes 45 s transfer at 1.2 times estimated hover power, 30 s landing reserve, then 20% energy margin. It is an illustrative mission allocation, not an approved flight policy. Tool motors are off during transfer. Airborne dusting adds tool power and uses the extended configuration.','',
        '## Packaging and compatibility','']
    for bottom,checks in result['checks'].items():
        r.append(f'- {bottom}: {checks["root_count"]} root allocations, {len(checks["errors"])} numerical conflicts.')
        r += ['  - '+e for e in checks['errors']]
    for key,f in result['battery_fit'].items(): r.append(f'- {key}: bare pack can fit the cartridge cell pocket in some orientation: {f["any_orientation_bare_fit"]}; reference-axis clearance {f["body_clearance_mm"]} mm. Installed cartridge fit is unqualified.')
    for variant,v in c['lift']['variants'].items():
        f=result['flights']['vacuum_'+variant]['screen']
        r.append(f'- {variant}: {f["envelope_mm"]} mm; width with 2° yaw and 25 mm lateral allowance each side {f["occupied_stair_width_mm"]:.1f} mm versus conservative {f["conservative_stair_width_mm"]:.1f} mm stair corridor. Remaining width {f["lateral_margin_remaining_mm"]:.1f} mm.')
    for name,f in result['flights'].items():
        if f['screen']['geometry_errors']:r.extend('- '+name+': '+e for e in f['screen']['geometry_errors'])
    r.append('- Lift/base static allocation checks include cameras, controller and beam routes. Guard/box checks use disk distance, not only rectangular bounds; dynamic swept volumes and clamp details remain excluded.')
    r+=['','## Traction and transitions','',
        '| Bottom | Level-floor torque per wheel N·m | 10 mm step wheel torque N·m | Caster-climb assumed minimum floor friction | Mass/position-bound support margin mm |','|---|---:|---:|---:|---:|']
    for key,t in result['traction'].items():
        step=t['thresholds'][1]
        r.append(f'| {key} | {t["required_torque_nm_each"]:.3f} | {step["driven_wheel_torque_nm_each"]:.3f} | {step["floor_mu_needed_during_caster_climb"]:.2f} | {t["support"]["mass_and_position_bound_margin_mm"]:.1f} |')
    r+=['','The transition model excludes tire deformation and impact. Wet coefficients are assumptions; a nominal torque pass is not a traction qualification. Inspect the uncertainty result, not only nominal CG.',
        '','## Extension','']
    e=result['extension']; r += [f'- {e["travel_mm"]:.0f} mm travel; {e["extended_guide_length_mm"]:.0f} mm guide length; {e["useful_sofa_depth_mm"]:.1f} mm useful depth after 80 mm stand-off.',
        f'- One-way stroke {e["one_way_time_s"]:.0f} s at 50 mm/s. Nominal moving height 40 mm; transit lifts the assembly 12 mm.',
        f'- Estimated added duct loss {e["total_added_loss_pa"]:.0f} Pa at 3.6 L/s: {e["straight_loss_pa"]:.0f} Pa straight + {e["minor_loss_pa"]:.0f} Pa fittings/contractions. Leakage, nozzle and filter excluded.',
        '','## Automatic station allowance','',
        f'- Per floor: {result["station"]["reserved_area_m2_per_floor"]:.2f} m² including approach; five bottom positions plus intact lift-top parking.',
        f'- Machinery allowance: {result["station"]["empty_station_mass_kg"]:.1f} kg empty, excluding spare robot modules and bulk contents.',
        f'- Water recipe per 1000 ft²: {result["station"]["water_ml_per_floor"]["wood"]/1000:.2f} L for wood or {result["station"]["water_ml_per_floor"]["tile"]/1000:.2f} L for tile, including ten pad washes.',
        '- 280 W DC supply allocation; charge and motion interlocked. 800 W mains evacuation is a separate appliance load.','',
        '## Automatic battery exchange','']
    e=result['battery_exchange']
    r += [f'- {e["spare_packs_per_station"]} spare packs and {e["rack_bays_per_station"]} bays per floor; {e["total_fleet_packs"]} packs across two floors including the one carried. Extra bays receive the returning pack and preserve recovery space.',
          f'- Cartridge tare: {e["cartridge_tare_g"][1]:.0f} g nominal, already included once in the core hardware subtotal. Loaded 6S example cartridge: {e["nominal_loaded_cartridge_g"]:.0f} g. Stored spares add {e["spare_cartridge_mass_kg_per_station"]:.2f} kg per station, outside robot mass.',
          '- Fixed receiver and dock logic-power hardware are also included in the carried core. Battery chemistry, capacity and current capability remain open.',
          f'- The 180 W total charge-input allowance gives {e["average_charge_to_cells_w"]:.1f} W average to cells at assumed 90% conversion and 80% charge-enabled time. This is an energy ceiling; charge acceptance can reduce it.',
          '- Two resident spares give each depleted pack two robot runs to recover. Recovery includes cooling, power sharing, charge taper and balancing; the following counts assume that recovery time is actually achieved.', '',
          '| Floor task | Run min | Charge-energy margin W | Total local packs for 60 / 90 / 120 min recovery |',
          '|---|---:|---:|---:|']
    for key,case in e['floor_cases'].items():
        counts=' / '.join(str(v['minimum_local_pack_count']) for v in case['recovery_scenarios'])
        r.append(f'| {key} | {case["runtime_min"]:.0f} | {case["average_charge_margin_w"]:.1f} | {counts} |')
    r += ['', 'Positive average energy margin is necessary, not proof of uninterrupted service. Flight scheduling must budget transfer/dusting energy separately; spare packs do not extend a single airborne sortie.', '',
          f'- Battery rack/core-withdrawal allocation conflicts: {len(e["geometry_errors"])}. This check excludes detailed contacts, gripper geometry and the complete moving gantry.',
          '- See [BATTERY_EXCHANGE.md](../../../docs/BATTERY_EXCHANGE.md) for the mechanism, power handover, reserve policy and failure recovery.', '', '## Open engineering gates','']
    r+=['- '+x for x in result['open_gates']]
    r+=['','See [SYSTEM_DESIGN.md](../../../docs/SYSTEM_DESIGN.md) for interfaces, mechanisms, source limits, electrical branches and the complete station sequence.','']
    return '\n'.join(r)


def build(c):
    ground={k:assembly(c,k) for k in c['bottoms']}
    checks={k:allocation_checks(c,a['parts'],k) for k,a in ground.items()}
    power={k:power_metrics(c,k) for k in ground}
    traction={k:traction_metrics(c,a) for k,a in ground.items()}
    flights={}
    for bottom in ground:
        for variant in c['lift']['variants']:
            a=assembly(c,bottom,variant)
            flights[bottom+'_'+variant]={'assembly':a,'screen':lift_metrics(c,a,variant)}
    extended={}
    for bottom in ('low','dust'):
        a=assembly(c,bottom,pose='extended')
        extended[bottom]={'assembly':a,'floor_supported_head_required':True}
    a=assembly(c,'dust',c['lift']['default'],pose='extended')
    extended['airborne_dust']={'assembly':a,'screen':lift_metrics(c,a,c['lift']['default'])}
    modules={}
    for module in ('core','cap'):
        rows=hardware_rows(c,[p for p in c['parts'] if p['module']==module]); modules[module]=[sum(r['mass_g'][i] for r in rows) for i in range(3)]
    for key in c['bottoms']:
        rows=[r for r in ground[key]['rows'] if r['module'] not in ('core','cap','battery','payload')]
        modules[key]=[sum(r['mass_g'][i] for r in rows) for i in range(3)]
    for variant in c['lift']['variants']:
        rows=hardware_rows(c,lift_parts(c,variant)); modules[variant]=[sum(r['mass_g'][i] for r in rows) for i in range(3)]
    return dict(ground=ground,checks=checks,power=power,traction=traction,flights=flights,extended=extended,module_masses=modules,
                battery_fit={k:battery_fit(c,k) for k in c['batteries']},extension=extension_metrics(c),station=station_metrics(c),
                battery_exchange=battery_exchange_metrics(c),
                open_gates=[
                 'Automatic battery exchange is required. Cartridge contacts/retention, cell monitoring, no-break dock logic power and independently supervised rack charging need electrical/mechanical detail; extra packs are not a no-wait guarantee.',
                 'Both battery packs remain comparisons. The 8S bare body fits only after rotating it onto its 47 mm side; installed restraint/lead clearance is unverified. It exceeds the selected lift motor voltage; do not substitute it in that propulsion curve.',
                 'TriCut stationary restraint, drive end, safe speed and cutter loading are not public dimensions. The cassette and drive are sized, but the interface insert needs the supplied brush or a supplier drawing.',
                 'Actual filter body/seal and clean/loaded pressure drop are unavailable. The maximum element allocation is not a measured filter.',
                 'Guard losses, hot/low-voltage motor performance, airflow near stairs and dynamic pet avoidance are unqualified. Current sizing results are screening cases.',
                 'Cell protection, regenerative clamp and automatic mating power contacts need schematic/PCB/thermal validation; IC/connector families are not finished subsystems.',
                 'The guided push strip, printed sliding air seals and telescope retrieval force need mechanical qualification; the reach calculation does not prove jam-free deployment.',
                 'Distributed frame/fastener/wiring mass is included, but production frame geometry and complete stress/creep checks are not finished.',
                 'Owner considers 644 x 1444 mm excessive: reopen lift packing and mass. Ceiling-fan target is now 2134 mm high, 305 mm below ceiling, with about 610 mm tool reach; current horizontal dust geometry does not implement fan access.',
                 'Autonomous station motions, floor navigation and flight estimators are specified as hardware/control contracts; no claim of implemented autonomy.' ])


def main():
    c=read(); result=build(c); OUT.mkdir(exist_ok=True)
    (OUT/'system_design.json').write_text(json.dumps({'config':c,'results':result},indent=2)+'\n')
    (OUT/'system_budget.md').write_text(report(c,result))
    fields=['configuration','instance','hardware_id','module','name','qty','low_g','nominal_g','high_g','mass_basis','source','procurement','notes']
    with (OUT/'system_hardware.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fields); writer.writeheader()
        cases=list(result['ground'].items())+[(k,x['assembly']) for k,x in result['flights'].items()]
        for name,a in cases:
            for row in a['rows']:
                out={key:row[key] for key in fields if key in row}
                out.update(configuration=name,low_g=row['mass_g'][0],nominal_g=row['mass_g'][1],high_g=row['mass_g'][2]); writer.writerow(out)
    for key,a in result['ground'].items():
        for view in ('top','side'): (OUT/f'{key}_{view}.svg').write_text(svg_layout(c,a,view))
    for variant in c['lift']['variants']:
        a=result['flights']['vacuum_'+variant]['assembly']
        (OUT/f'{variant}_top.svg').write_text(svg_layout(c,a))
    for key in ('low','dust'):
        a=result['extended'][key]['assembly']
        (OUT/f'{key}_extended_top.svg').write_text(svg_layout(c,a))
    for name,rows in [('station_hardware',c['station']['hardware']),('mechanical_stock',c['stock'])]:
        with (OUT/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,list(rows[0]));writer.writeheader();writer.writerows(rows)
    station_a=dict(bottom='vacuum',top='station reservations',parts=station_parts(c),mass_g=[0,result['station']['empty_station_mass_kg']*1000,0])
    svg=svg_layout(c,station_a).replace('Everyday vacuum / drive + station reservations','Automatic station / per floor').replace('with design payload and battery.','empty machinery allowance; excludes robot and bulk contents.')
    (OUT/'station_top.svg').write_text(svg)
    (OUT/'station_layout.json').write_text(json.dumps(station_parts(c),indent=2)+'\n')
    template=ROOT/'design/system/viewer.html'
    if template.exists():
        (OUT/'system_design.html').write_text(template.read_text().replace('__DATA__',json.dumps({'config':c,'results':result}).replace('</','<\\/')))
    print(json.dumps({'ground_mass_kg':{k:[round(m/1000,3) for m in a['mass_g']] for k,a in result['ground'].items()},
                      'ground_power_w':{k:round(x['normal_w'],1) for k,x in result['power'].items()},
                      'conflicts':{k:x['errors'] for k,x in result['checks'].items()},'module_mass_kg':{k:round(x[1]/1000,3) for k,x in result['module_masses'].items()}},indent=2))
    if any(x['errors'] for x in result['checks'].values()) or any(x['allocation_errors'] for x in result['power'].values()) or any(x['screen']['geometry_errors'] for x in result['flights'].values()) or result['battery_exchange']['geometry_errors']:
        raise SystemExit('Resolve allocation errors shown in the generated report')
    return result


if __name__=='__main__':
    main()
