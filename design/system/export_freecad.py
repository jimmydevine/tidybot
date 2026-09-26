"""Export reference layouts, not printable parts. Run from the repository root."""
import json
import os
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
OUT=ROOT/'design/system/output'
data=json.loads((OUT/'system_design.json').read_text())
c=data['config'];r=data['results']
if any(x['errors'] for x in r['checks'].values()):
    raise ValueError('Resolve component allocation conflicts before CAD export')
colors={'power':(0.79,.50,.15),'logic':(.28,.42,.73),'sensor':(.58,.29,.70),'battery':(.72,.56,.12),'structure':(.4,.46,.52),'drive':(.08,.49,.53),'air':(.24,.55,.40),'tool':(.72,.33,.32),'water':(.15,.56,.68),'extension':(.60,.40,.19),'lift':(.43,.39,.66)}
results=[]

def export(name,parts,body=True,flight=None):
    doc=App.newDocument('System_'+name);features=[]
    groups={}
    def feature(id,label,shape,group='structure',note='',reference=False):
        obj=doc.addObject('PartDesign::Feature',id);obj.Label=label;obj.Shape=shape
        if shape.isNull() or not shape.isValid():raise ValueError(name+':'+id)
        for prop,value in [('DesignScope','PRELIMINARY reference / allocation; not fabrication geometry'),('Subsystem',group),('Notes',note)]:
            obj.addProperty('App::PropertyString',prop);setattr(obj,prop,value)
        if obj.ViewObject:
            obj.ViewObject.ShapeColor=colors.get(group,colors['structure']);obj.ViewObject.LineColor=colors.get(group,colors['structure']);obj.ViewObject.Transparency=65 if reference else 0
        if group not in groups:groups[group]=doc.addObject('App::DocumentObjectGroup','Group_'+group)
        groups[group].addObject(obj);features.append(obj);return obj
    for p in parts:
        if p['shape']=='distributed':continue
        x,y,z=p['min'];w,d,h=p['size']
        shape=Part.makeBox(w,d,h,App.Vector(x,y,z))
        if p['shape'] in ('cylinder_z','ring_z') and abs(w-d)<1e-6:
            shape=Part.makeCylinder(w/2,h,App.Vector(x+w/2,y+d/2,z))
            if p['shape']=='ring_z':shape=shape.cut(Part.makeCylinder(w/2-3,h,App.Vector(x+w/2,y+d/2,z)))
        elif p['shape']=='cylinder_x' and abs(d-h)<1e-6:
            shape=Part.makeCylinder(d/2,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0))
            if p['id'].startswith('beam_'):shape=shape.cut(Part.makeCylinder(d/2-1,w,App.Vector(x,y+d/2,z+h/2),App.Vector(1,0,0)))
        elif p['shape']=='cylinder_y' and abs(w-h)<1e-6:
            shape=Part.makeCylinder(w/2,d,App.Vector(x+w/2,y,z+h/2),App.Vector(0,1,0))
            if p['id'].startswith('beam_'):shape=shape.cut(Part.makeCylinder(w/2-1,d,App.Vector(x+w/2,y,z+h/2),App.Vector(0,1,0)))
        # Unspecified functional bays are edge outlines; exact component proxies
        # and explicitly dimensioned stock are solids.
        solid=bool(p.get('parent')) or p['id'].startswith(('core_rail','rotor_','guard_','beam_')) or p['id']=='lidar'
        feature(p['id'],('REF: ' if solid else 'SPACE: ')+p['label'],shape if solid else Part.makeCompound(shape.Edges),p['group'],p.get('notes',''),solid)
    if body:
        feature('BodyLimit','LIMIT: 275 x 275 x 180 mm',Part.makeCompound(Part.makeBox(275,275,180).Edges))
        for i,(x,y) in enumerate(c['interfaces']['lock_centres_xy_mm']):
            feature('Stud_'+str(i),'REFERENCE: M4 continuous core load path',Part.makeCylinder(2,37,App.Vector(x,y,86)),note='Shows load path only. Rail holes, shoulder length and captive locks are not released.',reference=True)
    doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(features,str(OUT/(name+'.step')))
    results.append({'file':name,'valid_shapes':len(features),'fabrication_release':False})
    App.closeDocument(doc.Name)

for key,a in r['ground'].items():export(key,a['parts'])
for variant in c['lift']['variants']:export(variant,r['flights']['vacuum_'+variant]['assembly']['parts'],flight=variant)
for key in ('low','dust'):export(key+'_extended',r['extended'][key]['assembly']['parts'])
export('station',json.loads((OUT/'station_layout.json').read_text()),body=False)
(OUT/'cad_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print('SYSTEM CAD:',json.dumps(results))
