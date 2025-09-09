import streamlit as st
import pandas as pd
import json

# ===== Vollständige App: Listenansicht, Tour-Banner, ohne Welcome-Block, mit Umlaut-Suche =====

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
  --radius:8px; --shadow:0 1px 3px rgba(0,0,0,.05);
  --fs-11:11px; --fs-12:12px; --fs-13:13px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.45;
}

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:12px}
.container{width:100%; max-width:1400px}
.card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); box-shadow:var(--shadow); overflow:hidden}

/* Header */
.header{padding:8px 12px; border-bottom:1px solid var(--border); background:#0b1d3a; color:#fff}
.title{font-size:13px; font-weight:700; text-align:center}

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

/* Section chrome */
.section{
  background:var(--surface); border:1px solid var(--border); border-radius:8px; box-shadow:var(--shadow); position:relative;
}
.section::before{
  content:""; position:absolute; left:0; right:0; top:0; height:3px;
  background:linear-gradient(90deg, rgba(37,99,235,.35), rgba(37,99,235,.0));
  border-top-left-radius:8px; border-top-right-radius:8px;
}

/* Tour banner */
.tour-wrap{display:none; margin-bottom:8px}
.tour-banner{
  display:flex; align-items:center; justify-content:space-between;
  padding:6px 10px; border:1px solid var(--border); border-radius:6px;
  background:#f2f5fa; color:#344054; font-weight:700; font-size:12px;
}
.tour-banner small{font-weight:600; color:#667085; font-size:11px}

/* Table */
.table-wrap{margin-top:8px}
.table-section{padding:6px 8px}
.scroller{max-height:68vh; overflow:auto; border:1px solid var(--row-border); border-radius:6px; background:#fff}
table{width:100%; border-collapse:separate; border-spacing:0; font-size:var(--fs-12)}
thead th{
  position:sticky; top:0; background:#f2f5fa; color:#344054; font-weight:700;
  border-bottom:1px solid var(--row-border); padding:7px 8px; white-space:nowrap; z-index:1
}
tbody td{padding:6px 8px; border-bottom:1px solid var(--row-border); vertical-align:middle}
tbody tr:nth-child(odd){background:var(--stripe)}
tbody tr:hover{background:#eef4ff}
.csb-link{font-weight:700; color:#0b3a8a; cursor:pointer}
.csb-link:hover{text-decoration:underline}

/* small pills */
.tour-btn{
  display:inline-block; background:#fff; border:1px solid #bbf7d0; color:#065f46;
  padding:1px 7px; margin:1px 4px 1px 0; border-radius:999px; font-weight:700; font-size:11px; cursor:pointer
}
.tour-btn:hover{background:var(--ok-weak)}
.badge-key{background:var(--warn-weak); border:1px solid #fcd34d; color:#92400e; border-radius:999px; padding:1px 7px; font-weight:700; font-size:11px; display:inline-block}

/* MAP button: colored */
.table-map,
.map-pill{
  text-decoration:none; font-weight:700; font-size:11px;
  padding:5px 10px; border-radius:999px; border:1px solid var(--accent);
  background:var(--accent); color:#fff; display:inline-block; text-align:center;
}
.table-map:hover, .map-pill:hover{background:var(--accent-strong); border-color:var(--accent-strong)}

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

      <!-- Content -->
      <div class="content">
        <!-- Tour-Banner -->
        <div class="section tour-wrap" id="tourWrap">
          <div class="tour-banner">
            <span id="tourTitle"></span>
            <small id="tourExtra"></small>
          </div>
        </div>

        <!-- Tabelle -->
        <div class="section table-wrap">
          <div class="table-section">
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

/* Deutsche Normalisierung für Suche: ä/ö/ü -> ae/oe/ue, ß -> ss, Diakritika entfernen */
function normDE(s){
  if(!s) return '';
  let x = s.toLowerCase();
  x = x.replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
  return x.replace(/\\s+/g,' ').trim();
}

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

function renderTourTop(list, query, isExact){
  const wrap = $('#tourWrap'), title = $('#tourTitle'), extra = $('#tourExtra');
  if(!list.length){ wrap.style.display='none'; title.textContent=''; extra.textContent=''; return; }

  // Schlüsselsuche -> kein "Tour" im Titel
  if (query.startsWith('Schluessel ')) {
    const key = query.replace(/^Schluessel\\s+/, '');
    const label = 'Schluessel ' + key + ' - ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');
    title.textContent = label;

    const dayCount = {};
    list.forEach(k => (k.touren||[]).forEach(t=>{
      dayCount[t.liefertag] = (dayCount[t.liefertag]||0) + 1;
    }));
    extra.textContent = Object.entries(dayCount).sort().map(([d,c])=> d + ': ' + c).join('  •  ');
    wrap.style.display='block';
    return;
  }

  // Tour-Logik
  const label = isExact ? ('Tour ' + query) : ('Tour-Prefix ' + query + '*');
  title.textContent = label + ' - ' + list.length + ' ' + (list.length===1?'Kunde':'Kunden');

  const dayCount = {};
  list.forEach(k => (k.touren||[]).forEach(t=>{
    const cond = isExact ? (t.tournummer === query) : t.tournummer.startsWith(query);
    if(cond){ dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1; }
  }));
  extra.textContent = Object.entries(dayCount).sort().map(([d,c])=> d + ': ' + c).join('  •  ');
  wrap.style.display='block';
}

function closeTourTop(){
  const wrap = $('#tourWrap'); if(!wrap) return;
  $('#tourTitle').textContent=''; const ex = $('#tourExtra'); if(ex) ex.textContent='';
  wrap.style.display='none';
}

function onSmart(){
  const qRaw = $('#smartSearch').value.trim();
  closeTourTop();
  if(!qRaw){ renderTable([], ''); return; }

  // Nur Ziffern (1–4) -> Tour-/Prefixsuche
  if(/^\\d{1,4}$/.test(qRaw)){
    const exact = qRaw.length===4;
    const results = allCustomers.filter(k => (k.touren||[]).some(t => t.tournummer.startsWith(qRaw)));
    renderTourTop(results, qRaw, exact);
    renderTable(results, '');
    return;
  }

  // Textsuche mit deutscher Normalisierung (Büchen <-> Buechen)
  const qN = normDE(qRaw);
  const results = allCustomers.filter(k=>{
    const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+k.fachberater+' '+(k.schluessel||''));
    return normDE(text).includes(qN);
  });
  renderTable(results, '');
}

function onKey(){
  const q = $('#keySearch').value.trim();
  closeTourTop();
  if(!q){ renderTable([], ''); return; }
  const results = allCustomers.filter(k => (k.schluessel||'') === q);
  if(results.length){ renderTourTop(results, 'Schluessel ' + q, true); }
  renderTable(results, '');
}

function debounce(fn, d=160){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),d); }; }

document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData!=='undefined' && Object.keys(tourkundenData).length>0){ buildData(); }
  document.getElementById('smartSearch').addEventListener('input', debounce(onSmart, 160));
  document.getElementById('keySearch').addEventListener('input', debounce(onKey, 160));
  document.getElementById('btnReset').addEventListener('click', ()=>{
    document.getElementById('smartSearch').value=''; document.getElementById('keySearch').value='';
    closeTourTop(); renderTable([], '');
  });
});
</script>
</body>
</html>
"""

# ===== Streamlit-Rahmen =====

st.title("Kunden-Suchseite (Listenansicht, Tour-Banner)")
st.caption("Ein Feld fuer Text/Tour (1–4 Ziffern) und ein Feld fuer exakte Schluesselnummer.")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("Schluesseldatei (A=CSB, F=Schluessel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x):
        return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", "."))
        i = int(f)
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
        SPALTEN_MAPPING = {
            "csb_nummer":"Nr",
            "sap_nummer":"SAP-Nr.",
            "name":"Name",
            "strasse":"Strasse",
            "postleitzahl":"Plz",
            "ort":"Ort",
            "fachberater":"Fachberater"
        }
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
