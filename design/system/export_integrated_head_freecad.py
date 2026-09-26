"""R material geometry and sampled motion checks; exports review CAD, not STLs."""
import itertools
import json
import math
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'design/system'))
import integrated_head as R
import passive_head as Q
import head_coupling as P
import export_passive_head_freecad as EQ
import export_head_coupling_freecad as EP
import export_fixed_drive_freecad as EN
V=App.Vector


def profile(x, yz, thick):
    pts=[V(x,y,z) for y,z in yz]
    return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(thick,0,0))


def left_frame(d):
    x=d['end_wall_x_mm'];t=d['end_wall_thickness_mm'];outer=d['cage_left_x_mm']
    yz=[(6,13.5),(20,0),(52,0),(66,13.5),(66,47.6),(6,47.6)]
    side=profile(x,yz,t)
    # The curved floor approach and pivot cage are integral with the end wall.
    skid=profile(outer,[(6,13.5),(20,0),(52,0),(66,13.5),
        (66,15.1),(52,1.6),(20,1.6),(6,15.1)],x+t-outer)
    cage=EP.cylinder([outer,30,20],d['bearing_cage_outer_radius_mm'],x+t-outer)
    boss=EP.box([outer,44,16],[x+t-outer,8,8])
    frame=side.fuse(skid).fuse(cage).fuse(boss)
    frame=frame.cut(EP.cylinder([outer-.1,30,20],d['bearing_pocket_radius_mm'],35.1-outer+.1))
    frame=frame.cut(EP.cylinder([35.05,30,20],1.9,3))
    frame=frame.cut(EP.cylinder([outer-.1,48,20],1.1,x+t-outer+.2))
    return frame.removeSplitter()


def hood(d):
    x=d['end_wall_x_mm']+d['end_wall_thickness_mm'];length=275-2*x;t=d['hood_wall_mm']
    top=EP.box([x,10.8,46.2],[length,50.4,t])
    front=EP.box([x,10.8,14],[length,t,32.2])
    rear=EP.box([x,59.8,14],[length,t,32.2])
    rear=rear.cut(EP.box([121.5,59.7,19],[32,t+.2,22]))
    stub=EP.box([118.5,61.2,16],[38,4.8,28]).cut(EP.box([121.5,61.1,19],[32,5,22]))
    return top.fuse(front).fuse(rear).fuse(stub).removeSplitter()


def link(d,z=20):
    s=EP.box([25.5,23,z-6],[2,14,34]).fuse(EP.box([25.5,35,z-6],[2,18,14]))
    for h,r in [(z,1.6),(z+20,1.7)]:s=s.cut(EP.cylinder([25.4,30,h],r,2.2))
    # Swept round pin gives a true arc-ended slot, not a rectangular limit.
    radius=d['pitch_pin_y_mm']-30
    half=d['pitch_pin_radius_mm']+d['pitch_pin_clearance_mm']
    angle=math.radians(6)
    def pt(r,a):return V(25.4,30+r*math.cos(a),z+r*math.sin(a))
    hi,lo=radius+half,radius-half
    edges=[Part.Arc(pt(hi,-angle),pt(hi,0),pt(hi,angle)).toShape(),
        Part.makeLine(pt(hi,angle),pt(lo,angle)),
        Part.Arc(pt(lo,angle),pt(lo,0),pt(lo,-angle)).toShape(),
        Part.makeLine(pt(lo,-angle),pt(hi,-angle))]
    cut=Part.Face(Part.Wire(edges)).extrude(V(2.2,0,0))
    for a in (-angle,angle):
        cut=cut.fuse(EP.cylinder(list(pt(radius,a)),half,2.2))
    s=s.cut(cut)
    return s.removeSplitter()


def stop_pin():
    # M2 screw / 3 mm sleeve envelope. Threads, captive nut and wear grade open.
    return EP.cylinder([23.7,48,20],1.9,1.3).fuse(
        EP.cylinder([25,48,20],1.5,3.8)).fuse(EP.cylinder([28.8,48,20],1,6.5))


def geometry(d):
    fixed={};moving={};material={}
    def add(group,name,s,density,basis):
        if len(s.Solids)==1:s=s.Solids[0]
        group[name]=s
        centre=[sum(sol.Volume*sol.CenterOfMass[i] for sol in s.Solids)/s.Volume for i in range(3)]
        material[name]=dict(id=name,mass_g=s.Volume*density,volume_mm3=s.Volume,
            moving=group is moving,centre_mm=centre,basis=basis)
    for side in ('left','right'):
        mirror=(lambda s:EP.mirror(s)) if side=='right' else (lambda s:s)
        add(moving,side+'_integrated_end',mirror(left_frame(d)),d['polymer_density_g_mm3'],
            'Solid-volume PETG estimate: end wall, bearing pocket, skid ramps and stop boss; hardware separate')
        add(moving,side+'_drop_link',mirror(link(d)),d['aluminum_density_g_mm3'],
            '2 mm aluminum profile with pivot/carriage holes and pitch-stop arc slot; keyed attachment unresolved')
        t=d['rail_backing_thickness_mm']
        backing=EP.box([19.5-t,21.5,12],[t,17,62]).fuse(EP.box([19.5-t,21.5,72],[t,40,12]))
        # Open rearward: a round clearance hole would trap the P guide screw
        # during forward tool withdrawal even though the seated fit passed.
        relief=EP.cylinder([18.3,46,76],1.75,1.4).fuse(EP.box([18.3,46,74.25],[1.4,17,3.5]))
        backing=backing.cut(relief)
        add(fixed,side+'_rail_backing',mirror(backing.removeSplitter()),d['steel_density_g_mm3'],
            '1 mm steel L-shaped backing with rear-open P screw relief; rail attachment holes still unmodeled')
        spacer=EP.box([19.5,40,78],[3.2,23,6])
        relief=EP.cylinder([19.4,46,76],3.5,3.4).fuse(EP.box([19.4,46,72.5],[3.4,18,7]))
        spacer=spacer.cut(relief)
        add(fixed,side+'_carrier_spacer',mirror(spacer),d['polymer_density_g_mm3'],
            'Carrier offset pad; screws, load-spreading and keyed joints not modeled')
    add(moving,'hood_and_outlet',hood(d),d['polymer_density_g_mm3'],
        '1.4 mm solid walls with rear outlet; end joints, motor mounts, seals and fasteners budgeted separately')
    return fixed,moving,material


def moved_parts(parts,p):
    out={}
    for name,s in parts.items():
        if name.endswith('drop_link'):
            index=0 if name.startswith('left') else 1
            moved=s.copy();moved.translate(V(0,0,p['pivot_z_mm'][index]-20))
            out[name]=moved
        else:out[name]=EQ.transform(s,p)
    return out


def draw_svg(shapes,path):
    # Project actual edges: local end view and whole-head front elevation.
    lines=['<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="650" viewBox="0 0 1160 650">',
        '<rect width="1160" height="650" fill="#f6f8fa"/>',
        '<text x="25" y="34" font-size="24" font-family="sans-serif">R — integrated cassette ends (review geometry)</text>',
        '<text x="25" y="64" font-size="15" font-family="sans-serif">Blue: printed frame · orange: moving link · teal: fixed guide support · gray: roller envelope</text>',
        '<text x="25" y="94" font-size="17" font-family="sans-serif">Left end, looking along the axle</text>',
        '<text x="490" y="94" font-size="17" font-family="sans-serif">Front elevation, looking toward the rear</text>']
    for name,s in shapes.items():
        color='#0e7490' if ('backing' in name or 'rail' in name or 'spacer' in name) else '#d97706' if ('link' in name or 'pin' in name) else '#8994a3' if 'reference' in name else '#2563eb'
        for view in ('end','front'):
            if view=='end' and name.startswith('right'):continue
            for e in s.Edges:
                pts=e.discretize(Deflection=.15)
                xy=[(35+4*p.y,460-4*p.z) if view=='end' else (485+2.3*p.x,460-3.7*p.z) for p in pts]
                lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="1" opacity="0.8" points="'+ ' '.join(f'{a:.2f},{b:.2f}' for a,b in xy)+'"/>')
    lines += ['<text x="25" y="520" font-size="17" font-family="sans-serif">Shared end wall: bearing seat + front/rear skid ramps + pitch-stop boss</text>',
        '<text x="25" y="550" font-size="15" font-family="sans-serif">The orange link slides vertically. Its curved slot limits head pitch while the head pivots inside it.</text>',
        '<text x="25" y="580" font-size="15" font-family="sans-serif">Roller ends, pivot retainers, guide joints and powered lift remain unfinished. Do not print from this review.</text>',
        '<text x="25" y="610" font-size="15" font-family="sans-serif">Floor at z = 0; raised head travels 16 mm. Air-flex motion and full mass accounting are in the linked report.</text>','</svg>']
    path.write_text('\n'.join(lines)+'\n')


def main():
    d=R.read();q=Q.study();pd=P.read();fixed,moving,material=geometry(d)
    body,carrier=EP.geometry(pd);base,ctx=EP.context(pd)
    ctx['vac_side'].translate(V(q['config']['side_brush_shift_x_mm']+d['side_brush_shift_from_Q_mm'],0,0))
    ctx={k:v for k,v in ctx.items() if k not in ('vac_head','vac_head_drive')}
    context={**{'P_body_'+k:v for k,v in body.items()},**{'P_carrier_'+k:v for k,v in carrier.items()},**ctx,**EN.geometry(EN.N.read())}
    roller=EP.box([37.2,13.45,0],[200.6,45.1,45.1]);motor=EP.box([32,6,50],[71,60,29])
    guides,_=EQ.references(q['config'],q['poses'][0])
    checks=dict(source_fingerprint=P.source_fingerprint(),fabrication_release=False,
        pose_count=len(q['poses'])+1,intersections=[],withdrawal_intersections=[],pitch_stop_controls=[],valid_solids={},mass_rows=list(material.values()),
        minimum_roller_clearance_mm=1e9,minimum_guide_clearance_mm=1e9,
        scope='Actual modeled frame/hood/link/backing solids versus P/N and modified H allocations over Q poses; protected purchased envelopes and 120 mm withdrawal with head raised. Rail/carriage overlap, link/carriage face and guide-envelope tangency are intentional. Backing/guide and spacer/cheek face contact is intentional. Bearing pockets and stop slots are checked. Pivot fasteners, carriage antirotation, rail screws/end stops, motor/end inserts, flexible hose and powered lift joints are not modeled.')
    def clash(a,sa,b,sb,n=None,field='intersections'):
        if not sa.BoundBox.intersect(sb.BoundBox):return
        volume=sa.common(sb).Volume
        if volume>1e-5:checks[field].append(dict(a=a,b=b,pose=n,volume_mm3=volume))
    for a,sa in {**fixed,**moving}.items():
        checks['valid_solids'][a]=sa.isValid() and len(sa.Solids)==1
    for a,sa in fixed.items():
        for b,sb in {**context,**guides}.items():clash(a,sa,b,sb)
    for (a,sa),(b,sb) in itertools.combinations(fixed.items(),2):clash(a,sa,b,sb)
    poses=[*q['poses'],q['raised']]
    for n,p in enumerate(poses):
        if n%20==0:print('Checking R pose',n,flush=True)
        parts=moved_parts(moving,p);_,refs=EQ.references(q['config'],p)
        refs={k:v for k,v in refs.items() if not k.endswith('drop_link_reference')}
        for side in ('left','right'):
            s=stop_pin();s=EP.mirror(s) if side=='right' else s
            refs[side+'_pitch_pin_reference']=EQ.transform(s,p)
        protected={'roller_reference':EQ.transform(roller,p),'motor_reference':EQ.transform(motor,p)}
        for a,sa in parts.items():
            for b,sb in {**context,**fixed,**guides,**protected,**refs}.items():clash(a,sa,b,sb,n)
            checks['minimum_roller_clearance_mm']=min(checks['minimum_roller_clearance_mm'],sa.distToShape(protected['roller_reference'])[0])
            if not a.endswith('drop_link'):
                for sb in guides.values():checks['minimum_guide_clearance_mm']=min(checks['minimum_guide_clearance_mm'],sa.distToShape(sb)[0])
        for (a,sa),(b,sb) in itertools.combinations(parts.items(),2):clash(a,sa,b,sb,n)
        for a,sa in refs.items():
            for b,sb in {**context,**fixed,**protected}.items():clash(a,sa,b,sb,n)
    for angle in (-7,7):
        radians=math.radians(angle)
        p=Q.pose(q['config'],[0,-math.sin(radians),math.cos(radians)],0,0)
        links=moved_parts(moving,p)
        for side in ('left','right'):
            pin=stop_pin();pin=EP.mirror(pin) if side=='right' else pin
            volume=links[side+'_drop_link'].common(EQ.transform(pin,p)).Volume
            checks['pitch_stop_controls'].append(dict(angle_deg=angle,side=side,interference_mm3=volume))
    print('Checking R withdrawal',flush=True)
    unlocked={name:s.copy() for name,s in body.items()}
    for name,s in unlocked.items():
        if 'lock_' in name:s.translate(V(-pd['locks']['withdrawal_mm'] if name.startswith('left') else pd['locks']['withdrawal_mm'],0,0))
    fixed_context={**{'P_body_'+k:v for k,v in unlocked.items()},**ctx,**EN.geometry(EN.N.read())}
    withdrawing={**fixed,**moved_parts(moving,q['raised']),**guides,**carrier,
        'roller_reference':EQ.transform(roller,q['raised']),'motor_reference':EQ.transform(motor,q['raised'])}
    for distance in range(pd['withdrawal_mm']+1):
        for a,sa in withdrawing.items():
            moved=sa.copy();moved.translate(V(0,-distance,0))
            for b,sb in fixed_context.items():clash(a,moved,b,sb,distance,'withdrawal_intersections')
    checks['withdrawal_samples']=pd['withdrawal_mm']+1
    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
    choices={'level':poses[0],'left_step':min(q['poses'],key=lambda p:p['carriage_z_mm'][0]),'raised':q['raised']}
    for suffix,p in choices.items():
        doc=App.newDocument('integrated_head_'+suffix);objects=[];parts=moved_parts(moving,p);_,refs=EQ.references(q['config'],p)
        refs={k:v for k,v in refs.items() if not k.endswith('drop_link_reference')}
        solids={**fixed,**parts,**guides,**refs,'roller_reference':EQ.transform(roller,p),'motor_reference':EQ.transform(motor,p)}
        for name,s in solids.items():
            ob=doc.addObject('PartDesign::Feature',name);ob.Shape=s
            ob.addProperty('App::PropertyString','Scope');ob.Scope=checks['scope'];objects.append(ob)
        for name,s in context.items():
            ob=doc.addObject('PartDesign::Feature','context_'+name);ob.Shape=Part.makeCompound(s.Edges);objects.append(ob)
        doc.recompute();doc.saveAs(str(R.OUT/(doc.Name+'.FCStd')));Part.export(objects,str(R.OUT/(doc.Name+'.step')));App.closeDocument(doc.Name)
        if suffix=='level':draw_svg(solids,R.OUT/'integrated_head.svg')
    (R.OUT/'integrated_head_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({k:v for k,v in checks.items() if k not in ('intersections','mass_rows')},indent=2))
    print('Intersections:',len(checks['intersections']))
    print(json.dumps(checks['intersections'][:15],indent=2))


if __name__=='__main__' or any(Path(a).resolve()==Path(__file__).resolve() for a in sys.argv[1:]):main()
