"""Q standalone mechanism viewer; schematic projections of model coordinates."""
import json
import passive_head as Q


def template():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 610" role="img" aria-label="Twin-slide head motion">
<rect width="1120" height="610" fill="#f8fafc"/><g font-family="sans-serif" fill="#17324a" font-size="15">
<text x="28" y="35" font-size="25">Q • Passive head support comparison</text>
<text x="28" y="61">Carriages stay high; pivots sit 20 mm lower to reduce tipping from floor drag.</text>
<rect x="28" y="83" width="545" height="303" fill="white" stroke="#cbd5e1"/>
<rect x="595" y="83" width="497" height="303" fill="white" stroke="#cbd5e1"/>
<text x="44" y="109" font-size="17">FRONT • independent left/right movement</text>
<text x="612" y="109" font-size="17">SIDE • head can pitch around low pivots</text>
<g id="rails" fill="#51b6b0" stroke="#236b72"></g>
<polygon id="head-front" fill="#ffddb0" stroke="#ad650c"/>
<polygon id="head-back" fill="none" stroke="#ad650c" stroke-dasharray="5 3"/>
<g id="carriages" fill="#326d92" stroke="#17324a"></g>
<g id="links" stroke="#475569" stroke-width="5"></g>
<g id="bearings" fill="#e08d26" stroke="#17324a"></g>
<polygon id="head-side" fill="#ffddb0" stroke="#ad650c"/>
<path id="floor" fill="none" stroke="#57795d" stroke-width="2"/>
<path id="side-link" fill="none" stroke="#475569" stroke-width="5"/>
<circle id="side-pivot" r="6" fill="#e08d26" stroke="#17324a"/>
<rect id="crossbar" x="801.25" y="160" width="30" height="30" fill="#cbd5e1" stroke="#475569"/>
<text x="844" y="182" font-size="12">P crossbar reference</text>
<text x="44" y="365" font-size="13">Head end-frame pockets need redesign around the guides.</text>
<text x="612" y="365" font-size="13">Floor line represents a sampled plane, not a step crossing.</text>
<text id="pose-label" x="30" y="419" font-size="18"></text>
<text id="motion-label" x="30" y="450"></text>
<text x="30" y="484">75 g with counterbalance springs / 72 g with gravity loading: both include unfinished hardware.</text>
<text x="30" y="515">Potential saving is only 22–25 g. Friction and dock-only release prevent adoption at this stage.</text>
<text x="30" y="546">Retain the lift allowance; integrate guides, stops and air flex into the existing head frame.</text>
<text x="30" y="579" font-size="17">Transfer mass remains 5.275 kg, excluding lift — 775 g above the required maximum.</text>
</g></svg>'''


SCRIPT='''
const poses=data.poses.concat([data.raised]),select=document.getElementById('pose');
for(let i=0;i<poses.length;i++){const p=poses[i],o=document.createElement('option');o.value=i;o.textContent=p.state+(p.step_mm!==undefined?' • '+p.step_mm+' mm • caster '+p.heading_deg+'°':'');select.appendChild(o);}
const attr=(id,key,value)=>document.getElementById(id).setAttribute(key,value);
function move(v,p){return p.R.map((row,i)=>row.reduce((sum,a,j)=>sum+a*v[j],p.T[i]));}
function front(v){return [40+1.9*v[0],325-2.5*v[2]];}
function side(v){return [620+2.5*v[1],325-2.5*v[2]];}
function polygon(points,p,projection){return points.map(v=>projection(move(v,p)).join(',')).join(' ');}
function rect(x,y,w,h){return `<rect x="${x}" y="${y}" width="${w}" height="${h}"/>`;}
function render(){const p=poses[Number(select.value)||0],d=data.config;
 const left=d.rail_left_min_mm[0],width=d.rail_envelope_mm[0];
 document.getElementById('rails').innerHTML=[left,275-left-width].map(x=>rect(40+1.9*x,325-2.5*(d.rail_left_min_mm[2]+d.rail_envelope_mm[2]),1.9*width,2.5*d.rail_envelope_mm[2])).join('');
 const beam=data.crossmember;attr('crossbar','x',620+2.5*beam.min[1]);attr('crossbar','y',325-2.5*(beam.min[2]+beam.size[2]));attr('crossbar','width',2.5*beam.size[1]);attr('crossbar','height',2.5*beam.size[2]);
 const head=[[22.5,6,0],[252.5,6,0],[252.5,6,48],[22.5,6,48]],back=head.map(v=>[v[0],66,v[2]]);
 attr('head-front','points',polygon(head,p,front));attr('head-back','points',polygon(back,p,front));
 attr('head-side','points',polygon([[137.5,6,0],[137.5,66,0],[137.5,66,48],[137.5,6,48]],p,side));
 const pins=[move(d.pivot_left_mm,p),move([d.pivot_right_x_mm,d.pivot_left_mm[1],d.pivot_left_mm[2]],p)];
 document.getElementById('carriages').innerHTML=[left,275-left-width].map((x,i)=>rect(40+1.9*x,325-2.5*(p.carriage_z_mm[i]+10),1.9*width,50)).join('');
 document.getElementById('links').innerHTML=pins.map((v,i)=>{const a=front(v),x=40+1.9*(i?275-left-width:left+width);return `<path d="M${x},${325-2.5*p.carriage_z_mm[i]} L${x},${a[1]} L${a[0]},${a[1]}" fill="none"/>`;}).join('');
 document.getElementById('bearings').innerHTML=pins.map(v=>{const a=front(v);return `<circle cx="${a[0]}" cy="${a[1]}" r="5"/>`;}).join('');
 const centre=move([137.5,d.pivot_left_mm[1],d.pivot_left_mm[2]],p),q=side(centre);
 attr('side-link','d',`M${q[0]},${q[1]-2.5*d.carriage_above_pivot_mm} L${q[0]},${q[1]}`);attr('side-pivot','cx',q[0]);attr('side-pivot','cy',q[1]);
 const floorAt=y=>(p.plane_constant+p.ground_height_mm-p.normal[0]*137.5-p.normal[1]*y)/p.normal[2];
 const a=side([137.5,0,floorAt(0)]),b=side([137.5,100,floorAt(100)]);attr('floor','d',`M${a.join(',')} L${b.join(',')}`);
 document.getElementById('pose-label').textContent=p.state+' • pitch '+p.pitch_deg.toFixed(2)+'° • roll '+p.roll_deg.toFixed(2)+'°';
 document.getElementById('motion-label').textContent='Carriages: '+p.carriage_z_mm.map(v=>v.toFixed(2)).join(' / ')+' mm    |    right-pivot axial movement: '+p.right_float_used_mm.toFixed(3)+' mm';
}
select.addEventListener('change',render);document.getElementById('level').addEventListener('click',()=>{select.value=0;render()});document.getElementById('capture').addEventListener('click',()=>{select.value=poses.length-1;render()});render();
'''


def main():
    r=Q.study();data={k:r[k] for k in ('config','poses','raised')};data['crossmember']=Q.P.read()['crossmember']
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TidyBot passive head comparison</title>
<style>body{font:16px system-ui,sans-serif;color:#17324a;max-width:1120px;margin:20px auto;padding:0 14px;background:#f8fafc}svg{width:100%;height:auto}select,button{padding:8px;margin:4px}a{color:#086386}</style>
<label>Sampled position <select id="pose"></select></label><button id="level">Level</button><button id="capture">Dock captured</button>'''+template()+'''
<p>Catalog envelopes and projected head allocations. Springs, precise bearings/pins, frame pockets, capture hooks and service routing are incomplete.</p>
<p><a href="../../../docs/PASSIVE_HEAD.md">Design decision</a> · <a href="passive_head.md">Calculations</a> · <a href="passive_head_cad_checks.json">CAD scope/results</a> · <a href="passive_head_level.FCStd">Level FreeCAD</a> · <a href="passive_head_captured.step">Captured STEP</a></p><script>const data='''+json.dumps(data)+''';\n'''+SCRIPT+'</script></html>'
    (Q.OUT/'passive_head.html').write_text(page)


if __name__=='__main__':main()
