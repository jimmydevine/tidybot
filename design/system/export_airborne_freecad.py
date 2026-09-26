"""Export the airborne duster reference, without overwriting earlier CAD."""
import json
import os
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
OUT=ROOT/'design/system/output'
r=json.loads((OUT/'airborne_dusting.json').read_text())
case=r['cases']['quad10']
if case['screen']['geometry_errors']:
    raise ValueError('Resolve airborne duster allocation conflicts before export')
doc=App.newDocument('AirborneDustingReference');features=[]
colors={'tool':(.16,.52,.46),'structure':(.4,.46,.52),'sensor':(.58,.29,.7),
        'lift':(.65,.42,.18),'battery':(.74,.57,.13),'power':(.79,.5,.15),'logic':(.28,.42,.73)}
for p in case['assembly']['parts']:
    if p['shape']=='distributed':continue
    x,y,z=p['min'];w,d,h=p['size'];solid=False
    shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
    if p['shape']=='beam':
        a,b=[App.Vector(*v) for v in p['endpoints_mm']];axis=b-a;length=axis.Length;axis.normalize()
        radius=p['diameter_mm']/2
        shape=Part.makeCylinder(radius,length,a,axis).cut(Part.makeCylinder(radius-1,length,a,axis));solid=True
    elif p['shape'] in ('cylinder_z','ring_z') and abs(w-d)<1e-6:
        shape=Part.makeCylinder(w/2,h,App.Vector(x+w/2,y+d/2,z));solid=True
        if p['shape']=='ring_z':shape=shape.cut(Part.makeCylinder(w/2-3,h,App.Vector(x+w/2,y+d/2,z)))
    elif p['shape']=='cylinder_x' and abs(d-h)<1e-6:
        shape=Part.makeCylinder(d/2,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0));solid=True
    elif p['shape']=='cylinder_y' and abs(w-h)<1e-6:
        shape=Part.makeCylinder(w/2,d,App.Vector(x+w/2,y,z+h/2),App.Vector(0,1,0));solid=True
    solid=solid or p['id'].startswith(('air_','core_rail')) or bool(p.get('parent'))
    if not solid:shape=Part.makeCompound(shape.Edges)
    if shape.isNull() or not shape.isValid():raise ValueError(p['id'])
    obj=doc.addObject('PartDesign::Feature',p['id']);obj.Label=p['label'];obj.Shape=shape
    obj.addProperty('App::PropertyString','DesignScope');obj.DesignScope='Reference allocation; not printable fabrication geometry or flight qualification'
    obj.addProperty('App::PropertyString','Notes');obj.Notes=p.get('notes','')
    if obj.ViewObject:obj.ViewObject.ShapeColor=colors.get(p['group'],colors['structure'])
    features.append(obj)
doc.recompute();doc.saveAs(str(OUT/'airborne_dusting.FCStd'));Part.export(features,str(OUT/'airborne_dusting.step'))
(OUT/'airborne_cad_checks.json').write_text(json.dumps(dict(valid_shapes=len(features),fabrication_release=False,scope='Static reference geometry; joints, wiring, swept flight and docking paths unqualified'),indent=2)+'\n')
print('AIRBORNE CAD: '+str(len(features))+' valid reference shapes')
