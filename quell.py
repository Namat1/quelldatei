import streamlit as st
import pandas as pd
import json

# --- HTML: Listenansicht mit fester Tour-Uebersicht oben und Kundenliste darunter ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kunden-Suche</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{
      --ral-1021:#F3DA0B;--ral-5010:#0E294B;
      --ral-1021-light:#F8E555;--ral-5010-light:#1E3A5F;
      --ral-1021-soft:rgba(243,218,11,.08);--ral-5010-soft:rgba(14,41,75,.06);
      --bg:#f5f6f8;--surface:#fff;--surface-alt:#fafbfc;--border:#e5e7eb;
      --txt:#2c3e50;--muted:#6b7280;--shadow:0 6px 18px rgba(0,0,0,.06);
      --shadow2:0 10px 30px rgba(0,0,0,.12);
    }
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(135deg,#f8fafc 0%,#e2e8f0 100%);color:var(--txt);font-size:14px;line-height:1.45}
    .page{min-height:100vh;display:flex;justify-content:center;padding:18px}
    .container{width:100%;max-width:1400px}
    .card{background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow);overflow:hidden}
    .header{padding:14px 16px;border-bottom:1px solid var(--border);background:linear-gradient(135deg,var(--ral-5010) 0%,var(--ral-5010-light) 100%);color:#fff}
    .title{font-size:18px;font-weight:800;text-align:center}
    .searchbar{padding:12px 16px;background:var(--surface);display:grid;grid-template-columns:1fr 280px auto;gap:10px;align-items:center;border-bottom:1px solid var(--border)}
    @media(max-width:900px){.searchbar{grid-template-columns:1fr;}}
    .field{display:grid;grid-template-columns:86px 1fr;gap:8px;align-items:center}
    .label{font-weight:700;color:#e6ebf5}
    .label.dark{color:#334155}
    .input{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:linear-gradient(135deg,var(--surface) 0%,var(--surface-alt) 100%);transition:border-color .2s,box-shadow .2s}
    .input:focus{outline:none;border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,.12);background:#fff}
    .btn{padding:10px 14px;border:1px solid var(--border);background:#fff;border-radius:10px;cursor:pointer;font-weight:700}
    .btn:hover{background:#f3f4f6}
    .btn-danger{background:#dc3545;border-color:#dc3545;color:#fff}
    .btn-danger:hover{background:#c82333}
    .content{display:grid;grid-template-columns:320px 1fr;gap:10px;padding:12px 16px}
    @media(max-width:1100px){.content{grid-template-columns:1fr}}
    .sidebar{display:flex;flex-direction:column;gap:10px}
    .box{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden}
    .box-head{padding:8px 12px;font-weight:800;color:var(--ral-5010);background:linear-gradient(135deg,var(--ral-5010-soft) 0%,var(--surface-alt) 100%);border-bottom:1px solid var(--border)}
    .box-body{padding:8px 10px;max-height:300px;overflow:auto}
    .fb-item{display:grid;grid-template-columns:1fr auto;gap:6px;padding:6px 8px;border-bottom:1px solid #f2f4f7;font-size:12px;cursor:pointer}
    .fb-item:hover{background:linear-gradient(135deg,var(--ral-1021-soft) 0%,var(--surface-alt) 100%)}
    .fb-count{background:#6b7280;color:#fff;border-radius:999px;font-size:11px;padding:2px 8px}
    /* Tour uebersicht oben */
    .tour-wrap{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 12px;margin-bottom:10px}
    .tour-header{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px}
    .tour-title{font-weight:800;color:var(--ral-5010)}
    .tour-stats{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
    .tour-list{border:1px solid var(--border);border-radius:8px;overflow:hidden}
    .tour-row{display:grid;grid-template-columns:90px 110px 1fr 40px;gap:8px;padding:8px 10px;border-bottom:1px solid #f1f5f9;align-items:center;font-size:12px}
    .tour-row:nth-child(odd){background:#fbfdff}
    .tour-row:hover{background:#f3f7ff}
    .csb-link{font-weight:800;color:var(--ral-5010);cursor:pointer}
    .key-badge{background:#fff3cd;border:1px solid #ffeaa7;color:#856404;border-radius:999px;padding:2px 8px;font-weight:800;font-size:12px;display:inline-block}
    .maps-link{justify-self:end;text-decoration:none;background:linear-gradient(135deg,var(--ral-1021) 0%,var(--ral-1021-light) 100%);color:var(--ral-5010);font-weight:800;padding:3px 6px;border-radius:6px}
    .maps-link:hover{box-shadow:0 2px 8px rgba(243,218,11,.4)}
    /* Kundenliste Tabelle */
    .table-wrap{background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden}
    .scroller{max-height:67vh;overflow:auto}
    table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px}
    thead th{position:sticky;top:0;background:#f8fafc;border-bottom:1px solid var(--border);padding:11px 10px;font-weight:800;color:#334155;white-space:nowrap;z-index:1}
    tbody td{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:middle}
    tbody tr:nth-child(odd){background:#fcfdff}
    tbody tr:hover{background:#f3f7ff}
    .tour-btn{display:inline-block;background:#fff;border:1px solid #22c55e;color:#16a34a;padding:2px 8px;margin:2px;border-radius:999px;font-weight:700;font-size:11px;cursor:pointer}
    .tour-btn:hover{background:#22c55e;color:#fff}
  </style>
</head>
<body>
  <div class="page">
    <div class="container">
      <div class="card">
        <div class="header">
          <div class="title">Kunden-Suche</div>
        </div>

        <!-- Searchbar -->
        <div class="searchbar" id="searchbar">
          <div class="field">
            <div class="label dark">Suche</div>
            <input class="input" id="smartSearch" placeholder="Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1-4 Ziffern)">
          </div>
          <div class="field">
            <div class="label dark">Schluessel</div>
            <input class="input" id="keySearch" placeholder="Exakte Schluesselnummer">
          </div>
          <div style="display:flex;gap:8px;justify-content:flex-end">
            <button class="btn" id="btnFB">Fachberater</button>
            <button class="btn btn-danger" id="btnReset">Zuruecksetzen</button>
          </div>
        </div>

        <div class="content">
          <!-- Sidebar -->
          <div class="sidebar">
            <div class="box" id="fbBox" style="display:none;">
              <div class="box-head">Fachberater <span id="fbCount" style="font-weight:600;color:#6b7280"></span></div>
              <div class="box-body" id="fbList"></div>
            </div>
          </div>

          <!-- Main -->
          <div>
            <!-- Tour-Listenuebersicht (oben) -->
            <div class="tour-wrap" id="tourWrap" style="display:none;">
              <div class="tour-header">
                <div class="tour-title" id="tourTitle"></div>
                <div class="tour-stats" id="tourStats"></div>
              </div>
              <div class="tour-list" id="tourList"></div>
            </div>

            <!-- Kundenliste -->
            <div class="table-wrap">
              <div class="scroller" id="tableScroller" style="display:none;">
                <table>
                  <thead>
                    <tr>
                      <th>CSB</th>
                      <th>SAP</th>
                      <th>Name</th>
                      <th>Strasse</th>
                      <th>PLZ</th>
                      <th>Ort</th>
                      <th>Schluessel</th>
                      <th>Touren</th>
                      <th>Fachberater</th>
                      <th>Aktion</th>
                    </tr>
                  </thead>
                  <tbody id="tableBody"></tbody>
                </table>
              </div>
              <div id="welcome" style="padding:40px 16px;text-align:center;color:#6b7280">
                <h3 style="margin-bottom:6px;color:#334155">Willkommen</h3>
                <div>Tippe Tour (1-4 Ziffern) oder Text. Rechts: exakte Schluesselsuche.</div>
              </div>
            </div>
          </div>
        </div> <!-- content -->
      </div>
    </div>
  </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt
const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];
let fbIndex = {};

function buildData(){
  const map = new Map();
  for(const [tour, list] of Object.entries(tourkundenData)){
    list.forEach(k=>{
      const key = k.csb_nummer;
      if(!key) return;
      if(!map.has(key)) map.set(key, {...k, touren: []});
      map.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
  // Fachberater index
  fbIndex = {};
  allCustomers.forEach(k=>{
    const fb = (k.fachberater||'').trim();
    if(!fb) return;
    fbIndex[fb] = fbIndex[fb] || [];
    fbIndex[fb].push(k);
  });
}

function cs(v){ return (v||'').toString().replace(/\\.0$/,'') || '-'; }

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = cs(k.csb_nummer), sap = cs(k.sap_nummer), plz = cs(k.postleitzahl);
  const tdCSB = document.createElement('td');
  const b = el('span','csb-link',csb); b.onclick=()=>{ $('#smartSearch').value = csb; onSmart(); };
  tdCSB.appendChild(b);
  tr.appendChild(tdCSB);
  const tdSAP = el('td','',sap); tr.appendChild(tdSAP);
  tr.appendChild(el('td','',k.name||'-'));
  tr.appendChild(el('td','',k.strasse||'-'));
  tr.appendChild(el('td','',plz));
  tr.appendChild(el('td','',k.ort||'-'));
  const tdKey = document.createElement('td');
  if(k.schluessel){ tdKey.appendChild(el('span','key-badge',k.schluessel)); } else { tdKey.textContent='-'; }
  tr.appendChild(tdKey);
  const tdTours = document.createElement('td');
  (k.touren||[]).forEach(t=>{
    const tb = el('span','tour-btn',t.tournummer+' ('+t.liefertag.substring(0,2)+')');
    tb.onclick=()=>{ $('#smartSearch').value = t.tournummer; onSmart(); };
    tdTours.appendChild(tb);
  });
  tr.appendChild(tdTours);
  tr.appendChild(el('td','',k.fachberater||'-'));
  const tdAct = document.createElement('td');
  const maps = document.createElement('a');
  maps.className='maps-link';
  maps.textContent='Map';
  maps.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||''));
  maps.target='_blank';
  tdAct.appendChild(maps);
  tr.appendChild(tdAct);
  return tr;
}

function renderTable(list, emptyMsg){
  const body = $('#tableBody'), scroller = $('#tableScroller'), welcome = $('#welcome');
  body.innerHTML='';
  if(list.length){
    list.forEach(k=> body.appendChild(rowFor(k)));
    scroller.style.display='block';
    welcome.style.display='none';
  } else {
    scroller.style.display='none';
    welcome.style.display='block';
    welcome.innerHTML = '<h3 style="margin-bottom:6px;color:#334155">Keine Ergebnisse</h3><div>'+ (emptyMsg||'Keine Kunden gefunden') +'</div>';
  }
}

function renderTourTop(list, query, isExact){
  const wrap = $('#tourWrap'), title = $('#tourTitle'), stats = $('#tourStats'), listBox = $('#tourList');
  if(!list.length){ wrap.style.display='none'; listBox.innerHTML=''; stats.innerHTML=''; title.textContent=''; return; }
  // Build stats
  const dayCount = {};
  const toursSeen = new Set();
  list.forEach(k => (k.touren||[]).forEach(t=>{
    if(t.tournummer.startsWith(query)){ dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1; toursSeen.add(t.tournummer); }
  }));
  title.textContent = (isExact ? 'Tour ' + query : 'Tour-Prefix ' + query + '*') + ' – ' + list.length + ' Kunden';
  stats.innerHTML = Object.entries(dayCount).map(([d,c])=>'<span><b>'+d+':</b> '+c+'</span>').join('') + (isExact?'':'<span><b>Touren:</b> '+toursSeen.size+'</span>');
  // List rows
  listBox.innerHTML='';
  // Sort by CSB
  const sorted = list.slice().sort((a,b)=> (parseInt(cs(a.csb_nummer))||0) - (parseInt(cs(b.csb_nummer))||0));
  sorted.forEach(k=>{
    const csb = cs(k.csb_nummer), plz = cs(k.postleitzahl);
    const murl = 'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||''));
    const row = el('div','tour-row');
    const csbLink = el('span','csb-link', csb); csbLink.onclick=()=>{ $('#smartSearch').value = csb; onSmart(); };
    row.appendChild(csbLink);
    row.appendChild(el('span','', k.schluessel ? 'S: '+k.schluessel : 'S: -'));
    row.appendChild(el('span','', (k.name||'-')));
    const a = document.createElement('a'); a.className='maps-link'; a.textContent='Map'; a.href=murl; a.target='_blank';
    row.appendChild(a);
    listBox.appendChild(row);
  });
  wrap.style.display='block';
}

function closeTourTop(){
  $('#tourWrap').style.display='none';
  $('#tourList').innerHTML=''; $('#tourStats').innerHTML=''; $('#tourTitle').textContent='';
}

function onSmart(){
  const qRaw = $('#smartSearch').value.trim();
  const q = qRaw.toLowerCase();
  closeTourTop();
  // side boxes
  $('#fbBox').style.display='none';
  // Matching
  if(!q){
    renderTable([], ''); return;
  }
  const isDigits = /^\\d{1,4}$/.test(qRaw);
  let results = [];
  if(isDigits){
    const exact = qRaw.length===4;
    results = allCustomers.filter(k => (k.touren||[]).some(t => t.tournummer.startsWith(qRaw)));
    renderTourTop(results, qRaw, exact);
    renderTable(results, 'Keine Treffer fuer Tour'+(exact?'':'-Prefix')+' "'+qRaw+'"');
  } else {
    // fachberater box trigger (optional, ab 3 chars)
    if(q.length>=3){
      const matches = Object.keys(fbIndex).filter(nm => nm.toLowerCase().includes(q));
      if(matches.length===1){
        const name = matches[0];
        const list = fbIndex[name] || [];
        const fbBox = $('#fbBox'), fbList = $('#fbList'), fbCount = $('#fbCount');
        fbList.innerHTML='';
        list.slice().sort((a,b)=> (parseInt(cs(a.csb_nummer))||0) - (parseInt(cs(b.csb_nummer))||0)).forEach(k=>{
          const csb = cs(k.csb_nummer), plz = cs(k.postleitzahl);
          const row = document.createElement('div'); row.className='fb-item';
          const left = document.createElement('div'); left.innerHTML = '<b>'+csb+'</b> &middot; '+(k.name||'-');
          left.onclick=()=>{ $('#smartSearch').value = csb; onSmart(); };
          const right = document.createElement('div');
          const m = document.createElement('a'); m.className='maps-link'; m.textContent='Map';
          m.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||'')); m.target='_blank';
          right.appendChild(m);
          row.append(left,right);
          fbList.appendChild(row);
        });
        fbCount.textContent = ' ('+list.length+')';
        fbBox.style.display='block';
      }
    }
    results = allCustomers.filter(k=>{
      const txt = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+k.fachberater+' '+(k.schluessel||'')).toLowerCase();
      return txt.includes(q);
    });
    renderTable(results, 'Keine Kunden fuer "'+qRaw+'" gefunden');
  }
}

function onKey(){
  const q = $('#keySearch').value.trim();
  closeTourTop();
  $('#fbBox').style.display='none';
  if(!q){ renderTable([], ''); return; }
  const results = allCustomers.filter(k => (k.schluessel||'') === q);
  if(results.length){
    renderTourTop(results, 'Schluessel '+q, true);
  }
  renderTable(results, 'Kein Kunde mit Schluessel "'+q+'" gefunden');
}

function debounce(fn, d=200){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length>0){
    buildData();
  } else {
    document.getElementById('welcome').innerHTML = '<h3 style="margin-bottom:6px;color:#334155">Fehler</h3><div>Keine Kundendaten geladen</div>';
  }
  document.getElementById('smartSearch').addEventListener('input', debounce(onSmart, 160));
  document.getElementById('keySearch').addEventListener('input', debounce(onKey, 160));
  document.getElementById('btnReset').addEventListener('click', ()=>{
    document.getElementById('smartSearch').value=''; document.getElementById('keySearch').value='';
    closeTourTop(); document.getElementById('fbBox').style.display='none';
    renderTable([], '');
  });
  document.getElementById('btnFB').addEventListener('click', ()=>{
    const box = document.getElementById('fbBox');
    box.style.display = (box.style.display==='none'||box.style.display==='') ? 'block' : 'none';
  });
});
</script>
</body>
</html>
"""

st.title("Kunden-Suchseite (Listenansicht mit Tour-Uebersicht oben)")
st.markdown("Ein Feld fuer **Text/Tour** (1-4 Ziffern) und ein Feld fuer **exakte Schluesselnummer**. Bei Toursuche erscheint **oben** eine kompakte Uebersicht, darunter die **Kundenliste**.")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("Schluesseldatei (A=CSB, F=Schluessel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x): return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", ".")); i = int(f)
        return str(i) if f == i else s
    except Exception:
        return s

def build_key_map(key_df: pd.DataFrame) -> dict:
    if key_df.shape[1] < 6:
        st.warning("Schluesseldatei hat weniger als 6 Spalten – letzte vorhandene Spalte als Schluessel verwendet.")
    csb_col = 0
    key_col = 5 if key_df.shape[1] > 5 else key_df.shape[1] - 1
    mapping = {}
    for _, row in key_df.iterrows():
        csb = norm_str_num(row.iloc[csb_col] if key_df.shape[1] > 0 else "")
        schluessel_raw = row.iloc[key_col] if key_df.shape[1] > 0 else ""
        schluessel = "" if pd.isna(schluessel_raw) else str(schluessel_raw).strip()
        if csb:
            mapping[csb] = schluessel
    return mapping

if excel_file and key_file:
    if st.button("HTML erzeugen", type="primary"):
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        SPALTEN_MAPPING = {"csb_nummer":"Nr","sap_nummer":"SAP-Nr.","name":"Name","strasse":"Strasse","postleitzahl":"Plz","ort":"Ort","fachberater":"Fachberater"}
        LIEFERTAGE_MAPPING = {"Montag":"Mo","Dienstag":"Die","Mittwoch":"Mitt","Donnerstag":"Don","Freitag":"Fr","Samstag":"Sam"}

        try:
            with st.spinner("Lese Schluesseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            tour_dict = {}
            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns: 
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit():
                            continue
                        tournr = str(int(float(tournr_raw)))
                        eintrag = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean = norm_str_num(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        eintrag["schluessel"] = key_map.get(csb_clean, "")
                        eintrag["liefertag"] = tag
                        tour_dict.setdefault(tournr, []).append(eintrag)

            with st.spinner("Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine gueltigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0])))
            json_data_string = json.dumps(sorted_tours, indent=2, ensure_ascii=False)
            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")

            total_customers = sum(len(v) for v in sorted_tours.values())
            c1,c2,c3 = st.columns(3)
            with c1: st.metric("Touren", len(sorted_tours))
            with c2: st.metric("Kunden", total_customers)
            with c3: st.metric("Schluessel (Mapping)", len(key_map))

            st.download_button(
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="suche_liste.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei und Schluesseldatei hochladen.")
