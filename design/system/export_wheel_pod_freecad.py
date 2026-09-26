"""J candidate solids, supplier mating check and sampled interference audit.

Optional TIDYBOT_VENDOR_CAD points to extracted goBILDA STEP downloads. Sources
and hashes are recorded; normal exports use clearly labeled wheel/hub proxies.
No STL is released: bearing fits, structural joints and stops remain unfinished.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(ROOT/'design/system'))
import build as base
import floor_support as support
import height_mounting as height
import wheel_pod as design

OUT=ROOT/'design/system/output';r=json.loads((OUT/'wheel_pod.json').read_text())
d=r['config'];h=r['configured_support'];V=App.Vector
App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)


def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(x,y,z,radius,length,axis=(1,0,0)):return Part.makeCylinder(radius,length,V(x,y,z),V(*axis))
def ring(x,y,z,ro,ri,length,axis=(1,0,0)):return cyl(x,y,z,ro,length,axis).cut(cyl(x,y,z,ri,length,axis))
def merge(shapes):
    s=shapes[0]
    for b in shapes[1:]:s=s.fuse(b)
    return s.removeSplitter()
def moving(shape,travel):
    s=shape.copy();s.rotate(V(0,145,36),V(-1,0,0),support.pose(h,travel)['angle_deg']);return s


def bracket():
    # Manufacturer-drawing reconstruction; omit bend radius and small edge radii.
    face=box(24,92.5,21.5,2,25,14.5).fuse(cyl(24,105,36,12.5,2).common(box(24,92.5,36,2,25,12.5)))
    s=face.fuse(box(24,92.5,21.5,52,25,2))
    s=s.cut(cyl(23,105,36,3.75,4))
    for dy,dz in [(-8.5,0),(8.5,0),(0,-8.5),(0,8.5)]:
        s=s.cut(cyl(23,105+dy,36+dz,1.65,4))
        if dy:s=s.cut(Part.makeCone(3.15,1.65,1.5,V(24,105+dy,36+dz),V(1,0,0)))
    for j in range(7):s=s.cut(cyl(30.4+j*6.35,105,20.5,1.65,4,(0,0,1)))
    for j in range(6):
        x=33.5+j*6.35
        for y,edge in [(94.15,92.5),(115.85,115.85)]:
            s=s.cut(cyl(x,y,20.5,1.7,4,(0,0,1)).fuse(box(x-1.7,edge,20.5,3.4,1.65,4)))
    return s.removeSplitter()


def cradle():
    pieces=[box(29,92.5,18.5,73,27,3),box(39,119.5,18.5,54,31.5,3)]
    for x in (39,83):
        pieces += [box(x,119.5,21.5,10,25.5,14.5),cyl(x,145,36,9.5,10)]
    s=merge(pieces)
    for x in (39,83):s=s.cut(cyl(x-1,145,36,5,12))
    # Open the underside of the spring cup, and remove unused motor-deck material.
    # Relief reaches through the adjacent bearing web as well as the floor;
    # cutting only the 3 mm deck leaves a collision with the rocking cup.
    s=s.cut(box(73.7,120,18,12.6,18,18))
    s=s.cut(box(46,98,18,20,14,4))
    for x in (39.85,65.25):
        for y in (94.15,115.85):s=s.cut(cyl(x,y,17.5,1.7,5,(0,0,1)))
    # Lower spring fork joined through both cheeks to the deck.
    fork=merge([box(68.7,121,16,22.6,16,2),box(68.7,123,18,5,12,10),box(86.3,123,18,5,12,10)])
    fork=fork.cut(cyl(67.7,129,24,1.6,25))
    return s.fuse(fork).removeSplitter()


def upper_fork(shim):
    s=merge([box(68.7,123,60-shim,22.6,12,2),box(68.7,123,52-shim,5,12,8),box(86.3,123,52-shim,5,12,8)])
    return s.cut(cyl(67.7,129,56-shim,1.6,25)).removeSplitter()


def spring_solids(travel,shim):
    p=design.spring_pose(h,d,travel,shim);v=p['unit_yz'];axis=(0,*v);s=d['spring'];x=s['x_mm']
    lower=p['lower_pivot_yz_mm'];upper=p['upper_pivot_yz_mm'];l=p['lower_contact_yz_mm'];u=p['upper_contact_yz_mm']
    lc=cyl(x,lower[0]-3*v[0],lower[1]-3*v[1],6,6,axis).cut(cyl(x-7,*lower,1.6,14))
    uc=cyl(x,upper[0]-3*v[0],upper[1]-3*v[1],6,6,axis).cut(cyl(x-7,*upper,1.6,14))
    lg=cyl(x,*l,s['lower_guide_od_mm']/2,s['guide_length_mm'],axis)
    ug=ring(x,*u,s['upper_guide_od_mm']/2,s['upper_guide_id_mm']/2,s['guide_length_mm'],tuple(-q for q in axis))
    spring=ring(x,*l,5,3.5,p['length_mm'],axis)
    return dict(lower_cup=lc,upper_cup=uc,lower_guide=lg,upper_guide=ug,spring_envelope=spring,
                lower_trunnion=cyl(68.7,*lower,1.5,22.6),upper_trunnion=cyl(68.7,*upper,1.5,22.6))


def nominal():
    shapes=dict(motor_bracket=bracket(),moving_cradle=cradle())
    shapes['motor_reference']=merge([cyl(26,105,36,12.5,69),cyl(23.5,105,36,3.5,2.5),cyl(13.5,105,36,2,12.5)])
    for i,(dy) in enumerate((-8.5,8.5)):
        shapes['motor_screw_'+str(i)]=Part.makeCone(3,1.5,1.5,V(24,105+dy,36),V(1,0,0)).fuse(cyl(25.5,105+dy,36,1.5,4.5))
    for j,x in enumerate((39,83)):shapes['bushing_'+str(j)]=ring(x,145,36,5,4.015,10)
    return shapes


def fixed():
    shapes={'pivot_pin':cyl(26,145,36,4,80)}
    for p in support.stock(h):
        if not p['id'].startswith('H_left_'):continue
        s=box(*p['min'],*p['size'])
        if 'hole' in p:s=s.cut(cyl(p['min'][0]-1,145,36,4.1,p['size'][0]+2))
        shapes[p['id']]=s
    for j,x in enumerate(d['pivot']['collar_min_x_mm']):
        shapes['collar_'+str(j)]=ring(x,145,36,9,4.015,9)
        shapes['collar_clearance_'+str(j)]=ring(x,145,36,11.2,4.015,9)
    return shapes


def supplier_shapes():
    path=os.environ.get('TIDYBOT_VENDOR_CAD')
    if not path:return {},{}
    path=Path(path);a=path/'1309-0016-0004 assembly.STEP';b=path/'3626-0014-0072.step'
    hub=Part.read(str(a));hub.translate(V(-35.5162,-17.9721,-30.8362))
    wheel=Part.read(str(b));wheel.rotate(V(0,0,0),V(1,0,0),-90);wheel.translate(V(0,0,8))
    # Normalized supplier axis +Z points outward; map to global -X.
    for shape in (hub,wheel):shape.rotate(V(0,0,0),V(0,1,0),-90);shape.translate(V(22,105,36))
    return dict(hub=hub,wheel=wheel),{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (a,b)}


def main():
    nom=nominal();fix=fixed();vendor,hashes=supplier_shapes()
    checks=dict(fabrication_release=False,valid_shapes={},supplier_input_hashes=hashes,
                vendor_cad_used=bool(vendor),sampled_interference=[],axial_checks=[],mass={})

    # Exact CAD mating samples include complete rotations of the rotating hub/wheel.
    if vendor:
        for deg in range(0,360,30):
            for id in ('hub','wheel'):
                shape=vendor[id].copy();shape.rotate(V(0,105,36),V(1,0,0),deg)
                for other in ('motor_bracket','motor_screw_0','motor_screw_1','moving_cradle'):
                    common=shape.common(nom[other]).Volume
                    checks['axial_checks'].append(dict(angle_deg=deg,a=id,b=other,intersection_mm3=common))

    # Deliberately enumerate only disjoint groups. Fused cradle/fork, bearing seats,
    # guides attached to cups and contacts at the cap are intended interfaces.
    for travel in (-2.5,0,2.5,5,7.5,10):
        for shim in (0,3,6):
            moving_parts={k:moving(s,travel) for k,s in nom.items()};sp=spring_solids(travel,shim)
            parts={**moving_parts,**fix,**sp,'upper_fork':upper_fork(shim)}
            pairs=[('moving_cradle',k) for k in ('H_left_cheek_outer','H_left_cheek_inner','H_left_cap','collar_clearance_0','collar_clearance_1','lower_cup','upper_cup','upper_fork')]
            pairs += [('motor_reference','upper_fork'),('motor_reference','spring_envelope'),('lower_guide','upper_guide'),('lower_guide','upper_cup'),('upper_guide','lower_cup'),('lower_cup','upper_fork'),('upper_cup','upper_fork')]
            for a,b in pairs:
                volume=parts[a].common(parts[b]).Volume
                if volume>1e-5:checks['sampled_interference'].append(dict(travel_mm=travel,shim_mm=shim,a=a,b=b,intersection_mm3=volume))

    for travel,shim,suffix in [(0,3,''),(10,6,'_bump'),(-2.5,0,'_droop')]:
        name='wheel_pod'+suffix;doc=App.newDocument(name);objects=[]
        shapes={**fix,**{k:moving(s,travel) for k,s in nom.items()},**spring_solids(travel,shim),'upper_fork':upper_fork(shim)}
        if shim:shapes['preload_shim']=box(68.7,123,62-shim,22.6,12,shim)
        if vendor:shapes.update({k:moving(s,travel) for k,s in vendor.items()})
        else:
            shapes['wheel_envelope']=moving(ring(2,105,36,36,28,24),travel)
            shapes['hub_envelope']=moving(ring(14,105,36,14,2.015,8),travel)
        for key,shape in shapes.items():
            if shape.isNull() or not shape.isValid():raise ValueError((key,travel,'invalid shape'))
            obj=doc.addObject('PartDesign::Feature',key);obj.Label=key.replace('_',' ')
            wire=key.startswith('collar_clearance') or key.endswith('_envelope')
            obj.Shape=Part.makeCompound(shape.Edges) if wire else shape
            obj.addProperty('App::PropertyString','Scope');obj.Scope='Candidate geometry; seats and connections unqualified'
            if obj.ViewObject:
                obj.ViewObject.ShapeColor=(.22,.54,.49) if key in ('moving_cradle','upper_fork') else (.6,.64,.68)
                if key=='motor_reference':obj.ViewObject.ShapeColor=(.27,.31,.37)
            objects.append(obj)
        # Context remains wireframe to avoid confusing functional bays with solids.
        c,_=height.configured(support.baseline(),support.read(),height.read())
        wanted=('battery_bay','vac_bin_left','mop_drive','sofa_extension')
        for b in ('vacuum','mop','low'):
            for p in base.reference_parts(c,b):
                if p['id'] not in wanted:continue
                key='context_'+p['id']
                if doc.getObject(key):continue
                obj=doc.addObject('PartDesign::Feature',key);obj.Shape=Part.makeCompound(box(*p['min'],*p['size']).Edges);objects.append(obj)
        doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(objects,str(OUT/(name+'.step')))
        checks['valid_shapes'][name]=len(objects);App.closeDocument(doc.Name)

    printed_ids={'moving_cradle':nom['moving_cradle'],'upper_fork':upper_fork(0)}
    for k,v in spring_solids(0,6).items():
        if k in ('lower_cup','upper_cup','lower_guide','upper_guide'):printed_ids[k]=v
    printed_ids['maximum_shim']=box(68.7,123,56,22.6,12,6)
    mass={k:s.Volume*d['mass']['printed_density_g_mm3'] for k,s in printed_ids.items()}
    mass.update(motor_bracket=d['bracket']['mass_g'],pivot_pin=r['axial']['pivot_pin_mass_g'],collars=2*d['pivot']['collar_mass_g'])
    for k in ('bush_pair_allowance_g','spring_allowance_g','fasteners_allowance_g','stop_sensor_allowance_g'):mass[k]=d['mass'][k]
    checks['mass']=dict(candidate_per_side_items_g=mass,candidate_per_side_subtotal_g=sum(mass.values()),
        includes='Moving cradle, cups, guides, upper fork/shim, pin, collars, motor bracket and allowances',
        excludes='Motor, wheel, hub, fixed cheeks/cap/frame, finished structural fastening and cable retention',
        G_pod_allowance_g=62,G_mass_replaced=False)
    checks['axial_max_intersection_mm3']=max((x['intersection_mm3'] for x in checks['axial_checks']),default=None)
    checks['scope']='18 travel/shim samples for enumerated internal pairs; 12 wheel angles for axial mating if supplier CAD supplied. Not all-pairs, continuous clearance, tolerances or structural qualification.'
    (OUT/'wheel_pod_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({k:v for k,v in checks.items() if k not in ('axial_checks','sampled_interference')},indent=2))
    print('Interferences:',checks['sampled_interference'])


# FreeCAD invokes command-line Python files under their basename.
if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
