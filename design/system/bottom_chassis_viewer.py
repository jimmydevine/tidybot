"""Offline inspection of the rejected T frame arrangement and its mass scope."""
import json
import bottom_chassis as T


def main():
    r=T.study();cad=json.loads((T.OUT/'bottom_chassis_cad_checks.json').read_text())
    if r['source_fingerprint']!=cad['source_fingerprint']:raise RuntimeError('Regenerate T CAD')
    edges=json.loads((T.OUT/'bottom_chassis_view_data.json').read_text())
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TidyBot — bottom chassis comparison</title><style>
body{font:16px system-ui,sans-serif;color:#1d3548;background:#f3f6f8;padding:24px;margin:0}main{max-width:1150px;margin:auto}
h1{font-size:28px}section{background:white;border:1px solid #d5dfe5;border-radius:8px;padding:18px;margin:18px 0}
.controls{display:flex;gap:20px;flex-wrap:wrap}label{display:inline-flex;align-items:center;gap:8px}p{line-height:1.5}
.decision{background:#fff1e9;border-left:5px solid #b14b25;padding:14px}table{width:100%;border-collapse:collapse}td,th{text-align:left;border-bottom:1px solid #dde5ea;padding:8px}
svg{width:100%;max-height:590px}a{color:#176895}.note{color:#556a79}
</style><main><h1>Integrated bottom chassis comparison</h1>
<p class="decision"><strong>Rejected for development.</strong> Keeping the separate N wheel supports makes this frame heavier. The power support and front seats also obstruct head movement or withdrawal.</p>
<section><div class="controls"><label>Module <select id="bottom"><option value="vacuum">Vacuum</option><option value="mop">Mop</option></select></label>
<label>View <input id="yaw" type="range" min="-75" max="75" value="28"></label>
<label><input id="equipment" type="checkbox" checked> Equipment outlines</label><label><input id="conflicts" type="checkbox" checked> Highlight obstructions</label></div>
<svg id="drawing" viewBox="0 0 1000 600" aria-label="Chassis geometry with obstructing parts highlighted"></svg>
<p class="note">Blue: proposed frame · orange: retained N drive supports · gray: equipment and interfaces · red: a proposed part involved in a detected obstruction. Bolts and several mount details remain allowances.</p></section>
<section><p id="summary"></p><table><thead><tr><th>Local scope</th><th>Mass</th></tr></thead><tbody id="rows"></tbody></table>
<p id="loaded"></p><p>No R/S weight reductions are stacked. The lift top is excluded; battery and maximum modeled contents are included. Geometry compatibility with S is checked separately.</p>
<a href="bottom_chassis.md">Full accounting and load screens</a> · <a href="../../../docs/BOTTOM_CHASSIS.md">Decision and next comparison</a> · <a id="cadlink" href="bottom_chassis_vacuum.FCStd">Review CAD</a></section></main><script>
const results=__RESULTS__, edges=__EDGES__, checks=__CHECKS__;
const $=id=>document.getElementById(id);
function project(p){const y=+$('yaw').value*Math.PI/180,t=28*Math.PI/180,x=p[0]-137.5,b=p[1]-137.5,z=p[2]-65;return [500+2.2*(Math.cos(y)*x-Math.sin(y)*b),310+2.2*(-Math.sin(t)*(Math.sin(y)*x+Math.cos(y)*b)-Math.cos(t)*z)];}
function draw(){const bottom=$('bottom').value,r=results.find(r=>r.bottom===bottom),failed=new Set();
for(const key of ['equipment_intersections','head_intersections','withdrawal_intersections','core_upward_intersections'])for(const c of checks[key])if(c.bottom===bottom){failed.add(c.a);failed.add(c.b);}
const paths=[];for(const p of edges[bottom]){const drive=p.id.startsWith('N_');if(p.group==='context'&&!drive&&!$('equipment').checked)continue;
const color=p.group==='material'?($('conflicts').checked&&failed.has(p.id)?'#bd3f2d':'#176b9b'):drive?'#bb741c':'#9aabb7';
for(const e of p.edges){const pts=e.map(v=>project(v).map(n=>n.toFixed(2)).join(',')).join(' ');paths.push(`<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="${p.group==='material'?1.7:1}" opacity="${p.group==='material'?.95:.6}"/>`);}}
$('drawing').innerHTML=paths.join('');$('summary').textContent=`${(-r.conditional_saving_g).toFixed(1)} g heavier than the previous complete local scope.`;
const n=r.rows.filter(x=>x.id.startsWith('N_')).reduce((s,x)=>s+x.mass_g,0),caster=r.rows.filter(x=>x.id.startsWith('caster_')&&x.id!=='caster_saddle').reduce((s,x)=>s+x.mass_g,0);
$('rows').innerHTML=[['Previous scope',r.prior_scope_g],['Proposed frame/shelves/caster saddle material',r.material_g],['Unchanged complete N drive supports',n],['Caster, stem and retention allowance',caster],['New frame/mount completion allowances',r.candidate_scope_g-r.material_g-n-caster],['T total',r.candidate_scope_g]].map(([k,v])=>`<tr><td>${k}</td><td>${v.toFixed(1)} g</td></tr>`).join('');
$('loaded').textContent=`T alone would put loaded ${bottom} transfer mass at ${(r.candidate_transfer_g/1000).toFixed(3)} kg, ${r.candidate_over_budget_g.toFixed(0)} g above 4.5 kg. This proposal is not adopted.`;
$('cadlink').setAttribute('href',`bottom_chassis_${bottom}.FCStd`);}
for(const id of ['bottom','yaw','equipment','conflicts'])$(id).addEventListener('input',draw);draw();
</script></html>'''
    html=html.replace('__RESULTS__',json.dumps(r['cases'])).replace('__EDGES__',json.dumps(edges)).replace('__CHECKS__',json.dumps(cad))
    (T.OUT/'bottom_chassis.html').write_text(html)


if __name__=='__main__':main()
