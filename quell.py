import streamlit as st
import pandas as pd
import json
import base64
import unicodedata
import re

# ===== Vollständige App – technisch, heller Header, knallige Pills
# - KEINE "Aktion"-Spalte mehr
# - Addressen-Pill (klickbar -> Google Maps)
# - Touren in eigener Spalte
# - CSB/SAP gelbe Pills (klickbar für Suche)
# - Schlüssel grüne Pill
# - Telefon-Pills (FB/Markt) + Mail-Pills, alles untereinander
# - "Zurück zur Suche"-Button
# - Container wieder schmaler (1400px)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Kunden-Suche</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800;900&family=Inter+Tight:wght@700;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f3f6fb; --surface:#ffffff; --alt:#f9fbff;
  --grid:#cfd7e6; --grid-2:#bfc9dd; --head-grid:#b3bfd6;
  --txt:#0c1220; --muted:#293346;
  --accent:#2563eb; --accent-2:#1f4fd3;

  /* Pills */
  --pill-yellow-bg:#fff3b0; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#4a3001;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#ffe4e6;   --pill-red-bd:#fb7185;  --pill-red-tx:#7f1d1d;

  /* Tel/Mail chips */
  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;
  --chip-mail-bg:#eef2ff; --chip-mail-bd:#6366f1; --chip-mail-tx:#1e1b4b;

  --row-sep:#e6edff;
  --radius:6px; --radius-pill:999px;
  --fs-10:10px; --fs-11:11px; --fs-12:12px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.35; font-weight:800; letter-spacing:.1px;
}

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:10px}
.container{width:100%; max-width:1400px} /* <<< Container-Breite */
.card{background:var(--surface); border:1px solid var(--grid); border-radius:8px; overflow:hidden}

/* Header */
.header{
  padding:10px 12px;
  background:linear-gradient(180deg,#ffffff 0%, #f4f7fe 100%);
  color:#0b1226; display:flex; align-items:center; justify-content:center; gap:10px;
  border-bottom:1px solid var(--grid);
}
.brand-logo{height:44px; width:auto}
.title{font-weight:900; letter-spacing:.35px; font-size:13px; text-transform:uppercase}

/* Searchbar */
.searchbar{
  padding:8px 12px; display:grid; grid-template-columns:1fr 260px auto auto; gap:8px; align-items:center;
  border-bottom:1px solid var(--grid); background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr} }
@media(max-width:680px){ .searchbar{grid-template-columns:1fr} }
.field{display:grid; grid-template-columns:74px 1fr; gap:6px; align-items:center}
.label{font-weight:900; color:var(--muted); font-size:var(--fs-11); text-transform:uppercase; letter-spacing:.35px}
.input{
  width:100%; padding:7px 9px; border:1px solid var(--grid); border-radius:6px; background:#fff;
  font-size:var(--fs-12); font-weight:900;
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 2px rgba(37,99,235,.16)}

/* Buttons */
.btn{padding:7px 10px; border:1px solid var(--grid); background:#fff; color:#0f172a; border-radius:6px; cursor:pointer; font-weight:900; font-size:var(--fs-12)}
.btn:hover{background:#f2f5f9}
.btn-danger{border-color:#d7263d; background:#d7263d; color:#fff}
.btn-danger:hover{background:#bf1f33}
.btn-back{border-color:var(--accent); color:var(--accent-2); background:#eef2ff}
.btn-back:hover{background:#e2e8ff}

/* Tour-Banner */
.tour-wrap{display:none; padding:10px 12px 0}
.tour-banner{
  display:flex; align-items:center; justify-content:space-between; gap:12px;
  padding:8px 10px; border:1px dashed var(--head-grid); border-radius:6px;
  background:linear-gradient(180deg,#fbfcff,#f4f7fd);
  font-weight:900; font-size:12px; color:#0f172a;
}

/* Tabelle */
.table-section{padding:6px 12px 14px}
table{width:100%; border-collapse:separate; border-spacing:0; table-layout:fixed; font-size:var(--fs-12)}
thead th{
  position:sticky; top:0; z-index:2;
  background:linear-gradient(180deg,#f7f9fe,#eef2f8);
  color:#0f172a; font-weight:900; text-transform:uppercase; letter-spacing:.25px;
  border-bottom:2px solid var(--head-grid); border-right:1px solid var(--head-grid);
  padding:8px 9px; white-space:nowrap; text-align:left;
}
thead th:last-child{border-right:none}
tbody td{
  padding:8px 9px; vertical-align:top; font-weight:800;
  border-bottom:1px solid var(--grid); border-right:1px solid var(--grid);
  background:#fff;
}
tbody td:last-child{border-right:none}

/* Zeilentrennung je Kunde */
tbody tr:nth-child(odd) td{background:#f8fbff}
tbody tr:nth-child(even) td{background:#ffffff}
tbody tr+tr td{border-top:6px solid var(--row-sep)}
tbody tr:hover td{background:#eef4ff}

/* Zellen */
.cell{display:flex; flex-direction:column; gap:6px; width:100%}
.stack{display:flex; flex-direction:column; gap:6px}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Monospace Zahlen */
.mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:700}

/* ID-Chips (gelb) */
a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--pill-yellow-bg); color:var(--pill-yellow-tx);
  border:1.5px solid var(--pill-yellow-bd); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); text-decoration:none; line-height:1;
  box-shadow:0 0 0 2px rgba(245,158,11,.12) inset; width:fit-content;
}
a.id-chip:hover{filter:brightness(.97)}
.id-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

/* Adresse als Pill (klickbar -> Maps) */
a.addr-chip{
  display:inline-flex; align-items:center; gap:6px; width:fit-content;
  background:#fff; border:1.5px dashed var(--grid-2); color:#0f172a;
  border-radius:var(--radius-pill); padding:4px 10px; text-decoration:none; font-weight:900; font-size:var(--fs-11);
}
a.addr-chip:hover{background:#f7faff}

/* Schlüssel (grün) */
.badge-key{
  display:inline-block; background:var(--pill-green-bg); border:1.5px solid var(--pill-green-bd);
  color:var(--pill-green-tx); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); line-height:1;
  box-shadow:0 0 0 2px rgba(16,185,129,.12) inset; width:fit-content;
}

/* Touren (rot) */
.tour-inline{display:flex; flex-direction:column; gap:6px}
.tour-btn{
  display:inline-block; background:var(--pill-red-bg); border:1.5px solid var(--pill-red-bd); color:var(--pill-red-tx);
  padding:3px 9px; border-radius:var(--radius-pill); font-weight:900; font-size:var(--fs-10); cursor:pointer; line-height:1.25; letter-spacing:.15px;
  box-shadow:0 0 0 2px rgba(251,113,133,.12) inset; width:fit-content;
}
.tour-btn:hover{filter:brightness(.97)}

/* Telefon & Mail – untereinander */
a.phone-chip, a.mail-chip{
  display:inline-flex; align-items:center; gap:6px; border-radius:var(--radius-pill);
  padding:3px 9px; font-weight:900; font-size:var(--fs-11); line-height:1; text-decoration:none; cursor:pointer; width:fit-content;
}
a.phone-chip.chip-fb{background:var(--chip-fb-bg); color:var(--chip-fb-tx); border:1.5px solid var(--chip-fb-bd)}
a.phone-chip.chip-market{background:var(--chip-mk-bg); color:var(--chip-mk-tx); border:1.5px solid var(--chip-mk-bd)}
a.mail-chip{background:var(--chip-mail-bg); color:var(--chip-mail-tx); border:1.5px solid var(--chip-mail-bd)}
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(.97)}
.chip-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}
.mail-text{max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; display:inline-block}

/* Tour-Banner-Pill (etwas größer) */
.banner-pill{
  display:inline-flex; align-items:center; gap:8px;
  background:#fff7ed; color:#7c2d12; border:2px solid #fdba74; border-radius:999px;
  padding:6px 12px; font-weight:900;
}
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

      <div class="tour-wrap" id="tourWrap">
        <div class="tour-banner">
          <span class="banner-pill" id="tourTitle"></span>
          <small id="tourExtra"></small>
        </div>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none;">
          <colgroup>
            <col style="width:220px">  <!-- CSB / SAP -->
            <col style="width:560px">  <!-- Name / Adresse -->
            <col style="width:280px">  <!-- Touren -->
            <col style="width:120px">  <!-- Schlüssel -->
            <col style="width:520px">  <!-- Fachberater / Markt (Tel + Mail) -->
          </colgroup>
          <thead>
            <tr>
              <th>CSB / SAP</th>
              <th>Name / Adresse</th>
              <th>Touren</th>
              <th>Schlüssel</th>
              <th>Fachberater / Markt</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
/* ===== Daten (von Python ersetzt) ===== */
const tourkundenData   = {  };
const keyIndex         = {  };
const beraterIndex     = {  };  // nameKey -> phone
const beraterCSBIndex  = {  };  // csb -> { name, telefon, email_market }

const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];
let prevQuery = null;
const DIAL_SCHEME = 'callto';

function sanitizePhone(num){ return (num||'').toString().trim().replace(/[^\\d+]/g,''); }
function makePhoneChip(label, num, cls){
  if(!num) return null;
  const a = document.createElement('a');
  a.className = 'phone-chip '+cls;
  a.href = `${DIAL_SCHEME}:${sanitizePhone(num)}`;
  a.append(el('span','chip-tag',label), el('span','mono',' '+num));
  return a;
}
function makeMailChip(label, mail){
  if(!mail) return null;
  const a = document.createElement('a');
  a.className = 'mail-chip';
  a.href = `mailto:${mail}`;
  a.title = mail;
  a.append(el('span','chip-tag',label), (()=>{
    const s = document.createElement('span'); s.className='mail-text'; s.textContent=' '+mail; return s;
  })());
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
  s = s.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
  return s;
}
function normalizeNameKey(s){
  if(!s) return '';
  let x = s.replace(/[\\u200B-\\u200D\\uFEFF]/g,'').replace(/\\u00A0/g,' ').replace(/[–—]/g,'-').toLowerCase();
  x = x.replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/\\(.*?\\)/g,' ');
  x = x.replace(/[./,;:+*_#|]/g,' ').replace(/-/g,' ').replace(/[^a-z\\s]/g,' ').replace(/\\s+/g,' ').trim();
  return x;
}
function nameVariants(s){
  const base = normalizeNameKey(s); if(!base) return [];
  const parts = base.split(' ').filter(Boolean);
  const out = new Set([base]);
  if(parts.length >= 2){ const f=parts[0], l=parts[parts.length-1]; out.add(`${f} ${l}`); out.add(`${l} ${f}`); }
  return Array.from(out);
}
function pickBeraterPhone(name){
  if(!name) return '';
  const variants = nameVariants(name);
  for(const v of variants){ if(beraterIndex[v]) return beraterIndex[v]; }
  const keys = Object.keys(beraterIndex);
  for(const v of variants){
    const parts = v.split(' ').filter(Boolean);
    for(const k of keys){ if(parts.every(p=>k.includes(p))) return beraterIndex[k]; }
  }
  return '';
}
function dedupByCSB(list){
  const seen=new Set(), out=[];
  for(const k of list){ const csb=normalizeDigits(k.csb_nummer); if(!seen.has(csb)){ seen.add(csb); out.push(k); } }
  return out;
}
function buildData(){
  const map = new Map();
  for(const [tour, list] of Object.entries(tourkundenData)){
    const tourN = normalizeDigits(tour);
    list.forEach(k=>{
      const csb = normalizeDigits(k.csb_nummer); if(!csb) return;
      if(!map.has(csb)){
        const rec = {...k};
        rec.csb_nummer   = csb;
        rec.sap_nummer   = normalizeDigits(rec.sap_nummer);
        rec.postleitzahl = normalizeDigits(rec.postleitzahl);
        rec.touren = [];
        rec.schluessel  = normalizeDigits(rec.schluessel) || (keyIndex[csb]||'');
        if (beraterCSBIndex[csb] && beraterCSBIndex[csb].name){ rec.fachberater = beraterCSBIndex[csb].name; }
        rec.fb_phone     = rec.fachberater ? pickBeraterPhone(rec.fachberater) : '';
        rec.market_phone = (beraterCSBIndex[csb] && beraterCSBIndex[csb].telefon) ? beraterCSBIndex[csb].telefon : '';
        rec.market_mail  = (beraterCSBIndex[csb] && beraterCSBIndex[csb].email_market) ? beraterCSBIndex[csb].email_market : '';
        // Fachberater-Mail (Vorname.Nachname@edeka.de), nur wenn Name vorhanden & kein Sonderfall:
        if(rec.fachberater){
          const nk = normalizeNameKey(rec.fachberater).split(' ');
          if(nk.length>=2){
            const vor = nk[0], nach = nk[nk.length-1];
            rec.fb_mail = `${vor}.${nach}@edeka.de`;
          } else {
            rec.fb_mail = '';
          }
        } else rec.fb_mail = '';
        map.set(csb, rec);
      }
      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
}
/* Back-Navigation */
function pushPrevQuery(){ const v=$('#smartSearch').value.trim(); if(v){ prevQuery=v; $('#btnBack').style.display='inline-block'; } }
function popPrevQuery(){ if(prevQuery){ $('#smartSearch').value=prevQuery; prevQuery=null; $('#btnBack').style.display='none'; onSmart(); } }

/* UI builders */
function makeIdChip(label, value){
  const a=document.createElement('a'); a.className='id-chip'; a.href='javascript:void(0)'; a.title=label+' '+value+' suchen';
  a.addEventListener('click',()=>{ pushPrevQuery(); $('#smartSearch').value=value; onSmart(); });
  a.append(el('span','id-tag',label), el('span','mono',' '+value)); return a;
}
function makeAddrChip(name, strasse, plz, ort){
  const url='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((name||'')+', '+(strasse||'')+', '+(plz||'')+' '+(ort||''));
  const a=document.createElement('a'); a.className='addr-chip'; a.href=url; a.target='_blank'; a.title='Klick: Google Maps';
  const text=(strasse||'-')+', '+(plz||'')+' '+(ort||'-');
  a.append(el('span','chip-tag','Adresse'), el('span','', ' '+text));
  return a;
}
function twoLineCell(topNode, subNode){
  const w=el('div','cell');
  const s=el('div','stack');
  if(topNode) s.appendChild(topNode);
  if(subNode) s.appendChild(subNode);
  w.appendChild(s);
  return w;
}

/* Rendering */
function rowFor(k){
  const tr = document.createElement('tr');
  const csb = k.csb_nummer||'-', sap=k.sap_nummer||'-', plz=k.postleitzahl||'-';

  // CSB / SAP (untereinander, klickbare gelbe Pills)
  const td1 = document.createElement('td');
  const c1 = el('div','cell');
  const st1 = el('div','stack');
  st1.appendChild(makeIdChip('CSB', csb));
  st1.appendChild(makeIdChip('SAP', sap));
  c1.append(st1); td1.append(c1); tr.append(td1);

  // Name / Adresse (Adresse als Pill)
  const td2 = document.createElement('td');
  const nameTop = el('div','cell-top', k.name||'-');
  nameTop.style.fontWeight='900';
  const addrPill = makeAddrChip(k.name||'', k.strasse||'', plz, k.ort||'');
  td2.appendChild(twoLineCell(nameTop, addrPill));
  tr.append(td2);

  // Touren (eigene Spalte, vertikal gestapelt)
  const td3 = document.createElement('td');
  const tourStack = el('div','tour-inline');
  (k.touren||[]).forEach(t=>{
    const tnum=(t.tournummer||'');
    const b=el('span','tour-btn',tnum+' ('+t.liefertag.substring(0,2)+')');
    b.title='Tour '+tnum; b.onclick=()=>{ pushPrevQuery(); $('#smartSearch').value=tnum; onSmart(); };
    tourStack.appendChild(b);
  });
  td3.appendChild(tourStack);
  tr.append(td3);

  // Schlüssel (kleiner)
  const td4 = document.createElement('td');
  const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td4.appendChild(key ? el('span','badge-key',key) : el('span','', '-'));
  tr.append(td4);

  // Fachberater / Markt: alle Pills untereinander (FB-Tel, FB-Mail, Markt-Tel, Markt-Mail)
  const td5=document.createElement('td');
  const s5=el('div','stack');
  const fbTel = makePhoneChip('FB', k.fb_phone, 'chip-fb');
  const fbMail = makeMailChip('FB', k.fb_mail);
  const mkTel = makePhoneChip('Markt', k.market_phone, 'chip-market');
  const mkMail = makeMailChip('Markt', k.market_mail);
  if(fbTel) s5.appendChild(fbTel);
  if(fbMail) s5.appendChild(fbMail);
  if(mkTel) s5.appendChild(mkTel);
  if(mkMail) s5.appendChild(mkMail);
  if(!fbTel && !fbMail && !mkTel && !mkMail) s5.appendChild(el('div','cell-sub','-'));
  td5.appendChild(s5);
  tr.append(td5);

  return tr;
}
function renderTable(list){
  const body=$('#tableBody'), tbl=$('#resultTable'); body.innerHTML='';
  if(list.length){ list.forEach(k=>body.appendChild(rowFor(k))); tbl.style.display='table'; } else { tbl.style.display='none'; }
}

/* Tour-Banner */
function renderTourTop(list, query, isExact){
  const wrap=$('#tourWrap'), title=$('#tourTitle'), extra=$('#tourExtra');
  if(!list.length){ wrap.style.display='none'; title.textContent=''; extra.textContent=''; return; }
  if(query.startsWith('Schluessel ')){ const key=query.replace(/^Schluessel\\s+/, ''); title.textContent='Schlüssel '+key+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden'); }
  else{ title.textContent=(isExact?('Tour '+query):('Tour-Prefix '+query+'*'))+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden'); }
  const dayCount={}; list.forEach(k=>(k.touren||[]).forEach(t=>{ const tnum=t.tournummer||''; const cond=isExact?(tnum===query):tnum.startsWith(query.replace('Schluessel ','')); if(cond||query.startsWith('Schluessel ')){ dayCount[t.liefertag]=(dayCount[t.liefertag]||0)+1; }}));
  extra.textContent=Object.entries(dayCount).sort().map(([d,c])=>d+': '+c).join('  •  ');
  wrap.style.display='block';
}
function closeTourTop(){ $('#tourWrap').style.display='none'; $('#tourTitle').textContent=''; $('#tourExtra').textContent=''; }

/* Suche */
function onSmart(){
  const qRaw=$('#smartSearch').value.trim(); closeTourTop(); if(!qRaw){ renderTable([]); return; }
  if(/^\\d{1,3}$/.test(qRaw)){ const n=qRaw.replace(/^0+(\\d)/,'$1'); const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n))); renderTourTop(r,n,false); renderTable(r); return; }
  if(/^\\d{4}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1'); const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n)); const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n); const r=dedupByCSB([...tr,...cr]);
    if(tr.length) renderTourTop(tr,n,true); else closeTourTop(); renderTable(r); return;
  }
  const q=normDE(qRaw);
  const r=allCustomers.filter(k=>{ const fb=k.fachberater||''; const text=(k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||'')+' '+(k.fb_mail||'')+' '+(k.market_mail||'')); return normDE(text).includes(q); });
  renderTable(r);
}
function onKey(){
  const q=$('#keySearch').value.trim(); closeTourTop(); if(!q){ renderTable([]); return; }
  const n=q.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1'); const r=[]; for(const k of allCustomers){ const key=(k.schluessel||'')||(keyIndex[k.csb_nummer]||''); if(key===n) r.push(k); }
  if(r.length) renderTourTop(r,'Schluessel '+n,true); renderTable(r);
}
function debounce(fn,d=140){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(Object.keys(tourkundenData).length>0){ buildData(); }
  $('#smartSearch').addEventListener('input', debounce(onSmart,140));
  $('#keySearch').addEventListener('input', debounce(onKey,140));
  $('#btnReset').addEventListener('click', ()=>{ $('#smartSearch').value=''; $('#keySearch').value=''; closeTourTop(); renderTable([]); prevQuery=null; $('#btnBack').style.display='none'; });
  $('#btnBack').addEventListener('click', ()=>{ popPrevQuery(); });
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("Kunden-Suche – technisch & kompakt (ohne Aktionsspalte)")
st.caption("CSB/SAP gelbe Pills • Touren rot • Schlüssel grün • Adresse klickbar • Telefon/Mail-Pills gestapelt • 4-stellig = Tour ODER CSB")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png","jpg","jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Telefon, X=Markt-Mail)", type=["xlsx"])

def normalize_digits_py(v) -> str:
    if pd.isna(v): return ""
    s = str(v).strip().replace(".0","")
    s = "".join(ch for ch in s if ch.isdigit())
    if not s: return ""
    s = s.lstrip("0")
    return s if s else "0"

def norm_de_py(s: str) -> str:
    if not s: return ""
    x = s.replace("\u200b","").replace("\u200c","").replace("\u200d","").replace("\ufeff","")
    x = x.replace("\u00A0"," ").replace("–","-").replace("—","-").lower()
    x = x.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
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
    out = {}
    for _, row in df.iterrows():
        csb = normalize_digits_py(row.iloc[csb_col] if df.shape[1] > 0 else "")
        key = normalize_digits_py(row.iloc[key_col] if df.shape[1] > 0 else "")
        if csb: out[csb] = key
    return out

def build_berater_map(df: pd.DataFrame) -> dict:
    # A=Vorname, B=Nachname, C=Nummer
    out = {}
    for _, row in df.iterrows():
        v = ("" if df.shape[1] < 1 or pd.isna(row.iloc[0]) else str(row.iloc[0])).strip()
        n = ("" if df.shape[1] < 2 or pd.isna(row.iloc[1]) else str(row.iloc[1])).strip()
        t = ("" if df.shape[1] < 3 or pd.isna(row.iloc[2]) else str(row.iloc[2])).strip()
        if not t: continue
        k1 = norm_de_py(f"{v} {n}")
        k2 = norm_de_py(f"{n} {v}")
        for k in {k1, k2}:
            if k and k not in out:
                out[k] = t
    return out

def build_berater_csb_map(df: pd.DataFrame) -> dict:
    # A=Fachberater (Name), I=CSB (index 8), O=Markt-Telefon (index 14), X=Markt-Mail (index 23)
    out = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        mail = str(row.iloc[23]).strip() if df.shape[1] > 23 and not pd.isna(row.iloc[23]) else ""
        if csb:
            out[csb] = {"name": fach, "telefon": tel, "email_market": mail}
    return out

def to_data_url(file) -> str:
    mime = file.type or ("image/png" if file.name.lower().endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(file.read()).decode("utf-8")

if excel_file and key_file:
    if st.button("HTML erzeugen", type="primary"):
        if logo_file is None:
            st.error("Bitte Logo (PNG/JPG) hochladen.")
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
                with st.spinner("Lese Fachberater-Telefonliste..."):
                    berater_file.seek(0)
                    bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                    bf = bf.rename(columns={0:"Vorname",1:"Nachname",2:"Nummer"}).dropna(how="all")
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("Lese Fachberater–CSB-Zuordnung..."):
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
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="suche.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
