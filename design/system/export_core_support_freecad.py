"""S core supports: scoped CSG solids, component clearance and exchange paths."""
import itertools
import json
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'design/system'))
import core_support as S
import head_coupling as P
import export_head_coupling_freecad as EP
import export_fixed_drive_freecad as EN
V=App.Vector


def solid(p):
    additions=[EP.box(b[:3],b[3:]) for b in p['add']]
    shape=additions[0]
    for s in additions[1:]:shape=shape.fuse(s)
    for b in p['cut']:shape=shape.cut(EP.box(b[:3],b[3:]))
    return shape.removeSplitter()


def context(bottom):
    p=S.M.prepare(bottom);out={};core={};floor={}
    for v in p['parts']:
        if v.get('parent') or v.get('shape')=='distributed':continue
        # The old filled mount/battery allocations are not material. Check
        # actual protected cell/connection reservations below instead.
        if v['id'] in ('battery_bay','I_lidar_mount','I_cap_height_bound') or v.get('module')=='cap':continue
        if v['id'].startswith('G_') and v.get('drill_axis')=='z':
            shape=EP.box(v['min'],v['size']);xx,yy=v['drill_center']
            shape=shape.cut(EP.cylinder([xx,yy,v['min'][2]-1],v['drill_diameter']/2,v['size'][2]+2,(0,0,1)))
        elif v.get('shape_override')=='slider':
            # Outline used only as a forbidden volume; no new joint design here.
            shape=EP.box(v['min'],v['size'])
        else:shape=EP.box(v['min'],v['size'])
        out[v['id']]=shape
        (core if v.get('module')=='core' else floor)[v['id']]=shape
    # Include actual fixed-drive supports; superseded K pod regions are present
    # only in the inherited layout, so discard their allocations explicitly.
    for group in (out,floor):
        for name in list(group):
            if name.startswith(('J_','K_')):del group[name]
        group.update(EN.geometry(S.N.read()))
    return p,out,core,floor


def main():
    r=S.study();d=r['config'];modeled={p['id']:solid(p) for p in r['parts']}
    checks=dict(source_fingerprint=P.source_fingerprint(),fabrication_release=False,
        valid_solids={},volume_differences_mm3={},internal_intersections=[],component_intersections=[],
        protected_reservation_intersections=[],core_upward_intersections=[],battery_downward_intersections=[],
        minimum_nominal_guide_gap_mm=.2,scope='S material versus M equipment allocations and N drive supports for vacuum/mop; old filled battery/lidar-mount reservations excluded only for their intended replacement. Protected cell and electrical-end volumes checked separately. 100 mm cartridge withdrawal with tongues released and bottom removed. Upward core sweep includes new S pieces versus floor equipment. Full cartridge construction, cable sweeps, tolerances, sheet radii, motor/lift contacts and unmapped duster layout remain unverified.')
    def clash(a,sa,b,sb,field,step=None,bottom=None):
        if not sa.BoundBox.intersect(sb.BoundBox):return
        volume=sa.common(sb).Volume
        if volume>1e-5:checks[field].append(dict(a=a,b=b,volume_mm3=volume,step_mm=step,bottom=bottom))
    for p in r['parts']:
        shape=modeled[p['id']]
        checks['valid_solids'][p['id']]=shape.isValid() and len(shape.Solids)==1
        checks['volume_differences_mm3'][p['id']]=shape.Volume-p['volume_mm3']
    for (a,sa),(b,sb) in itertools.combinations(modeled.items(),2):clash(a,sa,b,sb,'internal_intersections')
    protected={'cell_pocket':EP.box([46,88,67],[158,62,53]),'electrical_end':EP.box([206,88,67],[16,62,53])}
    for a,sa in modeled.items():
        for b,sb in protected.items():clash(a,sa,b,sb,'protected_reservation_intersections')
    contexts={}
    for bottom in ('vacuum','mop'):
        p,ctx,core,floor=context(bottom);contexts[bottom]=(p,ctx,core,floor)
        for a,sa in modeled.items():
            for b,sb in ctx.items():clash(a,sa,b,sb,'component_intersections',bottom=bottom)
            # Exact swept solid for each rectangular primitive would hide CSG
            # holes. Sample every mm of the first 180 mm, then use the remaining
            # maximum floor height to prove it has completely cleared.
            for step in range(181):
                moved=sa.copy();moved.translate(V(0,0,step))
                for b,sb in floor.items():clash(a,moved,b,sb,'core_upward_intersections',step,bottom)
    cartridge=EP.box([44,86,66],[180,66,55])
    released={id:s.copy() for id,s in modeled.items()}
    for id,s in released.items():
        if id.endswith('battery_tongue'):s.translate(V(-d['receiver']['latch_stroke'] if id.startswith('left') else d['receiver']['latch_stroke'],0,0))
    fixed={**contexts['vacuum'][2],**released}
    for step in range(101):
        moved=cartridge.copy();moved.translate(V(0,0,-step))
        for b,sb in fixed.items():clash('cartridge',moved,b,sb,'battery_downward_intersections',step)
    # Negative control: a metal cartridge shoulder would be blocked by the
    # tongue if withdrawal were attempted without release.
    checks['closed_latch_negative_controls']=[]
    for side,x in [('left',44),('right',222.5)]:
        shoulder=EP.box([x,112,69.5],[1.5,8,2])
        checks['closed_latch_negative_controls'].append(dict(side=side,downward_attempt_mm=.5,
            interference_mm3=shoulder.common(modeled[side+'_battery_tongue']).Volume))
    checks['upward_steps']=181;checks['downward_steps']=101
    checks['printed_part_bounds_mm']={p['id']:[modeled[p['id']].BoundBox.XLength,modeled[p['id']].BoundBox.YLength,modeled[p['id']].BoundBox.ZLength] for p in r['parts'] if p['material']=='polymer'}
    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
    drawing=[]
    # Export a core-only review assembly; context components are outlines.
    for name,travel in [('installed',0),('withdrawn',100)]:
        doc=App.newDocument('core_support_'+name);objects=[]
        shapes=modeled if not travel else released
        for id,s in shapes.items():
            ob=doc.addObject('PartDesign::Feature',id);ob.Shape=s;objects.append(ob)
            if not travel:drawing.append(dict(id=id,role='latch' if id.endswith('battery_tongue') else 'fixed',material=next(p['material'] for p in r['parts'] if p['id']==id),edges=[[list(v) for v in e.discretize(Deflection=.2)] for e in s.Edges]))
        for id,s in contexts['vacuum'][2].items():
            ob=doc.addObject('PartDesign::Feature','context_'+id);ob.Shape=Part.makeCompound(s.Edges);objects.append(ob)
            if not travel:drawing.append(dict(id=id,role='context',material='frame' if id.startswith('G_') else 'equipment',edges=[[list(v) for v in e.discretize(Deflection=.5)] for e in s.Edges]))
        cart=cartridge.copy();cart.translate(V(0,0,-travel))
        ob=doc.addObject('PartDesign::Feature','cartridge_allocation');ob.Shape=Part.makeCompound(cart.Edges);objects.append(ob)
        if not travel:drawing.append(dict(id='cartridge',role='cartridge',material='cartridge',edges=[[list(v) for v in e.discretize(Deflection=.5)] for e in cart.Edges]))
        doc.recompute();doc.saveAs(str(S.OUT/(doc.Name+'.FCStd')));Part.export(objects,str(S.OUT/(doc.Name+'.step')));App.closeDocument(doc.Name)
    (S.OUT/'core_support_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    (S.OUT/'core_support_view_data.json').write_text(json.dumps(drawing)+'\n')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in checks.items() if k not in ('valid_solids','volume_differences_mm3','printed_part_bounds_mm')},indent=2))
    for key in ('internal_intersections','component_intersections','protected_reservation_intersections','core_upward_intersections','battery_downward_intersections'):
        print(key,json.dumps(checks[key][:10]))


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
