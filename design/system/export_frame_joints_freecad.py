"""G stock and slider reference CAD, preserving preceding revisions."""
import json
import os
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve();OUT=ROOT/'design/system/output'
r=json.loads((OUT/'frame_joints.json').read_text());k=r['config']['corner']
App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
cases={('frame_joints' if key=='vacuum' else 'frame_joints_'+key):value['assembly'] for key,value in r['ground'].items()}
cases['frame_joints_duster']=r['airborne_after']['cases']['quad10']['assembly']
cases['frame_joints_core']={'parts':[p for p in r['ground']['vacuum']['assembly']['parts'] if p['id'].startswith('G_') and p['module']=='core']}
counts={}
for name,a in cases.items():
    doc=App.newDocument(name);features=[]
    for p in a['parts']:
        if p['shape']=='distributed':continue
        x,y,z=p['min'];w,d,h=p['size'];solid=bool(p.get('parent')) or p['id'].startswith(('G_','floor_','air_')) or p['group']=='power'
        shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
        if p.get('drill_axis')=='z':
            xx,yy=p['drill_center'];shape=shape.cut(Part.makeCylinder(p['drill_diameter']/2,h+2,App.Vector(xx,yy,z-1)))
        if p.get('shape_override')=='slider':
            xx,yy=p['stud_center'];end=xx-p['release_direction']*k['release_travel_mm'];neck=k['stud_neck_clearance_mm'];entry=k['stud_entry_diameter_mm']
            holes=Part.makeCylinder(neck/2,h+2,App.Vector(xx,yy,z-1)).fuse(Part.makeCylinder(entry/2,h+2,App.Vector(end,yy,z-1)))
            holes=holes.fuse(Part.makeBox(abs(end-xx),neck,h+2,App.Vector(min(xx,end),yy-neck/2,z-1)))
            shape=shape.cut(holes)
        if p['shape']=='beam':
            start,end=[App.Vector(*v) for v in p['endpoints_mm']];axis=end-start;length=axis.Length;axis.normalize();radius=p['diameter_mm']/2
            shape=Part.makeCylinder(radius,length,start,axis).cut(Part.makeCylinder(radius-1,length,start,axis));solid=True
        elif p['shape'] in ('cylinder_z','ring_z') and abs(w-d)<1e-6:
            shape=Part.makeCylinder(w/2,h,App.Vector(x+w/2,y+d/2,z));solid=True
            if p['shape']=='ring_z':shape=shape.cut(Part.makeCylinder(w/2-3,h,App.Vector(x+w/2,y+d/2,z)))
        elif p['shape']=='cylinder_x' and abs(d-h)<1e-6:
            shape=Part.makeCylinder(d/2,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0));solid=True
        elif p['shape']=='cylinder_y' and abs(w-h)<1e-6:
            shape=Part.makeCylinder(w/2,d,App.Vector(x+w/2,y,z+h/2),App.Vector(0,1,0));solid=True
        if not solid:shape=Part.makeCompound(shape.Edges)
        if shape.isNull() or not shape.isValid():raise ValueError((name,p['id']))
        obj=doc.addObject('PartDesign::Feature',p['id']);obj.Label=p['label'];obj.Shape=shape
        obj.addProperty('App::PropertyString','Scope');obj.Scope='G candidate; component envelopes and slider holes, not a completed or proof-tested latch'
        if obj.ViewObject:obj.ViewObject.ShapeColor=(.2,.4,.65) if p['id'].startswith('G_lock') else (.62,.68,.73) if p['id'].startswith('G_') else (.77,.73,.61)
        features.append(obj)
    doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(features,str(OUT/(name+'.step')))
    counts[name]=len(features);App.closeDocument(doc.Name)
(OUT/'frame_joints_cad_checks.json').write_text(json.dumps(dict(valid_shapes=counts,total=sum(counts.values()),fabrication_release=False),indent=2)+'\n')
print('G CAD: '+str(counts))
