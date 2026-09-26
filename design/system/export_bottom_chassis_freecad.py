"""T review geometry with explicitly reported fit failures; not print files."""
import itertools
import json
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'design/system'))
import bottom_chassis as T
import core_support as S
import passive_head as Q
import head_coupling as P
import integrated_head as R
import export_core_support_freecad as ES
import export_head_coupling_freecad as EP
import export_fixed_drive_freecad as EN
import export_integrated_head_freecad as ER
import export_passive_head_freecad as EQ
V=App.Vector


def geometry(bottom,d):
    parts={v['id']:ES.solid(v) for v in T.geometry(bottom,d)}
    pd=P.read()
    for side in ('left','right'):
        id='left_side_rail' if side=='left' else 'right_front_rail'
        for y in pd['guide_pins']['y']:
            cut=EP.cylinder([23,y,76],1.65,6).fuse(Part.makeCone(1.5,3.1,1.6,V(26.4,y,76),V(1,0,0)))
            parts[id]=parts[id].cut(EP.mirror(cut) if side=='right' else cut)
        cut=EP.cylinder([23,pd['locks']['y'],pd['locks']['z']],pd['locks']['body_hole_diameter']/2,6)
        parts[id]=parts[id].cut(EP.mirror(cut) if side=='right' else cut)
    parts['caster_saddle']=parts['caster_saddle'].cut(EP.cylinder([137.5,232,55.5],4.25,5,(0,0,1)))
    for side,x in [('left',14),('right',261)]:
        for end,y in [('front',14),('rear',261)]:
            id=side+'_'+end+'_seat'
            parts[id]=parts[id].cut(EP.cylinder([x,y,81.8],2.15,5,(0,0,1)))
    return parts


def main():
    d=T.read();r=T.study(d);checks=dict(source_fingerprint=P.source_fingerprint(),
        fabrication_release=False,valid_solids={},internal_intersections=[],equipment_intersections=[],
        head_intersections=[],withdrawal_intersections=[],core_upward_intersections=[],bounds={},
        scope='T new material versus N, P and M equipment, plus S compatibility overlay. R/S masses not stacked. Drilled holes are not credited in T mass. Vacuum Q head poses and 120 mm withdrawal checked; mop head-motion check uses M ideal envelopes. No fastener fit, complete attachment/load-path, tolerance, cable, floor-clearance or automatic-exchange qualification.')
    view={}
    def clash(a,sa,b,sb,key,bottom=None,step=None):
        if not sa.BoundBox.intersect(sb.BoundBox):return
        v=sa.common(sb).Volume
        if v>1e-5:checks[key].append(dict(a=a,b=b,volume_mm3=v,bottom=bottom,step=step))
    for bottom in ('vacuum','mop'):
        modeled=geometry(bottom,d);p=T.M.prepare(bottom)
        ctx={}
        for v in p['parts']:
            id=v['id']
            if v.get('parent') or v.get('shape')=='distributed' or v.get('module')=='cap':continue
            if id.startswith(('H_','J_','K_','floor_')) or id in ('I_cap_height_bound','vac_flex','vac_head','vac_head_drive','mop_pad','mop_drive'):continue
            ctx[id]=EP.box(v['min'],v['size'])
        ctx.update(EN.geometry(T.N.read()))
        s_parts={('S_'+v['id']):ES.solid(v) for v in S.geometry()}
        # Check new T material against actual P receiver/carrier, not gross head.
        if bottom=='vacuum':
            body,carrier=EP.geometry(P.read());ctx.update({'P_body_'+k:v for k,v in body.items()})
            ctx.update({'P_carrier_'+k:v for k,v in carrier.items()})
            # Trim old duct at P stub and use R side-brush position.
            ctx['vac_duct']=EP.box([118.5,104,16],[38,53,28])
            ctx['vac_side'].translate(V(-2,0,0))
        for a,sa in modeled.items():
            checks['valid_solids'][bottom+'_'+a]=sa.isValid() and len(sa.Solids)==1
            for b,sb in {**ctx,**s_parts}.items():clash(a,sa,b,sb,'equipment_intersections',bottom)
        for (a,sa),(b,sb) in itertools.combinations(modeled.items(),2):clash(a,sa,b,sb,'internal_intersections',bottom)
        box=Part.makeCompound(list(modeled.values())).BoundBox
        checks['bounds'][bottom]=[box.XMin,box.YMin,box.ZMin,box.XMax,box.YMax,box.ZMax]
        core={v['id']:ctx[v['id']] for v in p['parts'] if v.get('module')=='core' and v['id'] in ctx}
        for a in list(core):
            if a.startswith('G_lock_') and a.endswith('_bottom') and not a.startswith('G_lock_pad_'):
                moved=core[a].copy()
                moved.translate(V(-8 if a.split('_')[2] in ('0','2') else 8,0,0));core[a]=moved
        # A rectangular component translated in +Z has an exact swept box.
        for a,sa in core.items():
            bb=sa.BoundBox;sweep=EP.box([bb.XMin,bb.YMin,bb.ZMin],[bb.XLength,bb.YLength,bb.ZLength+180])
            for b,sb in modeled.items():clash(a,sweep,b,sb,'core_upward_intersections',bottom)
        # New S supports have holes, so check their actual shapes at 1 mm steps.
        for a,sa in s_parts.items():
            for step in range(181):
                moved=sa.copy();moved.translate(V(0,0,step))
                for b,sb in modeled.items():clash(a,moved,b,sb,'core_upward_intersections',bottom,step)
        if bottom=='vacuum':
            q=Q.study();fixed,moving,_=ER.geometry(R.read())
            roller=EP.box([37.2,13.45,0],[200.6,45.1,45.1]);motor=EP.box([32,6,50],[71,60,29])
            for index,pose in enumerate([*q['poses'],q['raised']]):
                heads={**ER.moved_parts(moving,pose),'motor_envelope':EQ.transform(motor,pose),'roller_envelope':EQ.transform(roller,pose)}
                for a,sa in {**fixed,**heads}.items():
                    for b,sb in modeled.items():clash(a,sa,b,sb,'head_intersections',bottom,index)
            raised={**fixed,**ER.moved_parts(moving,q['raised']),**carrier,
                    'motor_envelope':EQ.transform(motor,q['raised']),'roller_envelope':EQ.transform(roller,q['raised'])}
            for step in range(121):
                for a,sa in raised.items():
                    moved=sa.copy();moved.translate(V(0,-step,0))
                    for b,sb in modeled.items():clash(a,moved,b,sb,'withdrawal_intersections',bottom,step)
            checks['vacuum_head_poses']=len(q['poses'])+1;checks['withdrawal_steps']=121
        else:
            _,mass=T.N.nominal_mass(bottom,T.N.read())
            poses=T.N.terrain(bottom,p,mass,T.N.read())+[dict(q_mm=16,normal=[0,0,1])]
            for index,pose in enumerate(poses):
                for part in [v for v in p['parts'] if v['id'] in ('mop_pad','mop_drive')]:
                    env=T.M.envelope(part,p['M']['modules'][bottom]['reference_mm'],pose['q_mm'],pose['normal'])
                    shape=EP.box(env['min'],env['size'])
                    for b,sb in modeled.items():clash(part['id'],shape,b,sb,'head_intersections',bottom,index)
            checks['mop_head_envelope_poses']=len(poses)
        doc=App.newDocument('bottom_chassis_'+bottom);objects=[];draw=[]
        for group,parts in [('material',modeled),('context',ctx)]:
            for id,shape in parts.items():
                ob=doc.addObject('PartDesign::Feature',group+'_'+id)
                ob.Shape=shape if group=='material' else Part.makeCompound(shape.Edges);objects.append(ob)
                draw.append(dict(id=id,group=group,edges=[[list(v) for v in e.discretize(Deflection=.4)] for e in shape.Edges]))
        doc.recompute();doc.saveAs(str(T.OUT/(doc.Name+'.FCStd')));Part.export(objects,str(T.OUT/(doc.Name+'.step')));App.closeDocument(doc.Name)
        view[bottom]=draw
    (T.OUT/'bottom_chassis_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    (T.OUT/'bottom_chassis_view_data.json').write_text(json.dumps(view)+'\n')
    checks['decision']='Rejected: mass increase and head/service-path obstructions. Keep as comparison evidence.'
    # Rewrite after attaching the decision, so viewers cannot imply approval.
    (T.OUT/'bottom_chassis_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    for key in checks:
        if key.endswith('intersections'):print(key,len(checks[key]),json.dumps(checks[key][:12]),flush=True)
    print('valid',all(checks['valid_solids'].values()),flush=True)


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
