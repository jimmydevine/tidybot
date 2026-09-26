"""Offline orthographic review of S CAD edges and cartridge extraction."""
import json
import core_support as S


def main():
    r=S.study();edges=json.loads((S.OUT/'core_support_view_data.json').read_text())
    checks=json.loads((S.OUT/'core_support_cad_checks.json').read_text())
    if checks['source_fingerprint']!=S.P.source_fingerprint():raise RuntimeError('Regenerate S CAD first')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TidyBot — core supports</title><style>
body{font:16px system-ui,sans-serif;color:#163046;background:#f3f6f8;margin:0;padding:24px}main{max-width:1180px;margin:auto}
h1{font-size:28px;margin:0 0 8px}p{line-height:1.5}section{background:white;border:1px solid #d8e0e6;border-radius:8px;padding:18px;margin-top:18px}
.controls{display:flex;gap:24px;flex-wrap:wrap;align-items:center}label{display:inline-flex;gap:8px;align-items:center}input[type=range]{width:180px}
svg{width:100%;height:auto;max-height:620px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:8px;border-bottom:1px solid #e1e6eb}
.summary{font-size:20px;font-weight:600}.note{color:#536677}a{color:#156294}button{padding:7px 13px}
</style><main><h1>Shared core supports and battery receiver</h1>
<p>The same cartridge remains. Two equipment bridges connect the receiver and lightweight trays to the retained metal frame.</p>
<section><div class="controls"><label>View <input id="yaw" type="range" min="-70" max="70" value="28"></label>
<label><input id="equipment" type="checkbox" checked> Equipment outlines</label>
<label><input id="unlocked" type="checkbox"> Release battery tongues</label>
<label>Cartridge down <input id="travel" type="range" min="0" max="100" value="0" disabled><output id="travelValue">0 mm</output></label><button id="reset">Reset</button></div>
<svg id="drawing" viewBox="0 0 1000 600" aria-label="Interactive core structure and downward cartridge path"></svg>
<p id="state"></p><p class="note">Blue: metal supports · orange: printed trays/liners · gray: retained frame/equipment · green: cartridge allocation. Bottom and top modules are removed for this exchange view.</p>
</section><section><p class="summary" id="mass"></p><table><tr><th>Complete local scope</th><th>Mass</th></tr><tbody id="rows"></tbody></table>
<p>Battery cells, complete cartridge hardware, protection, sensors and all eight module locks stay in the ledger. No saving is booked.</p>
<p class="note">This is a review of geometry and estimates. Several mounts, latch pawls, contact supports and wire paths are unfinished. The 0.2 mm nominal guide gap is not a qualified production fit. The display is not robot control software.</p>
<a href="core_support.md">Calculation and scope</a> · <a href="../../../docs/CORE_SUPPORT.md">Design decisions</a> · <a href="core_support_installed.FCStd">FreeCAD assembly</a>
</section></main><script>
const parts=__EDGES__, result=__RESULT__;
const $=id=>document.getElementById(id),svg=$('drawing');
function project(p){const yaw=+$('yaw').value*Math.PI/180,pitch=25*Math.PI/180,x=p[0]-137.5,y=p[1]-137.5,z=p[2]-91;
return [500+2*(Math.cos(yaw)*x-Math.sin(yaw)*y),270+2*(-Math.sin(pitch)*(Math.sin(yaw)*x+Math.cos(yaw)*y)-Math.cos(pitch)*z)];}
function draw(){let travel=$('unlocked').checked?+$('travel').value:0;$('travel').disabled=!$('unlocked').checked;if(!travel)$('travel').value=0;
let paths=[];for(const part of parts){if(part.role==='context'&&part.material==='equipment'&&!$('equipment').checked)continue;
const dx=part.role==='latch'&&$('unlocked').checked?(part.id.startsWith('left')?-3:3):0,dz=part.role==='cartridge'?-travel:0;
const color=part.role==='cartridge'?'#07846b':part.role==='context'?'#9ba9b5':part.material==='polymer'?'#c77722':'#226fa1';
for(const edge of part.edges){const pts=edge.map(p=>project([p[0]+dx,p[1],p[2]+dz]).map(v=>v.toFixed(2)).join(',')).join(' ');
paths.push(`<polyline fill="none" points="${pts}" stroke="${color}" stroke-width="${part.role==='context'?1:1.7}" opacity="${part.role==='context'?.55:.9}"/>`);}}
svg.innerHTML=paths.join('');$('travelValue').textContent=travel+' mm';
$('state').textContent=$('unlocked').checked?`Both tongues released 3 mm; cartridge ${travel} mm below its installed position.`:'Cartridge installed; both modeled tongues engaged. A station must support the cartridge before release.';}
for(const id of ['yaw','equipment','unlocked','travel'])$(id).addEventListener('input',draw);
$('reset').onclick=()=>{$('yaw').value=28;$('equipment').checked=true;$('unlocked').checked=false;$('travel').value=0;draw();};
const m=result.mass;$('mass').textContent=`${m.conditional_saving_g.toFixed(1)} g potential saving from the ${m.before_g.toFixed(0)} g tray/receiver scope`;
$('rows').innerHTML=[['Prior allowance',m.before_g],['Modeled material',m.material_g],['Hardware and completion allowance',m.unfinished_g],['Candidate total',m.candidate_g]].map(([label,value])=>`<tr><td>${label}</td><td>${value.toFixed(2)} g</td></tr>`).join('');draw();
</script></html>'''
    html=html.replace('__EDGES__',json.dumps(edges)).replace('__RESULT__',json.dumps(dict(mass=r['mass'])))
    (S.OUT/'core_support.html').write_text(html)


if __name__=='__main__':main()
