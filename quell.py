import streamlit as st
import pandas as pd
import json

# --- HTML mit vereinter Smart-Suche (Allgemein + Tour) und aufgeräumtem Layout ---
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

        .page {
            min-height: 100vh;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding: 24px;
        }

        .container {
            width: 100%;
            max-width: 1100px;
        }

        .card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
            overflow: hidden;
        }

        /* Header */
        .header {
            padding: 18px 18px 10px 18px;
            border-bottom: 1px solid #eef0f3;
        }

        .title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
            text-align: center;
        }

        .search-bar {
            display: grid;
            grid-template-columns: 1fr 240px;
            gap: 12px;
            align-items: center;
        }

        .search-group {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .search-label {
            font-weight: 600;
            color: #666;
            min-width: 84px;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            font-size: 14px;
            background: #fbfbfc;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #2563eb;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
        }

        .toolbar {
            padding: 10px 18px 14px 18px;
            display: flex;
            gap: 10px;
            justify-content: space-between;
            align-items: center;
        }

        .stats {
            font-size: 13px;
            color: #555;
            font-weight: 600;
        }

        .btn {
            padding: 8px 14px;
            font-size: 13px;
            border-radius: 10px;
            cursor: pointer;
            border: 1px solid #d1d5db;
            background: #fff;
            transition: background 0.2s, border-color 0.2s;
        }
        .btn:hover { background: #f5f6f8; }
        .btn-danger { background: #dc3545; border-color: #dc3545; color: #fff; }
        .btn-danger:hover { background: #c82333; }

        /* Main area */
        .main-area { display: grid; grid-template-columns: 260px 1fr; gap: 14px; padding: 0 18px 18px 18px; }
        .sidebar { display: none; }
        .sidebar.show { display: block; }
        .sidebar-card {
            border: 1px solid #e5e7eb; background: #fff; border-radius: 12px; overflow: hidden;
        }
        .sidebar-section { padding: 12px; border-bottom: 1px solid #eef0f3; }
        .sidebar-title { font-weight: 700; margin-bottom: 8px; font-size: 14px; }

        .fb-item {
            padding: 8px 10px;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            margin-bottom: 6px;
            cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            transition: background 0.15s, border-color 0.15s;
        }
        .fb-item:hover { background: #f2f7ff; border-color: #cfe1ff; }
        .fb-count { background: #6b7280; color: #fff; padding: 2px 7px; border-radius: 10px; font-size: 11px; }

        .key-result {
            padding: 8px 10px;
            background: #fff9e6;
            border: 1px solid #ffe8a3;
            border-radius: 10px;
            margin-bottom: 6px;
            cursor: pointer;
        }
        .key-result-number { font-weight: 700; color: #8a6d3b; }
        .key-result-info { font-size: 12px; color: #6b7280; margin-top: 3px; }

        .content-card { border: 1px solid #e5e7eb; background: #fff; border-radius: 12px; overflow: hidden; }

        .tour-info {
            padding: 12px 14px;
            background: #e9fbef;
            border-bottom: 1px solid #d1fadf;
            display: none;
        }
        .tour-info.show { display: block; }
        .tour-info-header { font-weight: 700; margin-bottom: 6px; color: #166534; }
        .tour-info-stats { display: flex; gap: 20px; font-size: 13px; flex-wrap: wrap; }

        .welcome {
            padding: 60px 20px;
            text-align: center;
            color: #6b7280;
        }
        .welcome h2 { font-size: 22px; margin-bottom: 8px; color: #374151; }

        /* Tabelle */
        .table-wrap { max-height: 70vh; overflow: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        thead { position: sticky; top: 0; background: #f8fafc; z-index: 5; }
        th, td { padding: 10px 8px; border-bottom: 1px solid #f0f2f5; text-align: left; }
        th { font-weight: 700; color: #4b5563; border-bottom: 2px solid #e5e7eb; white-space: nowrap; }
        tbody tr:hover { background: #fafcff; }

        .csb-btn { background: #eef5ff; border: 1px solid #cfe1ff; padding: 3px 8px; cursor: pointer; font-weight: 700; color: #1d4ed8; font-size: 12px; border-radius: 8px; }
        .csb-btn:hover { background: #e2eeff; }
        .key-badge { background: #fff3cd; color: #856404; padding: 2px 6px; border: 1px solid #ffeaa7; font-weight: 700; display: inline-block; border-radius: 8px; }
        .tour-btn { display: inline-block; background: #fff; border: 1px solid #22c55e; color: #16a34a; padding: 2px 6px; margin: 1px; cursor: pointer; font-size: 11px; font-weight: 600; border-radius: 8px; }
        .tour-btn:hover { background: #22c55e; color: #fff; }
        .maps-btn { background: #6b7280; color: #fff; padding: 5px 10px; border: none; cursor: pointer; font-size: 12px; text-decoration: none; display: inline-block; border-radius: 8px; }
        .maps-btn:hover { background: #4b5563; }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-thumb { background: #c9ced6; border-radius: 6px; }
        ::-webkit-scrollbar-thumb:hover { background: #aab3bf; }

        @media (max-width: 980px) {
            .main-area { grid-template-columns: 1fr; }
        }
        @media (max-width: 640px) {
            .search-bar { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<div class="page">
  <div class="container">
    <div class="card">
      <div class="header">
        <div class="title">Kunden-Suche</div>
        <div class="search-bar">
          <div class="search-group">
            <span class="search-label">Suche</span>
            <input type="text" id="smartSearch" placeholder="Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1–4 Ziffern)">
          </div>
          <div class="search-group">
            <span class="search-label">Schlüssel</span>
            <input type="text" id="keySearch" placeholder="Exakte Schlüsselnummer">
          </div>
        </div>
      </div>

      <div class="toolbar">
        <div class="stats" id="trefferInfo">Bereit</div>
        <div style="display:flex; gap:10px;">
          <button class="btn" onclick="showFachberater()">Fachberater-Liste</button>
          <button class="btn btn-danger" onclick="clearAll()">Zurücksetzen</button>
        </div>
      </div>

      <div class="main-area">
        <div class="sidebar" id="sidebar">
          <div class="sidebar-card">
            <div class="sidebar-section" id="fachberaterSection" style="display:none;">
              <div class="sidebar-title">Fachberater</div>
              <div id="fachberaterList"></div>
            </div>
            <div class="sidebar-section" id="keySection" style="display:none;">
              <div class="sidebar-title">Schlüssel-Ergebnisse</div>
              <div id="keyResultList"></div>
            </div>
          </div>
        </div>

        <div>
          <div id="tourInfo" class="tour-info">
            <div class="tour-info-header" id="tourInfoHeader"></div>
            <div class="tour-info-stats" id="tourInfoStats"></div>
          </div>

          <div class="content-card">
            <div id="welcome" class="welcome">
              <h2>Willkommen</h2>
              <p>Tippe zum Suchen: Text (Name/Ort/CSB/SAP/Fachberater) oder Tour (1–4 Ziffern).</p>
              <p>Schlüssel-Suche rechts: exakte Nummer.</p>
            </div>

            <div class="table-wrap" id="tableWrap" style="display:none;">
              <table>
                <thead>
                  <tr>
                    <th>CSB</th>
                    <th>SAP</th>
                    <th>Name</th>
                    <th>Straße</th>
                    <th>PLZ</th>
                    <th>Ort</th>
                    <th>Schlüssel</th>
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
      </div> <!-- main-area -->
    </div>
  </div>
</div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);

// Debounce
function debounce(fn, delay = 200) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn.apply(null, args), delay); };
}

let allCustomers = [];

function initializeData() {
  const kundenMap = new Map();
  for (const [tour, list] of Object.entries(tourkundenData)) {
    list.forEach(k => {
      const key = k.csb_nummer;
      if (!key) return;
      if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
      kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(kundenMap.values());
}

function createRow(k) {
  const tr = document.createElement('tr');

  const csb = k.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
  const sap = k.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
  const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
  const schluessel = k.schluessel || '-';

  const tdCSB = document.createElement('td');
  const csbBtn = document.createElement('button');
  csbBtn.className = 'csb-btn';
  csbBtn.textContent = csb;
  csbBtn.onclick = () => { $('#smartSearch').value = csb; smartSearch(); };
  tdCSB.appendChild(csbBtn);

  const tdSAP = document.createElement('td'); tdSAP.textContent = sap;
  const tdName = document.createElement('td'); tdName.textContent = k.name;
  const tdStrasse = document.createElement('td'); tdStrasse.textContent = k.strasse;
  const tdPLZ = document.createElement('td'); tdPLZ.textContent = plz;
  const tdOrt = document.createElement('td'); tdOrt.textContent = k.ort;

  const tdKey = document.createElement('td');
  if (schluessel !== '-') {
    const badge = document.createElement('span');
    badge.className = 'key-badge';
    badge.textContent = schluessel;
    tdKey.appendChild(badge);
  } else { tdKey.textContent = '-'; }

  const tdTour = document.createElement('td');
  k.touren.forEach(t => {
    const b = document.createElement('button');
    b.className = 'tour-btn';
    b.textContent = `${t.tournummer} (${t.liefertag.substring(0,2)})`;
    b.onclick = () => { $('#smartSearch').value = t.tournummer; smartSearch(); };
    tdTour.appendChild(b);
  });

  const tdFB = document.createElement('td'); tdFB.textContent = k.fachberater;

  const tdAct = document.createElement('td');
  const m = document.createElement('a');
  m.className = 'maps-btn';
  m.textContent = 'Maps';
  m.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
  m.target = '_blank';
  tdAct.appendChild(m);

  tr.append(tdCSB, tdSAP, tdName, tdStrasse, tdPLZ, tdOrt, tdKey, tdTour, tdFB, tdAct);
  return tr;
}

function render(customers, infoMsgIfEmpty) {
  const wrap = $('#tableWrap');
  const body = $('#tableBody');
  const welcome = $('#welcome');
  const stats = $('#trefferInfo');

  body.innerHTML = '';

  if (customers && customers.length > 0) {
    welcome.style.display = 'none';
    wrap.style.display = 'block';
    customers.forEach(k => body.appendChild(createRow(k)));
    stats.textContent = customers.length + ' Kunde' + (customers.length === 1 ? '' : 'n') + ' gefunden';
  } else {
    wrap.style.display = 'none';
    welcome.style.display = 'block';
    welcome.innerHTML = '<h2>Keine Ergebnisse</h2><p>' + (infoMsgIfEmpty || 'Keine Kunden gefunden') + '</p>';
    stats.textContent = 'Keine Treffer';
  }
}

function clearSidebar() {
  $('#sidebar').classList.remove('show');
  $('#fachberaterSection').style.display = 'none';
  $('#keySection').style.display = 'none';
}

function smartSearch() {
  const qRaw = $('#smartSearch').value.trim();
  const tourInfo = $('#tourInfo');
  clearSidebar();

  if (!qRaw) {
    tourInfo.classList.remove('show');
    $('#welcome').style.display = 'block';
    $('#tableWrap').style.display = 'none';
    $('#trefferInfo').textContent = 'Bereit';
    return;
  }

  const isDigits = /^\\d{1,4}$/.test(qRaw);
  let results = [];

  if (isDigits) {
    // Tour-Prefix (1-3), exakt (4)
    const exact = qRaw.length === 4;
    results = allCustomers.filter(k => k.touren.some(t => t.tournummer.startsWith(qRaw)));

    if (results.length > 0) {
      const toursSeen = new Set();
      const dayCount = {};
      results.forEach(k => k.touren.forEach(t => {
        if (t.tournummer.startsWith(qRaw)) {
          toursSeen.add(t.tournummer);
          dayCount[t.liefertag] = (dayCount[t.liefertag] || 0) + 1;
        }
      }));
      $('#tourInfoHeader').textContent = exact
        ? 'Tour ' + qRaw + ': ' + results.length + ' Kunden'
        : 'Tour-Prefix ' + qRaw + '*: ' + results.length + ' Kunden · ' + toursSeen.size + ' Touren';
      $('#tourInfoStats').innerHTML = Object.entries(dayCount).map(([d,c]) => '<span><strong>' + d + ':</strong> ' + c + ' Kunden</span>').join('');
      tourInfo.classList.add('show');
    } else {
      tourInfo.classList.remove('show');
    }
    render(results, 'Keine Treffer für Tour' + (exact ? '' : '-Prefix') + ' "' + qRaw + '"');

  } else {
    // Allgemeinsuche (Text)
    const q = qRaw.toLowerCase();
    tourInfo.classList.remove('show');
    results = allCustomers.filter(k => {
      const text = (k.name + ' ' + k.strasse + ' ' + k.ort + ' ' + k.csb_nummer + ' ' + k.sap_nummer + ' ' + k.fachberater).toLowerCase();
      return text.includes(q);
    });
    render(results, 'Keine Kunden für "' + qRaw + '" gefunden');
  }
}

function searchKey() {
  const q = $('#keySearch').value.trim();
  const tourInfo = $('#tourInfo');
  clearSidebar();
  tourInfo.classList.remove('show');

  if (!q) {
    $('#welcome').style.display = 'block';
    $('#tableWrap').style.display = 'none';
    $('#trefferInfo').textContent = 'Bereit';
    return;
  }

  const results = allCustomers.filter(k => k.schluessel === q);

  if (results.length > 0) {
    $('#sidebar').classList.add('show');
    $('#keySection').style.display = 'block';
    const list = $('#keyResultList');
    list.innerHTML = '';
    results.forEach(k => {
      const div = document.createElement('div');
      div.className = 'key-result';
      div.innerHTML = '<div class="key-result-number">Schlüssel: ' + k.schluessel + '</div>' +
                      '<div class="key-result-info">CSB: ' + k.csb_nummer + ' - ' + k.name + '</div>';
      div.onclick = () => { $('#smartSearch').value = (k.csb_nummer || ''); smartSearch(); };
      list.appendChild(div);
    });
  }
  render(results, 'Kein Kunde mit Schlüssel "' + q + '" gefunden');
}

function showFachberater() {
  clearAll();
  const counts = {};
  allCustomers.forEach(k => { if (k.fachberater) counts[k.fachberater] = (counts[k.fachberater] || 0) + 1; });

  $('#sidebar').classList.add('show');
  $('#fachberaterSection').style.display = 'block';

  const list = $('#fachberaterList');
  list.innerHTML = '';
  Object.entries(counts).sort((a,b) => a[0].localeCompare(b[0])).forEach(([fb,c]) => {
    const div = document.createElement('div');
    div.className = 'fb-item';
    div.innerHTML = '<span>' + fb + '</span><span class="fb-count">' + c + '</span>';
    div.onclick = () => { $('#smartSearch').value = fb; smartSearch(); };
    list.appendChild(div);
  });
}

function clearAll() {
  $('#smartSearch').value = '';
  $('#keySearch').value = '';
  $('#tourInfo').classList.remove('show');
  $('#sidebar').classList.remove('show');
  $('#fachberaterSection').style.display = 'none';
  $('#keySection').style.display = 'none';
  $('#welcome').style.display = 'block';
  $('#tableWrap').style.display = 'none';
  $('#trefferInfo').textContent = 'Bereit';
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  $('#smartSearch').addEventListener('input', debounce(smartSearch, 200));
  $('#keySearch').addEventListener('input', debounce(searchKey, 200));

  if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
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
st.markdown("Eine Eingabe: **Text** (Name/Ort/CSB/SAP/Fachberater) **oder** **Tour** (1–4 Ziffern). Schlüssel separat als exakte Suche.")

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
                # Schlüssel laden
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
                st.error("Keine Daten gefunden – Blattnamen/Spalten prüfen.")
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
