"""M allocation envelopes at working/raised poses; deliberately no print files."""
import hashlib
import json
import os
import sys
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(os.environ.get('TIDYBOT_PROJECT_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(ROOT/'design/system'))
import floating_heads as M


def main():
    r=json.loads((M.OUT/'floating_heads.json').read_text())
    for path,digest in r['input_hashes'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise ValueError('Stale M model: '+path)
    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetInt('CountBackupFiles',0)
    checks=dict(fabrication_release=False,scope='Allocation envelopes only; mounting hardware absent',scenes={})
    for b,v in r['modules'].items():
        for state,row in [('working',v['nominal']),('raised',v['raised_samples'][0])]:
            name='floating_heads_'+b+'_'+state;doc=App.newDocument(name);objects=[]
            md=r['config']['modules'][b];n=row['head_normal'];rot=M.rotation(n)
            matrix=App.Matrix()
            for i in range(3):
                for j in range(3):setattr(matrix,'A'+str(i+1)+str(j+1),rot[i][j])
            reference=App.Vector(*md['reference_mm'])
            for p in v['parts']:
                if p['id']=='I_cap_height_bound':continue
                shape=Part.makeBox(*p['size'],App.Vector(*p['min']))
                moving=p['id'] in md['moving_parts']
                if moving:
                    shape.translate(-reference);shape=shape.transformGeometry(matrix)
                    shape.translate(reference+App.Vector(0,0,row['q_mm']))
                if not shape.isValid() or shape.isNull():raise ValueError((name,p['id']))
                obj=doc.addObject('PartDesign::Feature',p['id']);obj.Label=p['id'].replace('_',' ')
                obj.Shape=shape if moving else Part.makeCompound(shape.Edges)
                obj.addProperty('App::PropertyString','Scope');obj.Scope='MOVING ALLOCATION; no actual roller or drive fit verified' if moving else 'FIXED ALLOCATION; not a finished part'
                if obj.ViewObject:obj.ViewObject.ShapeColor=(.85,.43,.13) if moving else (.5,.65,.67)
                objects.append(obj)
            doc.recompute();doc.saveAs(str(M.OUT/(name+'.FCStd')));Part.export(objects,str(M.OUT/(name+'.step')))
            checks['scenes'][name]=len(objects);App.closeDocument(doc.Name)
    (M.OUT/'floating_heads_cad_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('M valid allocation scenes:',checks['scenes'])


if __name__=='__main__' or any(Path(arg).resolve()==Path(__file__).resolve() for arg in sys.argv[1:]):main()
