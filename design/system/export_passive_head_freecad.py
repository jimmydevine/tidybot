"""Q guide/reference fit and actual kinematic head motion against P/N context.

The catalog guides are envelopes. Bearing cages, joints, springs and capture
remain unfinished; no STL or complete-assembly collision claim is exported.
"""
import itertools
import json
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'design/system'))
import passive_head as Q
import head_coupling as P
import export_head_coupling_freecad as EP
import export_fixed_drive_freecad as EN
V=App.Vector


def transform(shape,p):
    matrix=App.Matrix()
    for i in range(3):
        for j in range(3):setattr(matrix,f'A{i+1}{j+1}',p['R'][i][j])
        setattr(matrix,f'A{i+1}4',p['T'][i])
    s=shape.copy();s.transformShape(matrix,False);return s


def references(d,p):
    fixed={};moving={};xyz=d['rail_left_min_mm'];size=d['rail_envelope_mm']
    for side in (0,1):
        name='left' if side==0 else 'right'
        rail=EP.box(xyz,size)
        fixed[name+'_rail_envelope']=EP.mirror(rail) if side else rail
        z=p['carriage_z_mm'][side];pivot=p['pivot_z_mm'][side]
        # Carriage envelopes intentionally occupy their own rail envelopes.
        cart=EP.box([xyz[0]+1,25.2,z-10],[5,9.6,20])
        bx=xyz[0]+6
        bracket=EP.box([bx,23,pivot-6],[2,14,d['carriage_above_pivot_mm']+14])
        bracket=bracket.cut(EP.cylinder([bx-1,30,pivot],1.6,4))
        bracket=bracket.cut(EP.cylinder([bx-1,30,z],1.7,4))
        moving[name+'_carriage_envelope']=EP.mirror(cart) if side else cart
        moving[name+'_drop_link_reference']=EP.mirror(bracket) if side else bracket
    for side,x in [('left',d['pivot_left_mm'][0]),('right',d['pivot_right_x_mm'])]:
        _,y,z=d['pivot_left_mm']
        bearing=EP.cylinder([x-3,y,z],5,6).cut(EP.cylinder([x-4,y,z],1.5,8))
        moving[side+'_bearing_envelope']=transform(bearing,p)
    return fixed,moving


def main():
    r=Q.study();d=r['config'];pd=P.read();body,carrier=EP.geometry(pd);base,ctx=EP.context(pd)
    ctx['vac_side'].translate(V(d['side_brush_shift_x_mm'],0,0))
    # Validate against the N stock too, rather than inheriting P's omission.
    ctx={**{k:v for k,v in ctx.items() if k not in ('vac_head','vac_head_drive')},**EN.geometry(EN.N.read())}
    base_shapes={**{'P_body_'+k:v for k,v in body.items()},**{'P_carrier_'+k:v for k,v in carrier.items()},**ctx}
    head=next(v for v in base['parts'] if v['id']=='vac_head')
    motor=next(v for v in base['parts'] if v['id']=='vac_head_drive')
    roller=EP.box([37.2,13.45,0],[200.6,45.1,45.1])
    motor_shape=EP.box(motor['min'],motor['size'])
    head_shape=EP.box(head['min'],head['size'])
    nominal=r['poses'][0];fixed,_=references(d,nominal)
    checks=dict(fabrication_release=False,source_fingerprint=P.source_fingerprint(),
        guide_context_intersections=[],moving_reference_intersections=[],head_P_N_intersections=[],
        head_frame_rework_required=[],valid_shapes={},pose_count=len(r['poses'])+1,
        scope='Rail/carriage/bearing catalog envelopes and nominal drop-link stock. New guides versus P interface and modified M/H plus N stock; protected roller and motor versus new guides. Existing head-frame end regions need rework. P carrier supports, precise pivot pins/cages, spring/capture hardware, flex and full dock withdrawal absent. Rail/carriage overlap is intentional.')
    def overlaps(a,sa,b,sb,field,pose=None):
        if not sa.BoundBox.intersect(sb.BoundBox):return
        volume=sa.common(sb).Volume
        if volume>1e-5:checks[field].append(dict(a=a,b=b,volume_mm3=volume,pose=pose))
    for a,sa in fixed.items():
        checks['valid_shapes'][a]=sa.isValid()
        for b,sb in base_shapes.items():overlaps(a,sa,b,sb,'guide_context_intersections')
    minimum=1e9;closest=None
    for num,p in enumerate([*r['poses'],r['raised']]):
        _,moving=references(d,p)
        protected={'roller':transform(roller,p),'motor':transform(motor_shape,p)}
        whole=transform(head_shape,p)
        for a,sa in moving.items():
            checks['valid_shapes'][a]=checks['valid_shapes'].get(a,True) and sa.isValid()
            for b,sb in base_shapes.items():overlaps(a,sa,b,sb,'moving_reference_intersections',num)
            for b,sb in protected.items():overlaps(a,sa,b,sb,'moving_reference_intersections',num)
        for a,sa in fixed.items():
            for b,sb in protected.items():overlaps(a,sa,b,sb,'moving_reference_intersections',num)
            overlaps(a,sa,'old_head_frame_allocation',whole,'head_frame_rework_required',num)
        for a,sa in {**protected,'head_allocation':whole}.items():
            for b,sb in base_shapes.items():
                overlaps(a,sa,b,sb,'head_P_N_intersections',num)
                if b.startswith('P_'):
                    dist=sa.distToShape(sb)[0]
                    if dist<minimum:minimum=dist;closest=dict(pose=num,a=a,b=b)
    checks['minimum_sampled_P_gap_mm']=minimum;checks['closest_pair']=closest
    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
    choices={'level':nominal,'left_step':min(r['poses'],key=lambda p:p['carriage_z_mm'][0]),'captured':r['raised']}
    for name,p in choices.items():
        doc=App.newDocument('passive_head_'+name);objects=[];_,moving=references(d,p)
        solids={**fixed,**moving,'roller_reference':transform(roller,p),'motor_reference':transform(motor_shape,p)}
        for group,parts in [('Q',solids),('context',base_shapes),('head_frame_to_rework',{'allocation':transform(head_shape,p)})]:
            for id,s in parts.items():
                ob=doc.addObject('PartDesign::Feature',group+'_'+id);ob.Shape=s if group=='Q' else Part.makeCompound(s.Edges)
                ob.addProperty('App::PropertyString','Scope');ob.Scope=checks['scope'];objects.append(ob)
        doc.recompute();doc.saveAs(str(Q.OUT/(doc.Name+'.FCStd')));Part.export(objects,str(Q.OUT/(doc.Name+'.step')));App.closeDocument(doc.Name)
    (Q.OUT/'passive_head_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in checks.items() if k!='valid_shapes'},indent=2))


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
