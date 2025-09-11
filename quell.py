import streamlit as st
import pandas as pd
import json
import base64
import unicodedata
import re

# =========================
#  TECH-LOOK VERSION (clean, flat, precise)
#  - Beibehaltung der Pill-Farben (gelb = CSB/SAP, grün = Schlüssel, rot = Tour)
#  - Weniger verspielt: flach, klare Linien, weniger Rundungen, keine Gradients, präzise Typografie
#  - ProCall: callto:
#  - „Zurück zur Suche“-Button
#  - Umlaut-/Akzent-Suche, Zero-Width-Fix, robustes FB-Matching
# =========================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Kunden-Suche</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@450;600;700;900&family=Inter+Tight:wght@500;700;800;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f5f6f8; --surface:#ffffff; --alt:#fafbfc;
  --line:#d5d9e0; --line-strong:#c9ced6;
  --txt:#0f172a; --muted:#334155;
  --accent:#2563eb; --accent-strong:#1d4ed8;

  /* Chips */
  --pill-yellow:#fff6cc; --pill-yellow-border:#f1d264; --pill-yellow-text:#55310b;
  --pill-green:#dff6e8; --pill-green-border:#8ee1b2; --pill-green-text:#085a3f;
  --pill-red:#ffe0e0;   --pill-red-border:#ffc8c8;   --pill-red-text:#6b1a1a;

  /* Phone chips */
  --chip-fb-bg:#e6f3fb;     --chip-fb-bd:#98d7f5; --chip-fb-tx:#0b4a6b;
  --chip-market-bg:#ebe7fd; --chip-market-bd:#c9bdfa; --chip-market-tx:#342a8e;

  --radius:6px;
  --fs-10:10px; --fs-11:11px; --fs-12:12px; --fs-13:13px;
}

/* Global – technischer Look: flach, scharf, präzise */
*{box-sizing:border-box}
html, body{margin:0; padding:0; min-height:100%; overflow:visible !important; background:var(--bg);}
body{
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.45; font-weight:600;
  letter-spacing:0.1px;
}

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:12px;}
.container{width:100%; max-width:1400px;}
.card{background:var(--surface); border:1px solid var(--line); border-radius:var(--radius);}

/* Header – neutral, technisch */
.header{
  padding:10px 12px; border-bottom:1px solid var(--line);
  display:flex; align-items:center; gap:12px; justify-content:center;
}
.brand-logo{height:44px; width:auto}
.title{font-family:"Inter",system-ui; font-weight:900; font-size:13px; letter-spacing:.3px}

/* Searchbar – kompakt, klar */
.searchbar{
  padding:10px 12px; display:grid; grid-template-columns:1fr 280px auto auto; gap:10px; align-items:center;
  border-bottom:1px solid var(--line); background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr} }
@media(max-width:680px){ .searchbar{grid-template-columns:1fr} }

.field{display:grid; grid-template-columns:72px 1fr; gap:8px; align-items:center}
.label{font-weight:800; color:var(--muted); font-size:var(--fs-11); text-transform:uppercase; letter-spacing:.35px}
.input{
  width:100%; padding:7px 9px; border:1px solid var(--line); border-radius:5px;
  background:#fff; font-size:var(--fs-12); font-weight:700;
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 2px rgba(37,99,235,.15)}

.btn{
  padding:7px 10px; border:1px solid var(--line); background:#fff; color:#111827;
  border-radius:5px; cursor:pointer; font-weight:800; font-size:var(--fs-12); letter-spacing:.2px
}
.btn:hover{background:#f2f4f7}
.btn-danger{border-color:#e11d48; background:#e11d48; color:#fff}
.btn-danger:hover{background:#c81e44}
.btn-back{border-color:var(--accent); color:var(--accent-strong); background:#eef2ff;}
.btn-back:hover{background:#e0e7ff}

/* Content */
.content{padding:12px;}

/* Banner (Tour/Key) – sachlich, flach */
.tour-wrap{display:none; margin-bottom:10px}
.tour-banner{
  display:flex; align-items:center; justify-content:space-between;
  padding:8px 12px; border:1px solid var(--line-strong); border-radius:6px;
  background:#f0f3f8; color:#0f172a; font-weight:900; font-size:12px;
}

/* Tabelle ohne interne Scrolls; mit klarer Rasterung */
.table-section{padding:6px 0}
table{width:100%; border-collapse:separate; border-spacing:0; table-layout:fixed; font-size:var(--fs-12)}
thead th{
  position:sticky; top:0; background:#f3f5f8; color:#0f172a; font-weight:900;
  border-bottom:1px solid var(--line-strong); padding:8px 10px; white-space:nowrap; text-align:left; z-index:2
}
tbody td{padding:8px 10px; border-bottom:1px solid var(--line); vertical-align:top; text-align:left; font-weight:700}

/* 2-zeilig je Zelle, ohne Umbruchschaos */
.cell{display:flex; flex-direction:column; align-items:flex-start; gap:4px; min-height:36px}
.cell-top,.cell-sub{white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* kleine technische Label */
.small-label{font-family:"Inter",system-ui; font-size:var(--fs-10); font-weight:900; color:#0f172a; letter-spacing:.35px; text-transform:uppercase}

/* CSB/SAP – gelbe Chips, technischer Stil, mono digits */
a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--pill-yellow); color:var(--pill-yellow-text);
  border:1px solid var(--pill-yellow-border);
  border-radius:999px; padding:3px 9px; font-weight:900; font-size:var(--fs-11);
  text-decoration:none; line-height:1; letter-spacing:.2px
}
a.id-chip .mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:700}
a.id-chip:hover{filter:brightness(0.98)}
.id-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.9}

/* Schlüssel grün, klar getrennt */
.key-tour{display:flex; flex-direction:column; gap:8px; width:100%}
.key-line{display:flex; align-items:center; gap:10px}
.key-divider{height:1px; background:var(--line); border:0; width:100%; margin:0}
.badge-key{
  background:var(--pill-green);
  border:1px solid var(--pill-green-border);
  color:var(--pill-green-text);
  border-radius:999px; padding:3px 8px; font-weight:900; font-size:var(--fs-11);
}

/* Tour-Pills – rot, flach, Wrap */
.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-block; background:var(--pill-red); border:1px solid var(--pill-red-border); color:var(--pill-red-text);
  padding:3px 8px; border-radius:999px; font-weight:900; font-size:var(--fs-10); cursor:pointer; line-height:1.25; letter-spacing:.15px
}
.tour-btn:hover{filter:brightness(0.98)}

/* Phone-Chips – technisch, klar */
.phone-line{display:flex; flex-wrap:wrap; gap:6px}
a.phone-chip{
  display:inline-flex; align-items:center; gap:6px;
  border-radius:999px; padding:3px 9px; font-weight:900; font-size:var(--fs-11); line-height:1;
  text-decoration:none; cursor:pointer; letter-spacing:.15px
}
a.phone-chip .mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:700}
a.phone-chip.chip-fb{background:var(--chip-fb-bg); color:var(--chip-fb-tx); border:1px solid var(--chip-fb-bd)}
a.phone-chip.chip-market{background:var(--chip-market-bg); color:var(--chip-market-tx); border:1px solid var(--chip-market-bd)}
a.phone-chip:hover{filter:brightness(0.98)}
.chip-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.9}

/* Map Button – flach, deutlich */
.table-map{
  text-decoration:none; font-weight:900; font-size:var(--fs-11);
  padding:6px 11px; border-radius:5px; border:1px solid var(--accent);
  background:var(--accent); color:#fff; display:inline-block; text-align:center; letter-spacing:.2px
}
.table-map:hover{background:var(--accent-strong); border-color:var(--accent-strong)}
</style>
</head>
<body>
<div class="page">
  <div class="container">
    <div class="card">
      <div class="header">
        <img class="brand-logo" alt="Logo" src="__LOGO_DATA_URL__">
        <div class="title">Kunden-Suche</div>
      </div>

      <div class="searchbar">
        <div class="field">
          <div class="label">Suche</div>
          <input class="input" id="smartSearch" placeholder="Name / Ort / CSB / SAP / Tour / Fachberater / Telefon / …">
        </div>
        <div class="field">
          <div class="label">Schlüssel</div>
          <input class="input" id="keySearch" placeholder="exakt (z. B. 40)">
        </div>
        <button class="btn btn-back" id="btnBack" style="display:none;">Zurück zur Suche</button>
        <button class="btn btn-danger" id="btnReset">Zurücksetzen</button>
      </div>

      <div class="content">
        <div class="tour-wrap" id="tourWrap">
          <div class="tour-banner">
            <span id="tourTitle"></span>
            <small id="tourExtra"></small>
          </div>
        </div>

        <div class="table-section">
          <table id="resultTable" style="display:none;">
            <thead>
              <tr>
                <th>CSB / SAP</th>
                <th>Name / Straße</th>
                <th>PLZ / Ort</th>
                <th>Schlüssel / Touren</th>
                <th>Fachberater / Markttelefon</th>
                <th>Aktion</th>
              </tr>
            </thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>

      </div>
    </div>
  </div>
</div>

<script>
const tourkundenData   = {  };
const keyIndex         = {  };
const beraterIndex     = {  };
const beraterCSBIndex  = {  };

const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];
let prevQuery = null;
const DIAL_SCHEME = 'callto';
const DEBUG_PHONE = false;

/* Normalisierung / Utils */
function sanitizePhone(num){ return (num||'').toString().trim().replace(/[^\\d+]/g,''); }
function makePhoneChip(label, num, extraClass){
  const clean = sanitizePhone(num);
  const a = document.createElement('a');
  a.className = 'phone-chip ' + extraClass;
  a.href = `${DIAL_SCHEME}:${clean}`;
  const tag = el('span','chip-tag',label);
  const mono = el('span','mono',' '+num);
  a.append(tag, mono);
  return a;
}

function normDE(s){
  if(!s) return '';
  let x = s.toLowerCase();
  x = x.replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
  return x.replace(/\\s+/g,' ').trim();
}
function normalizeDigits(v){
  if(v == null) return '';
  let s = String(v).trim().replace(/\\.0$/,'');
  s = s.replace(/[^0-9]/g,'');
  s = s.replace(/^0+(\\d)/,'$1');
  return s;
}

/* Name-Normalisierung (robust, inkl. Zero-Width/BOM) */
function normalizeNameKey(s){
  if(!s) return '';
  let x = s;
  x = x.replace(/[\\u200B-\\u200D\\uFEFF]/g, '');      // zero-width, BOM
  x = x.replace(/\\u00A0/g,' ').replace(/[–—]/g,'-');  // nbsp, dashes
  x = x.toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,''); // accents
  x = x.replace(/\\(.*?\\)/g,' ');                      // remove (...) notes
  x = x.replace(/[./,;:+*_#|]/g,' ').replace(/-/g,' ');
  x = x.replace(/[^a-z\\s]/g,' ');                      // letters + space only
  x = x.replace(/\\s+/g,' ').trim();
  return x;
}
function nameVariants(s){
  const base = normalizeNameKey(s);
  if(!base) return [];
  const parts = base.split(' ').filter(Boolean);
  const out = new Set([base]);
  if(parts.length >= 2){
    const first = parts[0], last = parts[parts.length-1];
    out.add(`${first} ${last}`);
    out.add(`${last} ${first}`);
  }
  return Array.from(out);
}

/* FB-Matching (robust + eindeutige Token) */
function pickBeraterPhone(fachberaterName){
  if(!fachberaterName) return '';
  const variants = nameVariants(fachberaterName);
  if (DEBUG_PHONE){ console.log('[FB-MATCH] Original:', fachberaterName, 'Variants:', variants); }

  for (const v of variants){
    if (beraterIndex[v]) return beraterIndex[v];
  }
  const keys = Object.keys(beraterIndex);
  for (const v of variants){
    const parts = v.split(' ').filter(Boolean);
    for (const k of keys){
      if (parts.every(p => k.includes(p))) return beraterIndex[k];
    }
  }
  for (const v of variants){
    const parts = v.split(' ').filter(Boolean);
    if (!parts.length) continue;
    const last = parts[parts.length-1];
    const hits = keys.filter(k => k.includes(last));
    if (hits.length === 1) return beraterIndex[hits[0]];
  }
  for (const v of variants){
    const parts = v.split(' ').filter(Boolean);
    if (!parts.length) continue;
    const first = parts[0];
    const hits = keys.filter(k => k.includes(first));
    if (hits.length === 1) return beraterIndex[hits[0]];
  }
  return '';
}

/* Datenaufbau */
function dedupByCSB(list){
  const seen = new Set(); const out = [];
  for (const k of list){
    const key = normalizeDigits(k.csb_nummer);
    if (!seen.has(key)){ seen.add(key); out.push(k); }
  }
  return out;
}
function buildData(){
  const map = new Map();
  for(const [tour, list] of Object.entries(tourkundenData)){
    const tourN = normalizeDigits(tour);
    list.forEach(k=>{
      const csb = normalizeDigits(k.csb_nummer);
      if(!csb) return;

      if(!map.has(csb)){
        const rec = {...k};
        rec.csb_nummer   = csb;
        rec.sap_nummer   = normalizeDigits(rec.sap_nummer);
        rec.postleitzahl = normalizeDigits(rec.postleitzahl);
        rec.touren       = [];

        const keyFromIndex = keyIndex[csb] || "";
        rec.schluessel   = normalizeDigits(rec.schluessel) || keyFromIndex;

        if (beraterCSBIndex[csb] && beraterCSBIndex[csb].name){
          rec.fachberater = beraterCSBIndex[csb].name;
        }
        rec.fb_phone     = rec.fachberater ? pickBeraterPhone(rec.fachberater) : '';
        rec.market_phone = (beraterCSBIndex[csb] && beraterCSBIndex[csb].telefon) ? beraterCSBIndex[csb].telefon : '';

        map.set(csb, rec);
      }
      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
}

/* UI Bausteine */
function pushPrevQuery(){
  const val = $('#smartSearch').value.trim();
  if (val){ prevQuery = val; $('#btnBack').style.display = 'inline-block'; }
}
function popPrevQuery(){
  if (prevQuery){
    $('#smartSearch').value = prevQuery;
    prevQuery = null; $('#btnBack').style.display='none'; onSmart();
  }
}
function makeIdChip(label, value){
  const a = document.createElement('a');
  a.className = 'id-chip';
  a.href = 'javascript:void(0)';
  a.addEventListener('click', ()=>{
    pushPrevQuery();
    const input = $('#smartSearch');
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  });
  const tag = el('span','id-tag', label);
  const mono = el('span','mono', ' '+value);
  a.append(tag, mono);
  return a;
}
function twoLineCell(top, sub){
  const wrap = el('div','cell');
  const a = el('div','cell-top', top);
  const b = el('div','cell-sub', sub);
  wrap.append(a,b);
  return wrap;
}

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = normalizeDigits(k.csb_nummer) || '-';
  const sap = normalizeDigits(k.sap_nummer) || '-';
  const plz = normalizeDigits(k.postleitzahl) || '-';

  // CSB/SAP
  const td1 = document.createElement('td');
  const t1 = el('div','cell');
  const top1 = el('div','cell-top'); top1.appendChild(makeIdChip('CSB', csb));
  const sub1 = el('div','cell-sub'); sub1.appendChild(makeIdChip('SAP', sap));
  t1.append(top1, sub1); td1.appendChild(t1); tr.appendChild(td1);

  // Name / Straße
  const td2 = document.createElement('td');
  td2.appendChild(twoLineCell(k.name || '-', k.strasse || '-'));
  tr.appendChild(td2);

  // PLZ / Ort
  const td3 = document.createElement('td');
  td3.appendChild(twoLineCell(plz, k.ort || '-'));
  tr.appendChild(td3);

  // Schlüssel / Touren
  const td4 = document.createElement('td');
  const wrap4 = el('div','cell key-tour');

  const keyDisp = normalizeDigits(k.schluessel) || keyIndex[csb] || '';
  const keyLine = el('div','key-line');
  keyLine.appendChild(el('span','small-label','Schlüssel'));
  if(keyDisp){ keyLine.appendChild(el('span','badge-key', keyDisp)); } else { keyLine.appendChild(el('span','', '-')); }

  const divider = el('hr','key-divider');

  const toursWrap = el('div','cell-sub');
  const toursLabel = el('span','small-label','Touren');
  const tours = el('div','tour-inline');
  (k.touren||[]).forEach(t=>{
    const tnum = normalizeDigits(t.tournummer);
    const tb = el('span','tour-btn', tnum+' ('+t.liefertag.substring(0,2)+')');
    tb.onclick=()=>{ pushPrevQuery(); $('#smartSearch').value = tnum; onSmart(); };
    tours.appendChild(tb);
  });
  toursWrap.append(toursLabel, tours);

  wrap4.append(keyLine, divider, toursWrap);
  td4.appendChild(wrap4); tr.appendChild(td4);

  // Fachberater / Markttelefon
  const td5 = document.createElement('td');
  const top5 = el('div','cell-top', k.fachberater || '-');
  const sub5 = el('div','cell-sub phone-line');
  if (k.fb_phone){     sub5.appendChild(makePhoneChip('FB', k.fb_phone, 'chip-fb')); }
  if (k.market_phone){ sub5.appendChild(makePhoneChip('Markt', k.market_phone, 'chip-market')); }
  if (!k.fb_phone && !k.market_phone){ sub5.textContent='-'; }
  const wrap5 = el('div','cell'); wrap5.append(top5, sub5);
  td5.appendChild(wrap5); tr.appendChild(td5);

  // Aktion
  const td6 = document.createElement('td');
  const sub6 = el('div','cell-sub');
  const a = document.createElement('a');
  a.className='table-map'; a.textContent='Map';
  a.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||'')); a.target='_blank';
  sub6.appendChild(a);
  const wrap6 = el('div','cell'); wrap6.append(el('div','cell-top',''), sub6);
  td6.appendChild(wrap6); tr.appendChild(td6);

  return tr;
}

function renderTable(list){
  const body = $('#tableBody');
  const table = $('#resultTable');
  body.innerHTML='';
  if(list.length){
    list.forEach(k=> body.appendChild(rowFor(k)));
    table.style.display='table';
  } else {
    table.style.display='none';
  }
}

/* Banner */
function renderTourTop(list, query, isExact){
  const wrap = $('#tourWrap'), title = $('#tourTitle'), extra = $('#tourExtra');
  if(!list.length){ wrap.style.display='none'; title.textContent=''; extra.textContent=''; return; }
  if (query.startsWith('Schluessel ')) {
    const key = query.replace(/^Schluessel\\s+/, '');
    title.textContent = 'Schlüssel ' + key + ' — ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');
  } else {
    title.textContent = (isExact?('Tour '+query):('Tour-Prefix '+query+'*')) + ' — ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');
  }
  const dayCount = {};
  list.forEach(k => (k.touren||[]).forEach(t=>{
    const tnum = normalizeDigits(t.tournummer);
    const cond = isExact ? (tnum === query) : tnum.startsWith(query.replace('Schluessel ',''));
    if(cond || query.startsWith('Schluessel ')){ dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1; }
  }));
  extra.textContent = Object.entries(dayCount).sort().map(([d,c])=> d + ': ' + c).join('  •  ');
  wrap.style.display='block';
}
function closeTourTop(){ $('#tourWrap').style.display='none'; $('#tourTitle').textContent=''; $('#tourExtra').textContent=''; }

/* Suche */
function dedupByCSB(list){
  const seen = new Set(); const out = [];
  for (const k of list){
    const key = normalizeDigits(k.csb_nummer);
    if (!seen.has(key)){ seen.add(key); out.push(k); }
  }
  return out;
}

function onSmart(){
  const qRaw = $('#smartSearch').value.trim();
  closeTourTop();
  if(!qRaw){ renderTable([]); return; }

  if (/^\\d{1,3}$/.test(qRaw)){
    const qN = qRaw.replace(/^0+(\\d)/,'$1');
    const results = allCustomers.filter(k => (k.touren||[]).some(t => (t.tournummer||'').startsWith(qN)));
    renderTourTop(results, qN, false); renderTable(results); return;
  }
  if (/^\\d{4}$/.test(qRaw)){
    const qN = qRaw.replace(/^0+(\\d)/,'$1');
    const tourResults = allCustomers.filter(k => (k.touren||[]).some(t => (t.tournummer||'') === qN));
    const csbResults  = allCustomers.filter(k => (k.csb_nummer||'') === qN);
    const results = dedupByCSB([...tourResults, ...csbResults]);
    if (tourResults.length) renderTourTop(tourResults, qN, true); else closeTourTop();
    renderTable(results); return;
  }
  const qN = normDE(qRaw);
  const results = allCustomers.filter(k=>{
    const fb = k.fachberater || '';
    const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||''));
    return normDE(text).includes(qN);
  });
  renderTable(results);
}
function onKey(){
  const q = $('#keySearch').value.trim();
  closeTourTop();
  if(!q){ renderTable([]); return; }
  const qClean = q.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
  const matches = [];
  for (const k of allCustomers){
    const keyForRow = (k.schluessel||'') || (keyIndex[k.csb_nummer]||'');
    if (keyForRow === qClean) matches.push(k);
  }
  if(matches.length){ renderTourTop(matches, 'Schluessel ' + qClean, true); }
  renderTable(matches);
}
function debounce(fn, d=140){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData!=='undefined' && Object.keys(tourkundenData).length > 0){ buildData(); }
  document.getElementById('smartSearch').addEventListener('input', debounce(onSmart, 140));
  document.getElementById('keySearch').addEventListener('input', debounce(onKey, 140));
  document.getElementById('btnReset').addEventListener('click', ()=>{
    document.getElementById('smartSearch').value=''; document.getElementById('keySearch').value='';
    closeTourTop(); renderTable([]); prevQuery=null; document.getElementById('btnBack').style.display='none';
  });
  document.getElementById('btnBack').addEventListener('click', ()=>{ popPrevQuery(); });
});
</script>
</body>
</html>
"""

# =========================
#  STREAMLIT APP (Python)
# =========================
st.title("Kunden-Suchseite – Tech Look")
st.caption("Pills & Farben wie gehabt • flach & präzise • ProCall (callto:) • Zurück-Button • robuste Suche/Matching")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png","jpg","jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater-CSB-Zuordnung (A=Fachberater, I=CSB, O=Telefon/Markt)", type=["xlsx"])

# ---------- Helpers ----------
def normalize_digits_py(v) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip().replace(".0", "")
    s = "".join(ch for ch in s if ch.isdigit())
    if not s:
        return ""
    s = s.lstrip("0")
    return s if s else "0"

def norm_de_py(s: str) -> str:
    if not s:
        return ""
    x = s
    x = x.replace("\u200b","").replace("\u200c","").replace("\u200d","").replace("\ufeff","")
    x = x.replace("\u00A0", " ").replace("–","-").replace("—","-")
    x = x.lower().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    x = unicodedata.normalize("NFD", x)
    x = "".join(ch for ch in x if unicodedata.category(ch) != "Mn")
    x = re.sub(r"\(.*?\)", " ", x)
    x = re.sub(r"[./,;:+*_#|]", " ", x)
    x = re.sub(r"-", " ", x)
    x = re.sub(r"[^a-z\s]", " ", x)
    x = " ".join(x.split())
    return x

def build_key_map(df: pd.DataFrame) -> dict:
    if df.shape[1] < 6:
        st.warning("Schlüsseldatei hat < 6 Spalten – nehme letzte vorhandene Spalte als Schlüssel.")
    csb_col = 0
    key_col = 5 if df.shape[1] > 5 else df.shape[1] - 1
    mapping = {}
    for _, row in df.iterrows():
        csb = normalize_digits_py(row.iloc[csb_col] if df.shape[1] > 0 else "")
        key = normalize_digits_py(row.iloc[key_col] if df.shape[1] > 0 else "")
        if csb:
            mapping[csb] = key
    return mapping

def build_berater_map(df: pd.DataFrame) -> dict:
    mapping = {}
    for _, row in df.iterrows():
        v = ("" if df.shape[1] < 1 or pd.isna(row.iloc[0]) else str(row.iloc[0])).strip()
        n = ("" if df.shape[1] < 2 or pd.isna(row.iloc[1]) else str(row.iloc[1])).strip()
        t = ("" if df.shape[1] < 3 or pd.isna(row.iloc[2]) else str(row.iloc[2])).strip()
        if not t:
            continue
        full1 = norm_de_py(f"{v} {n}")
        full2 = norm_de_py(f"{n} {v}")
        for key in {full1, full2}:
            if key and key not in mapping:
                mapping[key] = t
    return mapping

def build_berater_csb_map(df: pd.DataFrame) -> dict:
    mapping = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        if csb:
            mapping[csb] = {"name": fach, "telefon": tel}
    return mapping

def to_data_url(file) -> str:
    mime = file.type or ("image/png" if file.name.lower().endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(file.read()).decode("utf-8")

# ---------- Build HTML ----------
if excel_file and key_file:
    if st.button("HTML erzeugen", type="primary"):
        if logo_file is None:
            st.error("Bitte ein Logo (PNG/JPG) hochladen.")
            st.stop()
        logo_data_url = to_data_url(logo_file)

        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        SPALTEN_MAPPING = {
            "csb_nummer":"Nr","sap_nummer":"SAP-Nr.","name":"Name","strasse":"Strasse",
            "postleitzahl":"Plz","ort":"Ort","fachberater":"Fachberater"
        }
        LIEFERTAGE_MAPPING = {"Montag":"Mo","Dienstag":"Die","Mittwoch":"Mitt","Donnerstag":"Don","Freitag":"Fr","Samstag":"Sam"}

        try:
            with st.spinner("Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            berater_map = {}
            if berater_file is not None:
                with st.spinner("Lese Fachberater-Telefonliste (ohne Header)..."):
                    berater_file.seek(0)
                    bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                    bf = bf.rename(columns={0: "Vorname", 1: "Nachname", 2: "Nummer"}).dropna(how="all")
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("Lese Fachberater-CSB-Zuordnung..."):
                    try:
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=0)
                    except Exception:
                        berater_csb_file.seek(0)
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=None)
                    berater_csb_map = build_berater_csb_map(bcf)

            tour_dict = {}
            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns: continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit(): continue
                        tournr = normalize_digits_py(tournr_raw)

                        entry = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean            = normalize_digits_py(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        entry["csb_nummer"]   = csb_clean
                        entry["sap_nummer"]   = normalize_digits_py(entry.get("sap_nummer", ""))
                        entry["postleitzahl"] = normalize_digits_py(entry.get("postleitzahl", ""))
                        entry["schluessel"]   = key_map.get(csb_clean, "")
                        entry["liefertag"]    = tag

                        if csb_clean and csb_clean in berater_csb_map and berater_csb_map[csb_clean].get("name"):
                            entry["fachberater"] = berater_csb_map[csb_clean]["name"]

                        tour_dict.setdefault(tournr, []).append(entry)

            with st.spinner("Verarbeite Kundendatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0))

            final_html = (HTML_TEMPLATE
                .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
                .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
                .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
                .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
                .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            st.download_button(
                "Download HTML (Tech Look)",
                data=final_html.encode("utf-8"),
                file_name="suche_tech.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
