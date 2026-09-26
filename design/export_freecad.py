"""Run with freecadcmd design/export_freecad.py after design/generate.py.

Exports bounding geometry and working states, never printable structural parts.
"""
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
DATA=json.loads((ROOT/'design/output/study.json').read_text())
OUT=ROOT/'design/output'


def shape_for(p):
    if p.get('shape')=='beam':
        a,b=App.Vector(*p['start']),App.Vector(*p['end']); vec=b-a
        return Part.makeCylinder(p['radius'],vec.Length,a,vec)
    if p.get('shape')=='cylinder':
        direction=App.Vector(0,1,0) if p['axis']=='y' else App.Vector(0,0,1)
        start=App.Vector(*p['center'])-direction*(p['height']/2)
        solid=Part.makeCylinder(p['radius'],p['height'],start,direction)
        # Guard cylinder is an occupied envelope. Edge-only form avoids implying
        # that a ring alone is a complete designed rotor barrier.
        return Part.makeCompound(solid.Edges) if p['group']=='guard' else solid
    lower=[x-s/2 for x,s in zip(p['center'],p['size'])]
    solid=Part.makeBox(*p['size'],App.Vector(*lower))
    return Part.makeCompound(solid.Edges) if p['group']=='envelope' else solid


def export(name,objects):
    doc=App.newDocument(name); features=[]
    for i,p in enumerate(objects):
        feature=doc.addObject('PartDesign::Feature',f'Envelope{i:03d}')
        feature.Label=p['name']; feature.Shape=shape_for(p)
        feature.addProperty('App::PropertyString','StudyScope').StudyScope='Concept envelope; NOT fabrication geometry'
        if feature.ViewObject:
            color=tuple(int(p['color'][j:j+2],16)/255 for j in (1,3,5))
            feature.ViewObject.ShapeColor=color
            if p['group'] in ('prop','stored'):feature.ViewObject.Transparency=70
        features.append(feature)
    doc.recompute()
    doc.saveAs(str(OUT/(name+'.FCStd')))
    Part.export(features,str(OUT/(name+'.step')))
    print(f'EXPORTED {name}: {len(features)} concept features')
    App.closeDocument(doc.Name)


variant=DATA['config']['default_variant']
export('robot_concept',DATA['robot_scenes'][variant])
export('station_concept',DATA['station_scenes'][variant][2])
scene=json.loads(json.dumps(DATA['robot_scenes'][variant]))
t=DATA['site']['staircase']['tread_depth']*1000
h=DATA['site']['staircase']['approx_riser_height']*1000
width=DATA['site']['staircase']['tread_width']*1000
for k in range(-2,4):
    scene.append(dict(name=f'Interior tread {k:+} / no landing or headroom model',group='stair',
                      center=[k*t,0,(k*h-3*h)/2],size=[t,width,k*h+3*h],color='#d4bd9a'))
export('stair_concept',scene)
