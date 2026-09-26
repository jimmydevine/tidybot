"""N nominal stock/interface geometry. Deliberately exports no print STLs."""
import itertools
import json
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(ROOT/'design/system'))
import fixed_drive as N
import export_wheel_pod_freecad as J
V=App.Vector


def box(p,s):return Part.makeBox(*s,V(*p))
def cyl(p,r,l,axis):return Part.makeCylinder(r,l,V(*p),V(*axis))
def mirror(s):return s.mirror(V(137.5,0,0),V(1,0,0))


def geometry(d):
    a=d['angle'];b=d['beam'];c=d['cleat'];t=a['wall'];rad=a['inside_radius'];x=a['x'];w=a['width']
    y=a['y_back']-t;z=a['z_bottom']+t
    angle=box([x,a['y_front'],a['z_bottom']],[w,a['y_back']-a['y_front'],t]).fuse(box([x,y,a['z_bottom']],[w,t,a['z_top']-a['z_bottom']]))
    root=box([x,y-rad,z],[w,rad,rad]).cut(cyl([x,y-rad,z+rad],rad,w,[1,0,0]))
    angle=angle.fuse(root)
    for xx,yy in itertools.product((39.85,65.25),(94.15,115.85)):
        angle=angle.cut(cyl([xx,yy,a['z_bottom']-1],1.7,t+2,[0,0,1]))
    for xx in (42.8,68.2):angle=angle.cut(cyl([xx,y-1,58.65],2.15,t+2,[0,1,0]))
    p=b['min'];l,by,bz=b['size'];bt=b['wall']
    beam=box(p,b['size']).cut(box([p[0]-1,p[1]+bt,p[2]+bt],[l+2,by-2*bt,bz-2*bt]))
    for xx in (42.8,68.2,275-42.8,275-68.2):beam=beam.cut(cyl([xx,129,58.65],2.15,by+2,[0,1,0]))
    for xx in (36.5,238.5):beam=beam.cut(cyl([xx,136.35,51.3],2.15,bz+2,[0,0,1]))
    ct=c['wall'];cl=c['leg'];cr=c['inside_radius']
    cleat=box([28,130,65],[cl,c['length'],ct]).fuse(box([28,130,65],[ct,c['length'],cl]))
    crs=box([28+ct,130,65+ct],[cr,c['length'],cr]).cut(cyl([28+ct+cr,130,65+ct+cr],cr,c['length'],[0,1,0]))
    cleat=cleat.fuse(crs).cut(cyl([36.5,136.35,64],2.15,ct+2,[0,0,1]))
    for yy in (134,148):cleat=cleat.cut(cyl([27,yy,74.5],2.15,ct+2,[1,0,0]))
    parts={'N_left_support_angle':angle.removeSplitter(),'N_right_support_angle':mirror(angle).removeSplitter(),
        'N_crossmember':beam,'N_left_cleat':cleat.removeSplitter(),'N_right_cleat':mirror(cleat).removeSplitter()}
    nominal=J.nominal()
    for key in ('motor_bracket','motor_reference','motor_screw_0','motor_screw_1'):
        parts['left_'+key]=nominal[key];parts['right_'+key]=mirror(nominal[key])
    wheel=J.ring(2,105,36,36,28,24)
    parts['left_wheel_envelope']=wheel;parts['right_wheel_envelope']=mirror(wheel)
    hub=J.ring(14,105,36,14,2.015,8)
    parts['left_hub_envelope']=hub;parts['right_hub_envelope']=mirror(hub)
    # Sleeves inserted from open tube ends; bolt holes remain bolt-sized.
    for i,xx in enumerate((42.8,68.2,275-42.8,275-68.2)):
        parts['horizontal_sleeve_'+str(i)]=J.ring(xx,130+bt,58.65,3,2.15,by-2*bt,(0,1,0))
    for i,xx in enumerate((36.5,238.5)):
        parts['vertical_sleeve_'+str(i)]=J.ring(xx,136.35,52.3+bt,3,2.15,bz-2*bt,(0,0,1))
    return parts


def context(bottom):
    p=N.M.prepare(bottom);parts=[]
    for v in p['parts']:
        id=v['id']
        if id in ('I_cap_height_bound',) or id.startswith(('H_left_cheek','H_right_cheek','H_left_cap','H_right_cap')):continue
        v=dict(v,min=v['min'][:],size=v['size'][:])
        if id.startswith('H_inner_rail_'):v['size'][1]=130-v['min'][1]
        parts.append(v)
    return parts


def main():
    d=N.read();shapes=geometry(d)
    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
    checks=dict(fabrication_release=False,valid_shapes={},stock_mass={},local_intersections=[],context_intersections={},
        exclusions='Fastener heads/nuts and access are not modeled except the preserved motor screws. Wheel/hub are envelopes, not supplier solids. The old inner rails stop at the new beam; their joints and the beam-cleat-rail connections need detailing. No continuous terrain collision check.')
    for id,s in shapes.items():
        if s.isNull() or not s.isValid():raise ValueError('Invalid '+id)
        checks['valid_shapes'][id]=True
        if id.startswith('N_'):checks['stock_mass'][id]=s.Volume*.0027
    # All new stock against all local solids, omitting deliberate stock faces
    # and material-interface contacts. Solid overlap above tolerance is an error.
    for (a,sa),(b,sb) in itertools.combinations(shapes.items(),2):
        if not (a.startswith('N_') or b.startswith('N_')):continue
        volume=sa.common(sb).Volume
        if volume>1e-5:checks['local_intersections'].append(dict(a=a,b=b,mm3=volume))
    for bottom in ('vacuum','mop'):
        name='fixed_drive_'+bottom;doc=App.newDocument(name);objects=[];conflicts=[]
        for id,s in shapes.items():
            obj=doc.addObject('PartDesign::Feature',id);obj.Shape=s;objects.append(obj)
            obj.addProperty('App::PropertyString','Scope');obj.Scope='Nominal comparison geometry; no fabrication release'
            if obj.ViewObject:obj.ViewObject.ShapeColor=(.24,.6,.56) if id.startswith('N_') else (.45,.49,.55)
        for p in context(bottom):
            s=box(p['min'],p['size'])
            for id,new in shapes.items():
                if id.startswith('N_'):
                    vol=new.common(s).Volume
                    if vol>1e-5:conflicts.append(dict(new=id,allocation=p['id'],mm3=vol))
            obj=doc.addObject('PartDesign::Feature',p['id']);obj.Shape=Part.makeCompound(s.Edges)
            obj.addProperty('App::PropertyString','Scope');obj.Scope='Retained allocation; inner rails terminate at beam; joint unfinished'
            objects.append(obj)
        checks['context_intersections'][bottom]=conflicts
        doc.recompute();doc.saveAs(str(N.OUT/(name+'.FCStd')));Part.export(objects,str(N.OUT/(name+'.step')));App.closeDocument(doc.Name)
    (N.OUT/'fixed_drive_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('N CAD:',len(shapes),'valid local solids; local conflicts',checks['local_intersections'],'context',checks['context_intersections'])


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
