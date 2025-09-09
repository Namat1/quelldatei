import streamlit as st
import pandas as pd
import json

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
  --bg:#f6f7f9; --surface:#ffffff; --alt:#f9fafb; --border:#e6eaf0;
  --txt:#1f2937; --muted:#6b7280; --head:#0f172a;
  --accent:#2563eb; --accent-weak:rgba(37,99,235,.12);
  --ok:#16a34a; --ok-weak:rgba(22,163,74,.12);
  --warn:#f59e0b; --warn-weak:rgba(245,158,11,.15);
  --radius:10px; --shadow:0 1px 4px rgba(0,0,0,.06);
  --fs-12:12px; --fs-13:13px; --fs-14:14px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  color:var(--txt); font-size:var(--fs-14); line-height:1.45;
}

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:16px}
.container{width:100%; max-width:1400px}
.card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); box-shadow:var(--shadow); overflow:hidden}

/* Header */
.header{padding:14px 16px; border-bottom:1px solid var(--border); background:#0b1d3a; color:#fff}
.title{font-size:16px; font-weight:700; text-align:center}

/* Searchbar */
.searchbar{
  padding:12px 16px; display:grid; grid-template-columns:1fr 280px auto; gap:10px; align-items:center;
  border-bottom:1px solid var(--border); background:var(--surface);
}
@media(max-width:960px){ .searchbar{grid-template-columns:1fr} }
.field{display:grid; grid-template-columns:86px 1fr; gap:8px; align-items:center}
.label{font-weight:600; color:#334155}
.input{
  width:100%; padding:10px 12px; border:1px solid var(--border); border-radius:var(--radius);
  background:linear-gradient(180deg, var(--surface), var(--alt));
  transition:border-color .15s, box-shadow .15s, background .15s;
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-weak); background:#fff}
.btn{padding:10px 12px; border:1px solid var(--border); background:#fff; border-radius:var(--radius); cursor:pointer; font-weight:600}
.btn:hover{background:#f3f4f6}
.btn-danger{background:#ef4444; border-color:#ef4444; color:#fff}
.btn-danger:hover{background:#dc2626}

/* Content (single column) */
.content{padding:12px 16px}

/* Tour summary (top list) */
.tour-wrap{display:none; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:10px; box-shadow:var(--shadow); margin-bottom:12px}
.tour-header{display:flex; justify-content:space-between; align-items:center; gap:10px; padding:4px 2px 8px}
.tour-title{font-weight:700; color:var(--head)}
.tour-stats{display:flex; gap:14px; flex-wrap:wrap; font-size:var(--fs-13); color:var(--muted)}
.tour-list{border:1px solid var(--border); border-radius:8px; overflow:hidden}
.tour-row{display:grid; grid-template-columns:90px 110px 1fr 60px; gap:8px; padding:8px 10px; border-bottom:1px solid #f1f5f9; align-items:center; font-size:var(--fs-13)}
.tour-row:nth-child(odd){background:#fbfdff}
.tour-row:hover{background:#f3f7ff}
.csb-link{font-weight:700; color:#0b3a8a; cursor:pointer}
.csb-link:hover{text-decoration:underline}
.key-badge{background:var(--warn-weak); border:1px solid #fcd34d; color:#92400e; border-radius:999px; padding:2px 8px; font-weight:700; font-size:var(--fs-12); display:inline-block}
.map-pill{
  justify-self:end; text-decoration:none; font-weight:700; font-size:var(--fs-12);
  padding:4px 10px; border-radius:999px; border:1px solid #e5e7eb; background:#fff; color:#374151;
}
.map-pill:hover{background:#f3f4f6}

/* Table */
.table-wrap{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden}
.scroller{max-height:68vh; overflow:auto}
table{width:100%; border-collapse:separate; border-spacing:0; font-size:var(--fs-13)}
thead th{
  position:sticky; top:0; background:#f8fafc; color:#334155; font-weight:700;
  border-bottom:1px solid var(--border); padding:11px 10px; white-space:nowrap; z-index:1
}
tbody td{padding:9px 10px; border-bottom:1px solid #f1f5f9; vertical-align:middle}
tbody tr:nth-child(odd){background:#fcfdff}
tbody tr:hover{background:#f3f7ff}
.tour-btn{
  display:inline-block; background:#fff; border:1px solid #bbf7d0; color:#065f46;
  padding:2px 8px; margin:2px 4px 2px 0; border-radius:999px; font-weight:700; font-size:var(--fs-12); cursor:pointer
}
.tour-btn:hover{background:var(--ok-weak)}
.badge-key{background:var(--warn-weak); border:1px solid #fcd34d; color:#92400e; border-radius:999px; padding:2px 8px; font-weight:700; font-size:var(--fs-12); display:inline-block}
.table-map{
  text-decoration:none; font-weight:700; font-size:var(--fs-12);
  padding:4px 10px; border-radius:999px; border:1px solid #e5e7eb; background:#fff; color:#374151;
}
.table-map:hover{background:#f3f4f6}

/* Welcome */
#welcome{padding:40px 16px; text-align:center; color:var(--muted)}
#welcome h3{margin:0 0 6px; color:#334155}

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
      <div class="header"><div class="title">Kunden-Suche</div></div>

      <!-- Search -->
      <div class="searchbar">
        <div class="field">
          <div class="label">Suche</div>
          <input class="input" id="smartSearch" placeholder="Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1-4 Ziffern)">
        </div>
        <div class="field">
          <div class="label">Schluessel</div>
          <input class="input" id="keySearch" placeholder="Exakte Schluesselnummer">
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="btn btn-danger" id="btnReset">Zuruecksetzen</button>
        </div>
      </div>

      <!-- Content (no sidebar) -->
      <div class="content">
        <!-- Tour-Top -->
        <div class="tour-wrap" id="tourWrap">
          <div class="tour-header">
            <div class="tour-title" id="tourTitle"></div>
            <div class="tour-stats" id="tourStats"></div>
          </div>
          <div class="tour-list" id="tourList"></div>
        </div>

        <!-- Table -->
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
          <div id="welcome">
            <h3>Willkommen</h3>
            <div>Tippe Tour (1-4 Ziffern) oder Text. Rechts: exakte Schluesselsuche.</div>
          </div>
        </div>
      </div> <!-- content -->
    </div>
  </div>
</div>

<script>
/* Data injection */
const tourkundenData = {  }; // wird durch Python ersetzt
const $ = s => document.querySelector(s);
const el = (t,c,txt)=>{const n=document.createElement(t); if(c) n.className=c; if(txt!==undefined) n.textContent=txt; return n;};

let allCustomers = [];

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
}

const cs = v => (v||'').toString().replace(/\\.0$/,'') || '-';

function rowFor(k){
  const tr = document.createElement('tr');
  const csb = cs(k.csb_nummer), sap = cs(k.sap_nummer), plz = cs(k.postleitzahl);

  const tdCSB = document.createElement('td');
  const b = el('span','csb-link',csb); b.onclick=()=>{ $('#smartSearch').value = csb; onSmart(); };
  tdCSB.appendChild(b); tr.appendChild(tdCSB);

  tr.appendChild(el('td','',sap));
  tr.appendChild(el('td','',k.name||'-'));
  tr.appendChild(el('td','',k.strasse||'-'));
  tr.appendChild(el('td','',plz));
  tr.appendChild(el('td','',k.ort||'-'));

  const tdKey = document.createElement('td');
  if(k.schluessel){ tdKey.appendChild(el('span','badge-key',k.schluessel)); } else { tdKey.textContent='-'; }
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
  const a = document.createElement('a');
  a.className='table-map'; a.textContent='Map';
  a.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||'')); a.target='_blank';
  tdAct.appendChild(a); tr.appendChild(tdAct);

  return tr;
}

function renderTable(list, emptyMsg){
  const body = $('#tableBody'), scroller = $('#tableScroller'), welcome = $('#welcome');
  body.innerHTML='';
  if(list.length){
    list.forEach(k=> body.appendChild(rowFor(k)));
    scroller.style.display='block'; welcome.style.display='none';
  } else {
    scroller.style.display='none'; welcome.style.display='block';
    welcome.innerHTML = '<h3>Keine Ergebnisse</h3><div>'+ (emptyMsg||'Keine Kunden gefunden') +'</div>';
  }
}

function renderTourTop(list, query, isExact){
  const wrap = $('#tourWrap'), title = $('#tourTitle'), stats = $('#tourStats'), listBox = $('#tourList');
  if(!list.length){ wrap.style.display='none'; listBox.innerHTML=''; stats.innerHTML=''; title.textContent=''; return; }

  const dayCount = {}; const toursSeen = new Set();
  list.forEach(k => (k.touren||[]).forEach(t=>{
    if(t.tournummer.startsWith(query)){ dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1; toursSeen.add(t.tournummer); }
  }));

  title.textContent = (isExact ? 'Tour ' + query : 'Tour-Prefix ' + query + '*') + ' \u2013 ' + list.length + ' Kunden';
  stats.innerHTML = Object.entries(dayCount).map(([d,c])=>'<span><b>'+d+':</b> '+c+'</span>').join('') + (isExact?'':'<span><b>Touren:</b> '+toursSeen.size+'</span>');

  listBox.innerHTML='';
  list.slice().sort((a,b)=> (parseInt(cs(a.csb_nummer))||0) - (parseInt(cs(b.csb_nummer))||0)).forEach(k=>{
    const csb = cs(k.csb_nummer), plz = cs(k.postleitzahl);
    const row = el('div','tour-row');
    const csbLink = el('span','csb-link', csb); csbLink.onclick=()=>{ $('#smartSearch').value = csb; onSmart(); };
    row.appendChild(csbLink);
    row.appendChild(el('span','', k.schluessel ? 'S: '+k.schluessel : 'S: -'));
    row.appendChild(el('span','', (k.name||'-')));
    const m = document.createElement('a'); m.className='map-pill'; m.textContent='Map';
    m.href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((k.name||'')+', '+(k.strasse||'')+', '+plz+' '+(k.ort||'')); m.target='_blank';
    row.appendChild(m);
    listBox.appendChild(row);
  });

  wrap.style.display='block';
}

function closeTourTop(){ $('#tourWrap').style.display='none'; $('#tourList').innerHTML=''; $('#tourStats').innerHTML=''; $('#tourTitle').textContent=''; }

function onSmart(){
  const qRaw = $('#smartSearch').value.trim();
  const q = qRaw.toLowerCase();
  closeTourTop();
  if(!q){ renderTable([], ''); return; }

  const isDigits = /^\\d{1,4}$/.test(qRaw);
  if(isDigits){
    const exact = qRaw.length===4;
    const results = allCustomers.filter(k => (k.touren||[]).some(t => t.tournummer.startsWith(qRaw)));
    renderTourTop(results, qRaw, exact);
    renderTable(results, 'Keine Treffer fuer Tour'+(exact?'':'-Prefix')+' "'+qRaw+'"');
    return;
  }

  const results = allCustomers.filter(k=>{
    const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+k.fachberater+' '+(k.schluessel||'')).toLowerCase();
    return text.includes(q);
  });
  renderTable(results, 'Keine Kunden fuer "'+qRaw+'" gefunden');
}

function onKey(){
  const q = $('#keySearch').value.trim();
  closeTourTop();
  if(!q){ renderTable([], ''); return; }
  const results = allCustomers.filter(k => (k.schluessel||'') === q);
  if(results.length){ renderTourTop(results, 'Schluessel '+q, true); }
  renderTable(results, 'Kein Kunde mit Schluessel "'+q+'" gefunden');
}

function debounce(fn, d=180){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData!=='undefined' && Object.keys(tourkundenData).length>0){ buildData(); }
  document.getElementById('smartSearch').addEventListener('input', debounce(onSmart, 180));
  document.getElementById('keySearch').addEventListener('input', debounce(onKey, 180));
  document.getElementById('btnReset').addEventListener('click', ()=>{
    document.getElementById('smartSearch').value=''; document.getElementById('keySearch').value='';
    closeTourTop(); renderTable([], '');
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
