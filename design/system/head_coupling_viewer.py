"""Offline, dimension-driven coupling illustration; the CAD export checks solids."""
import html
import head_coupling as P


def drawing(r, withdrawal=0):
    d=r['config'];a=d['air'];e=d['electrical'];c=d['cheeks'];l=d['locks']
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 760" role="img" aria-label="Removable head interface and lock section">',
       '<rect width="1140" height="760" fill="#f8fafc"/>',
       '<g font-family="sans-serif" font-size="15" fill="#172b40">']
    def text(x,y,t,size=15):s.append(f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(t)}</text>')
    def rect(x,y,w,h,fill,stroke='#334155',extra=''):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" {extra}/>')
    def line(x,y,x2,y2,color='#475569',extra=''):
        s.append(f'<path d="M{x},{y} L{x2},{y2}" fill="none" stroke="{color}" {extra}/>')
    text(28,34,'P • Removable head coupling',25)
    text(28,59,'Candidate geometry • supports, suspension, flex and latch housings remain unfinished')
    rect(28,80,566,587,'white','#cbd5e1');rect(614,80,498,340,'white','#cbd5e1')
    rect(614,435,498,232,'white','#cbd5e1')
    text(45,105,'TOP VIEW • body front and removable head',16)
    text(45,128,'Orange moves with tool; teal stays with robot. Supports omitted.',13)
    # Orthographic plan: increasing Y is down the page; body front is Y=0.
    scale=1.8;ox=63;oy=418
    def plan(p,size,fill,extra=''):
        rect(ox+scale*p[0],oy+scale*p[1],scale*size[0],scale*size[1],fill,extra=extra)
    plan([0,0],[275,122],'#e8edf3','stroke-dasharray="5 4"')
    text(68,652,'Body continues rearward; electronics above are hidden.',13)
    line(ox,oy,ox+275*scale,oy,'#1e293b','stroke-width="2"')
    text(45,407,'Y=0 • front of body',13)
    for p in d['plates']['mins']:plan(p,d['plates']['size'],'#0f9f9c')
    plan([109.5,a['body_flange_y']],[56,3],'#0f9f9c')
    plan(e['board_min'],e['board_size'],'#0f9f9c')
    for x in e['pin_x']:plan([x-1.2,r['electrical']['target_pad_face_y_mm']],[2.4,e['body_board_front_y']-r['electrical']['target_pad_face_y_mm']],'#0f9f9c')
    # The group is a diagram of the withdrawn tool; it is not a dock mechanism.
    s.append(f'<g id="moving-tool" transform="translate(0,{-scale*withdrawal})">')
    plan([22.5,6],[230,60],'#ffedd5')
    text(ox+46*scale,oy+41*scale,'Powered cleaning head',16)
    for x in [c['left_min'][0],275-c['left_min'][0]-c['size'][0]]:
        plan([x,c['left_min'][1]],c['size'],'#ed9d32')
    plan(d['crossmember']['min'],d['crossmember']['size'],'#ed9d32')
    plan([118.5,66],[38,25],'none','stroke-dasharray="4 3"')
    plan([109.5,a['tool_flange_y']],[56,3],'#ed9d32')
    plan([e['board_min'][0],r['electrical']['target_pad_face_y_mm']-e['target_board_t']],[32,e['target_board_t']],'#ed9d32')
    s.append('</g>')
    for x in [24.5,249]:
        for y in d['guide_pins']['y']:plan([x-3,y-2],[5,4],'#0f9f9c')
    line(48,360,48,206,'#a65b00','stroke-width="2"');line(48,206,43,216);line(48,206,53,216)
    text(70,181,'Forward withdrawal: 0–120 mm',16)
    text(70,203,'At 120 mm, mating face clears front by 21.8 mm.',13)
    # Enlarged horizontal slice through left key at Z70, looking down.
    text(632,106,'LEFT LOCK • section at Z70',16)
    text(632,129,'Screw head bridges two steel bores; shank only actuates.',13)
    k=25;bx=649;by=180
    def keyrect(x,y,w,h,fill,extra=''):
        rect(bx+(x-18)*k,by+(y-72)*16,w*k,h*16,fill,extra=extra)
    # Keep bore walls visible above and below the head.
    keyrect(22.7,72,1.5,8,'#fed7aa');keyrect(24.5,72,1.5,8,'#5ec6c2')
    keyrect(26,72,2,8,'#dce4ed')
    keyrect(22.7,73.9,1.5,4.2,'white');keyrect(24.5,73.95,3.5,4.1,'white')
    s.append('<defs><clipPath id="key-section"><rect x="632" y="150" width="280" height="180"/></clipPath></defs><g clip-path="url(#key-section)"><g id="moving-key">')
    keyrect(18,75,5.2,2,'#64748b') # shank continues beyond drawing
    keyrect(l['left_pin_min_x'],74.1,l['pin_length'],l['pin_diameter'],'#475569')
    s.append('</g></g>')
    text(930,185,'orange: tool cheek',13);text(930,206,'teal: receiver',13)
    text(930,227,'gray: chassis rail',13)
    line(884,276,839,276,'#475569','stroke-width="2"');line(839,276,848,271);line(839,276,848,281)
    text(923,280,'3 mm outward',13)
    text(632,350,'Nominal engagement: cheek 1.0 mm / receiver 0.7 mm.',14)
    text(632,374,'Only 0.5 mm minimum with ±0.2 mm axial variation.',14)
    text(632,398,'Actual screw chamfer, guides and wear must be checked.',14)
    text(632,462,'SUPPORTED DOCK EXCHANGE',16)
    for i,t in enumerate([
        '1  Capture robot, carrier and floating head.',
        '2  Stop drives; isolate tool and logic power.',
        '3  Retract both keys; withdraw 120 mm.',
        '4  Park head; present this floor’s extension.',
        '5  Seat and lock; check ID on limited logic power.',
        '6  Enable tool power only after validation.'
    ]):text(634,491+26*i,t,14)
    text(30,697,'Mass remains 5.275 kg at maximum debris, excluding lift: 775 g above the transfer limit.',17)
    text(30,723,'Carrier scope ≈68 g against 70 g allocation. Only 35 g remains for unfinished head compliance.',15)
    text(30,748,'735 mm dock handling depth before margins; sofa approach space does not confirm dock space.',15)
    s.extend(['</g>','</svg>']);return '\n'.join(s)


def main():
    r=P.study();svg=drawing(r);P.OUT.mkdir(parents=True,exist_ok=True)
    (P.OUT/'head_coupling.svg').write_text(svg+'\n')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TidyBot removable head coupling</title><style>
body{font:16px system-ui,sans-serif;color:#172b40;background:#f8fafc;max-width:1140px;margin:20px auto;padding:0 16px}svg{width:100%;height:auto}
.controls{display:flex;gap:16px;align-items:center;flex-wrap:wrap;padding:12px;background:white;border:1px solid #cbd5e1}
input[type=range]{width:260px}a{color:#075f89}output{min-width:250px}button{padding:6px 12px}
</style><div class="controls"><label>Withdrawal <input id="travel" type="range" min="0" max="120" value="0" step="1"></label>
<output id="travel-label">0 mm • engaged</output><button id="reset">Reinstall head</button></div>
<p>This moves the supported tool along its withdrawal axis. Keys retract before movement; the station shuttle, latch springs and floating-head linkage are still to be designed.</p>'''+svg+'''
<p><a href="../../../docs/HEAD_COUPLING.md">Design record</a> · <a href="head_coupling.md">Calculations</a> · <a href="head_coupling_cad_checks.json">CAD check scope/results</a> · <a href="head_coupling_0.step">Engaged STEP</a> · <a href="head_coupling_120.step">Withdrawn STEP</a></p>
<script>
const slider=document.getElementById('travel');
function render(){const d=Number(slider.value);document.getElementById('moving-tool').setAttribute('transform',`translate(0,${-1.8*d})`);
document.getElementById('moving-key').setAttribute('transform',`translate(${d>0?-75:0},0)`);
document.getElementById('travel-label').textContent=d+' mm • '+(d===0?'engaged':d===120?'clear for supported transfer':'keys retracted; moving forward');}
slider.addEventListener('input',render);document.getElementById('reset').addEventListener('click',()=>{slider.value=0;render();});render();
</script></html>'''
    (P.OUT/'head_coupling.html').write_text(page)


if __name__=='__main__':main()
