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
  --accent-hover:#1e40af;

  --pill-yellow-bg:#fff3b0; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#4a3001;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#ffe4e6;   --pill-red-bd:#fb7185;  --pill-red-tx:#7f1d1d;

  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;

  --row-sep:#e6edff;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  --radius:6px; --radius-pill:999px;
  --fs-10:10px; --fs-11:11px; --fs-12:12px;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#0f1419; --surface:#1a1f2e; --alt:#232937;
    --grid:#2d3748; --grid-2:#374151; --head-grid:#4a5568;
    --txt:#e2e8f0; --muted:#a0aec0;
  }
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.35; font-weight:800; letter-spacing:.1px;
  transition: background-color 0.3s ease;
}

/* Loading State */
.loading-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.9); z-index: 9999;
  display: none; align-items: center; justify-content: center;
}
.loading-spinner {
  width: 40px; height: 40px; border: 4px solid var(--grid);
  border-top-color: var(--accent); border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:10px}
.container{width:100%; max-width:1480px}
.card{
  background:var(--surface); 
  border:1px solid var(--grid); 
  border-radius:12px; 
  overflow:hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.2s ease;
}

/* Header */
.header{
  padding:10px 12px;
  background:linear-gradient(180deg,#ffffff 0%, #f4f7fe 100%);
  color:#0b1226; 
  display:flex; 
  align-items:center; 
  justify-content:space-between; 
  gap:10px;
  border-bottom:1px solid var(--grid);
  position: relative;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-logo{height:56px; width:auto; transition: transform 0.2s ease;}
.brand-logo:hover { transform: scale(1.05); }

/* Print Button */
.btn-print {
  padding: 8px 16px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 900;
  font-size: var(--fs-12);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}
.btn-print:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  background: linear-gradient(135deg, var(--accent-hover), var(--accent));
}
.btn-print svg {
  width: 16px;
  height: 16px;
}

/* Searchbar */
.searchbar{
  padding:8px 12px; 
  display:grid; 
  grid-template-columns:1fr 260px auto auto; 
  gap:8px; 
  align-items:center;
  border-bottom:1px solid var(--grid); 
  background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr} }
@media(max-width:680px){ .searchbar{grid-template-columns:1fr} }

.field{display:grid; grid-template-columns:74px 1fr; gap:6px; align-items:center}
.label{
  font-weight:900; 
  color:var(--muted); 
  font-size:var(--fs-11); 
  text-transform:uppercase; 
  letter-spacing:.35px
}
.input{
  width:100%; 
  padding:8px 12px; 
  border:1px solid var(--grid); 
  border-radius:8px; 
  background:#fff;
  font-size:var(--fs-12); 
  font-weight:900;
  transition: all 0.2s ease;
}
.input:focus{
  outline:none; 
  border-color:var(--accent); 
  box-shadow:0 0 0 3px rgba(37,99,235,.12);
  transform: translateY(-1px);
}
.input::placeholder {
  color: #9ca3af;
  font-weight: 600;
}

/* Buttons */
.btn{
  padding:8px 14px; 
  border:1px solid var(--grid); 
  background:#fff; 
  color:#0f172a; 
  border-radius:8px; 
  cursor:pointer; 
  font-weight:900; 
  font-size:var(--fs-12);
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}
.btn:hover{
  background:#f2f5f9;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
.btn:active {
  transform: translateY(0);
}
.btn-danger{
  border-color:#ef4444; 
  background:linear-gradient(135deg, #ef4444, #dc2626); 
  color:#fff
}
.btn-danger:hover{
  background:linear-gradient(135deg, #dc2626, #b91c1c);
}
.btn-back{
  border-color:var(--accent); 
  color:var(--accent-2); 
  background:linear-gradient(135deg, #eef2ff, #e0e7ff);
}
.btn-back:hover{
  background:linear-gradient(135deg, #e0e7ff, #c7d2fe);
}

/* Keyboard Shortcuts */
.kbd-hint {
  font-size: 10px;
  background: rgba(0,0,0,0.1);
  padding: 2px 4px;
  border-radius: 3px;
  margin-left: 4px;
  font-family: monospace;
}

/* Tour-Banner */
.tour-wrap{display:none; padding:10px 12px 0}
.tour-banner{
  display:flex; 
  align-items:center; 
  justify-content:space-between; 
  gap:12px; 
  padding:0; 
  background:transparent; 
  border:none;
  animation: slideDown 0.3s ease;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.tour-pill{
  display:inline-flex; 
  align-items:center; 
  gap:10px;
  background:linear-gradient(135deg, #ffedd5, #fed7aa); 
  color:#7c2d12;
  border:2px solid #fb923c; 
  border-radius:999px; 
  padding:10px 16px;
  font-weight:900; 
  font-size:13px; 
  letter-spacing:.2px;
  box-shadow:0 0 0 3px rgba(251,146,60,.18) inset, var(--shadow-sm);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
.tour-stats{
  font-weight:900; 
  font-size:11px; 
  color:#334155;
  opacity: 0.8;
}

/* Results Count */
.results-count {
  padding: 8px 12px;
  background: linear-gradient(90deg, var(--alt), transparent);
  font-size: var(--fs-11);
  color: var(--muted);
  display: none;
}
.results-count.show {
  display: block;
}

/* Tabelle */
.table-section{padding:6px 12px 14px; position: relative;}
.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
}
table{
  width:100%; 
  border-collapse:separate; 
  border-spacing:0; 
  table-layout:fixed; 
  font-size:var(--fs-12)
}
thead th{
  position:sticky; 
  top:0; 
  z-index:2;
  background:linear-gradient(180deg,#f7f9fe,#eef2f8);
  color:#0f172a; 
  font-weight:900; 
  text-transform:uppercase; 
  letter-spacing:.25px;
  border-bottom:2px solid var(--head-grid); 
  border-right:1px solid var(--head-grid);
  padding:10px 9px; 
  white-space:nowrap; 
  text-align:left;
  transition: background 0.2s ease;
}
thead th:hover {
  background:linear-gradient(180deg,#eef2f8,#e2e8f0);
}
thead th:last-child{border-right:none}
tbody td{
  padding:8px 9px; 
  vertical-align:top; 
  font-weight:800;
  border-bottom:1px solid var(--grid); 
  border-right:1px solid var(--grid);
  background:#fff;
  transition: all 0.15s ease;
}
tbody td:last-child{border-right:none}

/* Zeilenabgrenzung */
tbody tr:nth-child(odd) td{background:#f8fbff}
tbody tr:nth-child(even) td{background:#ffffff}
tbody tr+tr td{border-top:6px solid var(--row-sep)}
tbody tr{
  transition: all 0.2s ease;
}
tbody tr:hover {
  transform: translateX(2px);
}
tbody tr:hover td{
  background:linear-gradient(90deg, #eef4ff, #f0f6ff);
  box-shadow: inset 0 0 0 1px rgba(37,99,235,0.1);
}

/* Zellen */
.cell{display:flex; flex-direction:column; gap:4px; min-height:38px; width:100%}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Monospace Zahlen */
.mono{
  font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; 
  font-weight:700;
  letter-spacing: -0.5px;
}

/* ID-Chips mit Glow-Effect */
a.id-chip{
  display:inline-flex; 
  align-items:center; 
  gap:6px;
  background:linear-gradient(135deg, var(--pill-yellow-bg), #fef3c7); 
  color:var(--pill-yellow-tx);
  border:1.5px solid var(--pill-yellow-bd); 
  border-radius:var(--radius-pill); 
  padding:4px 10px;
  font-weight:900; 
  font-size:var(--fs-11); 
  text-decoration:none; 
  line-height:1;
  box-shadow:0 0 0 2px rgba(245,158,11,.12) inset, var(--shadow-sm);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}
a.id-chip::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: linear-gradient(45deg, transparent, rgba(245,158,11,0.3), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s;
}
a.id-chip:hover::before {
  transform: translateX(100%);
}
a.id-chip:hover{
  transform: translateY(-2px) scale(1.05);
  box-shadow:0 0 0 2px rgba(245,158,11,.2) inset, 0 4px 12px rgba(245,158,11,0.3);
}
.id-tag{
  font-size:var(--fs-10); 
  font-weight:900; 
  text-transform:uppercase; 
  letter-spacing:.35px; 
  opacity:.95
}

/* Schlüssel Badge mit Animation */
.badge-key{
  display:inline-block; 
  background:linear-gradient(135deg, var(--pill-green-bg), #a7f3d0); 
  border:1.5px solid var(--pill-green-bd);
  color:var(--pill-green-tx); 
  border-radius:var(--radius-pill); 
  padding:4px 10px;
  font-weight:900; 
  font-size:var(--fs-11); 
  line-height:1;
  box-shadow:0 0 0 2px rgba(16,185,129,.12) inset, var(--shadow-sm);
  animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

/* Touren mit besseren Hover-Effects */
.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-block; 
  background:linear-gradient(135deg, var(--pill-red-bg), #fecaca); 
  border:1.5px solid var(--pill-red-bd); 
  color:var(--pill-red-tx);
  padding:4px 10px; 
  border-radius:var(--radius-pill); 
  font-weight:900; 
  font-size:var(--fs-10); 
  cursor:pointer; 
  line-height:1.25; 
  letter-spacing:.15px;
  box-shadow:0 0 0 2px rgba(251,113,133,.12) inset, var(--shadow-sm);
  transition: all 0.2s ease;
}
.tour-btn:hover{
  transform: translateY(-2px) scale(1.05);
  box-shadow:0 0 0 2px rgba(251,113,133,.2) inset, 0 4px 8px rgba(251,113,133,0.2);
}

/* Phone/Mail Chips mit Icons */
.phone-col{display:flex; flex-direction:column; gap:6px}
a.phone-chip, a.mail-chip{
  display:inline-flex; 
  align-items:center; 
  gap:6px; 
  border-radius:var(--radius-pill);
  padding:4px 10px; 
  font-weight:900; 
  font-size:var(--fs-11); 
  line-height:1; 
  text-decoration:none; 
  cursor:pointer; 
  width:max-content; 
  max-width:100%;
  transition: all 0.2s ease;
  position: relative;
}
a.phone-chip.chip-fb{
  background:linear-gradient(135deg, var(--chip-fb-bg), #bfdbfe); 
  color:var(--chip-fb-tx); 
  border:1.5px solid var(--chip-fb-bd);
  box-shadow: var(--shadow-sm);
}
a.phone-chip.chip-market{
  background:linear-gradient(135deg, var(--chip-mk-bg), #ddd6fe); 
  color:var(--chip-mk-tx); 
  border:1.5px solid var(--chip-mk-bd);
  box-shadow: var(--shadow-sm);
}
a.mail-chip{
  background:linear-gradient(135deg, #e6f7f4, #a7f3d0); 
  color:#065f46; 
  border:1.5px solid #10b981; 
  max-width:100%;
  box-shadow: var(--shadow-sm);
}
a.phone-chip:hover, a.mail-chip:hover{
  transform: translateY(-2px) scale(1.02);
  box-shadow: var(--shadow-md);
}
a.phone-chip::before, a.mail-chip::before {
  content: '📞';
  font-size: 12px;
  position: absolute;
  left: -20px;
  opacity: 0;
  transition: all 0.2s ease;
}
a.mail-chip::before {
  content: '✉️';
}
a.phone-chip:hover::before, a.mail-chip:hover::before {
  left: 4px;
  opacity: 1;
}
.chip-tag{
  font-size:var(--fs-10); 
  font-weight:900; 
  text-transform:uppercase; 
  letter-spacing:.35px; 
  opacity:.95
}
.mail-chip .txt{
  white-space:normal; 
  word-break:break-all; 
  line-height:1.2
}

/* Adresse-Pill mit Map-Pin Animation */
a.addr-chip{
  display:inline-flex; 
  align-items:center; 
  gap:8px; 
  max-width:100%;
  background:linear-gradient(135deg, #e0ecff, #bfdbfe); 
  color:#0b3a8a; 
  border:1.5px solid #60a5fa; 
  border-radius:999px; 
  padding:5px 12px;
  text-decoration:none; 
  font-weight:900; 
  font-size:var(--fs-11);
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}
a.addr-chip:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 6px 20px rgba(96,165,250,0.3);
}
.addr-chip .txt{
  white-space:nowrap; 
  overflow:hidden; 
  text-overflow:ellipsis; 
  max-width:100%
}
.addr-dot{
  width:6px; 
  height:6px; 
  background:#ff2d55; 
  border-radius:999px; 
  display:inline-block;
  animation: blink 2s infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--muted);
}
.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.3;
}
.empty-text {
  font-size: 16px;
  font-weight: 600;
}

/* Print Styles */
@media print {
  body { background: white; }
  .btn, .btn-print, .btn-back, .btn-danger { display: none !important; }
  .searchbar { display: none !important; }
  .tour-wrap { page-break-after: avoid; }
  .card { box-shadow: none; border: none; }
  .header { 
    background: white; 
    border-bottom: 2px solid #000;
    padding: 20px;
  }
  table { font-size: 10px; }
  tbody tr:hover td { background: inherit !important; }
  a.phone-chip::before, a.mail-chip::before { display: none; }
  .addr-dot { animation: none; }
  @page { 
    size: A4 landscape; 
    margin: 10mm;
  }
}

/* Tooltip */
.tooltip {
  position: relative;
}
.tooltip::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.9);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}
.tooltip:hover::after {
  opacity: 1;
}
</style>
</head>
<body>
<div class="loading-overlay" id="loadingOverlay">
  <div class="loading-spinner"></div>
</div>

<div class="page">
  <div class="container">
    <div class="card">
      <div class="header">
        <div class="header-left">
          <img class="brand-logo" alt="Logo" src="__LOGO_DATA_URL__">
        </div>
        <button class="btn-print" onclick="window.print()" title="Drucken (Strg+P)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          Drucken
        </button>
      </div>

      <div class="searchbar">
        <div class="field">
          <div class="label">Suche <span class="kbd-hint">⌘K</span></div>
          <input class="input" id="smartSearch" placeholder="Name / Ort / CSB / SAP / Tour / Fachberater / Telefon / …">
        </div>
        <div class="field">
          <div class="label">Schlüssel</div>
          <input class="input" id="keySearch" placeholder="exakt (z. B. 40)">
        </div>
        <button class="btn btn-back" id="btnBack" style="display:none;">← Zurück zur Suche</button>
        <button class="btn btn-danger" id="btnReset" title="Alle Felder zurücksetzen (Esc)">✕ Zurücksetzen</button>
      </div>

      <div class="tour-wrap" id="tourWrap">
        <div class="tour-banner">
          <span class="tour-pill" id="tourTitle">🚚 Tour wird geladen...</span>
          <small class="tour-stats" id="tourExtra"></small>
        </div>
      </div>

      <div class="results-count" id="resultsCount"></div>

      <div class="table-section">
        <div class="table-wrapper">
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
                <th class="tooltip" data-tooltip="Customer Service Berater / SAP Nummer">CSB / SAP</th>
                <th>Name / Adresse</th>
                <th class="tooltip" data-tooltip="Zugeordnete Touren">Touren</th>
                <th class="tooltip" data-tooltip="Kundenschlüssel">Schlüssel</th>
                <th>Fachberater / Markt</th>
              </tr>
            </thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>
        
        <div class="empty-state" id="emptyState" style="display:none;">
          <div class="empty-icon">🔍</div>
          <div class="empty-text">Keine Ergebnisse gefunden</div>
          <small>Versuchen Sie es mit anderen Suchbegriffen</small>
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
let currentResults = 0;
const DIAL_SCHEME = 'callto';

// Loading states
function showLoading() {
  $('#loadingOverlay').style.display = 'flex';
}
function hideLoading() {
  setTimeout(() => $('#loadingOverlay').style.display = 'none', 300);
}

// Results counter
function updateResultsCount(count) {
  currentResults = count;
  const el = $('#resultsCount');
  if (count > 0) {
    el.textContent = `${count} ${count === 1 ? 'Ergebnis' : 'Ergebnisse'} gefunden`;
    el.classList.add('show');
  } else {
    el.classList.remove('show');
  }
}

function sanitizePhone(num){ return (num||'').toString().trim().replace(/[^\\d+]/g,''); }
function makePhoneChip(label, num, cls){
  if(!num) return null;
  const a = document.createElement('a');
  a.className = 'phone-chip '+cls;
  a.href = `${DIAL_SCHEME}:${sanitizePhone(num)}`;
  a.title = `${label} anrufen: ${num}`;
  a.append(el('span','chip-tag',label), el('span','mono',' '+num));
  return a;
}
function makeMailChip(label, addr){
  if(!addr) return null;
  const a = document.createElement('a');
  a.className = 'mail-chip';
  a.href = `mailto:${addr}`;
  a.title = `E-Mail an ${addr}`;
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
  return `${vor}.${nach}@edeka.de`.replace(/\s+/g,'');
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
  showLoading();
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
  hideLoading();
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
  const a = document.createElement('a'); a.className='addr-chip'; a.href=url; a.target='_blank'; a.title='📍 Adresse in Google Maps öffnen';
  a.append(el('span','addr-dot',''), el('span','chip-tag','Adresse'), (()=>{ const s=document.createElement('span'); s.className='txt'; s.textContent=' '+txt; return s; })());
  return a;
}

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = k.csb_nummer||'-', sap=k.sap_nummer||'-', plz=k.postleitzahl||'-';

  const td1 = document.createElement('td');
  const c1 = el('div','cell');
  const l1 = el('div','cell-top'); l1.appendChild(makeIdChip('CSB', csb));
  const l2 = el('div','cell-sub'); l2.appendChild(makeIdChip('SAP', sap));
  c1.append(l1,l2); td1.append(c1); tr.append(td1);

  const td2 = document.createElement('td');
  const c2 = el('div','cell');
  c2.append(el('div','cell-top', k.name||'-'));
  const addrPill = makeAddressChip(k.name||'', k.strasse||'', plz, k.ort||'');
  const line2 = el('div','cell-sub'); line2.appendChild(addrPill);
  c2.append(line2);
  td2.append(c2); tr.append(td2);

  const td4 = document.createElement('td'); const c4 = el('div','cell'); const tours=el('div','tour-inline');
  (k.touren||[]).forEach(t=>{ 
    const tnum=(t.tournummer||''); 
    const b=el('span','tour-btn',tnum+' ('+t.liefertag.substring(0,2)+')'); 
    b.title='🚚 Tour '+tnum+' anzeigen'; 
    b.onclick=()=>{ pushPrevQuery(); $('#smartSearch').value=tnum; onSmart(); }; 
    tours.appendChild(b); 
  });
  c4.appendChild(tours); td4.appendChild(c4); tr.append(td4);

  const td5 = document.createElement('td'); const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td5.appendChild(key ? el('span','badge-key','🔑 '+key) : el('span','', '-')); tr.append(td5);

  const td6=document.createElement('td'); const col=el('div','phone-col');
  const fbPhone = k.fb_phone;
  const fbMail  = k.fachberater ? fbEmailFromName(k.fachberater) : '';
  const mkPhone = k.market_phone;
  const mkMail  = k.market_email || '';
  const p1 = makePhoneChip('FB', fbPhone, 'chip-fb');      if(p1) col.appendChild(p1);
  const m1 = makeMailChip('FB Mail', fbMail);              if(m1) col.appendChild(m1);
  const p2 = makePhoneChip('Markt', mkPhone,'chip-market');if(p2) col.appendChild(p2);
  const m2 = makeMailChip('Mail', mkMail);                 if(m2) col.appendChild(m2);
  if(!col.childNodes.length) col.textContent='-';
  td6.appendChild(col); tr.append(td6);

  return tr;
}
function renderTable(list){
  const body=$('#tableBody'), tbl=$('#resultTable'), empty=$('#emptyState'); 
  body.innerHTML='';
  updateResultsCount(list.length);
  
  if(list.length){ 
    list.forEach(k=>body.appendChild(rowFor(k))); 
    tbl.style.display='table'; 
    empty.style.display='none';
  } else { 
    tbl.style.display='none'; 
    if($('#smartSearch').value.trim() || $('#keySearch').value.trim()) {
      empty.style.display='block';
    } else {
      empty.style.display='none';
    }
  }
}

function renderTourTop(list, query, isExact){
  const wrap=$('#tourWrap'), title=$('#tourTitle'), extra=$('#tourExtra');
  if(!list.length){ wrap.style.display='none'; title.textContent=''; extra.textContent=''; return; }
  const emoji = query.startsWith('Schluessel ') ? '🔑' : '🚚';
  if(query.startsWith('Schluessel ')){ 
    const key=query.replace(/^Schluessel\\s+/, ''); 
    title.textContent=`${emoji} Schlüssel ${key} — ${list.length} ${list.length===1?'Kunde':'Kunden'}`; 
  }
  else{ 
    title.textContent=`${emoji} ${isExact?('Tour '+query):('Tour-Prefix '+query+'*')} — ${list.length} ${list.length===1?'Kunde':'Kunden'}`; 
  }
  const dayCount={}; 
  list.forEach(k=>(k.touren||[]).forEach(t=>{ 
    const tnum=t.tournummer||''; 
    const cond=isExact?(tnum===query):tnum.startsWith(query.replace('Schluessel ','')); 
    if(cond||query.startsWith('Schluessel ')){ 
      dayCount[t.liefertag]=(dayCount[t.liefertag]||0)+1; 
    }
  }));
  extra.textContent=Object.entries(dayCount).sort().map(([d,c])=>`📅 ${d}: ${c}`).join('  •  ');
  wrap.style.display='block';
}
function closeTourTop(){ $('#tourWrap').style.display='none'; $('#tourTitle').textContent=''; $('#tourExtra').textContent=''; }

function onSmart(){
  const qRaw=$('#smartSearch').value.trim(); 
  closeTourTop(); 
  if(!qRaw){ renderTable([]); return; }
  
  // Show loading for complex searches
  if(qRaw.length > 3) showLoading();
  
  setTimeout(() => {
    if(/^\\d{1,3}$/.test(qRaw)){ 
      const n=qRaw.replace(/^0+(\\d)/,'$1'); 
      const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n))); 
      renderTourTop(r,n,false); 
      renderTable(r); 
      hideLoading();
      return; 
    }
    if(/^\\d{4}$/.test(qRaw)){
      const n=qRaw.replace(/^0+(\\d)/,'$1'); 
      const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n)); 
      const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n); 
      const r=dedupByCSB([...tr,...cr]);
      if(tr.length) renderTourTop(tr,n,true); else closeTourTop(); 
      renderTable(r); 
      hideLoading();
      return;
    }
    const q=normDE(qRaw);
    const r=allCustomers.filter(k=>{ 
      const fb=k.fachberater||''; 
      const text=(k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||'')+' '+(k.market_email||'')); 
      return normDE(text).includes(q); 
    });
    renderTable(r);
    hideLoading();
  }, 10);
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

function debounce(fn,d=140){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Strg+K oder Cmd+K für Suche fokussieren
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    $('#smartSearch').focus();
    $('#smartSearch').select();
  }
  // Escape zum Zurücksetzen
  if (e.key === 'Escape') {
    $('#btnReset').click();
  }
  // Strg+P für Drucken (bereits Standard)
});

document.addEventListener('DOMContentLoaded', ()=>{
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
    updateResultsCount(0);
  });
  $('#btnBack').addEventListener('click', ()=>{ popPrevQuery(); });
  
  // Auto-focus on search
  $('#smartSearch').focus();
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("🚀 Kunden-Suche – Premium Design")
st.caption("✨ Modernes Interface mit Animationen, Keyboard-Shortcuts, Druck-Funktion und Dark Mode Support")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    excel_file = st.file_uploader("📊 Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("🔑 Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("🖼️ Logo (PNG/JPG)", type=["png","jpg","jpeg"])

berater_file = st.file_uploader("📞 OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("👥 Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Tel, X=Markt-Mail)", type=["xlsx"])

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
        st.warning("⚠️ Schlüsseldatei hat < 6 Spalten – nehme letzte vorhandene Spalte als Schlüssel.")
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
    # A = Fachberater-Name, I = CSB, O = Markt-Telefon, X = Markt-Mail
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
    if st.button("🎨 HTML erzeugen", type="primary", use_container_width=True):
        if logo_file is None:
            st.error("❌ Bitte Logo (PNG/JPG) hochladen.")
            st.stop()
        logo_data_url = to_data_url(logo_file)

        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        SPALTEN_MAPPING = {
            "csb_nummer":"Nr","sap_nummer":"SAP-Nr.","name":"Name","strasse":"Strasse",
            "postleitzahl":"Plz","ort":"Ort","fachberater":"Fachberater"
        }
        LIEFERTAGE_MAPPING = {"Montag":"Mo","Dienstag":"Die","Mittwoch":"Mitt","Donnerstag":"Don","Freitag":"Fr","Samstag":"Sam"}

        try:
            with st.spinner("📖 Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            berater_map = {}
            if berater_file is not None:
                with st.spinner("📞 Lese Fachberater-Telefonliste..."):
                    berater_file.seek(0)
                    bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                    bf = bf.rename(columns={0:"Vorname",1:"Nachname",2:"Nummer"}).dropna(how="all")
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("👥 Lese Fachberater–CSB-Zuordnung..."):
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

            with st.spinner("🔄 Verarbeite Kundendatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("❌ Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0))

            final_html = (HTML_TEMPLATE
              .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
              .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
              .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
              .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
              .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            st.success("✅ HTML erfolgreich generiert!")
            st.download_button(
                "⬇️ Download HTML",
                data=final_html.encode("utf-8"),
                file_name="suche_premium.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
            
            # Feature-Liste anzeigen
            with st.expander("✨ Neue Features im Premium Design"):
                st.markdown("""
                **🎨 Design-Verbesserungen:**
                - Moderne Gradienten und Schatten-Effekte
                - Smooth Animations und Transitions
                - Dark Mode Support (automatisch)
                - Verbesserte visuelle Hierarchie
                
                **⚡ Funktionale Verbesserungen:**
                - 🖨️ **Drucken-Button** mit optimiertem Print-Layout
                - ⌨️ **Keyboard Shortcuts:**
                  - `Strg+K` / `Cmd+K` → Suche fokussieren
                  - `Esc` → Alle Felder zurücksetzen
                  - `Strg+P` → Drucken
                - 📊 Ergebniszähler
                - 🔄 Loading-States für besseres Feedback
                - 🔍 Empty-State wenn keine Ergebnisse
                - 💫 Hover-Effekte mit Glow und Animationen
                - 📍 Tooltips für bessere Orientierung
                - 😊 Emojis für bessere visuelle Erkennbarkeit
                
                **🚀 Performance:**
                - Optimierte Suche mit Loading-Indicator
                - Debounced Input für flüssigere Eingabe
                - Kompaktere und übersichtlichere Darstellung
                """)
                
        except Exception as e:
            st.error(f"❌ Fehler: {e}")
else:
    st.info("📁 Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
    
    # Demo-Features anzeigen
    with st.sidebar:
        st.markdown("### 🌟 Premium Features")
        st.markdown("""
        - **Drucken-Funktion** integriert
        - **Keyboard Shortcuts**
        - **Dark Mode** Support
        - **Loading Animations**
        - **Hover-Effekte**
        - **Ergebniszähler**
        - **Empty States**
        - **Tooltips**
        - **Responsive Design**
        """)
