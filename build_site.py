#!/usr/bin/env python3
"""Stage 3: build self-contained index.html from the verified CSV database
(josaa_iit_2025_r6.csv). Course groups come from groups.py so the site and the
coverage checker can never drift."""
import json, csv, os
from groups import CHIPS

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "josaa_iit_2025_r6.csv")
OUT = os.path.join(HERE, "index.html")

records, institutes, cores = [], set(), set()
with open(CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        records.append({
            "inst": r["institute_short"],
            "prog": r["program"],
            "deg": r["degree_type"],
            "dur": int(r["duration_years"]),
            "dual": r["is_dual"] == "yes",
            "gender": "Female" if r["gender"] == "Female-only" else "Neutral",
            "open": int(r["opening_rank"]),
            "close": int(r["closing_rank"]),
        })
        institutes.add(r["institute_short"])
        cores.add(r["program_core"])

institutes = sorted(institutes)
cores = sorted(cores)
degree_types = sorted({r["deg"] for r in records})

data_json = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
inst_json = json.dumps(institutes, ensure_ascii=False)
cores_json = json.dumps(cores, ensure_ascii=False)
chips_json = json.dumps(CHIPS, ensure_ascii=False)
deg_json = json.dumps(degree_types, ensure_ascii=False)

template = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JoSAA 2025 Round 6 — IIT Cutoffs (OPEN)</title>
<style>
:root{
  --bg:#0f1419;--panel:#1a2029;--panel2:#222b36;--line:#2d3744;
  --txt:#e6edf3;--muted:#8b98a5;--accent:#4493f8;
  --ok:#1f6f43;--okbg:#11271b;--warn:#7a5d12;--warnbg:#2a2210;--no:#5a2330;--nobg:#241016;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
header{padding:18px 22px;background:linear-gradient(135deg,#162130,#0f1419);border-bottom:1px solid var(--line)}
h1{margin:0 0 4px;font-size:20px}
.sub{color:var(--muted);font-size:13px}
.wrap{padding:16px 22px 60px}
.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;background:var(--panel);
  border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:12px}
.field{display:flex;flex-direction:column;gap:4px}
.field label{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
input,select{background:var(--panel2);border:1px solid var(--line);color:var(--txt);
  padding:8px 10px;border-radius:8px;font-size:14px;outline:none}
input:focus,select:focus{border-color:var(--accent)}
#course{min-width:240px}#college{min-width:190px}#degree{min-width:180px}
.chk{flex-direction:row;align-items:center;gap:6px}.chk input{width:16px;height:16px}
button.reset{background:var(--panel2);border:1px solid var(--line);color:var(--txt);padding:8px 12px;border-radius:8px;cursor:pointer}
button.reset:hover{border-color:var(--accent)}
.seclabel{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:4px 0 6px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.chip{background:var(--panel2);border:1px solid var(--line);color:var(--muted);padding:5px 11px;
  border-radius:999px;cursor:pointer;font-size:12.5px;user-select:none}
.chip:hover{border-color:var(--accent);color:var(--txt)}
.chip.active{background:var(--accent);border-color:var(--accent);color:#fff}
.chip .n{opacity:.7;font-size:11px;margin-left:4px}
.stats{display:flex;gap:14px;flex-wrap:wrap;margin:12px 0;font-size:13px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px 14px}
.stat b{font-size:17px;display:block}
.stat.ok b{color:#56d364}.stat.no b{color:#f85149}.stat.tot b{color:var(--accent)}
.activek{font-size:12px;color:var(--muted);margin-bottom:8px}
.activek b{color:var(--txt)}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line);font-size:13.5px}
th{background:var(--panel2);cursor:pointer;user-select:none;white-space:nowrap}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
th:hover{color:var(--accent)}
tr.ok{background:var(--okbg)}tr.warn{background:var(--warnbg)}tr.no{background:var(--nobg);color:var(--muted)}
tr:hover td{background:rgba(68,147,248,.08)}
.badge{display:inline-block;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;white-space:nowrap}
.badge.ok{background:var(--ok);color:#d3f9d8}.badge.warn{background:var(--warn);color:#fff3bf}.badge.no{background:var(--no);color:#ffc9c9}
.prog{font-weight:500}
.degtag{display:inline-block;margin-left:6px;font-size:10.5px;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:0 5px;vertical-align:middle}
mark{background:#3b5bdb;color:#fff;border-radius:2px;padding:0 1px}
.empty{padding:30px;text-align:center;color:var(--muted)}
.foot{margin-top:18px;color:var(--muted);font-size:12px;line-height:1.7}
</style>
</head>
<body>
<header>
  <h1>JoSAA 2025 · Round 6 — IIT Closing Ranks</h1>
  <div class="sub">Quota: All-India (AI) · Seat type: OPEN · Source: verified <code>josaa_iit_2025_r6.csv</code>. Pick multiple course groups and/or type keywords — matching is fuzzy (substring), so variants group together.</div>
</header>
<div class="wrap">
  <div class="controls">
    <div class="field">
      <label for="course">Course keywords (comma-separated, fuzzy)</label>
      <input id="course" list="corelist" placeholder="e.g. artificial, vlsi, electrical" autocomplete="off">
      <datalist id="corelist"></datalist>
    </div>
    <div class="field">
      <label for="college">College</label>
      <select id="college"></select>
    </div>
    <div class="field">
      <label for="degree">Degree / duration</label>
      <select id="degree">
        <option value="">All degrees</option>
        <option value="dur4">4-Year programs</option>
        <option value="dur5">5-Year programs</option>
        <option value="dual">Dual degree (any)</option>
        <option value="single">Single degree only</option>
      </select>
    </div>
    <div class="field">
      <label for="gender">Seat (gender pool)</label>
      <select id="gender">
        <option value="Neutral">Gender-Neutral</option>
        <option value="Female">Female-only</option>
        <option value="">Both</option>
      </select>
    </div>
    <div class="field">
      <label for="rank">Your rank</label>
      <input id="rank" type="number" value="2229" style="width:100px">
    </div>
    <div class="field chk">
      <input id="onlyok" type="checkbox">
      <label for="onlyok" style="text-transform:none;font-size:13px;letter-spacing:0">Attainable only</label>
    </div>
    <button class="reset" id="reset">Reset all</button>
  </div>

  <div class="seclabel">Course groups — click to multi-select (combines as OR)</div>
  <div class="chips" id="chips"></div>
  <div class="activek" id="activek"></div>

  <div class="stats">
    <div class="stat tot"><b id="s-total">0</b>showing</div>
    <div class="stat ok"><b id="s-ok">0</b>✅ attainable</div>
    <div class="stat no"><b id="s-no">0</b>❌ out of reach</div>
  </div>

  <table>
    <thead><tr>
      <th class="num" data-k="_pos">#</th>
      <th data-k="_status">Status</th>
      <th class="num" data-k="close">Closing ▲</th>
      <th class="num" data-k="open">Opening</th>
      <th data-k="inst">Institute</th>
      <th data-k="prog">Program</th>
    </tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  <div class="empty" id="empty" style="display:none">No programs match these filters.</div>

  <div class="foot">
    ✅ attainable = closing rank ≥ your rank · ⚠️ borderline = within 150 above your rank · ❌ out of reach.<br>
    Course groups cover all 131 programs (verified). Selecting several groups / typing several comma-separated terms shows the union. Degree filter: "Dual degree" = 5-yr B.Tech-M.Tech, BS-MS and B.Tech+MBA integrated programs.
  </div>
</div>

<script>
const DATA=__DATA__, INSTITUTES=__INSTITUTES__, CORES=__CORES__, CHIPS=__CHIPS__;
const $=s=>document.querySelector(s);
const tbody=$("#tbody");
const activeChips=new Set();
let sortKey="close", sortDir=1;

function progCount(kws){return DATA.filter(r=>kws.some(k=>r.prog.toLowerCase().includes(k))).length;}

// college dropdown + course autocomplete
$("#college").innerHTML='<option value="">All IITs ('+INSTITUTES.length+')</option>'+
  INSTITUTES.map(i=>`<option value="${i}">${i}</option>`).join("");
$("#corelist").innerHTML=CORES.map(c=>`<option value="${c}">`).join("");

// chips (multi-select)
const chipBox=$("#chips");
CHIPS.forEach(([label,kws],i)=>{
  const el=document.createElement("span");
  el.className="chip";
  el.innerHTML=`${label}<span class="n">${progCount(kws)}</span>`;
  el.onclick=()=>{activeChips.has(i)?activeChips.delete(i):activeChips.add(i);
    el.classList.toggle("active");render();};
  el.dataset.i=i; chipBox.appendChild(el);
});

function activeKeywords(){
  const kws=[];
  activeChips.forEach(i=>CHIPS[i][1].forEach(k=>kws.push(k)));
  $("#course").value.split(",").map(s=>s.trim().toLowerCase()).filter(Boolean).forEach(k=>kws.push(k));
  return kws;
}
function statusOf(c,r){return c>=r?(c-r<=150?"warn":"ok"):"no";}
function esc(s){return s.replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));}
function hl(t,kws){
  if(!kws.length) return esc(t);
  const low=t.toLowerCase(); let best=-1,bl=0;
  kws.forEach(k=>{const i=low.indexOf(k); if(i>=0&&(best<0||i<best)){best=i;bl=k.length;}});
  if(best<0) return esc(t);
  return esc(t.slice(0,best))+"<mark>"+esc(t.slice(best,best+bl))+"</mark>"+esc(t.slice(best+bl));
}

function render(){
  const college=$("#college").value, gender=$("#gender").value,
        rank=parseInt($("#rank").value)||0, onlyok=$("#onlyok").checked, degf=$("#degree").value;
  const kws=activeKeywords();

  $("#activek").innerHTML = kws.length
    ? "Active course keywords: "+kws.map(k=>`<b>${esc(k)}</b>`).join(", ")
    : "No course filter — showing all programs.";

  let rows=DATA.filter(r=>{
    if(gender&&r.gender!==gender) return false;
    if(college&&r.inst!==college) return false;
    if(degf==="dur4"&&r.dur!==4) return false;
    if(degf==="dur5"&&r.dur!==5) return false;
    if(degf==="dual"&&!r.dual) return false;
    if(degf==="single"&&r.dual) return false;
    if(kws.length && !kws.some(k=>r.prog.toLowerCase().includes(k))) return false;
    if(onlyok && r.close<rank) return false;
    return true;
  });

  rows.sort((a,b)=>{
    let av=a[sortKey],bv=b[sortKey];
    if(sortKey==="_status"){const o={ok:0,warn:1,no:2};av=o[statusOf(a.close,rank)];bv=o[statusOf(b.close,rank)];}
    return (typeof av==="string")?av.localeCompare(bv)*sortDir:(av-bv)*sortDir;
  });

  let okN=0,noN=0,out=[];
  rows.forEach((r,idx)=>{
    const st=statusOf(r.close,rank); st==="no"?noN++:okN++;
    const badge=st==="ok"?'<span class="badge ok">✅ Yes</span>'
      :st==="warn"?'<span class="badge warn">⚠️ Border</span>'
      :'<span class="badge no">❌ No</span>';
    out.push(`<tr class="${st}"><td class="num">${idx+1}</td><td>${badge}</td>`+
      `<td class="num">${r.close}</td><td class="num">${r.open}</td><td>${esc(r.inst)}</td>`+
      `<td><span class="prog">${hl(r.prog,kws)}</span><span class="degtag">${esc(r.deg)}</span></td></tr>`);
  });
  tbody.innerHTML=out.join("");
  $("#empty").style.display=rows.length?"none":"block";
  $("#s-total").textContent=rows.length; $("#s-ok").textContent=okN; $("#s-no").textContent=noN;
}

document.querySelectorAll("th").forEach(th=>{
  th.onclick=()=>{const k=th.dataset.k==="_pos"?"close":th.dataset.k;
    if(sortKey===k)sortDir*=-1; else{sortKey=k;sortDir=1;}
    document.querySelectorAll("th").forEach(t=>t.textContent=t.textContent.replace(/[ ▲▼]+$/,""));
    th.textContent+=sortDir>0?" ▲":" ▼"; render();};
});
["course","college","degree","gender","rank","onlyok"].forEach(id=>{
  $("#"+id).addEventListener("input",render); $("#"+id).addEventListener("change",render);});
$("#reset").onclick=()=>{$("#course").value="";$("#college").value="";$("#degree").value="";
  $("#gender").value="Neutral";$("#rank").value="2229";$("#onlyok").checked=false;
  activeChips.clear();document.querySelectorAll(".chip").forEach(c=>c.classList.remove("active"));render();};
render();
</script>
</body>
</html>
"""
out = (template.replace("__DATA__", data_json)
               .replace("__INSTITUTES__", inst_json)
               .replace("__CORES__", cores_json)
               .replace("__CHIPS__", chips_json))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print(f"Wrote {OUT}")
print(f"records:{len(records)} institutes:{len(institutes)} course-suggestions:{len(cores)} "
      f"chips:{len(CHIPS)} degree-types:{len(degree_types)}")
