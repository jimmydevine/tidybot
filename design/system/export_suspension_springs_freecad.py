"""L enlarged spring reservation in K joints; selected finite-pose audit."""
import hashlib
import json
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(ROOT/'design/system'))
import export_pod_joints_freecad as Kcad
import suspension_springs as L
import wheel_pod as J


def main():
    out=ROOT/'design/system/output';d=L.read()
    candidate=next(c for c in d['candidates'] if c['id']==d['preferred_candidate'])
    Kcad.old.d=L.spring_definition(candidate)
    checks=dict(fabrication_release=False,scope='L spring envelope and K local pod geometry only; no new complete-robot collision or structural qualification',
        input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                     [ROOT/'config/suspension_springs.json',out/'pod_joints_cad_checks.json']},
        spring_checks=[],unexpected_interferences=[],valid_shapes={})
    # Use the nominal module settings, including the lowest and highest settings,
    # and one extra 4.5 mm sensitivity setting. No unchecked shim is approved.
    shims=sorted({v for b in ('vacuum','mop','low') for v in L.calibrate(L.prepare(b,d),candidate)['shims_mm']}|{4.5})
    poses={}
    for t in (-2.5,0,1,3,5,10):
        for shim in shims:
            parts,bolts=Kcad.posed(t,shim)
            pose=J.spring_pose(Kcad.h,Kcad.old.d,t,shim)
            ring=Kcad.ring(80,*pose['lower_contact_yz_mm'],d['spring_envelope_od_mm']/2,
                           d['spring_envelope_id_mm']/2,pose['length_mm'],(0,*pose['unit_yz']))
            parts['spring_envelope']['shape']=ring
            for id,row in parts.items():
                if id=='spring_envelope' or row['material']=='envelope':continue
                if not ring.BoundBox.intersect(row['shape'].BoundBox):continue
                vol=ring.common(row['shape']).Volume
                if vol>1e-4:checks['unexpected_interferences'].append(dict(travel_mm=t,shim_mm=shim,a='spring_envelope',b=id,volume_mm3=vol))
            checks['spring_checks'].append(dict(travel_mm=t,shim_mm=shim,length_mm=pose['length_mm']))
            poses[(t,shim)]=(parts,bolts)
    for name,t,shim in [('suspension_springs',3,3.75),('suspension_springs_bump',10,3.75),('suspension_springs_droop',-2.5,2.5)]:
        parts,bolts=poses[(t,shim)];doc=App.newDocument(name);objects=[]
        intended={frozenset((b['id'],b['members'][-1])) for b in bolts if b['threaded_receiver']}
        intended|={frozenset(('motor_screw_'+str(i),'motor_reference')) for i in (0,1)}
        ids=[id for id,row in parts.items() if row['material']!='envelope']
        for i,a in enumerate(ids):
            for b in ids[i+1:]:
                if frozenset((a,b)) in intended:continue
                sa,sb=parts[a]['shape'],parts[b]['shape']
                if not sa.BoundBox.intersect(sb.BoundBox):continue
                vol=sa.common(sb).Volume
                if vol>1e-4:checks['unexpected_interferences'].append(dict(travel_mm=t,shim_mm=shim,a=a,b=b,volume_mm3=vol))
        for id,row in parts.items():
            shape=row['shape']
            if shape.isNull() or not shape.isValid():raise ValueError((name,id,'invalid shape'))
            obj=doc.addObject('PartDesign::Feature',id)
            obj.Shape=Part.makeCompound(shape.Edges) if row['material']=='envelope' else shape
            obj.addProperty('App::PropertyString','Scope');obj.Scope=checks['scope']
            objects.append(obj)
        doc.recompute();doc.saveAs(str(out/(name+'.FCStd')));Part.export(objects,str(out/(name+'.step')))
        checks['valid_shapes'][name]=len(objects);App.closeDocument(doc.Name)
    (out/'suspension_springs_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('L spring checks',len(checks['spring_checks']),'objects',checks['valid_shapes'],'interferences',checks['unexpected_interferences'])


# FreeCAD invokes command-line Python files under their basename.
if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
