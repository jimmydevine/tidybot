"""Generate the offline viewer, machine-readable checks and Markdown report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from study import ROOT, box, evaluate, load_inputs, packaging, write_report


def robot_scene(c,v,mode='flight'):
    b=c['body']; top=b['bottom_height_mm']+b['core_height_mm']
    objects=packaging(c)
    objects += [box('Bottom envelope (not solid material)','envelope',(0,0,b['bottom_height_mm']/2),
                    (b['length_mm'],b['width_mm'],b['bottom_height_mm']),'#65accb'),
                box('Core envelope (not solid material)','envelope',(0,0,b['bottom_height_mm']+b['core_height_mm']/2),
                    (b['length_mm'],b['width_mm'],b['core_height_mm']),'#deb96a')]
    for side in (-1,1):
        objects.append(dict(name=f'Drive wheel {side:+}',group='wheel',shape='cylinder',
                            center=[b['drive_x_mm'],side*b['drive_track_mm']/2,b['wheel_diameter_mm']/2],
                            radius=b['wheel_diameter_mm']/2,height=b['wheel_width_mm'],axis='y',color='#344559'))
    for x in b['support_x_mm']:
        objects.append(box('Support contact envelope','wheel',(x,0,8),(16,16,16),'#344559'))
    if mode=='cap':
        objects.append(box('Cap','cap',(0,0,top+b['cap_height_mm']/2),(b['length_mm'],b['width_mm'],b['cap_height_mm']),'#aac4d9'))
        return objects
    r=c['propulsion'][v['propulsion']]['prop_diameter_mm']/2
    allowance=c['screening']['guard_radial_allowance_mm']; h=c['screening']['guard_half_height_mm']
    for sx in (-1,1):
        for sy in (-1,1):
            x,y=sx*v['rotor_x_mm'],sy*v['rotor_y_mm']; z=v['rotor_plane_mm']
            objects.append(dict(name='Guard occupied envelope / barriers TBD',group='guard',shape='cylinder',center=[x,y,z],radius=r+allowance,height=2*h,axis='z',color='#df756c'))
            objects.append(dict(name='Propeller swept disk',group='prop',shape='cylinder',center=[x,y,z],radius=r,height=2,axis='z',color='#81b9c1'))
            objects.append(dict(name='Motor allowance',group='lift',shape='cylinder',center=[x,y,z-21.5],radius=20,height=43,axis='z',color='#52677a'))
            objects.append(dict(name='Arm occupied envelope',group='lift',shape='beam',start=[0,0,z-35],end=[x,y,z-35],radius=8,color='#627b8a'))
            objects.append(box('Vertical support allowance','lift',(sx*60,sy*80,(top+z-35)/2),(12,12,max(1,abs(z-35-top))),'#627b8a'))
    objects.append(box('Flight controller envelope','lift',(0,0,top+20),(60,45,22),'#829fe4'))
    return objects


def station_scene(c,v,phase):
    st=c['station']; b=c['body']; bh=b['bottom_height_mm']; top=bh+b['core_height_mm']
    w,d,h=st['width_mm'],st['depth_mm'],st['height_mm']; x=st['dock_x_mm']
    objects=[box('Station envelope','envelope',(d/2,0,h/2),(d,w,h),'#b8c4d3')]
    for y in (-w/2+15,w/2-15):
        objects.append(box('Frame post allowance','station',(d/2,y,h/2),(30,30,h),'#73869a'))
    objects.append(box('Top handling crossbeam','station',(x,0,h-35),(70,w-40,30),'#73869a'))
    for y in (-330,0,330):
        objects.append(box('Bottom tray','station',(x,y,st['bottom_tray_z_mm']-10),(b['length_mm']+40,b['width_mm']+30,20),'#546c7e'))
        if y:
            objects.append(box('Stored bottom envelope','stored',(x,y,st['bottom_tray_z_mm']+bh/2),(b['length_mm'],b['width_mm'],bh),'#799bab'))
    for y,name,color in [(-330,'Clean water tank','#77bbd4'),(0,'Waste container','#b29c86'),(330,'Dirty water tank','#a0a8b2')]:
        objects.append(box(name+' / 5L gross',( 'service'),(850,y,90),(200,150,170),color))
    dz=st['raised_core_bottom_z_mm']-bh if phase==2 else 0
    # Working volumes only; station sequence has no actuator model yet.
    for part in robot_scene(c,v,'flight' if phase==0 else 'cap'):
        q=json.loads(json.dumps(part))
        local_dz=dz
        if phase==2 and q['group'] in ('bottom','wheel'):
            local_dz=st['bottom_tray_z_mm']
        if phase==2 and q['name'].startswith('Bottom envelope'):
            local_dz=st['bottom_tray_z_mm']
        for key in ('center','start','end'):
            if key in q: q[key]=[q[key][0]+x,q[key][1],q[key][2]+local_dz]
        objects.append(q)
    if phase:
        for part in robot_scene(c,v):
            if part['group'] not in ('lift','guard','prop'): continue
            q=json.loads(json.dumps(part))
            for key in ('center','start','end'):
                if key in q: q[key]=[q[key][0]+x,q[key][1],q[key][2]+st['top_park_interface_z_mm']-top]
            objects.append(q)
    else:
        objects.append(box('Stored cap','cap',(x,st['cap_shelf_y_mm'],st['cap_shelf_z_mm']),(b['length_mm'],b['width_mm'],b['cap_height_mm']),'#aac4d9'))
    if phase==2:
        for y in (-b['width_mm']/2-15,b['width_mm']/2+15):
            objects.append(box('Core support / unselected mechanism','station',(x,y,st['raised_core_bottom_z_mm']-10),(160,25,20),'#dfba67'))
    return objects


def build(root=ROOT):
    c,site,ledger=load_inputs(root); results=evaluate(c,site,ledger)
    out=root/'design/output'; out.mkdir(parents=True,exist_ok=True)
    payload=dict(config=c,site=site,ledger=ledger,results=results,
                 robot_scenes={v['id']:robot_scene(c,v) for v in c['variants']},
                 cap_scene=robot_scene(c,c['variants'][0],'cap'),
                 station_scenes={v['id']:[station_scene(c,v,p) for p in range(3)] for v in c['variants']})
    (out/'study.json').write_text(json.dumps(payload,indent=2)+'\n')
    write_report(c,site,ledger,results,out/'report.md')
    template=(root/'design/viewer.html').read_text()
    (out/'concept.html').write_text(template.replace('/*STUDY_DATA*/',json.dumps(payload).replace('</','<\\/')))
    print('Generated design/output/concept.html, study.json and report.md')
    for r in results:
        failures=[q['name'] for q in r['checks'] if q['status'].startswith('FAIL')]
        print(f'{r["id"]}: {r["mass"]["total_g"]/1000:.2f} kg; failures: {", ".join(failures) or "none in simplified screens"}; NOT_VALIDATED')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    build(parser.parse_args().root.resolve())
