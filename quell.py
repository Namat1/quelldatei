import streamlit as st
import pandas as pd
import json

# --- HTML mit luftiger Karten-Listenansicht + 1 Feld fuer alle Suchen + 1 Feld fuer Schluessel ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kunden-Suche</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f6f7fb; color: #2f2f2f; font-size: 14px; line-height: 1.45;
    }

    .page { min-height: 100vh; display: flex; justify-content: center; padding: 24px; }
    .container { width: 100%; max-width: 1100px; }

    .card {
      background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; overflow: hidden;
      box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    }

    .header { padding: 20px; border-bottom: 1px solid #eef0f3; }
    .title { font-size: 20px; font-weight: 800; text-align: center; margin-bottom: 12px; }

    .search-grid {
      display: grid; grid-template-columns: 1fr 280px; gap: 12px; align-items: center;
    }
    @media (max-width: 760px) { .search-grid { grid-template-columns: 1fr; } }

    .field {
      display: grid; grid-template-columns: 86px 1fr; gap: 10px; align-items: center;
    }
    .label { font-weight: 700; color: #4b5563; }
    input[type="text"] {
      width: 100%; padding: 12px 14px; border: 1px solid #d1d5db; border-radius: 12px; font-size: 14px;
      background: #fbfbfc; transition: border-color .2s, box-shadow .2s, background .2s;
    }
    input[type="text"]:focus {
      outline: none; border-color: #2563eb; background: #fff; box-shadow: 0 0 0 3px rgba(37,99,235,.12);
    }

    .toolbar { padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; }
    .stats { font-size: 13px; color: #555; font-weight: 700; }
    .btn {
      padding: 10px 14px; font-size: 13px; border-radius: 10px; cursor: pointer;
      border: 1px solid #d1d5db; background: #fff; transition: background .2s, border-color .2s;
    }
    .btn:hover { background: #f3f4f6; }
    .btn-danger { background: #dc3545; border-color: #dc3545; color: #fff; }
    .btn-danger:hover { background: #c82333; }

    .content { padding: 0 20px 20px 20px; }

    .welcome {
      padding: 64px 20px; text-align: center; color: #6b7280;
    }
    .welcome h2 { font-size: 22px; margin-bottom: 8px; color: #374151; }

    /* Ergebnis-Karten */
    .results-grid {
      display: grid; gap: 14px;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
    }
    @media (max-width: 480px) { .results-grid { grid-template-columns: 1fr; } }

    .result-card {
      border: 1px solid #e7eaf0; background: #fff; border-radius: 12px; padding: 14px;
      display: grid; gap: 10px;
    }
    .line { display: grid; grid-template-columns: 120px 1fr; gap: 10px; }
    .k-label { color: #6b7280; font-weight: 700; }
    .k-value { color: #111827; font-weight: 600; }

    .pill-row { display: flex; gap: 6px; flex-wrap: wrap; }
    .csb-btn {
      background: #eef5ff; border: 1px solid #cfe1ff; padding: 3px 8px; cursor: pointer;
      font-weight: 800; color: #1d4ed8; font-size: 12px; border-radius: 999px;
    }
    .key-badge {
      background: #fff3cd; color: #856404; padding: 2px 8px; border: 1px solid #ffeaa7;
      font-weight: 800; border-radius: 999px; font-size: 12px;
    }
    .tour-badge {
      background: #ecfdf5; border: 1px solid #bbf7d0; color: #16a34a;
      padding: 2px 8px; font-size: 12px; border-radius: 999px; font-weight: 700;
      cursor: pointer;
    }
    .tour-badge:hover { background: #d1fae5; }

    .actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .maps-btn {
      background: #6b7280; color: #fff; padding: 6px 12px; border: none; cursor: pointer;
      font-size: 12px; text-decoration: none; border-radius: 10px; display: inline-block;
    }
    .maps-btn:hover { background: #4b5563; }

    .tour-info {
      margin-bottom: 14px; padding: 12px;
      background: #e9fbef; border: 1px solid #d1fadf; border-radius: 10px; display: none;
    }
    .tour-info.show { display: block; }
    .tour-info .head { font-weight: 800; color: #166534; margin-bottom: 6px; }
    .tour-info .stats-line { display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; }
  </style>
</head>
<body>
<div class="page">
  <div class="container">
    <div class="card">
      <div class="header">
        <div class="title">Kunden-Suche</div>
        <div class="search-grid">
          <div class="field">
            <div class="label">Suche</div>
            <input type="text" id="smartSearch" placeholder="Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1-4 Ziffern)">
          </div>
          <div class="field">
            <div class="label">Schluessel</div>
            <input type="text" id="keySearch" placeholder="Exakte Schluesselnummer">
          </div>
        </div>
      </div>

      <div class="toolbar">
        <div class="stats" id="hitInfo">Bereit</div>
        <div style="display:flex; gap:10px;">
          <button class="btn" onclick="showFachberater()">Fachberater-Liste</button>
          <button class="btn btn-danger" onclick="clearAll()">Zuruecksetzen</button>
        </div>
      </div>

      <div class="content">
        <div id="tourInfo" class="tour-info">
          <div class="head" id="tourInfoHead"></div>
          <div class="stats-line" id="tourInfoStats"></div>
        </div>

        <div id="welcome" class="welcome">
          <h2>Willkommen</h2>
          <p>Nutze links das Feld fuer Textsuche oder 1-4 stellige Tournummern. Rechts ist die exakte Schluesselsuche.</p>
        </div>

        <div id="results" class="results-grid" style="display:none;"></div>

        <div id="fbListWrap" style="display:none; margin-top:12px;">
          <div class="result-card">
            <div class="k-label" style="margin-bottom:6px;">Fachberater</div>
            <div id="fbList" class="pill-row"></div>
          </div>
        </div>

        <div id="keyListWrap" style="display:none; margin-top:12px;">
          <div class="result-card">
            <div class="k-label" style="margin-bottom:6px;">Schluessel-Ergebnisse</div>
            <div id="keyList"></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);

// debounce
function debounce(fn, delay=200){ let t; return (...a)=>{clearTimeout(t); t=setTimeout(()=>fn(...a),delay);} }

let allCustomers = [];

function initializeData(){
  const map = new Map();
  for(const [tour, list] of Object.entries(tourkundenData)){
    list.forEach(k=>{
      const key = k.csb_nummer;
      if(!key) return;
      if(!map.has(key)) map.set(key, {...k, touren: []});
      map.get(key).touren.push({tournummer: tour, liefertag: k.liefertag});
    });
  }
  allCustomers = Array.from(map.values());
}

function createCard(k){
  const csb = (k.csb_nummer||'').toString().replace(/\\.0$/, '') || '-';
  const sap = (k.sap_nummer||'').toString().replace(/\\.0$/, '') || '-';
  const plz = (k.postleitzahl||'').toString().replace(/\\.0$/, '') || '-';
  const key = k.schluessel || '-';

  const div = document.createElement('div');
  div.className = 'result-card';

  // erste Zeile: Name
  const name = document.createElement('div');
  name.className = 'line';
  name.innerHTML = '<div class="k-label">Name</div><div class="k-value">'+ (k.name||'-') +'</div>';
  div.appendChild(name);

  // Adresse
  const adr = document.createElement('div');
  adr.className = 'line';
  adr.innerHTML = '<div class="k-label">Adresse</div><div class="k-value">'+ (k.strasse||'-') + ', ' + plz + ' ' + (k.ort||'-') +'</div>';
  div.appendChild(adr);

  // IDs
  const ids = document.createElement('div');
  ids.className = 'line';
  const idsRight = document.createElement('div');
  idsRight.innerHTML = ''
    + '<div class="pill-row">'
    + '<button class="csb-btn" title="CSB suchen">'+ csb +'</button>'
    + '<span class="key-badge" title="Schluessel">'+ key +'</span>'
    + '</div>'
    + '<div style="margin-top:6px; color:#6b7280; font-size:12px;">SAP: <strong>'+ sap +'</strong></div>';
  ids.innerHTML = '<div class="k-label">Kennungen</div>';
  ids.appendChild(idsRight);
  div.appendChild(ids);

  // Touren
  const tours = document.createElement('div');
  tours.className = 'line';
  const tourWrap = document.createElement('div');
  tourWrap.className = 'pill-row';
  (k.touren||[]).forEach(t=>{
    const b = document.createElement('span');
    b.className = 'tour-badge';
    b.textContent = t.tournummer + ' (' + t.liefertag.substring(0,2) + ')';
    b.onclick = ()=>{ $('#smartSearch').value = t.tournummer; smartSearch(); };
    tourWrap.appendChild(b);
  });
  tours.innerHTML = '<div class="k-label">Touren</div>';
  tours.appendChild(tourWrap);
  div.appendChild(tours);

  // Fachberater
  const fb = document.createElement('div');
  fb.className = 'line';
  fb.innerHTML = '<div class="k-label">Fachberater</div><div class="k-value">'+ (k.fachberater||'-') +'</div>';
  div.appendChild(fb);

  // Actions
  const act = document.createElement('div');
  act.className = 'actions';
  const m = document.createElement('a');
  m.className = 'maps-btn';
  m.textContent = 'Maps';
  m.href = 'https://www.google.com/maps/search/?api=1&query='
           + encodeURIComponent((k.name||'') + ', ' + (k.strasse||'') + ', ' + plz + ' ' + (k.ort||''));
  m.target = '_blank';
  act.appendChild(m);
  div.appendChild(act);

  // CSB Button Funktion
  idsRight.querySelector('.csb-btn').onclick = ()=>{ $('#smartSearch').value = csb; smartSearch(); };

  return div;
}

function render(customers, msgIfEmpty){
  const grid = $('#results');
  const welcome = $('#welcome');
  const hit = $('#hitInfo');

  grid.innerHTML = '';

  if(customers && customers.length>0){
    welcome.style.display = 'none';
    grid.style.display = 'grid';
    customers.forEach(k=> grid.appendChild(createCard(k)));
    hit.textContent = customers.length + ' Kunde' + (customers.length===1?'':'n') + ' gefunden';
  } else {
    grid.style.display = 'none';
    welcome.style.display = 'block';
    welcome.innerHTML = '<h2>Keine Ergebnisse</h2><p>' + (msgIfEmpty||'Keine Kunden gefunden') + '</p>';
    hit.textContent = 'Keine Treffer';
  }
}

function clearPanels(){
  $('#fbListWrap').style.display = 'none';
  $('#keyListWrap').style.display = 'none';
}

function smartSearch(){
  const raw = $('#smartSearch').value.trim();
  const tourBox = $('#tourInfo');
  clearPanels();

  if(!raw){
    tourBox.classList.remove('show');
    $('#welcome').style.display = 'block';
    $('#results').style.display = 'none';
    $('#hitInfo').textContent = 'Bereit';
    return;
  }

  const isDigits = /^\\d{1,4}$/.test(raw);
  let results = [];

  if(isDigits){
    // Tour-Prefix (1-3), exakt (4)
    const exact = raw.length===4;
    results = allCustomers.filter(k => k.touren && k.touren.some(t => t.tournummer.startsWith(raw)));

    if(results.length>0){
      const toursSeen = new Set();
      const dayCount = {};
      results.forEach(k => k.touren.forEach(t=>{
        if(t.tournummer.startsWith(raw)){
          toursSeen.add(t.tournummer);
          dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1;
        }
      }));
      $('#tourInfoHead').textContent = exact
        ? 'Tour ' + raw + ': ' + results.length + ' Kunden'
        : 'Tour-Prefix ' + raw + '*: ' + results.length + ' Kunden · ' + toursSeen.size + ' Touren';
      $('#tourInfoStats').innerHTML = Object.entries(dayCount)
        .map(([d,c])=>'<span><strong>'+d+':</strong> '+c+' Kunden</span>').join('');
      tourBox.classList.add('show');
    } else {
      tourBox.classList.remove('show');
    }
    render(results, 'Keine Treffer fuer Tour' + (exact?'':'-Prefix') + ' "' + raw + '"');

  } else {
    // Allgemeinsuche
    const q = raw.toLowerCase();
    tourBox.classList.remove('show');
    results = allCustomers.filter(k=>{
      const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+k.fachberater).toLowerCase();
      return text.includes(q);
    });
    render(results, 'Keine Kunden fuer "'+raw+'" gefunden');
  }
}

function searchKey(){
  const q = $('#keySearch').value.trim();
  const tourBox = $('#tourInfo');
  clearPanels();
  tourBox.classList.remove('show');

  if(!q){
    $('#welcome').style.display = 'block';
    $('#results').style.display = 'none';
    $('#hitInfo').textContent = 'Bereit';
    return;
  }

  const results = allCustomers.filter(k => (k.schluessel||'') === q);

  if(results.length>0){
    const wrap = $('#keyListWrap'); const list = $('#keyList');
    list.innerHTML = '';
    results.forEach(k=>{
      const d = document.createElement('div');
      d.style.padding = '8px 10px';
      d.style.border = '1px solid #ffe8a3';
      d.style.background = '#fff9e6';
      d.style.borderRadius = '10px';
      d.style.marginBottom = '6px';
      d.style.cursor = 'pointer';
      d.innerHTML = '<div><strong>Schluessel: '+(k.schluessel||'-')+'</strong></div>'
                  + '<div style="font-size:12px;color:#6b7280;">CSB: '+(k.csb_nummer||'-')+' - '+(k.name||'-')+'</div>';
      d.onclick = ()=>{ $('#smartSearch').value = (k.csb_nummer||''); smartSearch(); };
      list.appendChild(d);
    });
    wrap.style.display = 'block';
  }
  render(results, 'Kein Kunde mit Schluessel "'+q+'" gefunden');
}

function showFachberater(){
  clearAll();
  const counts = {};
  allCustomers.forEach(k=>{ if(k.fachberater) counts[k.fachberater]=(counts[k.fachberater]||0)+1; });

  const wrap = $('#fbListWrap'); const list = $('#fbList');
  list.innerHTML = '';
  Object.entries(counts).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([fb,c])=>{
    const span = document.createElement('span');
    span.className = 'tour-badge';
    span.textContent = fb + ' (' + c + ')';
    span.onclick = ()=>{ $('#smartSearch').value = fb; smartSearch(); };
    list.appendChild(span);
  });
  wrap.style.display = 'block';
}

function clearAll(){
  $('#smartSearch').value = '';
  $('#keySearch').value = '';
  $('#tourInfo').classList.remove('show');
  clearPanels();
  $('#welcome').style.display = 'block';
  $('#results').style.display = 'none';
  $('#hitInfo').textContent = 'Bereit';
}

// init
document.addEventListener('DOMContentLoaded', ()=>{
  $('#smartSearch').addEventListener('input', debounce(smartSearch, 180));
  $('#keySearch').addEventListener('input', debounce(searchKey, 180));

  if(typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length>0){
    initializeData();
  } else {
    $('#welcome').innerHTML = '<h2>Fehler</h2><p>Keine Kundendaten geladen</p>';
  }
});
</script>
</body>
</html>
"""

st.title("Kunden-Suchseite")
st.markdown("Ein Feld fuer **Text oder Tour** (1-4 Ziffern) und ein Feld fuer **exakte Schluesselnummer**. Kartenansicht, luftig und uebersichtlich.")

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
            "csb_nummer": "Nr",
            "sap_nummer": "SAP-Nr.",
            "name": "Name",
            "strasse": "Strasse",
            "postleitzahl": "Plz",
            "ort": "Ort",
            "fachberater": "Fachberater"
        }
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}

        try:
            with st.spinner("Verarbeite Dateien..."):
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

                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine Daten gefunden – Blattnamen/Spalten pruefen.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda x: int(x[0])))
            json_data_string = json.dumps(sorted_tours, indent=2, ensure_ascii=False)
            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")

            total_customers = sum(len(v) for v in sorted_tours.values())
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Touren", len(sorted_tours))
            with c2: st.metric("Kunden", total_customers)
            with c3: st.metric("Schluessel (Mapping)", len(key_map))

            st.download_button(
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="kundenliste.html",
                mime="text/html",
                type="primary"
            )
        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei und Schluesseldatei hochladen.")
