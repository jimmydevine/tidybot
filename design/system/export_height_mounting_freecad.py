"""Reviewable I allocations and caster stack, not a fabrication model."""
import json
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(ROOT/'design/system'))
import build as base
import floor_support as support
import height_mounting as design

OUT=ROOT/'design/system/output'
r=json.loads((OUT/'height_mounting.json').read_text())
c=r['configured_layout'];h=r['configured_support'];d=r['config'];s=r['caster_stack']
App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
checks={}
for bottom,suffix in [('vacuum',''),('mop','_mop'),('low','_low')]:
    name='height_mounting'+suffix;doc=App.newDocument(name);objects=[]
    def add(id,shape,color=(.6,.65,.65),note='Functional allocation, not a finished part'):
        if shape.isNull() or not shape.isValid():raise ValueError((bottom,id))
        obj=doc.addObject('PartDesign::Feature',id);obj.Label=id.replace('_',' ');obj.Shape=shape
        obj.addProperty('App::PropertyString','Scope');obj.Scope=note
        if obj.ViewObject:obj.ViewObject.ShapeColor=color
        objects.append(obj)
    def box(p):return Part.makeBox(*p['size'],App.Vector(*p['min']))
    omitted=set(h['carrier']['removed_if_closed'])|{'wheel_left','wheel_right','pod_left','pod_right','caster'}
    for p in base.reference_parts(c,bottom):
        if p.get('parent') or p['shape']=='distributed' or p['id'] in omitted:continue
        col=(.1,.5,.7) if p['id'] in ('lidar','I_lidar_mount') else (.6,.65,.65)
        if p['id']=='top_port':col=(.7,.3,.12)
        if p['id'] in ('vac_bin_upper','blower_bay','mop_pump'):col=(.1,.55,.4)
        add('allocation_'+p['id'],Part.makeCompound(box(p).Edges),col)
    for p in support.stock(h,bottom):
        shape=box(p);hole=p.get('hole')
        if hole:
            if hole['axis']=='z':tool=Part.makeCylinder(hole['diameter']/2,p['size'][2]+2,App.Vector(hole['x'],hole['y'],p['min'][2]-1))
            else:tool=Part.makeCylinder(hole['diameter']/2,p['size'][0]+2,App.Vector(p['min'][0]-1,hole['y'],hole['z']),App.Vector(1,0,0))
            shape=shape.cut(tool)
        add(p['id'],shape,(.42,.58,.65),'H candidate stock at revised caster height; joints incomplete')
    x,y=h['caster']['centres_xy_mm'][bottom]
    add('bare_caster_sweep',Part.makeCompound(Part.makeCylinder(h['caster']['sweep_radius_mm'],h['caster']['bare_height_mm'],App.Vector(x,y,0)).Edges))
    add('fitting_neck_reserve',Part.makeCompound(Part.makeCylinder(8,d['caster']['added_height_mm'],App.Vector(x,y,h['caster']['bare_height_mm'])).Edges),note='16 mm neck envelope assumption; exact shoulder size must be confirmed')
    add('M8_thread_envelope',Part.makeCylinder(4,d['caster']['stem_length_mm'],App.Vector(x,y,s['plate_bottom_mm'])),(.55,.55,.55),'Plain cylinder representing M8 thread, not modeled threads or plug-end retention')
    for id,z,height,radius in [('washer',s['plate_top_mm'],d['caster']['washer_thickness_reserve_mm'],8),('locking_nut',s['washer_top_mm'],d['caster']['nut_height_reserve_mm'],7.5)]:
        shape=Part.makeCylinder(radius,height,App.Vector(x,y,z)).cut(Part.makeCylinder(4,height,App.Vector(x,y,z)))
        add(id+'_reserve',shape,(.5,.54,.58),'Procurement envelope; nut hex, washer SKU and tolerances unselected')
    add('caster_service_space',Part.makeCompound(box(design.retainer(d,h,bottom)).Edges),(.75,.5,.15))
    for side,xx in [('left',2),('right',249)]:
        ay,az=h['wheel']['axle_yz_mm']
        add(side+'_wheel',Part.makeCylinder(36,24,App.Vector(xx,ay,az),App.Vector(1,0,0)),(.2,.22,.23),'Nominal tire envelope; suspension travel checked by calculation')
    # Mounting-hole axes are a template from the C1 drawing, not final screws.
    l=d['lidar'];cx=l['min_mm'][0]+l['size_mm'][0]/2;cy=l['min_mm'][1]+l['size_mm'][1]/2
    for j,(dx,dy) in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)]):
        xx=cx+dx*l['mount_hole_square_mm']/2;yy=cy+dy*l['mount_hole_square_mm']/2
        add('lidar_mount_axis_'+str(j),Part.makeLine(App.Vector(xx,yy,l['min_mm'][2]-4),App.Vector(xx,yy,l['min_mm'][2]+4)),(.1,.5,.7),'M2.5 axis; maximum 4 mm insertion, actual screw length depends on support stack')
    doc.recompute();doc.saveAs(str(OUT/(name+'.FCStd')));Part.export(objects,str(OUT/(name+'.step')))
    checks[bottom]=len(objects);App.closeDocument(doc.Name)
(OUT/'height_mounting_cad_checks.json').write_text(json.dumps(dict(valid_shapes=checks,total=sum(checks.values()),fabrication_release=False),indent=2)+'\n')
print('I valid CAD shapes:',checks)
