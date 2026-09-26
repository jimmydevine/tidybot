"""Export revision F allocations independently of historical C/E CAD."""
import json
import os
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
OUT=ROOT/'design/system/output'
r=json.loads((OUT/'core_partition.json').read_text())
cases={('core_partition' if k=='vacuum' else 'core_partition_'+k):v['assembly'] for k,v in r['ground'].items()}
cases['core_partition_duster']=r['airborne_after']['cases']['quad10']['assembly']
counts={}
for name,a in cases.items():
    doc=App.newDocument(name);features=[]
    for p in a['parts']:
        if p['shape']=='distributed':continue
        x,y,z=p['min'];w,d,h=p['size'];solid=bool(p.get('parent')) or p['id'].startswith(('floor_','core_rail','air_')) or p['group']=='power'
        shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
        if p['shape']=='beam':
            start,end=[App.Vector(*v) for v in p['endpoints_mm']];axis=end-start;length=axis.Length;axis.normalize()
            radius=p['diameter_mm']/2
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
        obj.addProperty('App::PropertyString','Scope');obj.Scope='F allocation only; no hole pattern, structural or flight release'
        obj.addProperty('App::PropertyString','Notes');obj.Notes=p.get('notes','')
        if obj.ViewObject:
            obj.ViewObject.ShapeColor=(.25,.45,.8) if p['module']=='core' else (.85,.48,.12) if p['group']=='power' else (.55,.57,.6)
        features.append(obj)
    doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(features,str(OUT/(name+'.step')))
    counts[name]=len(features);App.closeDocument(doc.Name)
(OUT/'core_partition_cad_checks.json').write_text(json.dumps(dict(valid_shapes=counts,total=sum(counts.values()),fabrication_release=False),indent=2)+'\n')
print('F CAD: '+str(counts))
