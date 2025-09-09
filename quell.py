import streamlit as st
import pandas as pd
import json

# --- HTML: Listenansicht (Tabelle) mit vereinter Suche + Schluessel-Suche ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kunden-Suche</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f6f8; color: #2f2f2f; font-size: 14px; line-height: 1.45; }

    .page { min-height: 100vh; display: flex; justify-content: center; padding: 24px; }
    .container { width: 100%; max-width: 1100px; }

    .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); overflow: hidden; }

    .header { padding: 18px; border-bottom: 1px solid #eef0f3; }
    .title { font-size: 18px; font-weight: 800; text-align: center; margin-bottom: 10px; }

    .search-grid { display: grid; grid-template-columns: 1fr 280px; gap: 12px; align-items: center; }
    @media (max-width: 760px) { .search-grid { grid-template-columns: 1fr; } }

    .field { display: grid; grid-template-columns: 84px 1fr; gap: 10px; align-items: center; }
    .label { font-weight: 700; color: #4b5563; }
    input[type="text"] {
      width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 10px; font-size: 14px;
      background: #fbfbfc; transition: border-color .2s, box-shadow .2s, background .2s;
    }
    input[type="text"]:focus { outline: none; border-color: #2563eb; background: #fff; box-shadow: 0 0 0 3px rgba(37,99,235,.12); }

    .toolbar { padding: 10px 18px; display: flex; justify-content: space-between; align-items: center; gap: 10px; }
    .stats { font-size: 13px; color: #555; font-weight: 700; }
    .btn { padding: 8px 14px; font-size: 13px; border-radius: 10px; cursor: pointer; border: 1px solid #d1d5db; background: #fff; }
    .btn:hover { background: #f3f4f6; }
    .btn-danger { background: #dc3545; border-color: #dc3545; color: #fff; }
    .btn-danger:hover { background: #c82333; }

    /* Info-Band */
    .info { margin: 12px 18px 0 18px; padding: 10px 12px; border-radius: 10px; background: #e9fbef; border: 1px solid #d1fadf; color: #166534; display: none; }
    .info.show { display: block; }

    /* Tabelle */
    .table-wrap { padding: 12px 18px 18px 18px; }
    .table-scroller { max-height: 72vh; overflow: auto; border: 1px solid #e5e7eb; border-radius: 10px; }
    table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 13px; }
    thead th {
      position: sticky; top: 0; z-index: 2; background: #f8fafc; color: #374151; font-weight: 800;
      border-bottom: 1px solid #e5e7eb; padding: 12px 10px; white-space: nowrap;
    }
    tbody td { padding: 10px 10px; border-bottom: 1px solid #f0f2f5; vertical-align: middle; }
    tbody tr:nth-child(odd) { background: #fcfdff; }
    tbody tr:hover { background: #f3f7ff; }

    .csb-btn { background: #eef5ff; border: 1px solid #cfe1ff; padding: 3px 8px; cursor: pointer; font-weight: 800; color: #1d4ed8; font-size: 12px; border-radius: 999px; }
    .csb-btn:hover { background: #e2eeff; }
    .key-badge { background: #fff3cd; color: #856404; padding: 2px 8px; border: 1px solid #ffeaa7; font-weight: 800; border-radius: 999px; font-size: 12px; display: inline-block; }

    .tour-btn { display: inline-block; background: #fff; border: 1px solid #22c55e; color: #16a34a; padding: 2px 8px; margin: 1px; cursor: pointer; font-size: 11px; font-weight: 700; border-radius: 999px; }
    .tour-btn:hover { background: #22c55e; color: #fff; }

    .maps-btn { background: #6b7280; color: #fff; padding: 6px 10px; border: none; cursor: pointer; font-size: 12px; text-decoration: none; border-radius: 8px; display: inline-block; }
    .maps-btn:hover { background: #4b5563; }

    /* Welcome */
    .welcome { padding: 64px 18px 24px 18px; text-align: center; color: #6b7280; }
    .welcome h2 { font-size: 22px; margin-bottom: 8px; color: #374151; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-thumb { background: #c9ced6; border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: #aab3bf; }
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
          <button class="btn btn-danger" onclick="clearAll()">Zuruecksetzen</button>
        </div>
      </div>

      <div id="tourInfo" class="info"></div>

      <div class="table-wrap">
        <div id="welcome" class="welcome">
          <h2>Willkommen</h2>
          <p>Tippe zum Suchen: Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1-4 Ziffern). Rechts: exakte Schluesselsuche.</p>
        </div>

        <div class="table-scroller" id="tableScroller" style="display:none;">
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
  </div>
</div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);

// debounce
function debounce(fn, delay=180){ let t; return (...a)=>{clearTimeout(t); t=setTimeout(()=>fn(...a),delay);} }

let allCustomers = [];

function initializeData(){
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

function createRow(k){
  const tr = document.createElement('tr');

  const csb = (k.csb_nummer||'').toString().replace(/\\.0$/, '') || '-';
  const sap = (k.sap_nummer||'').toString().replace(/\\.0$/, '') || '-';
  const plz = (k.postleitzahl||'').toString().replace(/\\.0$/, '') || '-';
  const key = k.schluessel || '-';

  // CSB (Button)
  const tdCSB = document.createElement('td');
  const csbBtn = document.createElement('button');
  csbBtn.className = 'csb-btn';
  csbBtn.textContent = csb;
  csbBtn.onclick = ()=>{ $('#smartSearch').value = csb; smartSearch(); };
  tdCSB.appendChild(csbBtn);

  const tdSAP = document.createElement('td'); tdSAP.textContent = sap;
  const tdName = document.createElement('td'); tdName.textContent = k.name || '-';
  const tdStr = document.createElement('td'); tdStr.textContent = k.strasse || '-';
  const tdPLZ = document.createElement('td'); tdPLZ.textContent = plz;
  const tdOrt = document.createElement('td'); tdOrt.textContent = k.ort || '-';

  const tdKey = document.createElement('td');
  if(key !== '-'){
    const badge = document.createElement('span');
    badge.className = 'key-badge';
    badge.textContent = key;
    tdKey.appendChild(badge);
  } else { tdKey.textContent = '-'; }

  const tdTours = document.createElement('td');
  (k.touren||[]).forEach(t=>{
    const b = document.createElement('span');
    b.className = 'tour-btn';
    b.textContent = t.tournummer + ' (' + t.liefertag.substring(0,2) + ')';
    b.onclick = ()=>{ $('#smartSearch').value = t.tournummer; smartSearch(); };
    tdTours.appendChild(b);
  });

  const tdFB = document.createElement('td'); tdFB.textContent = k.fachberater || '-';

  const tdAct = document.createElement('td');
  const m = document.createElement('a');
  m.className = 'maps-btn';
  m.textContent = 'Maps';
  m.href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent((k.name||'') + ', ' + (k.strasse||'') + ', ' + plz + ' ' + (k.ort||''));
  m.target = '_blank';
  tdAct.appendChild(m);

  tr.append(tdCSB, tdSAP, tdName, tdStr, tdPLZ, tdOrt, tdKey, tdTours, tdFB, tdAct);
  return tr;
}

function render(customers, msgIfEmpty){
  const body = $('#tableBody');
  const scroller = $('#tableScroller');
  const welcome = $('#welcome');
  const hit = $('#hitInfo');

  body.innerHTML = '';

  if(customers && customers.length > 0){
    welcome.style.display = 'none';
    scroller.style.display = 'block';
    customers.forEach(k => body.appendChild(createRow(k)));
    hit.textContent = customers.length + ' Kunde' + (customers.length===1?'':'n') + ' gefunden';
  } else {
    scroller.style.display = 'none';
    welcome.style.display = 'block';
    welcome.innerHTML = '<h2>Keine Ergebnisse</h2><p>' + (msgIfEmpty || 'Keine Kunden gefunden') + '</p>';
    hit.textContent = 'Keine Treffer';
  }
}

function clearInfo(){
  const info = $('#tourInfo');
  info.classList.remove('show');
  info.textContent = '';
}

function smartSearch(){
  const raw = $('#smartSearch').value.trim();
  const info = $('#tourInfo');
  clearInfo();

  if(!raw){
    render([], '');
    $('#hitInfo').textContent = 'Bereit';
    return;
  }

  const isDigits = /^\\d{1,4}$/.test(raw);
  let results = [];

  if(isDigits){
    // Tour-Prefix (1-3) oder exakt (4)
    const exact = raw.length === 4;
    results = allCustomers.filter(k => k.touren && k.touren.some(t => t.tournummer.startsWith(raw)));

    if(results.length > 0){
      const toursSeen = new Set();
      const dayCount = {};
      results.forEach(k => k.touren.forEach(t=>{
        if(t.tournummer.startsWith(raw)){
          toursSeen.add(t.tournummer);
          dayCount[t.liefertag] = (dayCount[t.liefertag]||0)+1;
        }
      }));
      info.textContent = exact
        ? 'Tour ' + raw + ': ' + results.length + ' Kunden'
        : 'Tour-Prefix ' + raw + '*: ' + results.length + ' Kunden, ' + toursSeen.size + ' Touren';
      info.classList.add('show');
    }
    render(results, 'Keine Treffer fuer Tour' + (exact?'':'-Prefix') + ' "' + raw + '"');

  } else {
    // Textsuche
    const q = raw.toLowerCase();
    results = allCustomers.filter(k=>{
      const text = (k.name+' '+k.strasse+' '+k.ort+' '+k.csb_nummer+' '+k.sap_nummer+' '+k.fachberater).toLowerCase();
      return text.includes(q);
    });
    render(results, 'Keine Kunden fuer "'+raw+'" gefunden');
  }
}

function searchKey(){
  const q = $('#keySearch').value.trim();
  clearInfo();

  if(!q){
    render([], '');
    $('#hitInfo').textContent = 'Bereit';
    return;
  }

  const results = allCustomers.filter(k => (k.schluessel||'') === q);

  if(results.length > 0){
    // kleiner Hinweis im Info-Band
    const info = $('#tourInfo');
    info.textContent = 'Schluessel-Treffer: ' + results.length + ' Kunde' + (results.length===1?'':'n');
    info.classList.add('show');
  }
  render(results, 'Kein Kunde mit Schluessel "'+q+'" gefunden');
}

function clearAll(){
  $('#smartSearch').value = '';
  $('#keySearch').value = '';
  clearInfo();
  render([], '');
  $('#hitInfo').textContent = 'Bereit';
}

// init
document.addEventListener('DOMContentLoaded', ()=>{
  if(typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length>0){
    initializeData();
  } else {
    const w = document.getElementById('welcome');
    if(w) w.innerHTML = '<h2>Fehler</h2><p>Keine Kundendaten geladen</p>';
  }

  document.getElementById('smartSearch').addEventListener('input', debounce(smartSearch, 200));
  document.getElementById('keySearch').addEventListener('input', debounce(searchKey, 200));
});
</script>
</body>
</html>
"""

st.title("Kunden-Suchseite (Listenansicht)")
st.markdown("Ein Feld fuer **Text oder Tour** (1-4 Ziffern) und ein Feld fuer **exakte Schluesselnummer**. Tabellenansicht, luftig und uebersichtlich.")

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
                # Schluessel
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

            # sortiert
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
