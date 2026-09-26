"""P local solids and sampled envelope checks. Does not release print files."""
import itertools
import json
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'design/system'))
import head_coupling as P
import fixed_drive as N
import export_fixed_drive_freecad as EN
V=App.Vector


def box(p,s):return Part.makeBox(*s,V(*p))
def cylinder(p,r,l,axis=(1,0,0)):return Part.makeCylinder(r,l,V(*p),V(*axis))
def mirror(s):return s.mirror(V(137.5,0,0),V(1,0,0))
def ring(p,s,inner):
    x,y,z=p;w,t,h=s;wi,hi=inner
    return box(p,s).cut(box([x+(w-wi)/2,y-1,z+(h-hi)/2],[wi,t+2,hi]))


def geometry(d):
    body={};tool={};c=d['cheeks'];g=d['guide_pins'];l=d['locks'];a=d['air'];e=d['electrical']
    for side in range(2):
        plate=box(d['plates']['mins'][0],d['plates']['size'])
        for y in g['y']:plate=plate.cut(cylinder([23,y,g['z']],1.65,5))
        plate=plate.cut(cylinder([23,l['y'],l['z']],l['body_hole_diameter']/2,5))
        cheek=box(c['left_min'],c['size']);closed=c['closed_end_y']-(c['right_end_relief_mm'] if side else 0)
        cut=cylinder([22,closed,c['slot_z']],c['slot_radius'],3).fuse(box([22,closed,c['slot_z']-c['slot_radius']],[3,84-closed,2*c['slot_radius']]))
        cheek=cheek.cut(cut).cut(cylinder([22,l['y'],l['z']],l['hole_diameter']/2,4))
        parts={'receiver':plate,'lock_head':cylinder([l['left_pin_min_x'],l['y'],l['z']],l['pin_diameter']/2,l['pin_length']),
            'lock_actuating_shank':cylinder([l['left_pin_min_x']-l['thread_length'],l['y'],l['z']],l['thread_diameter']/2,l['thread_length'])}
        for i,y in enumerate(g['y']):
            parts[f'guide_sleeve_{i}']=cylinder([g['left_sleeve_start_x'],y,g['z']],2,g['sleeve_length']).cut(cylinder([22,y,g['z']],1.6,4))
            parts[f'guide_washer_{i}']=cylinder([21.7,y,g['z']],g['washer_od']/2,.5).cut(cylinder([21.6,y,g['z']],1.6,.7))
            # Flat head is flush with the rail's inner face at X28.
            screw=cylinder([18,y,g['z']],1.5,10)
            screw=screw.fuse(Part.makeCone(1.5,3,1.5,V(26.5,y,g['z']),V(1,0,0)))
            parts[f'guide_screw_{i}']=screw
        for id,s in parts.items():body[f'{"right" if side else "left"}_{id}']=mirror(s) if side else s
        tool[f'{"right" if side else "left"}_cheek']=mirror(cheek) if side else cheek
        riser=box(d['rear_risers']['left_min'],d['rear_risers']['size'])
        tool[f'{"right" if side else "left"}_riser']=mirror(riser) if side else riser
        shoe=box(d['end_shoes']['left_min'],d['end_shoes']['size'])
        tool[f'{"right" if side else "left"}_end_shoe']=mirror(shoe) if side else shoe
    q=d['crossmember'];x,y,z=q['min'];le,w,h=q['size'];t=q['wall']
    tool['crossmember']=box(q['min'],q['size']).cut(box([x-1,y+t,z+t],[le+2,w-2*t,h-2*t]))
    # Shoe overlaps the tube only as a fastening reservation: trim to actual
    # outside space so it is not shown as two occupied pieces of material.
    for id in ('left_end_shoe','right_end_shoe'):tool[id]=tool[id].cut(tool['crossmember'])
    cx,cz=a['centre_xz'];w,h=a['outer'];t=a['flange_thickness']
    tool['air_flange']=ring([cx-w/2,a['tool_flange_y'],cz-h/2],[w,t,h],a['inner'])
    body['air_flange']=ring([cx-w/2,a['body_flange_y'],cz-h/2],[w,t,h],a['inner'])
    sy=a['body_flange_y']+t
    body['air_stub']=ring([cx-19,sy,cz-14],[38,a['body_stub_end_y']-sy,28],a['inner'])
    gw,gh=a['gasket_outer'];body['gasket']=ring([cx-gw/2,a['tool_flange_y']+t,cz-gh/2],[gw,a['gasket_compressed_t'],gh],a['gasket_inner'])
    ey=e['body_board_front_y'];pad_y=ey-e['free_height_mm']+e['nominal_compression_mm']
    body['contact_pcb']=box(e['board_min'],e['board_size'])
    tool['target_pcb']=box([e['board_min'][0],pad_y-e['target_board_t'],e['board_min'][2]],[e['board_size'][0],e['target_board_t'],e['board_size'][2]])
    # These are envelopes, not reconstructed internal contact mechanisms.
    for i,(x,z) in enumerate(itertools.product(e['pin_x'],e['pin_z'])):
        body['contact_'+str(i)]=cylinder([x,pad_y,z],1.2,ey-pad_y,(0,1,0))
    return body,tool


def context(d):
    p=N.M.prepare('vacuum');out={}
    for v in p['parts']:
        if v.get('shape')=='distributed' or v.get('parent'):continue
        if v['id']=='vac_flex':continue # active flexible joint cannot be a solid box here
        if v['id'].startswith(('H_left_cheek','H_right_cheek','H_left_cap','H_right_cap')):continue
        v=dict(v,min=v['min'][:],size=v['size'][:])
        if v['id']=='H_front_bridge':v['min'][2]+=d['bridge_shift_z_mm']
        if v['id']=='vac_duct':v['size'][1]-=d['air']['body_stub_end_y']-v['min'][1];v['min'][1]=d['air']['body_stub_end_y']
        if v['id'].startswith('H_inner_rail_'):v['size'][1]=130-v['min'][1]
        s=box(v['min'],v['size'])
        if v['id'] in ('H_left_rail','H_right_rail'):
            for y in d['guide_pins']['y']:
                cut=cylinder([23,y,76],1.65,6).fuse(Part.makeCone(1.5,3.1,1.6,V(26.4,y,76),V(1,0,0)))
                s=s.cut(mirror(cut) if v['id']=='H_right_rail' else cut)
            cut=cylinder([23,d['locks']['y'],d['locks']['z']],d['locks']['body_hole_diameter']/2,6)
            s=s.cut(mirror(cut) if v['id']=='H_right_rail' else cut)
        out[v['id']]=s
    return p,out


def main():
    d=P.read();body,tool=geometry(d);p,ctx=context(d)
    # R integration found that P's risers overlapped the wheel envelope. Keep
    # actual N stock/envelopes in P's own seated and withdrawal regression checks.
    ctx.update(EN.geometry(N.read()))
    checks=dict(fabrication_release=False,valid_solids={},context_intersections=[],internal_intersections=[],head_motion_intersections=[],withdrawal_intersections=[],scope='Local solids; contact internals are envelopes. Guide fasteners are simplified. Springs, pull nuts, latch supports, carrier-to-head compliance, air-flange/PCB brackets, active flex and full wiring remain allowances. No full load or continuous-motion qualification.')
    combined={**{'body_'+k:v for k,v in body.items()},**{'tool_'+k:v for k,v in tool.items()}}
    checks['minimum_carrier_wheel_gap_mm']=min(s.distToShape(w)[0] for s in tool.values()
        for name,w in ctx.items() if 'wheel_envelope' in name)
    for id,s in combined.items():
        checks['valid_solids'][id]=s.isValid() and not s.isNull()
        if not checks['valid_solids'][id]:raise ValueError('Invalid '+id)
        for other,t in ctx.items():
            volume=s.common(t).Volume
            if volume>1e-5:checks['context_intersections'].append(dict(part=id,context=other,volume_mm3=volume))
    for (id,s),(other,t) in itertools.combinations(combined.items(),2):
        vol=s.common(t).Volume
        if vol>1e-5:checks['internal_intersections'].append(dict(a=id,b=other,volume_mm3=vol))
    pp,aa=N.nominal_mass('vacuum',N.read());poses=N.terrain('vacuum',pp,aa,N.read())+[dict(q_mm=16,normal=[0,0,1],state='raised level')]
    heads=[v for v in p['parts'] if v['id'] in ('vac_head','vac_head_drive')]
    minimum_head_gap=1e9;minimum_head_pair=None
    for num,pose in enumerate(poses):
        for v in heads:
            rotation=N.M.rotation(pose['normal']);ref=p['M']['modules']['vacuum']['reference_mm']
            matrix=App.Matrix()
            for i in range(3):
                for j in range(3):setattr(matrix,f'A{i+1}{j+1}',rotation[i][j])
                setattr(matrix,f'A{i+1}4',ref[i]+(pose['q_mm'] if i==2 else 0)-sum(rotation[i][j]*ref[j] for j in range(3)))
            s=box(v['min'],v['size']);s.transformShape(matrix,False)
            for id,t in combined.items():
                gap=s.distToShape(t)[0]
                if gap<minimum_head_gap:
                    minimum_head_gap=gap;minimum_head_pair=dict(pose=num,state=pose['state'],head=v['id'],part=id)
                vol=s.common(t).Volume
                if vol>1e-5:checks['head_motion_intersections'].append(dict(pose=num,state=pose['state'],head=v['id'],part=id,volume_mm3=vol))
    # Check the actual sliding solids at 1 mm intervals. Retract both lock keys
    # before the first movement; their full stroke cannot be inferred from one pose.
    unlocked={id:s.copy() for id,s in body.items()}
    for id,s in unlocked.items():
        if 'lock_' in id:s.translate(V(-d['locks']['withdrawal_mm'] if id.startswith('left') else d['locks']['withdrawal_mm'],0,0))
    fixed={**{'body_'+id:s for id,s in unlocked.items()},**{id:s for id,s in ctx.items() if id not in ('vac_head','vac_head_drive')}}
    movable={**tool,**{id:ctx[id] for id in ('vac_head','vac_head_drive')}}
    for dist in range(d['withdrawal_mm']+1):
        for id,original in movable.items():
            s=original.copy();s.translate(V(0,-dist,0))
            for other,t in fixed.items():
                # Soft seal compression/unloading and pogo motion are not rigid
                # body sliding collisions. Contact bank stays on the rear face.
                if other=='body_gasket' or other.startswith('body_contact_'):continue
                if s.BoundBox.intersect(t.BoundBox):
                    vol=s.common(t).Volume
                    if vol>1e-5:checks['withdrawal_intersections'].append(dict(distance_mm=dist,tool=id,fixed=other,volume_mm3=vol))
    checks['head_pose_count']=len(poses);checks['withdrawal_samples']=d['withdrawal_mm']+1
    checks['minimum_sampled_head_gap_mm']=minimum_head_gap
    checks['minimum_sampled_head_pair']=minimum_head_pair
    checks['source_fingerprint']=P.source_fingerprint()
    checks['cheek_cad_mass_g']=sum(tool[id].Volume for id in ('left_cheek','right_cheek'))*d['material_g_mm3']['steel']
    for dist in (0,d['withdrawal_mm']):
        doc=App.newDocument('head_coupling_'+str(dist));objects=[]
        for group,parts in [('body',body if dist==0 else unlocked),('tool',movable),('context',ctx)]:
            for id,original in parts.items():
                if group=='context' and id in ('vac_head','vac_head_drive'):continue
                s=original.copy()
                if group=='tool':s.translate(V(0,-dist,0))
                obj=doc.addObject('PartDesign::Feature',group+'_'+id)
                obj.Shape=Part.makeCompound(s.Edges) if group=='context' else s
                obj.addProperty('App::PropertyString','Scope');obj.Scope=checks['scope'];objects.append(obj)
                if obj.ViewObject:obj.ViewObject.ShapeColor={'body':(.2,.6,.6),'tool':(.9,.6,.25),'context':(.6,.65,.7)}[group]
        doc.recompute();doc.saveAs(str(P.OUT/(doc.Name+'.FCStd')));Part.export(objects,str(P.OUT/(doc.Name+'.step')));App.closeDocument(doc.Name)
    (P.OUT/'head_coupling_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({k:v for k,v in checks.items() if k!='valid_solids'},indent=2))


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
