import streamlit as st
import pandas as pd
import json
import base64
import unicodedata
import re

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

  --pill-yellow-bg:#fff3b0; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#4a3001;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#ffe4e6;   --pill-red-bd:#fb7185;  --pill-red-tx:#7f1d1d;

  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;

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
.container{width:100%; max-width:1480px}
.card{background:var(--surface); border:1px solid var(--grid); border-radius:8px; overflow:hidden}

/* Header */
.header{
  padding:10px 12px;
  background:linear-gradient(180deg,#ffffff 0%, #f4f7fe 100%);
  color:#0b1226; display:flex; align-items:center; justify-content:center; gap:10px;
  border-bottom:1px solid var(--grid);
}
.brand-logo{height:56px; width:auto}
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
.tour-banner{display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0; background:transparent; border:none;}
.tour-pill{
  display:inline-flex; align-items:center; gap:10px;
  background:#ffedd5; color:#7c2d12;
  border:2px solid #fb923c; border-radius:999px; padding:8px 14px;
  font-weight:900; font-size:13px; letter-spacing:.2px;
  box-shadow:0 0 0 3px rgba(251,146,60,.18) inset;
}
.tour-stats{font-weight:900; font-size:11px; color:#334155}

/* Tabelle */
.table-section{padding:6px 12px 14px; overflow-x:auto}
table{width:100%; border-collapse:separate; border-spacing:0; table-layout:fixed; font-size:var(--fs-12); min-width:920px}
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

/* Zeilen */
tbody tr:nth-child(odd) td{background:#f8fbff}
tbody tr:nth-child(even) td{background:#ffffff}
tbody tr+tr td{border-top:6px solid var(--row-sep)}
tbody tr:hover td{background:#eef4ff}

/* Zellen */
.cell{display:flex; flex-direction:column; gap:4px; min-height:38px; width:100%}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Monospace Zahlen */
.mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:700}

/* ID-Chips */
a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--pill-yellow-bg); color:var(--pill-yellow-tx);
  border:1.5px solid var(--pill-yellow-bd); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); text-decoration:none; line-height:1;
  box-shadow:0 0 0 2px rgba(245,158,11,.12) inset;
}
a.id-chip:hover{filter:brightness(.97)}
.id-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

/* Schlüssel */
.badge-key{
  display:inline-block; background:var(--pill-green-bg); border:1.5px solid var(--pill-green-bd);
  color:var(--pill-green-tx); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); line-height:1;
  box-shadow:0 0 0 2px rgba(16,185,129,.12) inset;
}

/* Touren */
.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-block; background:var(--pill-red-bg); border:1.5px solid var(--pill-red-bd); color:var(--pill-red-tx);
  padding:3px 9px; border-radius:var(--radius-pill); font-weight:900; font-size:var(--fs-10); cursor:pointer; line-height:1.25; letter-spacing:.15px;
  box-shadow:0 0 0 2px rgba(251,113,133,.12) inset;
}
.tour-btn:hover{filter:brightness(.97)}

/* Telefon-/Mail-Chips */
.phone-col{display:flex; flex-direction:column; gap:6px}
a.phone-chip, a.mail-chip{
  display:inline-flex; align-items:center; gap:6px; border-radius:var(--radius-pill);
  padding:3px 9px; font-weight:900; font-size:var(--fs-11); line-height:1; text-decoration:none; cursor:pointer; width:max-content; max-width:100%;
}
a.phone-chip.chip-fb{background:var(--chip-fb-bg); color:var(--chip-fb-tx); border:1.5px solid var(--chip-fb-bd)}
a.phone-chip.chip-market{background:var(--chip-mk-bg); color:var(--chip-mk-tx); border:1.5px solid var(--chip-mk-bd)}
a.mail-chip{background:#e6f7f4; color:#065f46; border:1.5px solid #10b981; max-width:100%}
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(.97)}
.chip-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}
.mail-chip .txt{white-space:normal; word-break:break-all; line-height:1.2}

/* Adresse-Pill */
a.addr-chip{
  display:inline-flex; align-items:center; gap:8px; max-width:100%;
  background:#e0ecff; color:#0b3a8a; border:1.5px solid #60a5fa; border-radius:999px; padding:4px 10px;
  text-decoration:none; font-weight:900; font-size:var(--fs-11);
}
.addr-chip .txt{white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%}
.addr-dot{width:6px; height:6px; background:#ff2d55; border-radius:999px; display:inline-block}

/* Map-Button */
.table-map{
  text-decoration:none; font-weight:900; font-size:var(--fs-11);
  padding:6px 10px; border-radius:6px; border:1px solid var(--accent);
  background:var(--accent); color:#fff; display:inline-block; text-align:center; letter-spacing:.2px
}
.table-map:hover{background:var(--accent-2); border-color:var(--accent-2)}

/* ========================= */
/*  Portrait-Layout (Cards)  */
/*  -> keine Scrolls nötig   */
/* ========================= */
@media (orientation: portrait) {
  .page{padding:6px}
  .container{max-width:100%}
  .header{padding:8px 10px}
  .brand-logo{height:44px}

  .searchbar{
    position:sticky; top:0; z-index:5;
    grid-template-columns:1fr; gap:6px; padding:8px 10px;
    border-bottom:1px solid var(--grid);
  }

  .tour-wrap{padding:8px 10px 0}
  .tour-pill{padding:6px 10px; font-size:12px}
  .tour-stats{font-size:10px}

  .table-section{padding:6px 8px 10px; overflow:visible}
  table{width:100%; min-width:0; border-spacing:0; table-layout:auto}
  thead{display:none}

  tbody tr{
    display:block;
    border:1px solid var(--grid);
    border-radius:10px;
    background:#fff;
    margin:10px 0;
    overflow:hidden;
  }
  tbody td{
    display:flex;
    gap:10px;
    align-items:flex-start;
    justify-content:space-between;
    padding:8px 10px;
    border:none;
    border-bottom:1px solid var(--grid);
    background:#fff !important;
  }
  tbody td:last-child{border-bottom:none}
  tbody tr+tr td{border-top:none}

  tbody td::before{
    content:attr(data-label);
    font-weight:900;
    color:var(--muted);
    text-transform:uppercase;
    letter-spacing:.35px;
    font-size:10px;
    line-height:1.2;
    margin-right:8px;
    flex:0 0 112px;
    white-space:nowrap;
  }

  .cell{gap:4px; min-height:auto}
  .cell-top,.cell-sub{white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
  .tour-inline{gap:4px}
  .tour-btn{font-size:10px; padding:2px 7px}
  .badge-key{font-size:10px; padding:3px 8px}
  a.phone-chip, a.mail-chip{font-size:10px; padding:3px 8px; max-width:100%}
  .mail-chip .txt{white-space:normal}
  a.addr-chip{font-size:10px; padding:3px 8px; max-width:100%}
}
</style>
</head>
<body>
<div class="page">
  <div class="container">
    <div class="card">
      <div class="header">
        <img class="brand-logo" alt="Logo" src="__LOGO_DATA_URL__">
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
          <span class="tour-pill" id="tourTitle"></span>
          <small class="tour-stats" id="tourExtra"></small>
        </div>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none;">
          <colgroup>
            <col style="width:210px">
            <col style="width:520px">
            <col style="width:260px">
            <col style="width:105px">
            <col style="width:418px">
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
const tourkundenData   = {  };
const keyIndex         = {  };
const beraterIndex     = {  };
const beraterCSBIndex  = {  };

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
function makeMailChip(label, addr){
  if(!addr) return null;
  const a = document.createElement('a');
  a.className = 'mail-chip';
  a.href = `mailto:${addr}`;
  const txt = document.createElement('span'); txt.className='txt mono'; txt.textContent=' '+addr;
  a.append(el('span','chip-tag',label), txt);
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
function fbEmailFromName(name){
  const parts = normalizeNameKey(name).split(' ').filter(Boolean);
  if(parts.length<2) return '';
  const vor = parts[0]; const nach = parts[parts.length-1];
  return `${vor}.${nach}@edeka.de`.replace(/\\s+/g,'');
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
        rec.market_email = (beraterCSBIndex[csb] && beraterCSBIndex[csb].email) ? beraterCSBIndex[csb].email : '';
        map.set(csb, rec);
      }
      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
}

function pushPrevQuery(){ const v=$('#smartSearch').value.trim(); if(v){ prevQuery=v; $('#btnBack').style.display='inline-block'; } }
function popPrevQuery(){ if(prevQuery){ $('#smartSearch').value=prevQuery; prevQuery=null; $('#btnBack').style.display='none'; onSmart(); } }

function makeIdChip(label, value){
  const a=document.createElement('a'); a.className='id-chip'; a.href='javascript:void(0)'; a.title=label+' '+value+' suchen';
  a.addEventListener('click',()=>{ pushPrevQuery(); $('#smartSearch').value=value; onSmart(); });
  a.append(el('span','id-tag',label), el('span','mono',' '+value)); return a;
}
function twoLineCell(top, sub){ const w=el('div','cell'); w.append(el('div','cell-top',top), el('div','cell-sub',sub)); return w; }
function makeAddressChip(name, strasse, plz, ort){
  const txt = `${strasse||''}, ${plz||''} ${ort||''}`.replace(/^,\\s*/, '').trim();
  const url = 'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(`${name||''}, ${txt}`);
  const a = document.createElement('a'); a.className='addr-chip'; a.href=url; a.target='_blank'; a.title='Adresse in Google Maps öffnen (klickbar)';
  a.append(el('span','addr-dot',''), el('span','chip-tag','Adresse'), (()=>{ const s=document.createElement('span'); s.className='txt'; s.textContent=' '+txt; return s; })());
  return a;
}

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = k.csb_nummer||'-', sap=k.sap_nummer||'-', plz=k.postleitzahl||'-';

  // CSB / SAP
  const td1 = document.createElement('td'); td1.setAttribute('data-label', 'CSB / SAP');
  const c1 = el('div','cell');
  const l1 = el('div','cell-top'); l1.appendChild(makeIdChip('CSB', csb));
  const l2 = el('div','cell-sub'); l2.appendChild(makeIdChip('SAP', sap));
  c1.append(l1,l2); td1.append(c1); tr.append(td1);

  // Name / Adresse
  const td2 = document.createElement('td'); td2.setAttribute('data-label', 'Name / Adresse');
  const c2 = el('div','cell');
  c2.append(el('div','cell-top', k.name||'-'));
  const addrPill = makeAddressChip(k.name||'', k.strasse||'', plz, k.ort||'');
  const line2 = el('div','cell-sub'); line2.appendChild(addrPill);
  c2.append(line2);
  td2.append(c2); tr.append(td2);

  // Touren
  const td4 = document.createElement('td'); td4.setAttribute('data-label', 'Touren');
  const c4 = el('div','cell'); const tours=el('div','tour-inline');
  (k.touren||[]).forEach(t=>{
    const tnum=(t.tournummer||'');
    const b=el('span','tour-btn',tnum+' ('+t.liefertag.substring(0,2)+')');
    b.title='Tour '+tnum;
    b.onclick=()=>{ pushPrevQuery(); $('#smartSearch').value=tnum; onSmart(); };
    tours.appendChild(b);
  });
  c4.appendChild(tours); td4.appendChild(c4); tr.append(td4);

  // Schlüssel
  const td5 = document.createElement('td'); td5.setAttribute('data-label', 'Schlüssel');
  const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td5.appendChild(key ? el('span','badge-key',key) : el('span','', '-')); tr.append(td5);

  // Fachberater / Markt
  const td6 = document.createElement('td'); td6.setAttribute('data-label', 'Fachberater / Markt');
  const col=el('div','phone-col');
  const fbPhone = k.fb_phone;
  const fbMail  = k.fachberater ? fbEmailFromName(k.fachberater) : '';
  const mkPhone = k.market_phone;
  const mkMail  = k.market_email || '';
  const p1 = makePhoneChip('FB', fbPhone, 'chip-fb');       if(p1) col.appendChild(p1);
  const m1 = makeMailChip('FB Mail', fbMail);               if(m1) col.appendChild(m1);
  const p2 = makePhoneChip('Markt', mkPhone,'chip-market'); if(p2) col.appendChild(p2);
  const m2 = makeMailChip('Mail', mkMail);                  if(m2) col.appendChild(m2);
  if(!col.childNodes.length) col.textContent='-';
  td6.appendChild(col); tr.append(td6);

  return tr;
}
function renderTable(list){
  const body=$('#tableBody'), tbl=$('#resultTable'); body.innerHTML='';
  if(list.length){ list.forEach(k=>body.appendChild(rowFor(k))); tbl.style.display='table'; } else { tbl.style.display='none'; }
}

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

function onSmart(){
  const qRaw=$('#smartSearch').value.trim(); closeTourTop(); if(!qRaw){ renderTable([]); return; }
  if(/^\\d{1,3}$/.test(qRaw)){ const n=qRaw.replace(/^0+(\\d)/,'$1'); const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n))); renderTourTop(r,n,false); renderTable(r); return; }
  if(/^\\d{4}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1'); const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n)); const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n); const r=dedupByCSB([...tr,...cr]);
    if(tr.length) renderTourTop(tr,n,true); else closeTourTop(); renderTable(r); return;
  }
  const q=normDE(qRaw);
  const r=allCustomers.filter(k=>{ const fb=k.fachberater||''; const text=(k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||'')+' '+(k.market_email||'')); return normDE(text).includes(q); });
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
st.title("Kunden-Suche – Tech-Lab (heller Header, knallige Pills)")
st.caption("Umlaut-Suche • 4-stellig = Tour oder CSB • Schlüssel exakte Suche • Telefon/Mail-Pills klickbar • Adresse-Pill (Google Maps)")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png","jpg","jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Tel, X=Markt-Mail)", type=["xlsx"])

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
    # A = Fachberater, I = CSB, O = Markt-Tel, X = Markt-Mail
    out = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        mail = str(row.iloc[23]).strip() if df.shape[1] > 23 and not pd.isna(row.iloc[23]) else ""
        if csb:
            out[csb] = {"name": fach, "telefon": tel, "email": mail}
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
