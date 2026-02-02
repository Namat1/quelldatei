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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=Inter+Tight:wght@500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f4f6fa;
  --surface:#ffffff;
  --alt:#f8fafc;

  --grid:#d5dde9;
  --grid-2:#c6d0e3;
  --head-grid:#b8c4da;
  --row-sep:#edf2fb;

  --txt:#0b1220;
  --muted:#334155;
  --muted-2:#64748b;

  --accent:#2563eb;
  --accent-2:#1e4fd1;

  --chip-neutral-bg:#f8fafc;
  --chip-neutral-bd:#cbd5e1;
  --chip-neutral-tx:#334155;

  --chip-tour-bg:#ffe4e6;
  --chip-tour-bd:#fb7185;
  --chip-tour-tx:#7f1d1d;

  --chip-key-bg:#dcfce7;
  --chip-key-bd:#22c55e;
  --chip-key-tx:#14532d;

  --chip-addr-bg:#e7f0ff;
  --chip-addr-bd:#7aa7ff;
  --chip-addr-tx:#0b3a8a;

  --shadow-soft:0 1px 0 rgba(15,23,42,.04), 0 8px 24px rgba(15,23,42,.06);

  --radius:10px;
  --radius-pill:999px;
}

*{box-sizing:border-box}
html,body{height:100%}
html, body{ overflow-x:hidden; }

body{
  margin:0;
  background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt);
  font-size:12px;
  line-height:1.35;
  font-weight:650;
  letter-spacing:.05px;
}

.page{min-height:100vh; display:flex; justify-content:center; padding:0}
.container{
  width:1728px;
  max-width:1728px;
  margin:0 auto;
}
.card{
  background:var(--surface);
  border:1px solid var(--grid);
  border-radius:var(--radius);
  overflow:hidden;
  box-shadow:var(--shadow-soft);
}

.header{
  padding:10px 12px;
  background:linear-gradient(180deg,#ffffff 0%, #f5f7ff 100%);
  border-bottom:1px solid var(--grid);
  display:flex; align-items:center; justify-content:center;
}
.brand-logo{height:46px; width:auto}

.searchbar{
  padding:10px 12px;
  display:grid;
  grid-template-columns:1fr 220px auto auto auto;
  gap:8px;
  align-items:center;
  border-bottom:1px solid var(--grid);
  background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr auto} }
@media(max-width:780px){ .searchbar{grid-template-columns:1fr} }

.field{display:grid; grid-template-columns:74px 1fr; gap:6px; align-items:center}
.label{
  font-weight:800;
  color:var(--muted);
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:.32px
}
.input{
  width:100%;
  padding:7px 10px;
  border:1px solid var(--grid);
  border-radius:8px;
  background:#fff;
  font-size:12px;
  font-weight:650;
}
.input:focus{
  outline:none;
  border-color:var(--accent);
  box-shadow:0 0 0 3px rgba(37,99,235,.14);
}

.btn{
  padding:7px 10px;
  border:1px solid var(--grid);
  background:#fff;
  color:#0f172a;
  border-radius:8px;
  cursor:pointer;
  font-weight:800;
  font-size:12px
}
.btn:hover{background:#f3f6fb}
.btn-danger{border-color:#ef4444; background:#ef4444; color:#fff}
.btn-danger:hover{filter:brightness(.95)}
.btn-back{border-color:var(--accent); color:var(--accent-2); background:#eff6ff}
.btn-back:hover{background:#e6f0ff}

.results-meta{
  justify-self:end;
  font-weight:800;
  font-size:11px;
  color:var(--muted-2);
  white-space:nowrap;
}

.table-section{
  padding:6px 12px 14px;
  overflow:visible;
}
table{
  width:100%;
  border-collapse:separate;
  border-spacing:0;
  table-layout:fixed;
  font-size:12px;
  min-width:0;
}

thead th{
  position:sticky; top:0; z-index:2;
  background:linear-gradient(180deg,#f7f9fe,#eef2f8);
  color:#0f172a;
  font-weight:900;
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:.22px;
  border-bottom:2px solid var(--head-grid);
  border-right:1px solid var(--head-grid);
  padding:8px 9px;
  white-space:nowrap;
  text-align:left;
}
thead th:last-child{border-right:none}

tbody td{
  padding:7px 9px;
  vertical-align:top;
  font-weight:650;
  border-bottom:1px solid var(--grid);
  border-right:1px solid var(--grid);
  background:#fff;
  overflow:hidden;
}
tbody td:last-child{border-right:none}

tbody tr:nth-child(odd) td{background:var(--alt)}
tbody tr:nth-child(even) td{background:#ffffff}
tbody tr+tr td{border-top:3px solid var(--row-sep)}
tbody tr:hover td{background:#eff6ff}

.cell{display:flex; flex-direction:column; gap:4px; min-height:36px; width:100%}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:650}

a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--chip-neutral-bg);
  color:var(--chip-neutral-tx);
  border:1px solid var(--chip-neutral-bd);
  border-radius:var(--radius-pill);
  padding:3px 9px;
  font-weight:900;
  font-size:11px;
  text-decoration:none;
  line-height:1;
  box-shadow:none;
}
a.id-chip:hover{filter:brightness(.98)}
.id-tag{font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

.badge-key{
  display:inline-block;
  background:var(--chip-key-bg);
  border:1px solid var(--chip-key-bd);
  color:var(--chip-key-tx);
  border-radius:var(--radius-pill);
  padding:3px 9px;
  font-weight:900;
  font-size:11px;
  line-height:1;
  box-shadow:none;
}

.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-flex;
  align-items:center;
  background:var(--chip-tour-bg);
  border:1px solid var(--chip-tour-bd);
  color:var(--chip-tour-tx);
  padding:3px 9px;
  border-radius:var(--radius-pill);
  font-weight:900;
  font-size:10px;
  cursor:pointer;
  line-height:1.25;
  letter-spacing:.12px;
  box-shadow:none;
}
.tour-btn:hover{filter:brightness(.98)}
.tour-btn .lf{
  margin-left:6px;
  padding:1px 6px;
  border-radius:999px;
  background:#eff6ff;
  border:1px solid #60a5fa;
  color:#1d4ed8;
  font-weight:1000;
  letter-spacing:.2px;
}

.phone-col{display:flex; flex-direction:column; gap:6px}
a.phone-chip, a.mail-chip{
  display:inline-flex; align-items:center; gap:6px;
  border-radius:var(--radius-pill);
  padding:3px 9px;
  font-weight:850;
  font-size:11px;
  line-height:1;
  text-decoration:none;
  cursor:pointer;
  width:max-content;
  max-width:100%;
  border:1px solid var(--grid-2);
  background:#fff;
  color:#0f172a;
}
a.phone-chip.chip-fb{background:#eef6ff; border-color:#bcd3ff; color:#123a7a}
a.phone-chip.chip-market{background:#f3efff; border-color:#d2c6ff; color:#2b1973}
a.mail-chip{ background:#ecfdf5; border-color:#b7f7d6; color:#14532d; max-width:100%; }
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(.98)}
.chip-tag{font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}
.mail-chip .txt{white-space:normal; word-break:break-word; line-height:1.2;}

a.addr-chip{
  display:inline-flex; align-items:center; gap:8px; max-width:100%;
  background:var(--chip-addr-bg);
  color:var(--chip-addr-tx);
  border:1px solid var(--chip-addr-bd);
  border-radius:999px;
  padding:4px 10px;
  text-decoration:none;
  font-weight:800;
  font-size:11px;
}
.addr-chip .txt{white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%}
.addr-dot{width:6px; height:6px; background:#ef4444; border-radius:999px; display:inline-block}

/* ============================== */
/* Tour-Übersicht (UI)            */
/* ============================== */
.tour-summary{
  margin:6px 12px 0;
  border:1px solid var(--grid);
  background:#ffffff;
  border-radius:10px;
  box-shadow:0 1px 0 rgba(15,23,42,.03), 0 6px 16px rgba(15,23,42,.06);
  overflow:hidden;
}
.tour-summary-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  padding:6px 8px;
  border-bottom:1px solid var(--grid);
  background:linear-gradient(180deg,#ffffff 0%, #f7f9fe 100%);
}
.tour-summary-title{
  font-weight:950;
  font-size:10px;
  color:#0f172a;
}
/* Meta bleibt im DOM, aber unsichtbar */
.tour-summary-meta{ display:none !important; }

.tour-summary-actions{ display:flex; align-items:center; gap:6px; }
.print-btn{
  padding:4px 7px;
  border:1px solid #bcd3ff;
  background:#eff6ff;
  color:#1d4ed8;
  border-radius:8px;
  cursor:pointer;
  font-weight:950;
  font-size:10px;
  line-height:1;
}
.print-btn:hover{ background:#e6f0ff; }

/* ✅ Copy Feedback */
.print-btn.ok{
  border-color:#86efac;
  background:#ecfdf5;
  color:#14532d;
}

.tour-summary-tablewrap{ padding:2px 6px 6px; }
.tour-summary-table{
  width:100%;
  border-collapse:separate;
  border-spacing:0;
  table-layout:fixed;
  font-size:9px;
}
.tour-summary-table th{
  text-align:left;
  font-weight:900;
  font-size:8px;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.22px;
  padding:3px 4px;
  border-bottom:1px solid var(--grid);
  background:#f3f6fb;
}
.tour-summary-table td{
  padding:3px 4px;
  border-bottom:1px solid var(--row-sep);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.tour-summary-table tr:last-child td{ border-bottom:none; }
.tour-row{ cursor:pointer; }
.tour-row:hover td{ background:#eff6ff; }

.lf-badge{
  display:inline-flex;
  align-items:center;
  padding:1px 5px;
  border-radius:999px;
  background:#eff6ff;
  border:1px solid #60a5fa;
  color:#1d4ed8;
  font-weight:950;
  font-size:8px;
}

/* ===================== */
/* A4 PRINT STYLES        */
/* ===================== */
@page{
  size: A4 landscape;
  margin: 10mm;
}
@media print{
  html,body{
    background:#fff !important;
    color:#000 !important;
  }
  .page{ display:block !important; }
  .container{ width:auto !important; max-width:none !important; margin:0 !important; }
  .card{
    box-shadow:none !important;
    border:none !important;
    border-radius:0 !important;
    background:#fff !important;
  }

  /* Alles ausblenden, nur Tour-Übersicht drucken */
  .header, .searchbar, .table-section{ display:none !important; }

  /* PRINT: Plain text, größer, KEINE Schatten/Verläufe/Boxen */
  #tourSummary{
    display:block !important;
    margin:0 !important;
    border:none !important;
    border-radius:0 !important;
    box-shadow:none !important;
    background:#fff !important;
  }
  .tour-summary-head{
    border:none !important;
    background:#fff !important;
    padding:0 0 6mm 0 !important;
  }

  /* Buttons nicht drucken */
  .print-btn{ display:none !important; }

  /* Titel groß */
  .tour-summary-title{
    font-size:18px !important;
    font-weight:900 !important;
    color:#000 !important;
  }
  .tour-summary-meta{ display:none !important; }

  /* Tabelle: plain, groß, gut lesbar */
  .tour-summary-tablewrap{ padding:0 !important; }
  .tour-summary-table{
    font-size:14px !important;
    border-collapse:collapse !important;
    table-layout:auto !important;
  }
  .tour-summary-table th,
  .tour-summary-table td{
    padding:6px 6px !important;
    border:1px solid #000 !important;
    background:#fff !important;
    color:#000 !important;
    white-space:normal !important;
    overflow:visible !important;
    text-overflow:clip !important;
  }
  .tour-summary-table th{
    font-size:13px !important;
    font-weight:900 !important;
    text-transform:none !important;
    letter-spacing:0 !important;
  }

  /* LF Badge: plain text */
  .lf-badge{
    border:none !important;
    background:transparent !important;
    color:#000 !important;
    padding:0 !important;
    font-size:14px !important;
    font-weight:900 !important;
  }

  .tour-row:hover td{ background:#fff !important; }

  /* ✅ PRINT: SAP-Spalte ausblenden */
  .tour-summary-table th:nth-child(2),
  .tour-summary-table td:nth-child(2){
    display:none !important; /* SAP */
  }
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

        <div class="results-meta" id="resultsMeta" style="display:none;"></div>
      </div>

      <!-- Tour-Übersicht -->
      <div class="tour-summary" id="tourSummary" style="display:none;">
        <div class="tour-summary-head">
          <div>
            <div class="tour-summary-title" id="tourSummaryTitle"></div>
            <div class="tour-summary-meta" id="tourSummaryMeta"></div>
          </div>
          <div class="tour-summary-actions">
            <button class="print-btn" id="btnCopyTour" title="Tour als Tabelle kopieren (Outlook/Teams/Word)">Kopieren</button>
            <button class="print-btn" id="btnPrintTour" title="Tour-Übersicht drucken (A4)">Drucken</button>
          </div>
        </div>

        <div class="tour-summary-tablewrap">
          <table class="tour-summary-table" id="tourSummaryTable">
            <thead>
              <tr>
                <th>CSB</th>
                <th>SAP</th>
                <th>Name</th>
                <th>Straße</th>
                <th>Ort</th>
                <th id="thLF">LF</th>
              </tr>
            </thead>
            <tbody id="tourSummaryBody"></tbody>
          </table>
        </div>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none;">
          <colgroup>
            <col style="width:14%">
            <col style="width:36%">
            <col style="width:18%">
            <col style="width:7%">
            <col style="width:25%">
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
const winterIndex      = {  };

const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];
let prevQuery = null;
let currentTourNumber = null;

const DIAL_SCHEME = 'callto';

function setResultsMeta(text){
  const m = $('#resultsMeta');
  if(!text){ m.style.display='none'; m.textContent=''; return; }
  m.textContent = text;
  m.style.display='block';
}

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
  if(parts.length >= 2){
    const f=parts[0], l=parts[parts.length-1];
    out.add(`${f} ${l}`);
    out.add(`${l} ${f}`);
  }
  return Array.from(out);
}
function fbEmailFromName(name){
  const parts = normalizeNameKey(name).split(' ').filter(Boolean);
  if(parts.length<2) return '';
  const vor = parts[0];
  const nach = parts[parts.length-1];
  return `${vor}.${nach}@edeka.de`.replace(/\\s+/g,'');
}
function pickBeraterPhone(name){
  if(!name) return '';
  const variants = nameVariants(name);
  for(const v of variants){ if(beraterIndex[v]) return beraterIndex[v]; }
  const keys = Object.keys(beraterIndex);
  for(const v of variants){
    const parts = v.split(' ').filter(Boolean);
    for(const k of keys){
      if(parts.every(p=>k.includes(p))) return beraterIndex[k];
    }
  }
  return '';
}
function dedupByCSB(list){
  const seen=new Set(), out=[];
  for(const k of list){
    const csb=normalizeDigits(k.csb_nummer);
    if(!seen.has(csb)){ seen.add(csb); out.push(k); }
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
        rec.touren = [];
        rec.schluessel   = normalizeDigits(rec.schluessel) || (keyIndex[csb]||'');

        if (beraterCSBIndex[csb] && beraterCSBIndex[csb].name){
          rec.fachberater = beraterCSBIndex[csb].name;
        }
        rec.fb_phone     = rec.fachberater ? pickBeraterPhone(rec.fachberater) : '';
        rec.market_phone = (beraterCSBIndex[csb] && beraterCSBIndex[csb].telefon) ? beraterCSBIndex[csb].telefon : '';
        rec.market_email = (beraterCSBIndex[csb] && beraterCSBIndex[csb].email) ? beraterCSBIndex[csb].email : '';

        rec.lf_map = (winterIndex[csb] ? winterIndex[csb] : {});
        map.set(csb, rec);
      }

      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
}

function pushPrevQuery(){
  const v=$('#smartSearch').value.trim();
  if(v){
    prevQuery=v;
    $('#btnBack').style.display='inline-block';
  }
}
function popPrevQuery(){
  if(prevQuery){
    $('#smartSearch').value=prevQuery;
    prevQuery=null;
    $('#btnBack').style.display='none';
    onSmart();
  }
}

function makeIdChip(label, value){
  const a=document.createElement('a');
  a.className='id-chip';
  a.href='javascript:void(0)';
  a.title=label+' '+value+' suchen';
  a.addEventListener('click',()=>{
    pushPrevQuery();
    $('#smartSearch').value=value;
    onSmart();
  });
  a.append(el('span','id-tag',label), el('span','mono',' '+value));
  return a;
}

function makeAddressChip(name, strasse, plz, ort){
  const txt = `${strasse||''}, ${plz||''} ${ort||''}`.replace(/^,\\s*/, '').trim();
  const url = 'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(`${name||''}, ${txt}`);
  const a = document.createElement('a');
  a.className='addr-chip';
  a.href=url;
  a.target='_blank';
  a.title='Adresse in Google Maps öffnen (klickbar)';
  a.append(
    el('span','addr-dot',''),
    el('span','chip-tag','Adresse'),
    (()=>{ const s=document.createElement('span'); s.className='txt'; s.textContent=' '+txt; return s; })()
  );
  return a;
}

function closeTourSummary(){
  $('#tourSummary').style.display='none';
  $('#tourSummaryTitle').textContent='';
  $('#tourSummaryMeta').textContent='';
  $('#tourSummaryBody').innerHTML='';
  currentTourNumber = null;
}

function lfSortKey(lf){
  if(!lf) return 999999;
  const m = String(lf).match(/(\\d+)/);
  return m ? parseInt(m[1],10) : 999999;
}

/* Titel: nur Tournummer + Wochentag(e) */
function renderTourSummary(list, tour){
  const wrap = $('#tourSummary');
  const body = $('#tourSummaryBody');
  body.innerHTML = '';

  if(!list || !list.length){
    closeTourSummary();
    return;
  }

  currentTourNumber = String(tour).trim();

  // Wochentag(e) für diese Tour
  const daySet = new Set();
  for(const k of list){
    for(const t of (k.touren||[])){
      if(String(t.tournummer||'').trim() === String(tour).trim()){
        if(t.liefertag) daySet.add(String(t.liefertag).trim());
      }
    }
  }
  const dayOrder = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"];
  const days = Array.from(daySet).sort((a,b)=>dayOrder.indexOf(a)-dayOrder.indexOf(b));
  const dayLabel = days.length ? days.join("/") : "";

  $('#tourSummaryTitle').textContent = dayLabel ? `${tour} – ${dayLabel}` : `${tour}`;
  $('#tourSummaryMeta').textContent  = "";

  const sorted = [...list].sort((a,b)=>{
    const lfa = (a.lf_map && a.lf_map[tour]) ? a.lf_map[tour] : '';
    const lfb = (b.lf_map && b.lf_map[tour]) ? b.lf_map[tour] : '';
    const ka = lfSortKey(lfa);
    const kb = lfSortKey(lfb);
    if(ka !== kb) return ka - kb;
    return (a.name||'').localeCompare((b.name||''), 'de');
  });

  for(const k of sorted){
    const tr = document.createElement('tr');
    tr.className = 'tour-row';
    tr.title = 'Klicken: CSB '+(k.csb_nummer||'')+' suchen';
    tr.addEventListener('click', ()=>{
      pushPrevQuery();
      $('#smartSearch').value = (k.csb_nummer||'').toString();
      onSmart();
      window.scrollTo({top:0, behavior:'smooth'});
    });

    const csb  = (k.csb_nummer||'-');
    const sap  = (k.sap_nummer||'-');
    const name = (k.name||'-');
    const str  = (k.strasse||'-');
    const ort  = (k.ort||'-');
    const lf   = (k.lf_map && k.lf_map[tour]) ? String(k.lf_map[tour]).trim() : '';

    const td1=document.createElement('td'); td1.textContent=csb;
    const td2=document.createElement('td'); td2.textContent=sap;
    const td3=document.createElement('td'); td3.textContent=name;
    const td4=document.createElement('td'); td4.textContent=str;
    const td5=document.createElement('td'); td5.textContent=ort;

    const td6=document.createElement('td');
    if(lf){
      const s=document.createElement('span');
      s.className='lf-badge';
      s.textContent=lf;
      td6.appendChild(s);
    } else {
      td6.textContent='-';
    }

    tr.append(td1,td2,td3,td4,td5,td6);
    body.appendChild(tr);
  }

  wrap.style.display='block';
}

/* ===================== */
/* COPY: echte Tabelle (text/html + text/plain fallback) */
/* - ULTRA klein, andere Schrift (Arial Narrow/Calibri)  */
/* - SAP mit drin                                        */
/* ===================== */

function cleanCell(s){
  return String(s ?? '')
    .replace(/\\r?\\n/g,' ')
    .replace(/\\t/g,' ')
    .replace(/\\s+/g,' ')
    .trim();
}

function escapeHtml(s){
  return String(s ?? '')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;')
    .replace(/'/g,'&#039;');
}

function buildTourClipboardHTML(){
  const title = ($('#tourSummaryTitle').textContent || '').trim();
  const rows  = Array.from(document.querySelectorAll('#tourSummaryBody tr'));

  const data = [];
  for(const tr of rows){
    const tds = tr.querySelectorAll('td');
    if(!tds || tds.length < 6) continue;

    data.push({
      csb:  cleanCell(tds[0].textContent),
      sap:  cleanCell(tds[1].textContent),
      name: cleanCell(tds[2].textContent),
      str:  cleanCell(tds[3].textContent),
      ort:  cleanCell(tds[4].textContent),
      lf:   cleanCell(tds[5].textContent),
    });
  }

  const fontStack = "'Arial Narrow', Calibri, Arial, Tahoma, sans-serif";

  // ✅ ULTRA kompakt (Office): pt statt px, sehr wenig Padding, sehr dünne Linien
  const html = `
<div style="font-family:${fontStack};
            font-size:6pt; line-height:1.0;
            mso-line-height-rule:exactly;
            -webkit-text-size-adjust:100%;">
  <div style="font-weight:700;margin:0 0 2px 0;font-size:6pt;">
    Tour ${escapeHtml(title)}
  </div>

  <table style="border-collapse:collapse;border:0.25pt solid #222;
                font-family:${fontStack};
                font-size:6pt; line-height:1.0;">
    <thead>
      <tr>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;white-space:nowrap;">CSB</th>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;white-space:nowrap;">SAP</th>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;">Name</th>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;">Straße</th>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;">Ort</th>
        <th style="border:0.25pt solid #222;padding:0.25pt 1.5pt;text-align:left;background:#f2f2f2;white-space:nowrap;">Ladefolge</th>
      </tr>
    </thead>
    <tbody>
      ${data.map(r => `
        <tr>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;white-space:nowrap;">${escapeHtml(r.csb)}</td>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;white-space:nowrap;">${escapeHtml(r.sap)}</td>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;">${escapeHtml(r.name)}</td>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;">${escapeHtml(r.str)}</td>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;">${escapeHtml(r.ort)}</td>
          <td style="border:0.25pt solid #222;padding:0.25pt 1.5pt;white-space:nowrap;">${escapeHtml(r.lf)}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
</div>`.trim();

  return html;
}

function buildTourClipboardPlain(){
  const title = ($('#tourSummaryTitle').textContent || '').trim();
  const rows  = Array.from(document.querySelectorAll('#tourSummaryBody tr'));

  let out = `Tour\\t${title}\\nCSB\\tSAP\\tName\\tStraße\\tOrt\\tLadefolge\\n`;
  for(const tr of rows){
    const tds = tr.querySelectorAll('td');
    if(!tds || tds.length < 6) continue;
    const csb  = cleanCell(tds[0].textContent);
    const sap  = cleanCell(tds[1].textContent);
    const name = cleanCell(tds[2].textContent);
    const str  = cleanCell(tds[3].textContent);
    const ort  = cleanCell(tds[4].textContent);
    const lf   = cleanCell(tds[5].textContent);
    out += `${csb}\\t${sap}\\t${name}\\t${str}\\t${ort}\\t${lf}\\n`;
  }
  return out.trim();
}

async function copyTourTableToClipboard(){
  const html = buildTourClipboardHTML();
  const text = buildTourClipboardPlain();

  try{
    if(navigator.clipboard && window.isSecureContext && window.ClipboardItem){
      const item = new ClipboardItem({
        "text/html": new Blob([html], { type: "text/html" }),
        "text/plain": new Blob([text], { type: "text/plain" }),
      });
      await navigator.clipboard.write([item]);
      return true;
    }
  }catch(e){}

  try{
    if(navigator.clipboard && window.isSecureContext){
      await navigator.clipboard.writeText(text);
      return true;
    }
  }catch(e){}

  try{
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly','');
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    return ok;
  }catch(e){
    return false;
  }
}

async function onCopyTour(){
  if($('#tourSummary').style.display==='none') return;

  const btn = $('#btnCopyTour');
  const oldText = btn.textContent;

  const ok = await copyTourTableToClipboard();

  if(ok){
    btn.textContent = 'Kopiert ✓';
    btn.classList.add('ok');
  }else{
    btn.textContent = 'Kopieren fehlgeschlagen';
  }

  setTimeout(()=>{
    btn.textContent = oldText;
    btn.classList.remove('ok');
  }, 1200);
}

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = k.csb_nummer||'-';
  const sap = k.sap_nummer||'-';
  const plz = k.postleitzahl||'-';

  const td1 = document.createElement('td'); td1.setAttribute('data-label', 'CSB / SAP');
  const c1 = el('div','cell');
  const l1 = el('div','cell-top'); l1.appendChild(makeIdChip('CSB', csb));
  const l2 = el('div','cell-sub'); l2.appendChild(makeIdChip('SAP', sap));
  c1.append(l1,l2); td1.append(c1); tr.append(td1);

  const td2 = document.createElement('td'); td2.setAttribute('data-label', 'Name / Adresse');
  const c2 = el('div','cell');
  c2.append(el('div','cell-top', k.name||'-'));
  const addrPill = makeAddressChip(k.name||'', k.strasse||'', plz, k.ort||'');
  const line2 = el('div','cell-sub'); line2.appendChild(addrPill);
  c2.append(line2);
  td2.append(c2); tr.append(td2);

  const td4 = document.createElement('td'); td4.setAttribute('data-label', 'Touren');
  const c4 = el('div','cell');
  const tours = el('div','tour-inline');

  const lfMap = k.lf_map || {};

  (k.touren||[]).forEach(t=>{
    const tnum = (t.tournummer||'').toString().trim();
    const day  = (t.liefertag||'').substring(0,2);
    const lf   = (lfMap[tnum] || '').toString().trim();

    const b = document.createElement('span');
    b.className = 'tour-btn';
    b.appendChild(document.createTextNode(`${tnum} (${day})`));

    if(lf){
      const lfSpan = document.createElement('span');
      lfSpan.className = 'lf';
      lfSpan.textContent = lf;
      b.appendChild(lfSpan);
    }

    b.title='Tour '+tnum;
    b.onclick=()=>{
      pushPrevQuery();
      $('#smartSearch').value=tnum;
      onSmart();
      window.scrollTo({top:0, behavior:'smooth'});
    };
    tours.appendChild(b);
  });

  c4.appendChild(tours);
  td4.appendChild(c4);
  tr.append(td4);

  const td5 = document.createElement('td'); td5.setAttribute('data-label', 'Schlüssel');
  const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td5.appendChild(key ? el('span','badge-key',key) : el('span','', '-'));
  tr.append(td5);

  const td6 = document.createElement('td'); td6.setAttribute('data-label', 'Fachberater / Markt');
  const col=el('div','phone-col');
  const fbPhone = k.fb_phone;
  const fbMail  = k.fachberater ? fbEmailFromName(k.fachberater) : '';
  const mkPhone = k.market_phone;
  const mkMail  = k.market_email || '';

  const p1 = makePhoneChip('FB', fbPhone, 'chip-fb');        if(p1) col.appendChild(p1);
  const m1 = makeMailChip('FB Mail', fbMail);                if(m1) col.appendChild(m1);
  const p2 = makePhoneChip('Markt', mkPhone,'chip-market');  if(p2) col.appendChild(p2);
  const m2 = makeMailChip('Mail', mkMail);                   if(m2) col.appendChild(m2);
  if(!col.childNodes.length) col.textContent='-';
  td6.appendChild(col); tr.append(td6);

  return tr;
}

function renderTable(list){
  const body=$('#tableBody');
  const tbl=$('#resultTable');
  body.innerHTML='';
  if(list.length){
    list.forEach(k=>body.appendChild(rowFor(k)));
    tbl.style.display='table';
    setResultsMeta(list.length+' Treffer');
  } else {
    tbl.style.display='none';
    setResultsMeta('');
  }
}

function onSmart(){
  const qRaw=$('#smartSearch').value.trim();
  closeTourSummary();

  if(!qRaw){ renderTable([]); return; }

  if(/^\\d{1,3}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1');
    const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n)));
    renderTable(r);
    return;
  }

  if(/^\\d{4}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1');
    const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n));
    const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n);
    const r=dedupByCSB([...tr,...cr]);

    if(tr.length){
      renderTourSummary(tr, n);
    }
    renderTable(r);
    return;
  }

  const q=normDE(qRaw);
  const r=allCustomers.filter(k=>{
    const fb=k.fachberater||'';
    const text=(k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||'')+' '+(k.market_email||''));
    return normDE(text).includes(q);
  });
  renderTable(r);
}

function onKey(){
  const q=$('#keySearch').value.trim();
  closeTourSummary();

  if(!q){ renderTable([]); return; }

  const n=q.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
  const r=[];
  for(const k of allCustomers){
    const key=(k.schluessel||'')||(keyIndex[k.csb_nummer]||'');
    if(key===n) r.push(k);
  }
  renderTable(r);
}

function debounce(fn,d=140){
  let t;
  return (...a)=>{
    clearTimeout(t);
    t=setTimeout(()=>fn(...a),d);
  };
}

/* ✅ Druck-spezifische Headline-Umbenennung */
function setPrintHeaders(){
  const th = document.getElementById('thLF');
  if(!th) return;
  const screenText = 'LF';
  const printText  = 'Ladefolge';

  const beforePrint = ()=>{ th.textContent = printText; };
  const afterPrint  = ()=>{ th.textContent = screenText; };

  window.addEventListener('beforeprint', beforePrint);
  window.addEventListener('afterprint', afterPrint);
}

document.addEventListener('DOMContentLoaded', ()=>{
  if(Object.keys(tourkundenData).length>0){ buildData(); }
  setPrintHeaders();

  $('#smartSearch').addEventListener('input', debounce(onSmart,140));
  $('#keySearch').addEventListener('input', debounce(onKey,140));

  $('#btnReset').addEventListener('click', ()=>{
    $('#smartSearch').value='';
    $('#keySearch').value='';
    closeTourSummary();
    renderTable([]);
    prevQuery=null;
    $('#btnBack').style.display='none';
  });

  $('#btnBack').addEventListener('click', ()=>{ popPrevQuery(); });

  $('#btnCopyTour').addEventListener('click', onCopyTour);

  $('#btnPrintTour').addEventListener('click', ()=>{
    if($('#tourSummary').style.display==='none'){ return; }
    window.print();
  });

  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape'){
      $('#btnReset').click();
    }
    if(e.key === 'Enter'){
      const a = document.activeElement;
      if(a && (a.id==='smartSearch' || a.id==='keySearch')){
        onSmart();
        onKey();
      }
    }
  });
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("Kunden-Suche – V2 (Dispo UI, FIX 1728px ohne horizontal Scroll)")
st.caption("Druck: SAP-Spalte weg • LF-Header im Druck = „Ladefolge“ • Kopieren: echte HTML-Tabelle (Arial Narrow/Calibri, 6pt) + TSV Fallback.")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Tel, X=Markt-Mail)", type=["xlsx"])


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
    x = s.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\ufeff", "")
    x = x.replace("\u00A0", " ").replace("–", "-").replace("—", "-").lower()
    x = x.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
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
        if csb:
            out[csb] = key
    return out


def build_berater_map(df: pd.DataFrame) -> dict:
    out = {}
    for _, row in df.iterrows():
        v = ("" if df.shape[1] < 1 or pd.isna(row.iloc[0]) else str(row.iloc[0])).strip()
        n = ("" if df.shape[1] < 2 or pd.isna(row.iloc[1]) else str(row.iloc[1])).strip()
        t = ("" if df.shape[1] < 3 or pd.isna(row.iloc[2]) else str(row.iloc[2])).strip()
        if not t:
            continue
        k1 = norm_de_py(f"{v} {n}")
        k2 = norm_de_py(f"{n} {v}")
        for k in {k1, k2}:
            if k and k not in out:
                out[k] = t
    return out


def build_berater_csb_map(df: pd.DataFrame) -> dict:
    out = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        mail = str(row.iloc[23]).strip() if df.shape[1] > 23 and not pd.isna(row.iloc[23]) else ""
        if csb:
            out[csb] = {"name": fach, "telefon": tel, "email": mail}
    return out


def format_lf(v) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip().replace(".0", "")
    if not s:
        return ""
    if s.isdigit():
        return f"LF{int(s)}"
    s2 = s.replace(" ", "").upper()
    if s2.startswith("LF"):
        return s2
    return s


def build_winter_map(excel_file_obj) -> dict:
    out = {}
    try:
        dfw = pd.read_excel(excel_file_obj, sheet_name="Mo-Sa Winter")
    except Exception:
        return out

    # Spalte B: Tour (idx 1), Spalte C: LA.F (idx 2), Spalte D: KD.NR (idx 3)
    for _, row in dfw.iterrows():
        kd = normalize_digits_py(row.iloc[3] if len(row) > 3 else "")
        tour = normalize_digits_py(row.iloc[1] if len(row) > 1 else "")
        lf = format_lf(row.iloc[2] if len(row) > 2 else "")

        if not kd or not tour or not lf:
            continue

        out.setdefault(kd, {})[tour] = lf
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
            "csb_nummer": "Nr",
            "sap_nummer": "SAP-Nr.",
            "name": "Name",
            "strasse": "Strasse",
            "postleitzahl": "Plz",
            "ort": "Ort",
            "fachberater": "Fachberater"
        }
        LIEFERTAGE_MAPPING = {
            "Montag": "Mo",
            "Dienstag": "Die",
            "Mittwoch": "Mitt",
            "Donnerstag": "Don",
            "Freitag": "Fr",
            "Samstag": "Sam"
        }

        try:
            with st.spinner("Lese Schlüsseldatei..."):
                key_file.seek(0)
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
                    bf = bf.rename(columns={0: "Vorname", 1: "Nachname", 2: "Nummer"}).dropna(how="all")
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("Lese Fachberater–CSB-Zuordnung..."):
                    berater_csb_file.seek(0)
                    try:
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=0)
                    except Exception:
                        berater_csb_file.seek(0)
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=None)
                    berater_csb_map = build_berater_csb_map(bcf)

            with st.spinner("Lese Ladefolgen (Mo-Sa Winter)..."):
                excel_file.seek(0)
                winter_map = build_winter_map(excel_file)

            tour_dict = {}

            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns:
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace(".", "", 1).isdigit():
                            continue

                        tournr = normalize_digits_py(tournr_raw)

                        entry = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean = normalize_digits_py(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        entry["csb_nummer"] = csb_clean
                        entry["sap_nummer"] = normalize_digits_py(entry.get("sap_nummer", ""))
                        entry["postleitzahl"] = normalize_digits_py(entry.get("postleitzahl", ""))
                        entry["schluessel"] = key_map.get(csb_clean, "")
                        entry["liefertag"] = tag

                        if csb_clean and csb_clean in berater_csb_map and berater_csb_map[csb_clean].get("name"):
                            entry["fachberater"] = berater_csb_map[csb_clean]["name"]

                        tour_dict.setdefault(tournr, []).append(entry)

            with st.spinner("Verarbeite Kundendatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        excel_file.seek(0)
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(
                tour_dict.items(),
                key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0
            ))

            final_html = (
                HTML_TEMPLATE
                .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
                .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
                .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
                .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
                .replace("const winterIndex      = {  }", f"const winterIndex      = {json.dumps(winter_map, ensure_ascii=False)}")
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
