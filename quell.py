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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f8fafc; --surface:#ffffff; --alt:#f1f5f9;
  --grid:#e2e8f0; --head-grid:#94a3b8;
  --txt:#0f172a; --muted:#64748b;

  --accent:#2563eb; --accent-2:#1d4ed8;
  --success:#10b981; --warning:#f59e0b; --danger:#ef4444;

  --pill-yellow-bg:#fef3c7; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#92400e;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#fee2e2; --pill-red-bd:#ef4444; --pill-red-tx:#991b1b;
  --pill-blue-bg:#dbeafe; --pill-blue-bd:#3b82f6; --pill-blue-tx:#1e40af;

  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;

  --radius: 6px; --radius-pill: 999px;
  --fs-10: 10px; --fs-11: 11px; --fs-12: 12px;
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:"Inter", system-ui, sans-serif;
  color:var(--txt); font-size:var(--fs-11); line-height:1.4; font-weight:500;
}

/* Layout */
.page{min-height:100vh; display:flex; justify-content:center; padding:8px}
.container{width:100%; max-width:1500px}
.card{background:var(--surface); border:1px solid var(--grid); border-radius:var(--radius); overflow:hidden}

/* Header */
.header{
  padding:8px 12px; background:linear-gradient(180deg,#ffffff 0%, #f8fafc 100%);
  display:flex; align-items:center; justify-content:center;
  border-bottom:1px solid var(--grid);
}
.brand-logo{height:48px; width:auto}

/* Search */
.searchbar{
  padding:10px 12px; background:var(--surface); border-bottom:1px solid var(--grid);
  display:grid; grid-template-columns:1fr 240px auto auto; gap:8px; align-items:end;
}
@media(max-width:1100px){.searchbar{grid-template-columns:1fr 1fr auto auto}}
@media(max-width:768px){.searchbar{grid-template-columns:1fr; gap:6px}}

.field{display:flex; flex-direction:column; gap:3px}
.label{font-weight:600; color:var(--muted); font-size:var(--fs-10); text-transform:uppercase; letter-spacing:0.3px}
.input{
  width:100%; padding:6px 10px; border:1px solid var(--grid); border-radius:var(--radius); 
  background:#fff; font-size:var(--fs-11); font-weight:500;
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 2px rgba(37,99,235,0.1)}

.btn{
  padding:6px 12px; border:1px solid var(--grid); background:#fff; 
  color:var(--txt); border-radius:var(--radius); cursor:pointer; 
  font-weight:600; font-size:var(--fs-11); white-space:nowrap;
}
.btn:hover{background:var(--alt)}
.btn-danger{border-color:var(--danger); background:var(--danger); color:#fff}
.btn-danger:hover{background:#dc2626}
.btn-back{border-color:var(--accent); color:var(--accent); background:var(--pill-blue-bg)}

/* Tour Banner */
.tour-wrap{
  display:none; padding:8px 12px; background:var(--pill-yellow-bg); 
  border-bottom:1px solid var(--warning);
}
.tour-banner{display:flex; align-items:center; justify-content:space-between; gap:10px}
.tour-pill{
  background:var(--pill-yellow-bg); color:var(--pill-yellow-tx);
  border:1px solid var(--pill-yellow-bd); border-radius:var(--radius-pill); 
  padding:4px 12px; font-weight:600; font-size:var(--fs-11);
}
.tour-stats{font-weight:500; font-size:var(--fs-10); color:var(--muted)}

/* Table */
.table-section{padding:8px 12px}
table{
  width:100%; border-collapse:separate; border-spacing:0; 
  border:1px solid var(--grid); border-radius:var(--radius); background:var(--surface);
}

thead th{
  background:linear-gradient(180deg,#f1f5f9,#e2e8f0); color:var(--txt); 
  font-weight:600; font-size:var(--fs-10); text-transform:uppercase; 
  letter-spacing:0.3px; padding:6px 8px; text-align:left;
  border-bottom:1px solid var(--head-grid); border-right:1px solid var(--grid);
}
thead th:last-child{border-right:none}

tbody td{
  padding:6px 8px; vertical-align:top; background:#fff;
  border-bottom:1px solid var(--grid); border-right:1px solid var(--grid);
}
tbody td:last-child{border-right:none}
tbody tr:nth-child(odd) td{background:#f8fafc}
tbody tr:hover td{background:#eef4ff}

/* Columns */
.col-csb{width:180px} .col-name{width:450px} .col-tours{width:200px} 
.col-key{width:80px} .col-contact{width:350px}

/* Cell Content */
.cell{display:flex; flex-direction:column; gap:2px; min-height:32px}
.cell-top,.cell-sub{
  max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.cell-top{font-weight:600; color:var(--txt)}
.cell-sub{font-size:var(--fs-10); color:var(--muted)}

.mono{font-family:"JetBrains Mono", monospace; font-weight:600}

/* Chips */
a.id-chip{
  display:inline-flex; align-items:center; gap:4px;
  background:var(--pill-yellow-bg); color:var(--pill-yellow-tx);
  border:1px solid var(--pill-yellow-bd); border-radius:var(--radius-pill); 
  padding:2px 6px; font-weight:600; font-size:var(--fs-10); 
  text-decoration:none; line-height:1;
}
a.id-chip:hover{filter:brightness(0.95)}
.id-tag{font-size:9px; font-weight:600; text-transform:uppercase; letter-spacing:0.3px}

.badge-key{
  background:var(--pill-green-bg); border:1px solid var(--pill-green-bd); 
  color:var(--pill-green-tx); border-radius:var(--radius-pill); 
  padding:2px 6px; font-weight:600; font-size:var(--fs-10);
}

.tour-inline{display:flex; flex-wrap:wrap; gap:3px}
.tour-btn{
  background:var(--pill-red-bg); border:1px solid var(--pill-red-bd); 
  color:var(--pill-red-tx); padding:2px 6px; border-radius:var(--radius-pill); 
  font-weight:600; font-size:9px; cursor:pointer; line-height:1.2;
}
.tour-btn:hover{filter:brightness(0.95)}

/* Contact */
.phone-col{display:flex; flex-direction:column; gap:3px}
a.phone-chip, a.mail-chip{
  display:inline-flex; align-items:center; gap:4px; 
  border-radius:var(--radius-pill); padding:2px 6px; 
  font-weight:600; font-size:var(--fs-10); text-decoration:none; 
  border:1px solid; max-width:100%;
}
a.phone-chip.chip-fb{background:var(--chip-fb-bg); color:var(--chip-fb-tx); border-color:var(--chip-fb-bd)}
a.phone-chip.chip-market{background:var(--chip-mk-bg); color:var(--chip-mk-tx); border-color:var(--chip-mk-bd)}
a.mail-chip{background:#ecfdf5; color:#065f46; border-color:#10b981}
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(0.95)}

.chip-tag{font-size:9px; font-weight:600; text-transform:uppercase; letter-spacing:0.3px}
.mail-chip .txt{white-space:normal; word-break:break-all; line-height:1.2}

a.addr-chip{
  display:inline-flex; align-items:center; gap:4px; max-width:100%;
  background:var(--pill-blue-bg); color:var(--pill-blue-tx); 
  border:1px solid var(--pill-blue-bd); border-radius:var(--radius-pill); 
  padding:2px 6px; text-decoration:none; font-weight:600; font-size:var(--fs-10);
}
.addr-chip:hover{filter:brightness(0.95)}
.addr-chip .txt{white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.addr-dot{width:4px; height:4px; background:var(--danger); border-radius:50%}

/* Mobile */
@media(max-width:768px){
  table,thead,tbody,th,td,tr{display:block}
  thead tr{position:absolute; top:-9999px; left:-9999px}
  tbody tr{border:1px solid var(--grid); margin-bottom:8px; border-radius:var(--radius); padding:8px}
  tbody td{border:none!important; padding:4px 0!important; position:relative; padding-left:25%!important}
  tbody td:before{
    content:attr(data-label)": "; position:absolute; left:0; top:4px; width:20%;
    font-weight:600; color:var(--muted); font-size:var(--fs-10); text-transform:uppercase;
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
          <input class="input" id="smartSearch" placeholder="Name, Ort, CSB, SAP, Tour, Fachberater...">
        </div>
        <div class="field">
          <div class="label">Schlüssel</div>
          <input class="input" id="keySearch" placeholder="exakt (z.B. 40)">
        </div>
        <button class="btn btn-back" id="btnBack" style="display:none;">← Zurück</button>
        <button class="btn btn-danger" id="btnReset">Reset</button>
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
            <col class="col-csb"><col class="col-name"><col class="col-tours">
            <col class="col-key"><col class="col-contact">
          </colgroup>
          <thead>
            <tr>
              <th>CSB / SAP</th><th>Name / Adresse</th><th>Touren</th>
              <th>Schlüssel</th><th>Kontakt</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
const tourkundenData={}, keyIndex={}, beraterIndex={}, beraterCSBIndex={};

const $=s=>document.querySelector(s);
const el=(t,c,txt)=>{const n=document.createElement(t); if(c)n.className=c; if(txt!==undefined)n.textContent=txt; return n;};

let allCustomers=[], prevQuery=null;
const DIAL_SCHEME='tel';

function sanitizePhone(num){return (num||'').toString().trim().replace(/[^\\d+]/g,'');}
function normDE(s){
  if(!s)return'';
  let x=s.toLowerCase();
  x=x.replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x=x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
  return x.replace(/\\s+/g,' ').trim();
}
function normalizeDigits(v){
  if(v==null)return'';
  let s=String(v).trim().replace(/\\.0$/,'');
  s=s.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1');
  return s;
}
function normalizeNameKey(s){
  if(!s)return'';
  let x=s.replace(/[\\u200B-\\u200D\\uFEFF]/g,'').replace(/\\u00A0/g,' ').replace(/[–—]/g,'-').toLowerCase();
  x=x.replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x=x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/\\(.*?\\)/g,' ');
  x=x.replace(/[./,;:+*_#|]/g,' ').replace(/-/g,' ').replace(/[^a-z\\s]/g,' ').replace(/\\s+/g,' ').trim();
  return x;
}
function nameVariants(s){
  const base=normalizeNameKey(s); if(!base)return[];
  const parts=base.split(' ').filter(Boolean);
  const out=new Set([base]);
  if(parts.length>=2){const f=parts[0],l=parts[parts.length-1]; out.add(`${f} ${l}`); out.add(`${l} ${f}`);}
  return Array.from(out);
}
function fbEmailFromName(name){
  const parts=normalizeNameKey(name).split(' ').filter(Boolean);
  if(parts.length<2)return'';
  const vor=parts[0],nach=parts[parts.length-1];
  return `${vor}.${nach}@edeka.de`.replace(/\s+/g,'');
}
function pickBeraterPhone(name){
  if(!name)return'';
  const variants=nameVariants(name);
  for(const v of variants){if(beraterIndex[v])return beraterIndex[v];}
  const keys=Object.keys(beraterIndex);
  for(const v of variants){
    const parts=v.split(' ').filter(Boolean);
    for(const k of keys){if(parts.every(p=>k.includes(p)))return beraterIndex[k];}
  }
  return'';
}
function dedupByCSB(list){
  const seen=new Set(),out=[];
  for(const k of list){const csb=normalizeDigits(k.csb_nummer); if(!seen.has(csb)){seen.add(csb); out.push(k);}}
  return out;
}

function buildData(){
  console.log('Building data...');
  console.log('beraterIndex:', beraterIndex);
  console.log('beraterCSBIndex:', beraterCSBIndex);
  
  const map=new Map();
  for(const[tour,list]of Object.entries(tourkundenData)){
    const tourN=normalizeDigits(tour);
    list.forEach(k=>{
      const csb=normalizeDigits(k.csb_nummer); if(!csb)return;
      if(!map.has(csb)){
        const rec={...k};
        rec.csb_nummer=csb;
        rec.sap_nummer=normalizeDigits(rec.sap_nummer);
        rec.postleitzahl=normalizeDigits(rec.postleitzahl);
        rec.touren=[];
        rec.schluessel=normalizeDigits(rec.schluessel)||(keyIndex[csb]||'');
        
        // Fachberater aus beraterCSBIndex
        if(beraterCSBIndex[csb]&&beraterCSBIndex[csb].name){
          rec.fachberater=beraterCSBIndex[csb].name;
        }
        
        // Fachberater Telefon aus beraterIndex
        rec.fb_phone=rec.fachberater?pickBeraterPhone(rec.fachberater):'';
        
        // Markt Telefon und Email aus beraterCSBIndex
        rec.market_phone=(beraterCSBIndex[csb]&&beraterCSBIndex[csb].telefon)?beraterCSBIndex[csb].telefon:'';
        rec.market_email=(beraterCSBIndex[csb]&&beraterCSBIndex[csb].email)?beraterCSBIndex[csb].email:'';
        
        console.log('Customer',csb,'- FB:',rec.fachberater,'FB-Phone:',rec.fb_phone,'Market-Phone:',rec.market_phone,'Market-Email:',rec.market_email);
        
        map.set(csb,rec);
      }
      map.get(csb).touren.push({tournummer:tourN,liefertag:k.liefertag});
    });
  }
  allCustomers=Array.from(map.values());
  console.log('Total customers:',allCustomers.length);
}

function pushPrevQuery(){const v=$('#smartSearch').value.trim(); if(v){prevQuery=v; $('#btnBack').style.display='inline-block';}}
function popPrevQuery(){if(prevQuery){$('#smartSearch').value=prevQuery; prevQuery=null; $('#btnBack').style.display='none'; onSmart();}}

function makePhoneChip(label,num,cls){
  if(!num)return null;
  const a=document.createElement('a');
  a.className='phone-chip '+cls;
  a.href=`${DIAL_SCHEME}:${sanitizePhone(num)}`;
  a.append(el('span','chip-tag',label),el('span','mono',' '+num));
  return a;
}
function makeMailChip(label,addr){
  if(!addr)return null;
  const a=document.createElement('a');
  a.className='mail-chip';
  a.href=`mailto:${addr}`;
  const txt=document.createElement('span'); txt.className='txt mono'; txt.textContent=' '+addr;
  a.append(el('span','chip-tag',label),txt);
  return a;
}
function makeIdChip(label,value){
  const a=document.createElement('a'); a.className='id-chip'; a.href='javascript:void(0)'; a.title=label+' '+value+' suchen';
  a.addEventListener('click',()=>{pushPrevQuery(); $('#smartSearch').value=value; onSmart();});
  a.append(el('span','id-tag',label),el('span','mono',' '+value)); return a;
}
function makeAddressChip(name,strasse,plz,ort){
  const txt=`${strasse||''}, ${plz||''} ${ort||''}`.replace(/^,\\s*/,'').trim();
  const url='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(`${name||''}, ${txt}`);
  const a=document.createElement('a'); a.className='addr-chip'; a.href=url; a.target='_blank'; a.title='Adresse in Google Maps öffnen';
  const txtSpan=document.createElement('span'); txtSpan.className='txt'; txtSpan.textContent=' '+txt;
  a.append(el('span','addr-dot',''),el('span','chip-tag','Adresse'),txtSpan);
  return a;
}

function rowFor(k){
  const tr=document.createElement('tr');
  const csb=k.csb_nummer||'-',sap=k.sap_nummer||'-',plz=k.postleitzahl||'-';

  const td1=document.createElement('td'); td1.setAttribute('data-label','CSB / SAP');
  const c1=el('div','cell');
  const l1=el('div','cell-top'); l1.appendChild(makeIdChip('CSB',csb));
  const l2=el('div','cell-sub'); l2.appendChild(makeIdChip('SAP',sap));
  c1.append(l1,l2); td1.append(c1); tr.append(td1);

  const td2=document.createElement('td'); td2.setAttribute('data-label','Name / Adresse');
  const c2=el('div','cell');
  c2.append(el('div','cell-top',k.name||'-'));
  const addrPill=makeAddressChip(k.name||'',k.strasse||'',plz,k.ort||'');
  const line2=el('div','cell-sub'); line2.appendChild(addrPill);
  c2.append(line2); td2.append(c2); tr.append(td2);

  const td3=document.createElement('td'); td3.setAttribute('data-label','Touren');
  const c3=el('div','cell'); const tours=el('div','tour-inline');
  (k.touren||[]).forEach(t=>{const tnum=(t.tournummer||''); const b=el('span','tour-btn',tnum+' ('+t.liefertag.substring(0,2)+')'); b.title='Tour '+tnum; b.onclick=()=>{pushPrevQuery(); $('#smartSearch').value=tnum; onSmart();}; tours.appendChild(b);});
  c3.appendChild(tours); td3.appendChild(c3); tr.append(td3);

  const td4=document.createElement('td'); td4.setAttribute('data-label','Schlüssel');
  const key=(k.schluessel||'')||(keyIndex[csb]||'');
  td4.appendChild(key?el('span','badge-key',key):el('span','','-')); tr.append(td4);

  const td5=document.createElement('td'); td5.setAttribute('data-label','Kontakt');
  const col=el('div','phone-col');
  
  // Debug: Log contact data for this customer
  console.log('Contact data for customer', csb, ':', {
    fachberater: k.fachberater,
    fb_phone: k.fb_phone,
    market_phone: k.market_phone,
    market_email: k.market_email
  });
  
  const fbPhone=k.fb_phone;
  const fbMail=k.fachberater?fbEmailFromName(k.fachberater):'';
  const mkPhone=k.market_phone;
  const mkMail=k.market_email||'';
  
  const p1=makePhoneChip('FB',fbPhone,'chip-fb'); if(p1)col.appendChild(p1);
  const m1=makeMailChip('FB Mail',fbMail); if(m1)col.appendChild(m1);
  const p2=makePhoneChip('Markt',mkPhone,'chip-market'); if(p2)col.appendChild(p2);
  const m2=makeMailChip('Mail',mkMail); if(m2)col.appendChild(m2);
  
  if(!col.childNodes.length)col.textContent='-';
  td5.appendChild(col); tr.append(td5);

  return tr;
}

function renderTable(list){
  const body=$('#tableBody'),tbl=$('#resultTable'); body.innerHTML='';
  if(list.length){list.forEach(k=>body.appendChild(rowFor(k))); tbl.style.display='table';}else{tbl.style.display='none';}
}

function renderTourTop(list,query,isExact){
  const wrap=$('#tourWrap'),title=$('#tourTitle'),extra=$('#tourExtra');
  if(!list.length){wrap.style.display='none'; title.textContent=''; extra.textContent=''; return;}
  if(query.startsWith('Schluessel ')){const key=query.replace(/^Schluessel\\s+/,''); title.textContent='Schlüssel '+key+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden');}
  else{title.textContent=(isExact?('Tour '+query):('Tour-Prefix '+query+'*'))+' — '+list.length+' '+(list.length===1?'Kunde':'Kunden');}
  const dayCount={}; list.forEach(k=>(k.touren||[]).forEach(t=>{const tnum=t.tournummer||''; const cond=isExact?(tnum===query):tnum.startsWith(query.replace('Schluessel ','')); if(cond||query.startsWith('Schluessel ')){dayCount[t.liefertag]=(dayCount[t.liefertag]||0)+1;}}));
  extra.textContent=Object.entries(dayCount).sort().map(([d,c])=>d+': '+c).join('  •  ');
  wrap.style.display='block';
}
function closeTourTop(){$('#tourWrap').style.display='none'; $('#tourTitle').textContent=''; $('#tourExtra').textContent='';}

function onSmart(){
  const qRaw=$('#smartSearch').value.trim(); closeTourTop(); if(!qRaw){renderTable([]); return;}
  if(/^\\d{1,3}$/.test(qRaw)){const n=qRaw.replace(/^0+(\\d)/,'$1'); const r=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'').startsWith(n))); renderTourTop(r,n,false); renderTable(r); return;}
  if(/^\\d{4}$/.test(qRaw)){
    const n=qRaw.replace(/^0+(\\d)/,'$1'); const tr=allCustomers.filter(k=>(k.touren||[]).some(t=>(t.tournummer||'')===n)); const cr=allCustomers.filter(k=>(k.csb_nummer||'')===n); const r=dedupByCSB([...tr,...cr]);
    if(tr.length)renderTourTop(tr,n,true); else closeTourTop(); renderTable(r); return;
  }
  const q=normDE(qRaw);
  const r=allCustomers.filter(k=>{const fb=k.fachberater||''; const text=(k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+fb+' '+(k.schluessel||'')+' '+(k.fb_phone||'')+' '+(k.market_phone||'')+' '+(k.market_email||'')); return normDE(text).includes(q);});
  renderTable(r);
}
function onKey(){
  const q=$('#keySearch').value.trim(); closeTourTop(); if(!q){renderTable([]); return;}
  const n=q.replace(/[^0-9]/g,'').replace(/^0+(\\d)/,'$1'); const r=[]; for(const k of allCustomers){const key=(k.schluessel||'')||(keyIndex[k.csb_nummer]||''); if(key===n)r.push(k);}
  if(r.length)renderTourTop(r,'Schluessel '+n,true); renderTable(r);
}
function debounce(fn,d=140){let t; return(...a)=>{clearTimeout(t); t=setTimeout(()=>fn(...a),d);};}

document.addEventListener('DOMContentLoaded',()=>{
  if(Object.keys(tourkundenData).length>0){buildData();}
  $('#smartSearch').addEventListener('input',debounce(onSmart,140));
  $('#keySearch').addEventListener('input',debounce(onKey,140));
  $('#btnReset').addEventListener('click',()=>{$('#smartSearch').value=''; $('#keySearch').value=''; closeTourTop(); renderTable([]); prevQuery=null; $('#btnBack').style.display='none';});
  $('#btnBack').addEventListener('click',()=>{popPrevQuery();});
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.set_page_config(page_title="Kompakte Kunden-Suche", page_icon="🔍", layout="wide")

st.title("🔍 Kunden-Suche – Kompakt")
st.caption("Schlankes Design • Verbesserte Kontaktdaten-Verarbeitung • Optimiert für Effizienz")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with col3:
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
        st.warning(f"Schlüsseldatei hat nur {df.shape[1]} Spalten – nehme letzte vorhandene Spalte als Schlüssel.")
    csb_col = 0
    key_col = 5 if df.shape[1] > 5 else df.shape[1] - 1
    out = {}
    processed = 0
    for _, row in df.iterrows():
        csb = normalize_digits_py(row.iloc[csb_col] if df.shape[1] > 0 else "")
        key = normalize_digits_py(row.iloc[key_col] if df.shape[1] > 0 else "")
        if csb: 
            out[csb] = key
            processed += 1
    st.info(f"✅ Schlüsseldatei: {processed} Einträge verarbeitet")
    return out

def build_berater_map(df: pd.DataFrame) -> dict:
    out = {}
    processed = 0
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
                processed += 1
    st.info(f"✅ Fachberater-Telefone: {processed} Einträge verarbeitet")
    return out

def build_berater_csb_map(df: pd.DataFrame) -> dict:
    out = {}
    processed = 0
    
    # Debug: Show column info
    st.write("**Debug: Spalten in Fachberater-CSB-Datei:**")
    for i, col in enumerate(df.columns):
        st.write(f"Spalte {i} ({chr(65+i)}): {col}")
    
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        mail = str(row.iloc[23]).strip() if df.shape[1] > 23 and not pd.isna(row.iloc[23]) else ""
        
        if csb:
            out[csb] = {"name": fach, "telefon": tel, "email": mail}
            processed += 1
            
            # Debug: Show first few entries
            if processed <= 3:
                st.write(f"**Debug Entry {processed}:** CSB={csb}, Name='{fach}', Tel='{tel}', Email='{mail}'")
    
    st.info(f"✅ Fachberater-CSB-Zuordnung: {processed} Einträge verarbeitet")
    return out

def to_data_url(file) -> str:
    mime = file.type or ("image/png" if file.name.lower().endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(file.read()).decode("utf-8")

if excel_file and key_file:
    if st.button("📋 Kompakte HTML erzeugen", type="primary"):
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

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0))

            final_html = (HTML_TEMPLATE
              .replace("const tourkundenData={}", f"const tourkundenData={json.dumps(sorted_tours, ensure_ascii=False)}")
              .replace("const keyIndex={}", f"const keyIndex={json.dumps(key_map, ensure_ascii=False)}")
              .replace("const beraterIndex={}", f"const beraterIndex={json.dumps(berater_map, ensure_ascii=False)}")
              .replace("const beraterCSBIndex={}", f"const beraterCSBIndex={json.dumps(berater_csb_map, ensure_ascii=False)}")
              .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            # Statistics
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            unique_customers = len(set(k.get('csb_nummer') for customers in sorted_tours.values() for k in customers if k.get('csb_nummer')))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Touren", len(sorted_tours))
            with col2:
                st.metric("Kunden (total)", total_customers)
            with col3:
                st.metric("Kunden (unique)", unique_customers)

            st.download_button(
                "📥 Kompakte HTML herunterladen",
                data=final_html.encode("utf-8"),
                file_name="kunden_suche_kompakt.html",
                mime="text/html",
                type="primary"
            )
            
        except Exception as e:
            st.error(f"Fehler: {e}")
            st.exception(e)
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen.")
