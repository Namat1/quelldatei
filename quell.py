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
  /* =========================
     V3 DISPO THEME (ruhig, klar)
     + 90% von 1920px (max 1728)
     + Darkmode Toggle
     ========================= */

  /* LIGHT (Default) */
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

  /* Chips */
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

  --fs-10:10px; --fs-11:11px; --fs-12:12px;
}

/* DARK overrides via [data-theme="dark"] */
:root[data-theme="dark"]{
  --bg:#0b1220;
  --surface:#0f172a;
  --alt:#0c152b;

  --grid:#22304b;
  --grid-2:#2a3a5a;
  --head-grid:#2f446b;
  --row-sep:#0a1224;

  --txt:#e5e7eb;
  --muted:#cbd5e1;
  --muted-2:#94a3b8;

  --accent:#60a5fa;
  --accent-2:#93c5fd;

  --chip-neutral-bg:#0b1730;
  --chip-neutral-bd:#2a3a5a;
  --chip-neutral-tx:#cbd5e1;

  --chip-tour-bg:#2a0f18;
  --chip-tour-bd:#fb7185;
  --chip-tour-tx:#fecdd3;

  --chip-key-bg:#052214;
  --chip-key-bd:#22c55e;
  --chip-key-tx:#bbf7d0;

  --chip-addr-bg:#0b1730;
  --chip-addr-bd:#3b82f6;
  --chip-addr-tx:#bfdbfe;

  --shadow-soft:0 1px 0 rgba(0,0,0,.22), 0 14px 30px rgba(0,0,0,.28);
}

*{box-sizing:border-box}
html,body{height:100%}
html,body{overflow-x:hidden} /* Safety: niemals horizontal scroll */

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

/* Frame: 90% von 1920 (= max 1728) */
.page{min-height:100vh; display:flex; justify-content:center; padding:0}
.container{
  width:90vw;
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

/* Header */
.header{
  padding:10px 12px;
  background:linear-gradient(180deg, color-mix(in srgb, var(--surface) 92%, #ffffff 8%) 0%, color-mix(in srgb, var(--surface) 72%, #93c5fd 6%) 100%);
  border-bottom:1px solid var(--grid);
  display:flex; align-items:center; justify-content:center;
}
.brand-logo{height:46px; width:auto}

/* Searchbar */
.searchbar{
  padding:10px 12px;
  display:grid;
  grid-template-columns:1fr 220px auto auto auto auto;
  gap:8px;
  align-items:center;
  border-bottom:1px solid var(--grid);
  background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr auto auto} }
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
  background:color-mix(in srgb, var(--surface) 92%, #ffffff 8%);
  color:var(--txt);
  font-size:12px;
  font-weight:650;
}
.input:focus{
  outline:none;
  border-color:var(--accent);
  box-shadow:0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent);
}

/* Buttons */
.btn{
  padding:7px 10px;
  border:1px solid var(--grid);
  background:color-mix(in srgb, var(--surface) 86%, #ffffff 14%);
  color:var(--txt);
  border-radius:8px;
  cursor:pointer;
  font-weight:800;
  font-size:12px
}
.btn:hover{filter:brightness(1.03)}
:root[data-theme="dark"] .btn:hover{filter:brightness(1.08)}
.btn-danger{border-color:#ef4444; background:#ef4444; color:#fff}
.btn-danger:hover{filter:brightness(.95)}
.btn-back{border-color:var(--accent); color:var(--accent-2); background:color-mix(in srgb, var(--accent) 12%, var(--surface))}
.btn-back:hover{filter:brightness(1.02)}

/* Darkmode Toggle Button */
.btn-toggle{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  white-space:nowrap;
}
.toggle-dot{
  width:10px; height:10px; border-radius:999px;
  background:var(--muted-2);
  box-shadow:0 0 0 3px color-mix(in srgb, var(--muted-2) 14%, transparent);
}
:root[data-theme="dark"] .toggle-dot{
  background:var(--accent);
  box-shadow:0 0 0 3px color-mix(in srgb, var(--accent) 16%, transparent);
}
.toggle-label{
  font-weight:900;
  font-size:11px;
  letter-spacing:.25px;
  text-transform:uppercase;
  color:var(--muted);
}
:root[data-theme="dark"] .toggle-label{color:var(--muted)}

.results-meta{
  justify-self:end;
  font-weight:800;
  font-size:11px;
  color:var(--muted-2);
  white-space:nowrap;
}

/* Tour-Statusleiste */
.tour-wrap{
  display:none;
  padding:10px 12px;
  background:color-mix(in srgb, #ffedd5 84%, var(--surface));
  border-bottom:1px solid color-mix(in srgb, #fdba74 70%, var(--grid));
}
.tour-banner{display:flex; align-items:center; justify-content:space-between; gap:12px}
.tour-pill{
  display:inline-flex; align-items:center; gap:10px;
  background:color-mix(in srgb, #ffedd5 86%, var(--surface));
  color:color-mix(in srgb, #7c2d12 85%, var(--txt));
  border:1px solid #fdba74;
  border-radius:999px;
  padding:7px 12px;
  font-weight:900;
  font-size:12px;
  box-shadow:none;
}
.tour-stats{font-weight:800; font-size:11px; color:var(--muted-2)}

/* Tabelle (kein overflow-x Container) */
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

/* Sticky Header */
thead th{
  position:sticky; top:0; z-index:2;
  background:linear-gradient(180deg, color-mix(in srgb, var(--surface) 75%, #ffffff 25%), color-mix(in srgb, var(--surface) 82%, #93c5fd 6%));
  color:var(--txt);
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
  background:var(--surface);
  overflow:hidden;
}
tbody td:last-child{border-right:none}

/* Zeilen */
tbody tr:nth-child(odd) td{background:var(--alt)}
tbody tr:nth-child(even) td{background:var(--surface)}
tbody tr+tr td{border-top:3px solid var(--row-sep)}
tbody tr:hover td{background:color-mix(in srgb, var(--accent) 12%, var(--surface))}

/* Zellen */
.cell{display:flex; flex-direction:column; gap:4px; min-height:36px; width:100%}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Monospace Zahlen */
.mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:650}

/* ID-Chips */
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
a.id-chip:hover{filter:brightness(1.03)}
.id-tag{font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

/* Schlüssel */
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

/* Touren */
.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-block;
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
.tour-btn:hover{filter:brightness(1.03)}

/* Telefon-/Mail */
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
  background:color-mix(in srgb, var(--surface) 92%, #ffffff 8%);
  color:var(--txt);
}
a.phone-chip.chip-fb{background:color-mix(in srgb, #eef6ff 55%, var(--surface)); border-color:color-mix(in srgb, #bcd3ff 65%, var(--grid-2)); color:color-mix(in srgb, #123a7a 75%, var(--txt))}
a.phone-chip.chip-market{background:color-mix(in srgb, #f3efff 55%, var(--surface)); border-color:color-mix(in srgb, #d2c6ff 65%, var(--grid-2)); color:color-mix(in srgb, #2b1973 75%, var(--txt))}
a.mail-chip{background:color-mix(in srgb, #ecfdf5 55%, var(--surface)); border-color:color-mix(in srgb, #b7f7d6 65%, var(--grid-2)); color:color-mix(in srgb, #14532d 75%, var(--txt)); max-width:100%}
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(1.04)}
.chip-tag{font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

/* WICHTIG: E-Mails dürfen nicht die Tabelle verbreitern */
.mail-chip .txt{
  white-space:normal;
  word-break:break-word;
  line-height:1.2;
}

/* Adresse-Pill */
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

/* ========================= */
/* Portrait full-width cards  */
/* ========================= */
@media (orientation: portrait) {
  body{ font-size:11px; }
  .container{ max-width:none; width:100% }
  .card{ border-left:none; border-right:none; border-radius:0; box-shadow:none }

  .header{
    padding:8px max(12px, env(safe-area-inset-right))
             8px max(12px, env(safe-area-inset-left));
  }
  .brand-logo{ height:38px }

  .searchbar{
    position:sticky; top:0; z-index:5;
    grid-template-columns:1fr;
    gap:6px;
    padding:8px max(12px, env(safe-area-inset-right))
            8px max(12px, env(safe-area-inset-left));
    border-bottom:1px solid var(--grid);
    background:var(--surface);
  }
  .results-meta{ justify-self:start; }

  .label{ font-size:10px }
  .input{ padding:6px 8px; font-size:11px }
  .btn{ padding:6px 8px; font-size:11px }

  .tour-wrap{
    padding:8px max(12px, env(safe-area-inset-right))
            8px max(12px, env(safe-area-inset-left));
  }
  .tour-banner{ gap:8px }
  .tour-pill{ padding:5px 10px; font-size:11px }
  .tour-stats{ font-size:10px }

  .table-section{
    padding:8px max(12px, env(safe-area-inset-right))
            12px max(12px, env(safe-area-inset-left));
    overflow:visible;
  }
  table{ width:100%; min-width:0; border-spacing:0; table-layout:auto }
  thead{ display:none }

  tbody tr{
    display:block;
    margin:10px 0;
    background:var(--surface);
    border:1px solid var(--grid);
    border-radius:12px;
    box-shadow:0 1px 0 rgba(0,0,0,.02);
    overflow:hidden;
  }
  tbody tr:nth-child(odd) td,
  tbody tr:nth-child(even) td{ background:var(--surface) }
  tbody tr+tr td{ border-top:none }

  tbody td{
    display:flex;
    gap:10px;
    align-items:flex-start;
    justify-content:space-between;
    padding:8px 10px;
    border:none;
    border-bottom:1px solid var(--grid);
    overflow:visible;
  }
  tbody td:last-child{ border-bottom:none }

  tbody td::before{
    content:attr(data-label);
    flex:0 0 96px;
    margin-right:8px;
    white-space:nowrap;
    font-weight:900;
    color:var(--muted);
    text-transform:uppercase;
    letter-spacing:.3px;
    font-size:10px;
    line-height:1.2;
  }

  .cell{ gap:3px; min-height:auto }
  .cell-top,.cell-sub{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis }
  .tour-inline{ gap:4px; row-gap:6px }
  .tour-btn{ font-size:10px; padding:2px 6px; line-height:1.2 }
  .badge-key{ font-size:10px; padding:2px 7px }
  a.phone-chip, a.mail-chip{ font-size:10px; padding:3px 7px; max-width:100%; white-space:normal; line-height:1.25 }
  .mail-chip .txt{ white-space:normal; word-break:break-word }
  a.addr-chip{ font-size:10px; padding:3px 8px; max-width:100%; white-space:normal }
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

        <button class="btn btn-toggle" id="btnTheme" title="Darkmode umschalten">
          <span class="toggle-dot" aria-hidden="true"></span>
          <span class="toggle-label" id="themeLabel">Dark</span>
        </button>

        <button class="btn btn-back" id="btnBack" style="display:none;">Zurück zur Suche</button>
        <button class="btn btn-danger" id="btnReset">Zurücksetzen</button>

        <div class="results-meta" id="resultsMeta" style="display:none;"></div>
      </div>

      <div class="tour-wrap" id="tourWrap">
        <div class="tour-banner">
          <span class="tour-pill" id="tourTitle"></span>
          <small class="tour-stats" id="tourExtra"></small>
        </div>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none;">
          <!-- 1920: Prozent-Spalten (kein horizontal scroll) -->
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

const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];
let prevQuery = null;
const DIAL_SCHEME = 'callto';

/* =========================
   Theme Toggle (persisted)
   ========================= */
const THEME_KEY = 'kunden_suche_theme';

function applyTheme(theme){
  const root = document.documentElement;
  if(theme === 'dark'){
    root.setAttribute('data-theme', 'dark');
    $('#themeLabel').textContent = 'Light';
  }else{
    root.removeAttribute('data-theme');
    $('#themeLabel').textContent = 'Dark';
  }
}

function initTheme(){
  const saved = localStorage.getItem(THEME_KEY);
  if(saved === 'dark' || saved === 'light'){
    applyTheme(saved);
    return;
  }
  // Default: folgt System, aber nur wenn nicht gespeichert
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(prefersDark ? 'dark' : 'light');
}

function toggleTheme(){
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const next = isDark ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem(THEME_KEY, next);
}

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

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = k.csb_nummer||'-';
  const sap = k.sap_nummer||'-';
  const plz = k.postleitzahl||'-';

  /* CSB / SAP */
  const td1 = document.createElement('td'); td1.setAttribute('data-label', 'CSB / SAP');
  const c1 = el('div','cell');
  const l1 = el('div','cell-top'); l1.appendChild(makeIdChip('CSB', csb));
  const l2 = el('div','cell-sub'); l2.appendChild(makeIdChip('SAP', sap));
  c1.append(l1,l2); td1.append(c1); tr.append(td1);

  /* Name / Adresse */
  const td2 = document.createElement('td'); td2.setAttribute('data-label', 'Name / Adresse');
  const c2 = el('div','cell');
  c2.append(el('div','cell-top', k.name||'-'));
  const addrPill = makeAddressChip(k.name||'', k.strasse||'', plz, k.ort||'');
  const line2 = el('div','cell-sub'); line2.appendChild(addrPill);
  c2.append(line2);
  td2.append(c2); tr.append(td2);

  /* Touren */
  const td4 = document.createElement('td'); td4.setAttribute('data-label', 'Touren');
  const c4 = el('div','cell'); const tours=el('div','tour-inline');
  (k.touren||[]).forEach(t=>{
    const tnum=(t.tournummer||'');
    const b=el('span','tour-btn',tnum+' ('+t.liefertag.substring(0,2)+')');
    b.title='Tour '+tnum;
    b.onclick=()=>{
      pushPrevQuery();
      $('#smartSearch').value=tnum;
      onSmart();
    };
    tours.appendChild(b);
  });
  c4.appendChild(tours); td4.appendChild(c4); tr.append(td4);

  /* Schlüssel */
  const td5 = document.createElement('td'); td5.setAttribute('data-label', 'Schlüssel');
  const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td5.appendChild(key ? el('span','badge-key',key) : el('span','', '-'));
  tr.append(td5);

  /* Fachberater / Markt */
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

function renderTourTop(list, query, isExact){
  const wrap=$('#tourWrap'), title=$('#tourTitle'), extra=$('#tourExtra');
  if(!list.length){
    wrap.style.display='none';
    title.textContent='';
    extra.textContent='';
    return;
  }

  if(query.startsWith('Schluessel ')){
    const key=query.replace(/^Schluessel\\s+/, '');
    title.textContent='Schlüssel '+key+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden');
  } else {
    title.textContent=(isExact?('Tour '+query):('Tour-Prefix '+query+'*'))+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden');
  }

  const dayCount={};
  list.forEach(k=>(k.touren||[]).forEach(t=>{
    const tnum=t.tournummer||'';
    const cond=isExact ? (tnum===query) : tnum.startsWith(query.replace('Schluessel ',''));
    if(cond || query.startsWith('Schluessel ')){
      dayCount[t.liefertag]=(dayCount[t.liefertag]||0)+1;
    }
  }));
  extra.textContent=Object.entries(dayCount).sort().map(([d,c])=>d+': '+c).join('  •  ');
  wrap.style.display='block';

  setResultsMeta(title.textContent);
}
function closeTourTop(){
  $('#tourWrap').style.display='none';
  $('#tourTitle').textContent='';
  $('#tourExtra').textContent='';
  setResultsMeta('');
}

function onSmart(){
  const qRaw=$('#smartSearch').value.trim();
  closeTourTop();
  if(!qRaw){ renderTable([]); return; }

  if(/^\\d{1,3}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1');
    const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n)));
    renderTourTop(r,n,false);
    renderTable(r);
    return;
  }

  if(/^\\d{4}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1');
    const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n));
    const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n);
    const r=dedupByCSB([...tr,...cr]);
    if(tr.length) renderTourTop(tr,n,true);
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
  closeTourTop();
  if(!q){ renderTable([]); return; }

  const n=q.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
  const r=[];
  for(const k of allCustomers){
    const key=(k.schluessel||'')||(keyIndex[k.csb_nummer]||'');
    if(key===n) r.push(k);
  }
  if(r.length) renderTourTop(r,'Schluessel '+n,true);
  renderTable(r);
}

function debounce(fn,d=140){
  let t;
  return (...a)=>{
    clearTimeout(t);
    t=setTimeout(()=>fn(...a),d);
  };
}

document.addEventListener('DOMContentLoaded', ()=>{
  initTheme();
  $('#btnTheme').addEventListener('click', toggleTheme);

  if(Object.keys(tourkundenData).length>0){ buildData(); }

  $('#smartSearch').addEventListener('input', debounce(onSmart,140));
  $('#keySearch').addEventListener('input', debounce(onKey,140));

  $('#btnReset').addEventListener('click', ()=>{
    $('#smartSearch').value='';
    $('#keySearch').value='';
    closeTourTop();
    renderTable([]);
    prevQuery=null;
    $('#btnBack').style.display='none';
  });

  $('#btnBack').addEventListener('click', ()=>{ popPrevQuery(); });

  /* Dispo-Flow: ESC reset, ENTER sucht */
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
    // Optional: Taste "D" toggelt Theme (nur wenn kein Input fokus)
    if((e.key === 'd' || e.key === 'D') && document.activeElement && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){
      toggleTheme();
    }
  });
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("Kunden-Suche – V3 (Dispo UI, 90% von 1920 + Darkmode)")
st.caption("Ruhiges Dispo-Theme • Darkmode Toggle • 90% Breite (max 1728) • Portrait: Cards • Landscape: Tabelle")

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
                        if spaltenname not in df.columns:
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit():
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
