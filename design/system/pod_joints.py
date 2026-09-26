"""K stop mechanics and explicit assembly-mass replacement boundary."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import build as base
import floor_support as H
import height_mounting as I
import wheel_pod as J

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'design/system/output'


def read():return json.loads((ROOT/'config/pod_joints.json').read_text())


def slot(h,k):
    s=k['stop'];y,z=s['fixed_yz_mm'];py,pz=h['wheel']['pivot_yz_mm']
    radius=math.hypot(y-py,z-pz);phi=math.atan2(z-pz,y-py)
    gap=(s['slot_width_mm']-s['sleeve_od_mm'])/2
    if gap<=0:raise ValueError('Positive sleeve/slot running clearance required')
    trim=2*math.asin(gap/(2*radius))
    limits=[math.radians(H.pose(h,t)['angle_deg']) for t in (-h['wheel']['droop_candidate_mm'],h['wheel']['bump_mm'])]
    start=phi+limits[0]+trim;end=phi+limits[1]-trim
    if start>=end:raise ValueError('Slot clearance consumes travel')
    return dict(radius_mm=radius,phi_rad=phi,radial_gap_mm=gap,end_trim_rad=trim,
        start_rad=start,end_rad=end,centreline_length_mm=radius*(end-start),
        ends_yz_mm=[[py+radius*math.cos(a),pz+radius*math.sin(a)] for a in (start,end)],
        nominal_contact_travel_mm=[-h['wheel']['droop_candidate_mm'],h['wheel']['bump_mm']])


def stop_contact(h,k,which):
    s=slot(h,k);t=s['nominal_contact_travel_mm'][which]
    end=H.rotate_yz(h,*s['ends_yz_mm'][which],t);fixed=k['stop']['fixed_yz_mm']
    delta=[a-b for a,b in zip(fixed,end)];length=math.hypot(*delta)
    n=[v/length for v in delta];py,pz=h['wheel']['pivot_yz_mm']
    lever=abs((fixed[0]-py)*n[1]-(fixed[1]-pz)*n[0])
    return dict(travel_mm=t,normal_yz=n,contact_lever_mm=lever,cap_distance_mm=length)


def load_screen(h,j,k,shim_values=None,cap_branch_n=85):
    stop=stop_contact(h,k,1);ny,nz=stop['normal_yz'];w=h['wheel'];cases=[]
    # Flip the contact normal to give a resisting moment on the moving arm.
    y,z=k['stop']['fixed_yz_mm'];py,pz=w['pivot_yz_mm']
    if (y-py)*nz-(z-pz)*ny<0:ny,nz=-ny,-nz
    for shim in (range(7) if shim_values is None else shim_values):
        sp=J.spring_pose(h,j,w['bump_mm'],shim);pose=H.pose(h,w['bump_mm'])
        for fh in (-25,25):
            fs=sp['force_n'];fy=-fs*sp['unit_yz'][0];fz=-fs*sp['unit_yz'][1]
            torque=150*(py-pose['axle_y_mm'])+fh*36-fs*sp['moment_arm_mm']
            force=torque/stop['contact_lever_mm']
            # Wheel load gives negative X moment; stop force gives positive.
            xs=[14,80,k['stop']['moving_plate_min_x_mm']+k['stop']['moving_plate_thickness_mm']/2]
            ar=[];pin=[]
            for loads in ([fh,fy,force*ny],[150,fz,force*nz]):
                a=H.simply_supported_loads(xs,loads,w['bushing_centres_x_mm']);ar.append(a)
                pin.append(H.simply_supported_loads(w['bushing_centres_x_mm'],[-v for v in a['reactions_n']],w['fixed_support_centres_x_mm']))
            m=math.hypot(*(p['max_moment_nmm'] for p in pin))
            bearing=max(math.hypot(*v) for v in zip(*(a['reactions_n'] for a in ar)))
            # Local inner-rail group: pin reaction plus sleeve reaction, with
            # either sign of an extra 85 N cap load at the spring's Y station.
            # This is a declared load bound, not a full frame equilibrium model.
            joint=[]
            for cap in (-cap_branch_n,cap_branch_n):
                fy_pin=-pin[0]['reactions_n'][1];fz_pin=-pin[1]['reactions_n'][1]
                fy_stop=-force*ny;fz_stop=-force*nz
                total_y=fy_pin+fy_stop;total_z=fz_pin+fz_stop+cap
                moment_joint=(145-146.25)*fz_pin-(36-57.5)*fy_pin+(y-146.25)*fz_stop-(z-57.5)*fy_stop+(129-146.25)*cap
                joint.extend(math.hypot(total_y/2,total_z/2+sign*moment_joint/8.5) for sign in (-1,1))
            cases.append(dict(shim_mm=shim,fore_aft_n=fh,stop_force_n=force,pin_moment_nmm=m,bearing_reaction_n=bearing,
                max_inner_joint_bolt_n=max(joint)))
    f=max(v['stop_force_n'] for v in cases);moment=max(v['pin_moment_nmm'] for v in cases)
    steel_bend=32*moment/(math.pi*8**3)
    arm=103-(k['stop']['moving_plate_min_x_mm']+k['stop']['moving_plate_thickness_mm']/2)
    screw_bend=32*f*arm/(math.pi*k['stop']['bolt_root_diameter_mm']**3)
    # Explicit narrow-strip analogy; no credit for sleeve reinforcing bolt or tray plate action.
    tray=[]
    for t in (3,4):
        stress=6*150*k['tray']['strip_cantilever_mm']/(k['tray']['net_strip_width_mm']*t*t)
        deflection=150*k['tray']['strip_cantilever_mm']**3/(3*69000*(k['tray']['net_strip_width_mm']*t**3/12))
        tray.append(dict(thickness_mm=t,bending_mpa=stress,deflection_mm=deflection,passes=stress<=120 and deflection<=.5))
    joint_force=max(v['max_inner_joint_bolt_n'] for v in cases)
    # Integrated front-edge ligament through the countersink and straight bore.
    edge=142-137.25;cone=1.95;t=3.175
    tear_area=2*(cone*(edge-(4.15+2.2)/2)+(t-cone)*(edge-2.2))
    joint=dict(max_bolt_force_n=joint_force,M3_shear_mpa=joint_force/5.03,M4_shear_mpa=joint_force/8.78,
        M3_passes=joint_force/5.03<=120,M4_passes=joint_force/8.78<=120,
        angle_countersink_edge_shear_mpa=joint_force/tear_area,angle_edge_passes=joint_force/tear_area<=80,
        rail_rear_edge_shear_mpa=joint_force/(2*3*(156-150.5-2.2)),
        cap_branch_bound_n=cap_branch_n,
        scope=f'Two M4 bolts at Y=142/150.5, Z=57.5; inner rail/cheek to Y=156; angle front Y=137.25. Includes full +/-{cap_branch_n:g} N cap branch bound. Other frame joints, preload and fatigue remain unqualified.')
    return dict(cases=cases,max_stop_force_n=f,pivot_bending_mpa=steel_bend,pivot_passes=steel_bend<=150,inner_rail_joint=joint,
        stop_bolt_bending_mpa=screw_bend,stop_bolt_passes=screw_bend<=150,
        slot_bearing_mpa=f/(k['stop']['sleeve_od_mm']*k['stop']['moving_plate_thickness_mm']),
        slot_edge_shear_mpa=f/(2*k['stop']['edge_ligament_mm']*k['stop']['moving_plate_thickness_mm']),
        bearing_block_peak_reaction_n=max(v['bearing_reaction_n'] for v in cases),tray_strip=tray,
        scope='Static hand-calculation screens. No claim of complete fatigue, plate torsion, thread/preload or motor-bracket qualification.')


def replaced_layout(g,mass,cg):
    c=deepcopy(g);c['hardware']['pod'].update(name='K complete suspension pod with fixed local supports',mass_g=mass,
        mass_basis='K modeled solids/catalog items plus itemized fasteners and completion reserve; motor/wheel/hub excluded')
    # Separate the motor from the pod so their mass centres are not conflated.
    for p in c['parts']:
        if p['id'] not in ('pod_left','pod_right'):continue
        side=p['id'].split('_')[1];p['hardware']=[{'id':'drive_motor','qty':1}]
        p['mass_cg_mm']=[60.5 if side=='left' else 214.5,105,36]
    for side in ('left','right'):
        xyz=[cg[0] if side=='left' else 275-cg[0],cg[1],cg[2]]
        c['parts'].append(dict(id='K_pod_'+side,module='drive',label='K complete suspension pod',min=[0,0,0],size=[1,1,1],
            mass_cg_mm=xyz,hardware=[{'id':'pod','qty':1}],shape='distributed',group='drive',notes='Mass-only overlay; see K CAD'))
    return c


def study(cad=None):
    k=read();j=J.read();h=J.configured(H.read(),j);g=H.baseline()
    r=dict(revision=k['revision'],config=k,slot=slot(h,k),contacts=[stop_contact(h,k,i) for i in (0,1)],loads=load_screen(h,j,k),
           fabrication_release=False,full_structural_qualification=False,
           input_hashes={p:hashlib.sha256((ROOT/'config'/p).read_bytes()).hexdigest() for p in
            ('system_design.json','core_partition.json','frame_joints.json','floor_support.json','height_mounting.json','wheel_pod.json','pod_joints.json')})
    if cad:
        c=replaced_layout(g,cad['mass']['per_pod_interval_g'],cad['mass']['cg_mm'])
        r['mass']=cad['mass'];r['ground']={}
        for b in ('vacuum','mop','low'):
            old=base.assembly(g,b);new=base.assembly(c,b)
            r['ground'][b]=dict(before_g=old['mass_g'],after_g=new['mass_g'],cg_mm=new['cg_mm'],
                nominal_delta_g=new['mass_g'][1]-old['mass_g'][1])
        r['preload']=J.preload(h,j,c)
        r['mass_boundary']='Only G pod entries are replaced; motors kept once and separated for CG. All other G hardware, including bottom-frame and unfinished carrier allowances, remains. I changes are not silently combined.'
    return r


def main():
    path=OUT/'pod_joints_cad_checks.json';cad=json.loads(path.read_text()) if path.exists() else None
    r=study(cad);(OUT/'pod_joints.json').write_text(json.dumps(r,indent=2)+'\n')
    lines=['# K connected suspension candidate','',r['config']['status'],'',
        'One closed curved slot and a fixed steel sleeve provide both travel stops. The slot endpoints are shortened to account for nominal sleeve/slot clearance. No spring or printed part serves as the hard stop.','',
        f"Nominal travel: −2.5 to +10 mm. Slot width 8.5 mm around an 8 mm sleeve; each endpoint is trimmed by {math.degrees(r['slot']['end_trim_rad']):.3f}°.",'',
        f"Maximum screened stop force {r['loads']['max_stop_force_n']:.1f} N; 8 mm pivot bending {r['loads']['pivot_bending_mpa']:.1f} MPa; stop-screw root bending {r['loads']['stop_bolt_bending_mpa']:.1f} MPa.",'',
        f"The local inner-rail group reaches {r['loads']['inner_rail_joint']['max_bolt_force_n']:.1f} N per bolt in the declared load cases. M3 shear screen: {r['loads']['inner_rail_joint']['M3_passes']}; M4: {r['loads']['inner_rail_joint']['M4_passes']}. The front angle edge includes the countersink's reduction in ligament.",'',
        '| Tray strip | Bending | Deflection | Screen |','|---|---:|---:|---|']
    for v in r['loads']['tray_strip']:lines.append(f"| {v['thickness_mm']} mm | {v['bending_mpa']:.1f} MPa | {v['deflection_mm']:.3f} mm | {v['passes']} |")
    lines+=['','The 4 mm aluminum tray is selected for this conservative strip analogy. It does not prove the complete two-dimensional plate, motor bracket, local threads or fatigue.','']
    if cad:
        lines += [f"Complete pod estimate: {r['mass']['per_pod_interval_g'][1]:.1f} g nominal per side, including fixed local supports. Earlier J's 106.2 g excluded the fixed cap/cheeks/frame joints.",'',r['mass_boundary'],'',
            '| Assembly | G nominal | K nominal | Change |','|---|---:|---:|---:|']
        for b,v in r['ground'].items():lines.append(f"| {b} | {v['before_g'][1]/1000:.3f} kg | {v['after_g'][1]/1000:.3f} kg | +{v['nominal_delta_g']:.1f} g |")
        lines+=['','| Bottom | Required left shim | Required right shim | Existing 0–6 mm range |','|---|---:|---:|---|']
        for b,v in r['preload'].items():
            vals=['–'.join(f'{x:.2f}' for x in q)+' mm' for q in v['required_shim_ranges_mm']]
            lines.append(f"| {b} | {vals[0]} | {vals[1]} | {v['within_adjuster_range']} |")
    lines+=['','Do not extend the shim range without rechecking spring coil bind and guide bottoming. The spring remains a sourcing target. The mass update does not establish flight endurance or change battery selection.','',
        'See [design record](../../../docs/POD_JOINTS_AND_STOPS.md) and [CAD checks](pod_joints_cad_checks.json) for modeled fasteners, clearance limits and unfinished work.']
    (OUT/'pod_joints.md').write_text('\n'.join(lines)+'\n')
    if cad:(OUT/'pod_joints.html').write_text((ROOT/'design/system/pod_joints_viewer.html').read_text().replace('__MODEL__',json.dumps(r)))
    print('K calculations written', 'with CAD mass' if cad else 'awaiting CAD mass')


if __name__=='__main__':main()
