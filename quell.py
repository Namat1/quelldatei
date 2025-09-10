import streamlit as st
import pandas as pd
import json
import base64
import unicodedata

# =========================
#  HTML TEMPLATE
# =========================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Kunden-Suche</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f6f7f9; --surface:#ffffff; --alt:#fafbfd; --border:#d9e2ef;
  --row-border:#e6edf5; --stripe:#f5f8fc;
  --txt:#1f2937; --muted:#667085; --head:#0f172a;
  --accent:#2563eb; --accent-weak:rgba(37,99,235,.12); --accent-strong:#1d4ed8;
  --ok:#16a34a; --ok-weak:rgba(22,163,74,.12);
  --warn:#f59e0b; --warn-weak:rgba(245,158,11,.18);
  --chip-fb:#0ea5e9; --chip-fb-weak:rgba(14,165,233,.12);
  --chip-market:#8b5cf6; --chip-market-weak:rgba(139,92,246,.12);
  --pill-yellow:#fef3c7; --pill-yellow-border:#fcd34d; --pill-yellow-text:#92400e;
  --pill-red:#fee2e2; --pill-red-border:#fecaca; --pill-red-text:#991b1b;
  --radius:8px; --shadow:0 1px 3px rgba(0,0,0,.05);
  --fs-10:10px; --fs-11:11px; --fs-12:12px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.45;
}
.page{min-height:100vh; display:flex; justify-content:center; padding:12px}
.container{width:100%; max-width:1400px}
.card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); box-shadow:var(--shadow); overflow:hidden}

/* Header */
.header{padding:14px 12px; border-bottom:1px solid var(--border); background:var(--surface);
  display:flex; flex-direction:column; align-items:center; gap:6px}
.brand-logo{height:56px; width:auto}
.title{font-size:13px; font-weight:700; color:#344054}

/* Searchbar */
.searchbar{
  padding:8px 12px; display:grid; grid-template-columns:1fr 250px auto; gap:8px; align-items:center;
  border-bottom:1px solid var(--border); background:var(--surface);
}
@media(max-width:960px){ .searchbar{grid-template-columns:1fr} }
.field{display:grid; grid-template-columns:70px 1fr; gap:6px; align-items:center}
.label{font-weight:600; color:#344054; font-size:var(--fs-12)}
.input{
  width:100%; padding:7px 9px; border:1px solid var(--border); border-radius:7px;
  background:linear-gradient(180deg, var(--surface), var(--alt));
  transition:border-color .15s, box-shadow .15s, background .15s; font-size:var(--fs-12)
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 2px var(--accent-weak); background:#fff}
.btn{padding:7px 9px; border:1px solid var(--border); background:#fff; border-radius:7px; cursor:pointer; font-weight:600; font-size:var(--fs-12)}
.btn:hover{background:#f3f4f6}
.btn-danger{background:#ef4444; border-color:#ef4444; color:#fff}
.btn-danger:hover{background:#dc2626}

/* Content */
.content{padding:10px 12px}

/* Tour banner */
.tour-wrap{display:none; margin-bottom:8px}
.tour-banner{
  display:flex; align-items:center; justify-content:space-between;
  padding:6px 10px; border:1px solid var(--border); border-radius:6px;
  background:#f2f5fa; color:#344054; font-weight:700; font-size:12px;
}
.tour-banner small{font-weight:600; color:#667085; font-size:11px}

/* Table */
.table-section{padding:6px 8px}
.scroller{max-height:68vh; overflow:auto; border:1px solid var(--row-border); border-radius:6px; background:#fff}
table{width:100%; border-collapse:separate; border-spacing:0; table-layout:fixed; font-size:var(--fs-12)}
thead th{
  position:sticky; top:0; background:#f2f5fa; color:#344054; font-weight:700;
  border-bottom:1px solid var(--row-border); padding:7px 8px; white-space:nowrap; z-index:1; text-align:left
}
tbody td{padding:6px 8px; border-bottom:1px solid var(--row-border); vertical-align:top; text-align:left}
tbody tr:nth-child(odd){background:var(--stripe)}
tbody tr:hover{background:#eef4ff}

/* Einheitliches 2-Zeilen-Layout je Zelle */
.cell{display:flex; flex-direction:column; align-items:flex-start; gap:3px; min-height:32px}
.cell-top,.cell-sub{white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Links / Labels / Badges */
.csb-link{font-weight:700; color:#0b3a8a; cursor:pointer}
.csb-link:hover{text-decoration:underline}
.small-label{font-size:var(--fs-10); font-weight:800; color:#64748b; letter-spacing:.25px; text-transform:uppercase}

/* Schlüssel / Touren – klare Trennung */
.key-tour{display:flex; flex-direction:column; gap:6px; width:100%}
.key-line{display:flex; align-items:center; gap:6px}
.key-divider{height:1px; background:#e9eef6; border:0; width:100%; margin:0}
.badge-key{background:var(--warn-weak); border:1px solid #fcd34d; color:#92400e; border-radius:999px; padding:2px 7px; font-weight:700; font-size:11px}

/* GELBE Chips (CSB/SAP) */
a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--pill-yellow); color:var(--pill-yellow-text);
  border:1px solid var(--pill-yellow-border);
  border-radius:999px; padding:2px 8px; font-weight:800; font-size:var(--fs-10);
  text-decoration:none; line-height:1;
}
a.id-chip:hover{filter:brightness(0.97)}
.id-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.3px; opacity:.9}

/* TOUR-Pills (leichtes Rot) */
.tour-inline{display:flex; flex-wrap:wrap; gap:4px; white-space:normal}
.tour-btn{
  display:inline-block; background:var(--pill-red); border:1px solid var(--pill-red-border); color:var(--pill-red-text);
  padding:1px 6px; border-radius:999px; font-weight:800; font-size:var(--fs-10); cursor:pointer; line-height:1.3
}
.tour-btn:hover{filter:brightness(0.97)}

/* Telefone als klickbare Chips (ProCall/Telefon) */
.phone-line{display:flex; flex-wrap:wrap; gap:6px}
a.phone-chip{
  display:inline-flex; align-items:center; gap:6px;
  border-radius:999px; padding:2px 8px; font-weight:700; font-size:var(--fs-10); line-height:1;
  text-decoration:none; cursor:pointer;
}
a.phone-chip.chip-fb{background:var(--chip-fb-weak); color:#075985; border:1px solid #7dd3fc}
a.phone-chip.chip-market{background:var(--chip-market-weak); color:#4338ca; border:1px solid #c4b5fd}
a.phone-chip:hover{filter:brightness(0.96)}
.chip-tag{font-size:var(--fs-10); font-weight:800; text-transform:uppercase; letter-spacing:.3px; opacity:.9}

/* Map Button */
.table-map{
  text-decoration:none; font-weight:700; font-size:var(--fs-11);
  padding:5px 10px; border-radius:999px; border:1px solid var(--accent);
  background:var(--accent); color:#fff; display:inline-block; text-align:center;
}
.table-map:hover{background:var(--accent-strong); border-color:var(--accent-strong)}

/* Scrollbar */
::-webkit-scrollbar{width:10px; height:10px}
::-webkit-scrollbar-thumb{background:#cbd5e1; border-radius:6px}
::-webkit-scrollbar-thumb:hover{background:#94a3b8}
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
          <div class="label">Schluessel</div>
          <input class="input" id="keySearch" placeholder="Exakte Schluesselnummer">
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="btn btn-danger" id="btnReset">Zuruecksetzen</button>
        </div>
      </div>

      <div class="content">
        <div class="tour-wrap" id="tourWrap">
          <div class="tour-banner">
            <span id="tourTitle"></span>
            <small id="tourExtra"></small>
          </div>
        </div>

        <div class="table-section">
          <div class="scroller" id="tableScroller" style="display:none;">
            <table>
              <thead>
                <tr>
                  <th>CSB / SAP</th>
                  <th>Name / Strasse</th>
                  <th>PLZ / Ort</th>
                  <th>Schluessel / Touren</th>
                  <th>Fachberater / Markt Telefon</th>
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
</div>

<script>
const tourkundenData   = {  };
const keyIndex         = {  };
const beraterIndex     = {  };
const beraterCSBIndex  = {  };

const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];

/* ProCall-/Telefon-Wählschema */
const DIAL_SCHEME = 'callto'; // 'callto' für ProCall | alternativ 'tel'
function sanitizePhone(num){ return (num||'').toString().trim().replace(/[^\d+]/g,''); }
function makePhoneChip(label, num, extraClass){
  const clean = sanitizePhone(num);
  const a = document.createElement('a');
  a.className = 'phone-chip ' + extraClass;
  a.href = `${DIAL_SCHEME}:${clean}`;
  a.title = (label === 'FB' ? 'Fachberater' : 'Markt') + ' anrufen';
  const tag = document.createElement('span'); tag.className='chip-tag'; tag.textContent = label;
  a.appendChild(tag);
  a.appendChild(document.createTextNode(' ☎ ' + num));
  return a;
}

/* Helpers */
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
        rec.fb_phone     = '';
        if (rec.fachberater){
          const nameKey = normDE(rec.fachberater);
          if (beraterIndex[nameKey]) rec.fb_phone = beraterIndex[nameKey];
        }
        rec.market_phone = beraterCSBIndex[csb] && beraterCSBIndex[csb].telefon ? beraterCSBIndex[csb].telefon : '';

        map.set(csb, rec);
      }
      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
}

function twoLineCell(top, sub){
  const wrap = el('div','cell');
  const a = el('div','cell-top', top);
  const b = el('div','cell-sub', sub);
  wrap.append(a,b);
  return wrap;
}

function makeIdChip(label, value){
  const a = document.createElement('a');
  a.className = 'id-chip';
  a.href = 'javascript:void(0)';
  a.addEventListener('click', ()=>{
    const input = $('#smartSearch');
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  });
  const tag = el('span','id-tag', label);
  a.appendChild(tag);
  a.appendChild(document.createTextNode(' ' + value));
  return a;
}

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = normalizeDigits(k.csb_nummer) || '-';
  const sap = normalizeDigits(k.sap_nummer) || '-';
  const plz = normalizeDigits(k.postleitzahl) || '-';

  /* CSB / SAP als gelbe Pills (click -> Suche) */
  const td1 = document.createElement('td');
  const wrap1 = el('div','cell');
  const top1 = el('div','cell-top'); top1.appendChild(makeIdChip('CSB', csb));
  const sub1 = el('div','cell-sub'); sub1.appendChild(makeIdChip('SAP', sap));
  wrap1.append(top1, sub1);
  td1.appendChild(wrap1); tr.appendChild(td1);

  /* Name / Straße */
  const td2 = document.createElement('td');
  td2.appendChild(twoLineCell(k.name || '-', k.strasse || '-'));
  tr.appendChild(td2);

  /* PLZ / Ort */
  const td3 = document.createElement('td');
  td3.appendChild(twoLineCell(plz, k.ort || '-'));
  tr.appendChild(td3);

  /* Schlüssel / Touren (Tour-Pills rot) */
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
    tb.onclick=()=>{ $('#smartSearch').value = tnum; onSmart(); };
    tours.appendChild(tb);
  });
  toursWrap.appendChild(toursLabel);
  toursWrap.appendChild(tours);

  wrap4.append(keyLine, divider, toursWrap);
  td4.appendChild(wrap4);
  tr.appendChild(td4);

  /* Fachberater / Markt-Telefon (Pills klickbar) */
  const td5 = document.createElement('td');
  const top5 = el('div','cell-top', k.fachberater || '-');
  const sub5 = el('div','cell-sub phone-line');
  if (k.fb_phone){
    sub5.appendChild(makePhoneChip('FB', k.fb_phone, 'chip-fb'));
  }
  if (k.market_phone){
    sub5.appendChild(makePhoneChip('Markt', k.market_phone, 'chip-market'));
  }
  if (!k.fb_phone && !k.market_phone){ sub5.textContent='-'; }
  const wrap5 = el('div','cell'); wrap5.append(top5, sub5);
  td5.appendChild(wrap5); tr.appendChild(td5);

  /* Aktion */
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
  const scroller = $('#tableScroller');
  body.innerHTML='';
  if(list.length){
    list.forEach(k=> body.appendChild(rowFor(k)));
    scroller.style.display='block';
  } else {
    scroller.style.display='none';
  }
}

/* Banner */
function renderTourTop(list, query, isExact){
  const wrap = $('#tourWrap'), title = $('#tourTitle'), extra = $('#tourExtra');
  if(!list.length){ wrap.style.display='none'; title.textContent=''; extra.textContent=''; return; }
  if (query.startsWith('Schluessel ')) {
    const key = query.replace(/^Schluessel\\s+/, '');
    title.textContent = 'Schluessel ' + key + ' - ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');
  } else {
    title.textContent = (isExact?('Tour '+query):('Tour-Prefix '+query+'*')) + ' - ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');
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
function normDE_js(s){
  if(!s) return '';
  let x = s.toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
  return x.replace(/\\s+/g,' ').trim();
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
  const qN = normDE_js(qRaw);
  const results = allCustomers.filter(k=>{
    const fb = k.fachberater || '';
    const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||''));
    return normDE_js(text).includes(qN);
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
function debounce(fn, d=160){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData!=='undefined' && Object.keys(tourkundenData).length>0){ buildData(); }
  document.getElementById('smartSearch').addEventListener('input', debounce(onSmart, 160));
  document.getElementById('keySearch').addEventListener('input', debounce(onKey, 160));
  document.getElementById('btnReset').addEventListener('click', ()=>{
    document.getElementById('smartSearch').value=''; document.getElementById('keySearch').value='';
    closeTourTop(); renderTable([]);
  });
});
</script>
</body>
</html>
"""

# =========================
#  STREAMLIT APP
# =========================
st.title("Kunden-Suchseite – klickbare Telefon- & ID-Pills, rote Tour-Pills")
st.caption("CSB/SAP als gelbe Pills (klickbar) • Tour-Pills rot • Telefon-Pills öffnen ProCall (callto:).")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png","jpg","jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater-CSB-Zuordnung (A=Fachberater, I=CSB, O=Telefon/Markt)", type=["xlsx"])

def normalize_digits_py(v) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip().replace(".0", "")
    s = "".join(ch for ch in s if ch.isdigit())
    if not s:
        return ""
    s = s.lstrip("0")
    return s if s else "0"

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

def norm_de_py(s: str) -> str:
    if not s: return ""
    x = s.lower().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    x = unicodedata.normalize("NFD", x)
    x = "".join(ch for ch in x if unicodedata.category(ch) != "Mn")
    return " ".join(x.split())

def build_berater_map(df: pd.DataFrame) -> dict:
    """Vorname A, Nachname B, Nummer C  -> 'vorname nachname' -> nummer"""
    mapping = {}
    for _, row in df.iterrows():
        v = str(row.iloc[0]) if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        n = str(row.iloc[1]) if df.shape[1] > 1 and not pd.isna(row.iloc[1]) else ""
        t = str(row.iloc[2]) if df.shape[1] > 2 and not pd.isna(row.iloc[2]) else ""
        key = norm_de_py((v + " " + n).strip())
        if key:
            mapping[key] = t.strip()
    return mapping

def build_berater_csb_map(df: pd.DataFrame) -> dict:
    """A=Fachberater (Name), I=CSB, O=Telefon/Markt  -> CSB -> {name, telefon}"""
    mapping = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]) if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]) if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        if csb:
            mapping[csb] = {"name": fach.strip(), "telefon": tel.strip()}
    return mapping

def to_data_url(file) -> str:
    mime = file.type or ("image/png" if file.name.lower().endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(file.read()).decode("utf-8")

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
                with st.spinner("Lese Fachberater-Telefonliste..."):
                    try: bf = pd.read_excel(berater_file, sheet_name=0, header=0)
                    except Exception:
                        berater_file.seek(0); bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("Lese Fachberater-CSB-Zuordnung..."):
                    try: bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=0)
                    except Exception:
                        berater_csb_file.seek(0); bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=None)
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

            with st.spinner("Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours       = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0))
            final_html = (HTML_TEMPLATE
                .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
                .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
                .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
                .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
                .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            total_customers = sum(len(v) for v in sorted_tours.values())
            m1,m2,m3 = st.columns(3)
            with m1: st.metric("Touren", len(sorted_tours))
            with m2: st.metric("Kunden", total_customers)
            with m3: st.metric("Schlüssel (Mapping)", len(key_map))

            st.download_button(
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="suche_pills_klickbar.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
