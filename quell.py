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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size:13px;
  line-height:1.4;
  color:#1a1a1a;
  background:#fff;
}

/* Container */
.wrapper{max-width:1600px;margin:0 auto;padding:8px}

/* Header */
.header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 16px;
  background:#fff;
  border-bottom:2px solid #e5e5e5;
  margin-bottom:8px;
}
.logo{height:48px;width:auto}
.btn-print{
  padding:6px 16px;
  background:#2563eb;
  color:#fff;
  border:none;
  border-radius:4px;
  font-size:13px;
  font-weight:500;
  cursor:pointer;
}
.btn-print:hover{background:#1d4ed8}

/* Suchbereich */
.search-bar{
  display:flex;
  gap:8px;
  padding:8px 16px;
  background:#f9f9f9;
  border:1px solid #e5e5e5;
  margin-bottom:8px;
  flex-wrap:wrap;
}
.search-field{flex:1;min-width:200px;display:flex;align-items:center;gap:8px}
.search-label{
  font-size:11px;
  font-weight:600;
  text-transform:uppercase;
  color:#666;
  white-space:nowrap;
}
.search-input{
  flex:1;
  padding:5px 8px;
  border:1px solid #d0d0d0;
  border-radius:3px;
  font-size:13px;
  background:#fff;
}
.search-input:focus{outline:none;border-color:#2563eb}
.btn{
  padding:5px 12px;
  border:1px solid #d0d0d0;
  background:#fff;
  border-radius:3px;
  font-size:13px;
  font-weight:500;
  cursor:pointer;
}
.btn:hover{background:#f5f5f5}
.btn-reset{background:#dc2626;color:#fff;border-color:#dc2626}
.btn-reset:hover{background:#b91c1c}
.btn-back{background:#f0f9ff;color:#2563eb;border-color:#2563eb}

/* Tour-Info */
.tour-info{
  display:none;
  padding:8px 16px;
  background:#fffbeb;
  border:1px solid #fbbf24;
  margin-bottom:8px;
  font-size:13px;
}
.tour-title{font-weight:600;color:#92400e}
.tour-stats{color:#78350f;margin-left:16px;font-size:12px}

/* Tabelle */
.table-container{
  background:#fff;
  border:1px solid #e5e5e5;
  overflow:hidden;
}
.table-scroll{
  max-height:calc(100vh - 200px);
  overflow:auto;
}
table{
  width:100%;
  border-collapse:collapse;
  font-size:12px;
}
thead th{
  position:sticky;
  top:0;
  background:#f5f5f5;
  font-weight:600;
  text-align:left;
  padding:8px;
  border-bottom:2px solid #d0d0d0;
  font-size:11px;
  text-transform:uppercase;
  color:#333;
  z-index:10;
}
tbody td{
  padding:6px 8px;
  border-bottom:1px solid #e5e5e5;
  vertical-align:top;
  background:#fff;
}
tbody tr:hover td{background:#f9fafb}

/* Kompakte Zellen */
.cell-wrap{display:flex;flex-direction:column;gap:2px}
.cell-main{font-weight:500;color:#1a1a1a}
.cell-sub{font-size:11px;color:#666}

/* IDs */
.id-chip{
  display:inline-block;
  padding:2px 6px;
  background:#fef3c7;
  border:1px solid #fbbf24;
  border-radius:3px;
  font-size:11px;
  font-weight:500;
  color:#78350f;
  text-decoration:none;
  cursor:pointer;
}
.id-chip:hover{background:#fed7aa}
.id-label{font-size:10px;opacity:0.8}

/* Schlüssel */
.key-badge{
  display:inline-block;
  padding:2px 6px;
  background:#d1fae5;
  border:1px solid #10b981;
  border-radius:3px;
  font-size:11px;
  font-weight:500;
  color:#065f46;
}

/* Touren */
.tour-tags{display:flex;flex-wrap:wrap;gap:4px}
.tour-tag{
  display:inline-block;
  padding:2px 6px;
  background:#fee2e2;
  border:1px solid #f87171;
  border-radius:3px;
  font-size:10px;
  font-weight:500;
  color:#7f1d1d;
  cursor:pointer;
}
.tour-tag:hover{background:#fecaca}

/* Kontakt-Pills */
.contact-list{display:flex;flex-direction:column;gap:3px}
.contact-chip{
  display:inline-flex;
  align-items:center;
  gap:4px;
  padding:2px 6px;
  border:1px solid;
  border-radius:3px;
  font-size:11px;
  text-decoration:none;
  max-width:100%;
}
.chip-fb{background:#eff6ff;border-color:#3b82f6;color:#1e3a8a}
.chip-market{background:#f3e8ff;border-color:#9333ea;color:#581c87}
.chip-mail{background:#f0fdfa;border-color:#14b8a6;color:#134e4a}
.contact-label{font-size:9px;font-weight:600;text-transform:uppercase;opacity:0.8}
.contact-value{font-family:'JetBrains Mono',monospace;font-size:11px}

/* Adresse */
.addr-link{
  display:inline-flex;
  align-items:center;
  gap:4px;
  padding:2px 6px;
  background:#f0f9ff;
  border:1px solid #60a5fa;
  border-radius:3px;
  font-size:11px;
  color:#1e3a8a;
  text-decoration:none;
}
.addr-link:hover{background:#e0f2fe}
.addr-icon{font-size:10px}

/* Spaltenbreiten */
.col-id{width:180px}
.col-name{width:380px}
.col-tour{width:200px}
.col-key{width:80px}
.col-contact{width:340px}

/* Druckoptimierung */
@media print {
  body{font-size:10px}
  .header{border-bottom:1px solid #000;page-break-after:avoid}
  .btn-print,.btn,.search-bar{display:none !important}
  .tour-info{border:1px solid #000;page-break-after:avoid}
  .table-scroll{max-height:none;overflow:visible}
  table{font-size:9px;page-break-inside:auto}
  thead{display:table-header-group}
  tbody tr{page-break-inside:avoid;page-break-after:auto}
  tbody td{padding:4px;border-bottom:1px solid #ccc}
  .id-chip,.key-badge,.tour-tag,.contact-chip,.addr-link{
    border:1px solid #000 !important;
    background:none !important;
    padding:1px 3px;
  }
  a{text-decoration:none;color:#000}
}

/* Scrollbar optimiert */
.table-scroll::-webkit-scrollbar{width:8px;height:8px}
.table-scroll::-webkit-scrollbar-track{background:#f5f5f5}
.table-scroll::-webkit-scrollbar-thumb{background:#c0c0c0;border-radius:4px}
.table-scroll::-webkit-scrollbar-thumb:hover{background:#999}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <img class="logo" src="__LOGO_DATA_URL__" alt="Logo">
    <button class="btn-print" onclick="window.print()">Drucken</button>
  </div>

  <div class="search-bar">
    <div class="search-field">
      <span class="search-label">Suche</span>
      <input class="search-input" id="smartSearch" placeholder="Name, Ort, CSB, SAP, Tour, Fachberater...">
    </div>
    <div class="search-field">
      <span class="search-label">Schlüssel</span>
      <input class="search-input" id="keySearch" placeholder="z.B. 40">
    </div>
    <button class="btn btn-back" id="btnBack" style="display:none">← Zurück</button>
    <button class="btn btn-reset" id="btnReset">Zurücksetzen</button>
  </div>

  <div class="tour-info" id="tourInfo">
    <span class="tour-title" id="tourTitle"></span>
    <span class="tour-stats" id="tourStats"></span>
  </div>

  <div class="table-container">
    <div class="table-scroll">
      <table id="dataTable" style="display:none">
        <thead>
          <tr>
            <th class="col-id">CSB / SAP</th>
            <th class="col-name">Name / Adresse</th>
            <th class="col-tour">Touren</th>
            <th class="col-key">Schlüssel</th>
            <th class="col-contact">Fachberater / Kontakt</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
const tourkundenData = {};
const keyIndex = {};
const beraterIndex = {};
const beraterCSBIndex = {};

const $ = s => document.querySelector(s);
const el = (tag, cls, txt) => {
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(txt !== undefined) e.textContent = txt;
  return e;
};

let allCustomers = [];
let prevQuery = null;

function sanitizePhone(n) {
  return (n||'').toString().trim().replace(/[^\\d+]/g,'');
}

function normDE(s) {
  if(!s) return '';
  return s.toLowerCase()
    .replace(/ä/g,'ae').replace(/ö/g,'oe')
    .replace(/ü/g,'ue').replace(/ß/g,'ss')
    .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
    .replace(/\\s+/g,' ').trim();
}

function normalizeDigits(v) {
  if(v == null) return '';
  let s = String(v).trim().replace(/\\.0$/,'');
  return s.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
}

function normalizeNameKey(s) {
  if(!s) return '';
  return s.replace(/[\\u200B-\\u200D\\uFEFF]/g,'')
    .replace(/\\u00A0/g,' ').toLowerCase()
    .replace(/ä/g,'ae').replace(/ö/g,'oe')
    .replace(/ü/g,'ue').replace(/ß/g,'ss')
    .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
    .replace(/\\(.*?\\)/g,' ').replace(/[^a-z\\s]/g,' ')
    .replace(/\\s+/g,' ').trim();
}

function nameVariants(s) {
  const base = normalizeNameKey(s);
  if(!base) return [];
  const parts = base.split(' ').filter(Boolean);
  const out = new Set([base]);
  if(parts.length >= 2) {
    out.add(`${parts[0]} ${parts[parts.length-1]}`);
    out.add(`${parts[parts.length-1]} ${parts[0]}`);
  }
  return Array.from(out);
}

function fbEmailFromName(name) {
  const parts = normalizeNameKey(name).split(' ').filter(Boolean);
  if(parts.length < 2) return '';
  return `${parts[0]}.${parts[parts.length-1]}@edeka.de`;
}

function pickBeraterPhone(name) {
  if(!name) return '';
  const variants = nameVariants(name);
  for(const v of variants) {
    if(beraterIndex[v]) return beraterIndex[v];
  }
  return '';
}

function dedupByCSB(list) {
  const seen = new Set();
  return list.filter(k => {
    const csb = normalizeDigits(k.csb_nummer);
    if(seen.has(csb)) return false;
    seen.add(csb);
    return true;
  });
}

function buildData() {
  const map = new Map();
  for(const [tour, list] of Object.entries(tourkundenData)) {
    const tourN = normalizeDigits(tour);
    list.forEach(k => {
      const csb = normalizeDigits(k.csb_nummer);
      if(!csb) return;
      
      if(!map.has(csb)) {
        const rec = {...k};
        rec.csb_nummer = csb;
        rec.sap_nummer = normalizeDigits(rec.sap_nummer);
        rec.postleitzahl = normalizeDigits(rec.postleitzahl);
        rec.touren = [];
        rec.schluessel = normalizeDigits(rec.schluessel) || keyIndex[csb] || '';
        if(beraterCSBIndex[csb] && beraterCSBIndex[csb].name) {
          rec.fachberater = beraterCSBIndex[csb].name;
        }
        rec.fb_phone = rec.fachberater ? pickBeraterPhone(rec.fachberater) : '';
        rec.market_phone = beraterCSBIndex[csb]?.telefon || '';
        rec.market_email = beraterCSBIndex[csb]?.email || '';
        map.set(csb, rec);
      }
      map.get(csb).touren.push({tournummer: tourN, liefertag: k.liefertag});
    });
  }
  allCustomers = Array.from(map.values());
}

function createRow(k) {
  const tr = document.createElement('tr');
  const csb = k.csb_nummer || '-';
  const sap = k.sap_nummer || '-';
  const plz = k.postleitzahl || '-';
  
  // CSB/SAP
  const td1 = document.createElement('td');
  const wrap1 = el('div', 'cell-wrap');
  const csb_chip = document.createElement('a');
  csb_chip.className = 'id-chip';
  csb_chip.href = '#';
  csb_chip.innerHTML = `<span class="id-label">CSB</span> ${csb}`;
  csb_chip.onclick = e => {
    e.preventDefault();
    pushPrevQuery();
    $('#smartSearch').value = csb;
    onSmart();
  };
  const sap_chip = document.createElement('a');
  sap_chip.className = 'id-chip';
  sap_chip.href = '#';
  sap_chip.innerHTML = `<span class="id-label">SAP</span> ${sap}`;
  sap_chip.onclick = e => {
    e.preventDefault();
    pushPrevQuery();
    $('#smartSearch').value = sap;
    onSmart();
  };
  wrap1.appendChild(el('div', 'cell-main')).appendChild(csb_chip);
  wrap1.appendChild(el('div', 'cell-sub')).appendChild(sap_chip);
  td1.appendChild(wrap1);
  tr.appendChild(td1);
  
  // Name/Adresse
  const td2 = document.createElement('td');
  const wrap2 = el('div', 'cell-wrap');
  wrap2.appendChild(el('div', 'cell-main', k.name || '-'));
  const addr = `${k.strasse||''}, ${plz} ${k.ort||''}`.replace(/^,\\s*/,'').trim();
  const addr_link = document.createElement('a');
  addr_link.className = 'addr-link';
  addr_link.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((k.name||'')+', '+addr)}`;
  addr_link.target = '_blank';
  addr_link.innerHTML = `<span class="addr-icon">📍</span> ${addr}`;
  wrap2.appendChild(el('div', 'cell-sub')).appendChild(addr_link);
  td2.appendChild(wrap2);
  tr.appendChild(td2);
  
  // Touren
  const td3 = document.createElement('td');
  const tours = el('div', 'tour-tags');
  (k.touren || []).forEach(t => {
    const tag = el('span', 'tour-tag', `${t.tournummer} (${t.liefertag.substring(0,2)})`);
    tag.onclick = () => {
      pushPrevQuery();
      $('#smartSearch').value = t.tournummer;
      onSmart();
    };
    tours.appendChild(tag);
  });
  td3.appendChild(tours);
  tr.appendChild(td3);
  
  // Schlüssel
  const td4 = document.createElement('td');
  const key = k.schluessel || keyIndex[csb] || '';
  td4.appendChild(key ? el('span', 'key-badge', key) : el('span', '', '-'));
  tr.appendChild(td4);
  
  // Kontakt
  const td5 = document.createElement('td');
  const contacts = el('div', 'contact-list');
  
  if(k.fb_phone) {
    const a = document.createElement('a');
    a.className = 'contact-chip chip-fb';
    a.href = `callto:${sanitizePhone(k.fb_phone)}`;
    a.innerHTML = `<span class="contact-label">FB</span> <span class="contact-value">${k.fb_phone}</span>`;
    contacts.appendChild(a);
  }
  
  const fbMail = k.fachberater ? fbEmailFromName(k.fachberater) : '';
  if(fbMail) {
    const a = document.createElement('a');
    a.className = 'contact-chip chip-mail';
    a.href = `mailto:${fbMail}`;
    a.innerHTML = `<span class="contact-label">FB Mail</span> <span class="contact-value">${fbMail}</span>`;
    contacts.appendChild(a);
  }
  
  if(k.market_phone) {
    const a = document.createElement('a');
    a.className = 'contact-chip chip-market';
    a.href = `callto:${sanitizePhone(k.market_phone)}`;
    a.innerHTML = `<span class="contact-label">Markt</span> <span class="contact-value">${k.market_phone}</span>`;
    contacts.appendChild(a);
  }
  
  if(k.market_email) {
    const a = document.createElement('a');
    a.className = 'contact-chip chip-mail';
    a.href = `mailto:${k.market_email}`;
    a.innerHTML = `<span class="contact-label">Mail</span> <span class="contact-value">${k.market_email}</span>`;
    contacts.appendChild(a);
  }
  
  if(!contacts.children.length) contacts.textContent = '-';
  td5.appendChild(contacts);
  tr.appendChild(td5);
  
  return tr;
}

function renderTable(list) {
  const body = $('#tableBody');
  const table = $('#dataTable');
  body.innerHTML = '';
  
  if(list.length) {
    list.forEach(k => body.appendChild(createRow(k)));
    table.style.display = 'table';
  } else {
    table.style.display = 'none';
  }
}

function showTourInfo(list, query, exact) {
  const info = $('#tourInfo');
  const title = $('#tourTitle');
  const stats = $('#tourStats');
  
  if(!list.length) {
    info.style.display = 'none';
    return;
  }
  
  if(query.startsWith('Schluessel ')) {
    const key = query.replace(/^Schluessel\\s+/, '');
    title.textContent = `Schlüssel ${key}: ${list.length} Kunde(n)`;
  } else {
    title.textContent = `Tour ${exact ? query : query+'*'}: ${list.length} Kunde(n)`;
  }
  
  const days = {};
  list.forEach(k => {
    (k.touren || []).forEach(t => {
      if(query.startsWith('Schluessel ') || 
         (exact ? t.tournummer === query : t.tournummer.startsWith(query))) {
        days[t.liefertag] = (days[t.liefertag] || 0) + 1;
      }
    });
  });
  
  stats.textContent = Object.entries(days).sort()
    .map(([d,c]) => `${d}: ${c}`).join(' • ');
  info.style.display = 'block';
}

function hideTourInfo() {
  $('#tourInfo').style.display = 'none';
}

function pushPrevQuery() {
  const v = $('#smartSearch').value.trim();
  if(v) {
    prevQuery = v;
    $('#btnBack').style.display = 'inline-block';
  }
}

function popPrevQuery() {
  if(prevQuery) {
    $('#smartSearch').value = prevQuery;
    prevQuery = null;
    $('#btnBack').style.display = 'none';
    onSmart();
  }
}

function onSmart() {
  const qRaw = $('#smartSearch').value.trim();
  hideTourInfo();
  
  if(!qRaw) {
    renderTable([]);
    return;
  }
  
  // 1-3 stellig: Tour-Prefix
  if(/^\\d{1,3}$/.test(qRaw)) {
    const n = qRaw.replace(/^0+(\\d)/, '$1');
    const r = allCustomers.filter(k => 
      (k.touren || []).some(t => t.tournummer.startsWith(n))
    );
    showTourInfo(r, n, false);
    renderTable(r);
    return;
  }
  
  // 4-stellig: Tour oder CSB
  if(/^\\d{4}$/.test(qRaw)) {
    const n = qRaw.replace(/^0+(\\d)/, '$1');
    const tourResults = allCustomers.filter(k => 
      (k.touren || []).some(t => t.tournummer === n)
    );
    const csbResults = allCustomers.filter(k => k.csb_nummer === n);
    const r = dedupByCSB([...tourResults, ...csbResults]);
    if(tourResults.length) showTourInfo(tourResults, n, true);
    renderTable(r);
    return;
  }
  
  // Textsuche
  const q = normDE(qRaw);
  const r = allCustomers.filter(k => {
    const text = [
      k.name, k.strasse, k.ort,
      k.csb_nummer, k.sap_nummer,
      k.fachberater || '',
      k.schluessel || '',
      k.fb_phone || '',
      k.market_phone || '',
      k.market_email || ''
    ].join(' ');
    return normDE(text).includes(q);
  });
  renderTable(r);
}

function onKey() {
  const q = $('#keySearch').value.trim();
  hideTourInfo();
  
  if(!q) {
    renderTable([]);
    return;
  }
  
  const n = q.replace(/[^0-9]/g, '').replace(/^0+(\\d)/, '$1');
  const r = allCustomers.filter(k => {
    const key = k.schluessel || keyIndex[k.csb_nummer] || '';
    return key === n;
  });
  
  if(r.length) showTourInfo(r, 'Schluessel ' + n, true);
  renderTable(r);
}

function debounce(fn, delay = 150) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// Tastatur-Shortcuts
document.addEventListener('keydown', e => {
  if(e.key === 'Escape') {
    $('#btnReset').click();
  }
  if((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    $('#smartSearch').focus();
  }
});

// Init
document.addEventListener('DOMContentLoaded', () => {
  if(Object.keys(tourkundenData).length > 0) {
    buildData();
  }
  
  $('#smartSearch').addEventListener('input', debounce(onSmart));
  $('#keySearch').addEventListener('input', debounce(onKey));
  $('#btnReset').addEventListener('click', () => {
    $('#smartSearch').value = '';
    $('#keySearch').value = '';
    hideTourInfo();
    renderTable([]);
    prevQuery = null;
    $('#btnBack').style.display = 'none';
  });
  $('#btnBack').addEventListener('click', popPrevQuery);
  
  $('#smartSearch').focus();
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("Kunden-Suche – Optimiert")
st.caption("Klares Design • Druck-optimiert • Kompakt • Alle Funktionen erhalten")

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
              .replace("const tourkundenData = {}", f"const tourkundenData = {json.dumps(sorted_tours, ensure_ascii=False)}")
              .replace("const keyIndex = {}", f"const keyIndex = {json.dumps(key_map, ensure_ascii=False)}")
              .replace("const beraterIndex = {}", f"const beraterIndex = {json.dumps(berater_map, ensure_ascii=False)}")
              .replace("const beraterCSBIndex = {}", f"const beraterCSBIndex = {json.dumps(berater_csb_map, ensure_ascii=False)}")
              .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            st.download_button(
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="kunden_suche.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
