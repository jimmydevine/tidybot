"""K nominal connected hardware; no print release. Run from repository root."""
import csv
import json
import math
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve();sys.path.insert(0,str(ROOT/'design/system'))
import export_wheel_pod_freecad as old
import pod_joints as K
import wheel_pod as J
import floor_support as H
import height_mounting as I
import build as base
V=App.Vector;box=old.box;cyl=old.cyl;ring=old.ring;merge=old.merge
OUT=ROOT/'design/system/output';k=K.read();j=J.read();h=J.configured(H.read(),j);s=K.slot(h,k)
rho={'aluminum':.0027,'steel':.00785,'printed':.00127}


def arc_band(x,width):
    """Exact planar annular sector plus round caps, extruded along X."""
    radius=s['radius_mm'];a,b=s['start_rad'],s['end_rad'];r=width/2
    def point(rr,t):return V(x,145+rr*math.cos(t),36+rr*math.sin(t))
    edges=[Part.Arc(point(radius+r,a),point(radius+r,(a+b)/2),point(radius+r,b)).toShape(),
        Part.makeLine(point(radius+r,b),point(radius-r,b)),
        Part.Arc(point(radius-r,b),point(radius-r,(a+b)/2),point(radius-r,a)).toShape(),
        Part.makeLine(point(radius-r,a),point(radius+r,a))]
    sh=Part.Face(Part.Wire(edges)).extrude(V(k['stop']['moving_plate_thickness_mm'],0,0))
    for y,z in s['ends_yz_mm']:sh=sh.fuse(cyl(x,y,z,r,k['stop']['moving_plate_thickness_mm']))
    return sh.removeSplitter()


def hardware(shim):
    p={};fasteners=[]
    def add(id,shape,material,moving=False,scope='Candidate metal/printed part; tolerances and strength qualification incomplete'):
        p[id]=dict(shape=shape,material=material,moving=moving,scope=scope)
    def drill(ids,start,axis,r,length):
        for id in ids:p[id]['shape']=p[id]['shape'].cut(Part.makeCylinder(r,length,V(*start),V(*axis)))
    def bolt(id,start,axis,length,grip,parts,diam=3,csk=False,threaded=False,nut_height=2.4):
        # 'start' is the bearing plane for pan heads, outside flush plane for CSK.
        v=V(*axis);a=V(*start);rad=diam/2
        sh=Part.makeCylinder(rad,length,a,v)
        if csk:
            sh=sh.fuse(Part.makeCone(diam,rad,rad,a,v))
        else:sh=sh.fuse(Part.makeCylinder(diam,2.4,a-v*2.4,v))
        moving=p[parts[0]]['moving'];add(id,sh,'steel',moving,'Fastener envelope; thread geometry omitted')
        drill(parts[:-1] if threaded else parts,list(a-v),axis,rad+.2,length+2)
        if threaded:drill([parts[-1]],list(a-v),axis,1.25,length+2)  # M3 x 0.5 tap-drill representation
        if csk:
            # Only the entry member receives a countersink.
            p[parts[0]]['shape']=p[parts[0]]['shape'].cut(Part.makeCone(diam+.15,rad+.2,rad-.05,a,v))
        if not threaded:
            w=a+v*grip
            washer=Part.makeCylinder(diam,.5,w,v).cut(Part.makeCylinder(rad+.2,.5,w,v))
            add(id+'_washer',washer,'steel',moving,'Washer envelope')
            # Hex prism, oriented with flats in local Y/Z before axis transform.
            pts=[V(0,(diam*1.833/math.sqrt(3))*math.cos(q*math.pi/3),(diam*1.833/math.sqrt(3))*math.sin(q*math.pi/3)) for q in range(6)]
            face=Part.Face(Part.makePolygon(pts+[pts[0]]));nut=face.extrude(V(nut_height,0,0))
            nut=nut.cut(cyl(0,0,0,rad+.1,nut_height));nut.rotate(V(0,0,0),App.Rotation(V(1,0,0),v).Axis,App.Rotation(V(1,0,0),v).Angle*180/math.pi);nut.translate(w+v*.5)
            add(id+'_nut',nut,'steel',moving,'Nut envelope; locking method unselected')
        fasteners.append(dict(id=id,diameter_mm=diam,length_mm=length,grip_mm=grip,threaded_receiver=threaded,moving=moving,members=parts))

    tray=box(29,92.5,17.5,79,62,4)
    tray=tray.cut(box(68,122,17,24,14,5))
    tray=tray.cut(box(46,98,17,20,14,5))
    add('tray',tray,'aluminum',True)
    for n,x in enumerate((39,83)):
        sh=box(x,136,21.5,10,18,23.5).cut(cyl(x-1,145,36,5,12))
        add('bearing_block_'+str(n),sh,'aluminum',True)
        add('bushing_'+str(n),ring(x,145,36,5,4.015,10),'printed',True,'igus bushing geometry, mass covered by catalog allowance')
        for yy in (140,150):bolt('bearing_bolt_'+str(n)+'_'+str(yy),(x+5,yy,17.5),(0,0,1),10,4,['tray','bearing_block_'+str(n)],csk=True,threaded=True)
    add('motor_bracket',old.bracket(),'aluminum',True,'Pololu 2676 drawing reconstruction; 8.5 g catalog mass used')
    for id,shape in old.nominal().items():
        if id.startswith('motor_screw'):add(id,shape,'steel',True,'J flush motor screw envelope')
    for x in (39.85,65.25):
        for yy in (94.15,115.85):bolt('motor_foot_'+str(x)+'_'+str(yy),(x,yy,23.5),(0,0,-1),12,6,['motor_bracket','tray'])

    fork=merge([box(62,121,15,36,16,2.5),box(68.7,123,17.5,5,12,10.5),box(86.3,123,17.5,5,12,10.5)])
    fork=fork.cut(cyl(67.7,129,24,1.6,25));add('lower_fork',fork,'printed',True)
    for x in (65,94.5):bolt('lower_fork_bolt_'+str(x),(x,129,15),(0,0,1),8,2.5,['lower_fork','tray'],csk=True,threaded=True)

    xx=k['stop']['moving_plate_min_x_mm']
    stopplate=arc_band(xx,k['stop']['slot_width_mm']+2*k['stop']['edge_ligament_mm']).fuse(box(xx,111,21.5,3,43,18.5))
    stopplate=stopplate.cut(arc_band(xx,k['stop']['slot_width_mm'])).cut(cyl(97,145,36,12.2,8))
    add('stop_arm',stopplate.removeSplitter(),'aluminum',True)
    angle=merge([box(101.5,119,21.5,2,35,8),box(101.5,119,21.5,6.5,35,2)]).cut(cyl(97,145,36,12.2,12))
    add('stop_arm_angle',angle,'aluminum',True,'10 mm angle trimmed to 8 / 6.5 mm legs; radii unmodeled')
    for yy in (123,132):
        bolt('arm_angle_horizontal_'+str(yy),(103.5,yy,25.5),(-1,0,0),6,2,['stop_arm_angle','stop_arm'],csk=True,threaded=True)
    for yy in (138,150):
        bolt('arm_angle_vertical_'+str(yy),(104.5,yy,23.5),(0,0,-1),10,6,['stop_arm_angle','tray'],csk=True)

    for id,x in [('outer',26),('inner',103)]:
        cheek=box(x,132,28,3,24 if id=='inner' else 22,34)
        if id=='inner':
            cheek=cheek.fuse(box(x,113,37,3,22,18))
            cheek=cheek.cut(box(x-1,131,27,5,7,7))  # Clear moving angle; pivot-hole ligament remains intact.
            cheek=cheek.cut(box(x-1,152,27,5,5,3))
        cheek=cheek.cut(cyl(x-1,145,36,4.1,5));add('cheek_'+id,cheek,'aluminum')
    add('cap',box(26,109,62,80,45,3),'aluminum')
    add('outer_floor_rail',box(26,13,65,2,140,21),'context',False,'Existing H frame route; retained frame allowance, excluded from pod mass')
    add('inner_floor_rail',box(106,85,54,3,71,11),'context',False,'H frame route extended to Y=156 for rear-bolt edge distance; retained frame allowance')
    add('outer_cap_angle',merge([box(29,132,52,2,22,10),box(29,132,60,10,22,2)]),'aluminum')
    add('inner_cap_angle',merge([box(99.825,137.25,52,3.175,18.75,10),box(93,137.25,58.825,10,18.75,3.175)]),'aluminum',False,'1/2 inch x 1/2 inch x 1/8 inch angle, legs trimmed to 10 mm; tapped cap joint')
    add('outer_rail_angle',merge([box(28,132,65,2,22,10),box(28,132,65,10,22,2)]),'aluminum')
    for yy in (136,150):
        bolt('outer_cheek_joint_'+str(yy),(26,yy,56.5),(1,0,0),10,5,['cheek_outer','outer_cap_angle'],csk=True)
        bolt('outer_rail_joint_'+str(yy),(26,yy,71),(1,0,0),8,4,['outer_floor_rail','outer_rail_angle'],csk=True)
    for yy in (142,150.5):bolt('inner_cheek_joint_'+str(yy),(99.825,yy,57.5),(1,0,0),16,9.175,['inner_cap_angle','cheek_inner','inner_floor_rail'],diam=4,csk=True,nut_height=3.2)
    bolt('outer_stack_joint',(35,143,67),(0,0,-1),12,7,['outer_rail_angle','cap','outer_cap_angle'])
    bolt('inner_cap_joint',(97,146.5,65),(0,0,-1),6,3,['cap','inner_cap_angle'],csk=True,threaded=True)
    upper=old.upper_fork(shim).fuse(box(66,133,60-shim,26,12,2))
    add('upper_fork',upper,'printed')
    if shim:add('preload_shim',box(66,123,62-shim,26,22,shim),'printed')
    for x in (70,88.5):bolt('upper_fork_bolt_'+str(x),(x,141,65),(0,0,-1),10+shim,5+shim,['cap']+(['preload_shim'] if shim else [])+['upper_fork'],csk=True)
    add('pivot_pin',cyl(26,145,36,4,80),'steel')
    for n,x in enumerate((29.5,93.5)):
        add('collar_'+str(n),ring(x,145,36,9,4.015,9),'aluminum',False,'Ruland MCL-8-A: 5.1 g catalog mass, clamp screw not modeled')
        add('collar_clearance_'+str(n),ring(x,145,36,11.2,4.015,9),'envelope')

    # Captured sleeve stack. The thin nut is not assumed to be self-locking.
    yy,zz=k['stop']['fixed_yz_mm']
    add('stop_sleeve',ring(97,yy,zz,4,2.65,6),'steel')
    add('stop_washer',ring(96.2,yy,zz,5,2.65,.8),'steel')
    add('stop_nut',ring(93.5,yy,zz,8/math.sqrt(3),2.5,2.7),'steel',False,'Circumscribed thin-nut envelope, mass conservatively uses cylinder')
    screw=Part.makeCone(5,2.5,2.5,V(106,yy,zz),V(-1,0,0)).fuse(cyl(92,yy,zz,2.5,11.5))
    add('stop_screw',screw,'steel')
    drill(['cheek_inner'],(102,yy,zz),(1,0,0),2.75,5)
    p['cheek_inner']['shape']=p['cheek_inner']['shape'].cut(Part.makeCone(5.15,2.75,2.4,V(106,yy,zz),V(-1,0,0)))
    return p,fasteners


def posed(travel,shim):
    parts,bolts=hardware(shim)
    for row in parts.values():
        if row['moving']:row['shape']=old.moving(row['shape'],travel)
    for key,shape in old.spring_solids(travel,shim).items():parts[key]=dict(shape=shape,material='envelope' if key=='spring_envelope' else 'steel' if 'trunnion' in key else 'printed',moving=False,scope='J spring/cup geometry; trunnion end retention unresolved')
    parts['motor_reference']=dict(shape=old.moving(old.nominal()['motor_reference'],travel),material='reference',moving=True,scope='Motor envelope, excluded from pod mass')
    return parts,bolts


def main():
    checks=dict(fabrication_release=False,config_hashes=K.study()['input_hashes'],valid_shapes={},interferences=[],external_conflicts=[],contact_checks=[],all_pair_conflicts=[],all_pair_boolean_checks=0,mass={})
    # Parts intentionally touching at joints are excluded. Every moving group is
    # checked against fixed structure and stop hardware; moving spring cups separately.
    for t in (-2.5,0,5,10):
        for shim in (0,6):
            parts,bolts=posed(t,shim)
            fixed=[id for id,row in parts.items() if not row['moving'] and row['material'] not in ('envelope','reference') and id not in ('pivot_pin','lower_cup','lower_guide','lower_trunnion','upper_guide','upper_cup','upper_trunnion')]
            moving=[id for id,row in parts.items() if row['moving'] and row['material'] not in ('envelope','reference')]
            for a in moving:
                for b in fixed:
                    if (a.startswith('bushing') and b.startswith('collar')):continue
                    sa,sb=parts[a]['shape'],parts[b]['shape']
                    if not sa.BoundBox.intersect(sb.BoundBox):continue
                    v=sa.common(sb).Volume
                    if v>1e-4:checks['interferences'].append(dict(travel_mm=t,shim_mm=shim,a=a,b=b,volume_mm3=v))
            for a,b in [('motor_reference','stop_nut'),('motor_reference','stop_screw'),('lower_cup','lower_fork'),('lower_cup','tray'),('upper_cup','upper_fork'),('upper_guide','lower_cup'),('lower_guide','upper_cup')]:
                v=parts[a]['shape'].common(parts[b]['shape']).Volume
                if v>1e-4:checks['interferences'].append(dict(travel_mm=t,shim_mm=shim,a=a,b=b,volume_mm3=v))
            # Separate material families at the bearing/fork interface must not be
            # treated as an intended fusion inherited from J's all-printed cradle.
            for a,b in [('bearing_block_1','lower_fork'),('stop_arm','collar_clearance_1'),('stop_arm_angle','collar_clearance_1')]:
                v=parts[a]['shape'].common(parts[b]['shape']).Volume
                if v>1e-4:checks['interferences'].append(dict(travel_mm=t,shim_mm=shim,a=a,b=b,volume_mm3=v))
            pin=parts['stop_sleeve']['shape'];arm=parts['stop_arm']['shape']
            checks['contact_checks'].append(dict(travel_mm=t,shim_mm=shim,distance_mm=pin.distToShape(arm)[0],intersection_mm3=pin.common(arm).Volume))

    for t,shim in ((0,3),(10,6),(-2.5,0)):
        parts,bolts=posed(t,shim)
        intended={frozenset((b['id'],b['members'][-1])) for b in bolts if b['threaded_receiver']}
        intended|={frozenset(('motor_screw_'+str(i),'motor_reference')) for i in (0,1)}
        keys=[id for id,row in parts.items() if row['material']!='envelope']
        for i,a in enumerate(keys):
            for b in keys[i+1:]:
                if frozenset((a,b)) in intended:continue
                sa,sb=parts[a]['shape'],parts[b]['shape']
                if not sa.BoundBox.intersect(sb.BoundBox):continue
                checks['all_pair_boolean_checks']+=1;v=sa.common(sb).Volume
                if v>1e-4:checks['all_pair_conflicts'].append(dict(travel_mm=t,shim_mm=shim,a=a,b=b,volume_mm3=v))
        configured,_=I.configured(H.baseline(),H.read(),I.read())
        wanted={'battery_bay','vac_bin_left','vac_bin_front','vac_bin_upper','blower_bay','filter_bay','mop_tank','mop_pump','sofa_extension','extension_cable','G_bottom_supervisor'}
        for bottom in ('vacuum','mop','low'):
            for allocation in base.reference_parts(configured,bottom):
                if allocation['id'] not in wanted:continue
                sh=box(*allocation['min'],*allocation['size'])
                for id,row in parts.items():
                    if row['material']=='envelope' or not row['shape'].BoundBox.intersect(sh.BoundBox):continue
                    v=row['shape'].common(sh).Volume
                    if v>1e-4:checks['external_conflicts'].append(dict(travel_mm=t,shim_mm=shim,bottom=bottom,part=id,allocation=allocation['id'],volume_mm3=v))
    base_parts,_=hardware(0)
    checks['overtravel_intersections_mm3']={str(t):old.moving(base_parts['stop_arm']['shape'],t).common(base_parts['stop_sleeve']['shape']).Volume for t in (-2.6,10.1)}

    for t,shim,suffix in [(0,3,''),(10,6,'_bump'),(-2.5,0,'_droop')]:
        parts,bolts=posed(t,shim);name='pod_joints'+suffix;doc=App.newDocument(name);objs=[]
        for id,row in parts.items():
            shape=row['shape']
            if shape.isNull() or not shape.isValid():raise ValueError((id,t,'invalid'))
            obj=doc.addObject('PartDesign::Feature',id);obj.Shape=Part.makeCompound(shape.Edges) if row['material']=='envelope' else shape
            obj.addProperty('App::PropertyString','Scope');obj.Scope=row['scope']
            if obj.ViewObject:obj.ViewObject.ShapeColor=(.2,.5,.55) if row['material']=='printed' else (.65,.68,.72) if row['material']=='aluminum' else (.3,.35,.4)
            objs.append(obj)
        doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(objs,str(OUT/(name+'.step')))
        checks['valid_shapes'][name]=len(objs);App.closeDocument(doc.Name)

    parts,bolts=posed(0,6);ledger=[]
    for id,row in parts.items():
        if row['material'] not in rho or id.startswith('bushing'):continue
        mass=row['shape'].Volume*rho[row['material']]
        if id=='motor_bracket':mass=8.5
        if id.startswith('collar_'):mass=5.1
        solids=row['shape'].Solids;volume=sum(s.Volume for s in solids)
        if volume<=0:raise ValueError((id,'mass part has no solid'))
        centre=[sum(s.Volume*s.CenterOfMass[i] for s in solids)/volume for i in range(3)]
        ledger.append(dict(id=id,mass_g=mass,cg_mm=centre,basis='catalog' if id=='motor_bracket' or id.startswith('collar_') else 'solid nominal volume'))
    for id,mass,cg in [('spring_and_bushings',5,[70,135,36]),('sensor_and_cables',8,[80,140,45])]:ledger.append(dict(id=id,mass_g=mass,cg_mm=cg,basis='allowance'))
    subtotal=sum(v['mass_g'] for v in ledger);reserve=k['mass']['reserve_g'];mass=[subtotal*f+extra for f,extra in zip(k['mass']['stock_factors'],reserve)]
    cg=[(sum(v['mass_g']*v['cg_mm'][i] for v in ledger)+reserve[1]*[65,135,42][i])/mass[1] for i in range(3)]
    checks['mass']=dict(items=ledger,modeled_and_allowance_subtotal_g=subtotal,completion_reserve_g=reserve,per_pod_interval_g=mass,cg_mm=cg,
        includes='Moving metalwork, fixed cap/cheeks, local rail clips, shown fasteners, J springs/pivot/collars, sensor/cable and completion reserves',
        excludes='Motor, wheel, hub and longitudinal floor rails/frame. Existing frame/carrier allowances retained in K mass scenario.')
    checks['fasteners']=bolts
    (OUT/'pod_joints_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    with (OUT/'pod_joints_hardware.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','mass_g','cg_mm','basis']);w.writeheader();w.writerows(ledger)
    print('K CAD objects',checks['valid_shapes'],'interferences',len(checks['interferences']),'mass',mass)
    print(checks['interferences'])


# FreeCAD invokes command-line Python files under their basename.
if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
