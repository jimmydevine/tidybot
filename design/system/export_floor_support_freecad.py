"""H stock routes and mechanism references, not fabrication geometry."""
import json
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve();OUT=ROOT/'design/system/output'
sys.path.insert(0,str(ROOT/'design/system'))
import floor_support as study
import build as base

r=json.loads((OUT/'floor_support.json').read_text());d=r['config'];g=study.baseline();w=d['wheel']
App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
counts={}
cases=[('floor_support','vacuum',0),('floor_support_mop','mop',0),('floor_support_low','low',0),
       ('floor_support_bump','vacuum',w['bump_mm']),('floor_support_droop','vacuum',-w['droop_candidate_mm'])]
for name,bottom,travel in cases:
    doc=App.newDocument(name);objects=[]
    def feature(id,shape,color=(.38,.58,.68),scope='H candidate stock; joints and fasteners incomplete'):
        if shape.isNull() or not shape.isValid():raise ValueError((name,id))
        obj=doc.addObject('PartDesign::Feature',id);obj.Label=id.replace('_',' ');obj.Shape=shape
        obj.addProperty('App::PropertyString','Scope');obj.Scope=scope
        if obj.ViewObject:obj.ViewObject.ShapeColor=color
        objects.append(obj)
    for p in study.stock(d,bottom):
        x,y,z=p['min'];a,b,c=p['size'];shape=Part.makeBox(a,b,c,App.Vector(x,y,z));hole=p.get('hole')
        if hole:
            if hole['axis']=='x':tool=Part.makeCylinder(hole['diameter']/2,a+2,App.Vector(x-1,hole['y'],hole['z']),App.Vector(1,0,0))
            else:tool=Part.makeCylinder(hole['diameter']/2,c+2,App.Vector(hole['x'],hole['y'],z-1))
            shape=shape.cut(tool)
        feature(p['id'],shape)
    # Keep G component allocations as wireframes. Candidate stock replaces the
    # old support shapes visually, but no installed H weight is claimed.
    omitted=set(d['carrier']['removed_if_closed'])|{'wheel_left','wheel_right','pod_left','pod_right','caster'}
    for p in base.reference_parts(g,bottom):
        if p.get('parent') or p['shape']=='distributed' or p['id'] in omitted:continue
        shape=Part.makeBox(*p['size'],App.Vector(*p['min']))
        feature('allocation_'+p['id'],Part.makeCompound(shape.Edges),(.66,.68,.65),'Unchanged G functional allocation; not a finished casing')
    position=study.pose(d,travel);ax,az=position['axle_y_mm'],position['axle_z_mm'];py,pz=w['pivot_yz_mm']
    for side,mirror in [('left',False),('right',True)]:
        xx=249 if mirror else 2
        feature(side+'_wheel',Part.makeCylinder(36,24,App.Vector(xx,ax,az),App.Vector(1,0,0)),(.21,.25,.27),'72 x 24 mm tire envelope; actual wheel cavity and hub not resolved here')
        xx=180 if mirror else 26
        feature(side+'_motor',Part.makeCylinder(12.5,69,App.Vector(xx,ax,az),App.Vector(1,0,0)),(.63,.64,.63),'Motor body envelope; output shaft and cable loop omitted')
        xx=169 if mirror else 26
        feature(side+'_pin',Part.makeCylinder(w['pivot_diameter_mm']/2,80,App.Vector(xx,py,pz),App.Vector(1,0,0)),(.77,.77,.73),'Smooth pin reference; axial retainers remain to specify')
        for j,cx in enumerate(w['bushing_centres_x_mm']):
            length=w['bushing_length_mm'];x=cx-length/2
            if mirror:x=275-x-length
            axis=App.Vector(1,0,0);origin=App.Vector(x,py,pz)
            bush=Part.makeCylinder(w['bushing_od_mm']/2,length,origin,axis).cut(Part.makeCylinder(w['pivot_diameter_mm']/2,length,origin,axis))
            feature(side+'_bush_'+str(j),bush,(.72,.61,.31),'Unselected replaceable bushing; material/rating and ear fit remain open')
        # Arm centreline, not a fictitious solid with an assigned mass.
        xx=98 if not mirror else 177
        feature(side+'_arm_route',Part.makeLine(App.Vector(xx,ax,az),App.Vector(xx,py,pz)),(.18,.45,.63),'Moving tray route only; motor bracket, ears, bump and droop stops not detailed')
        sy,sz=study.rotate_yz(d,py-w['spring_lever_mm'],w['spring_seat_z_mm'],travel)
        sx=w['spring_x_mm'] if not mirror else 275-w['spring_x_mm']
        feature(side+'_spring_space',Part.makeCompound(Part.makeCylinder(w['spring_od_limit_mm']/2,w['spring_top_z_mm']-sz,App.Vector(sx,sy,sz)).Edges),(.7,.48,.2),'Spring envelope only; cups, guide and end pivot not detailed')
    cx,cy=d['caster']['centres_xy_mm'][bottom]
    shape=Part.makeCylinder(d['caster']['sweep_radius_mm'],d['caster']['bare_height_mm'],App.Vector(cx,cy,0))
    feature('caster_swivel_envelope',Part.makeCompound(shape.Edges),(.5,.5,.5),'Bare 360-degree caster envelope; retained fitting is not selected')
    retainer_z=d['caster']['bare_height_mm']+d['caster']['reference_fitting_height_mm']+d['caster']['plate_mm']
    shape=Part.makeCylinder(8,d['caster']['retainer_allowance_mm'],App.Vector(cx,cy,retainer_z))
    feature('caster_retainer_reserve',Part.makeCompound(shape.Edges),(.7,.48,.2),'16 mm diameter x 5 mm mounting-retainer reserve; exact fitting and fasteners unselected')
    doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(objects,str(OUT/(name+'.step')))
    counts[name]=len(objects);App.closeDocument(doc.Name)
(OUT/'floor_support_cad_checks.json').write_text(json.dumps(dict(valid_shapes=counts,total=sum(counts.values()),fabrication_release=False),indent=2)+'\n')
print('H CAD:',counts)
