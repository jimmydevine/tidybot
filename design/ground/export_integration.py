"""Run after integrate_vacuum.py, using freecadcmd from the repository root."""
import json
import os
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
OUT=ROOT/'design/ground/output'
data=json.loads((OUT/'vacuum_integration.json').read_text())
if data['checks']['errors']: raise ValueError('Resolve placement conflicts before export')
doc=App.newDocument('VacuumIntegration')
features=[]
for p in data['parts']:
    x,y,z=p['min'];w,d,h=p['size']
    shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
    if p.get('shape')=='cylinder_x':
        if abs(d-h)>1e-6: raise ValueError('Cylinder reference must have equal y and z dimensions')
        shape=Part.makeCylinder(d/2,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0))
    elif p.get('shape')=='cylinder_z':
        if abs(w-d)>1e-6: raise ValueError('Vertical sweep must have equal x and y dimensions')
        shape=Part.makeCylinder(w/2,h,App.Vector(x+w/2,y+d/2,z))
    reservation='proposed' in p['basis'] or not p.get('parent') and p['id']!='lidar'
    obj=doc.addObject('PartDesign::Feature',p['id'])
    obj.Label=('SPACE: ' if reservation else 'REF: ')+p['label']
    obj.Shape=Part.makeCompound(shape.Edges) if reservation or p['id']=='caster_sweep' else shape
    if obj.Shape.isNull() or not obj.Shape.isValid():raise ValueError(p['id'])
    for prop,value in [('StudyScope','Placement only; NOT fabrication geometry'),('DimensionBasis',p['basis']),('Notes',p.get('note','')),('Source',p.get('source','')),('Subsystem',p['group'])]:
        obj.addProperty('App::PropertyString',prop);setattr(obj,prop,value)
    if obj.ViewObject:
        obj.ViewObject.ShapeColor=(0.65,0.78,0.89);obj.ViewObject.LineColor=(0.3,0.4,0.5)
    features.append(obj)
limit=doc.addObject('PartDesign::Feature','RigidLimit');limit.Label='LIMIT: 275 x 275 x 180 mm'
limit.Shape=Part.makeCompound(Part.makeBox(275,275,180).Edges);features.append(limit)
for name,z in [('BottomMate',data['bottom_mate_z_mm']),('CoreTop',data['core_top_z_mm'])]:
    obj=doc.addObject('PartDesign::Feature',name)
    pts=[App.Vector(x,y,z) for x,y in [(2.5,2.5),(272.5,2.5),(272.5,272.5),(2.5,272.5),(2.5,2.5)]]
    obj.Shape=Part.makePolygon(pts);obj.Label=f'PLANE: {name}, z={z} mm; no solid panel implied';features.append(obj)
doc.recompute()
doc.saveAs(str(OUT/'vacuum_integration.FCStd'))
Part.export(features,str(OUT/'vacuum_integration.step'))
print(f'EXPORTED {len(features)} valid reference/outline shapes; not fabrication parts')
App.closeDocument(doc.Name)
