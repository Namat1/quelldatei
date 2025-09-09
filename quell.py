import streamlit as st
import pandas as pd
import json

# --- Kompaktes Listen-HTML ohne Overlays ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Kunden-Suche</title>
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }

        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            background: #f5f5f5;
            color: #333;
            font-size: 13px;
            line-height: 1.4;
        }

        .container { 
            max-width: 1400px; 
            margin: 0 auto;
            padding: 10px;
        }

        /* Header mit Suchfeldern */
        .search-bar {
            background: white;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }

        .search-group {
            display: flex;
            gap: 5px;
            align-items: center;
            flex: 1;
            min-width: 200px;
        }

        .search-label {
            font-weight: 600;
            white-space: nowrap;
            color: #666;
        }

        input[type="text"] { 
            flex: 1;
            padding: 5px 8px; 
            border: 1px solid #ccc; 
            font-size: 13px;
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: #0066cc; 
        }

        button { 
            padding: 5px 12px; 
            font-size: 13px; 
            border: 1px solid #ccc; 
            background: white;
            cursor: pointer; 
        }

        button:hover { 
            background: #f0f0f0;
        }

        .stats { 
            font-size: 12px; 
            color: #666;
            margin-left: auto;
        }

        /* Hauptbereich */
        .main-area {
            display: flex;
            gap: 10px;
        }

        .sidebar {
            width: 250px;
            background: white;
            border: 1px solid #ddd;
            padding: 10px;
            max-height: calc(100vh - 100px);
            overflow-y: auto;
        }

        .sidebar-title {
            font-weight: 600;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
        }

        .content {
            flex: 1;
            background: white;
            border: 1px solid #ddd;
        }

        /* Tabelle */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        .data-table thead {
            background: #f8f8f8;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .data-table th {
            padding: 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            white-space: nowrap;
        }

        .data-table td {
            padding: 6px 8px;
            border-bottom: 1px solid #eee;
        }

        .data-table tbody tr:hover {
            background: #f9f9f9;
        }

        .data-table tbody tr.highlighted {
            background: #fff3cd;
        }

        /* Kompakte Info-Spalten */
        .csb-cell {
            font-weight: 600;
            color: #0066cc;
            cursor: pointer;
        }

        .csb-cell:hover {
            text-decoration: underline;
        }

        .key-cell {
            color: #d9534f;
            font-weight: 600;
        }

        .tour-cell {
            font-size: 11px;
        }

        .tour-tag {
            display: inline-block;
            background: #e7f3ff;
            padding: 2px 4px;
            margin: 1px;
            cursor: pointer;
            border: 1px solid #b3d9ff;
        }

        .tour-tag:hover {
            background: #cce5ff;
        }

        .maps-link {
            color: #0066cc;
            text-decoration: none;
            font-size: 11px;
        }

        .maps-link:hover {
            text-decoration: underline;
        }

        /* Tour-Bereich */
        .tour-section {
            padding: 10px;
            background: #f0f8ff;
            border-bottom: 2px solid #0066cc;
            display: none;
        }

        .tour-section.show {
            display: block;
        }

        .tour-header {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .tour-stats {
            display: flex;
            gap: 20px;
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }

        /* Fachberater Liste */
        .fb-list {
            font-size: 12px;
        }

        .fb-item {
            padding: 4px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }

        .fb-item:hover {
            background: #f0f0f0;
        }

        .fb-count {
            float: right;
            color: #999;
        }

        /* Schlüssel-Liste */
        .key-list {
            margin-top: 20px;
        }

        .key-item {
            display: flex;
            justify-content: space-between;
            padding: 4px;
            border-bottom: 1px solid #eee;
            font-size: 12px;
        }

        .key-item:hover {
            background: #f0f0f0;
        }

        .hidden { 
            display: none !important; 
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-thumb {
            background: #ccc;
        }

        /* Mobile */
        @media(max-width: 768px) {
            .main-area {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                max-height: 200px;
            }
            
            .search-bar {
                flex-direction: column;
            }
            
            .search-group {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-bar">
            <div class="search-group">
                <span class="search-label">Suche:</span>
                <input type="text" id="globalSearch" placeholder="Name, Ort, CSB, SAP...">
            </div>
            <div class="search-group">
                <span class="search-label">Schlüssel:</span>
                <input type="text" id="keySearch" placeholder="Schlüsselnummer">
            </div>
            <div class="search-group">
                <span class="search-label">Tour:</span>
                <input type="text" id="tourSearch" placeholder="4-stellig">
            </div>
            <button id="resetBtn">Zurücksetzen</button>
            <div class="stats" id="trefferInfo">0 Treffer</div>
        </div>

        <div id="tourSection" class="tour-section">
            <div class="tour-header" id="tourHeader"></div>
            <div class="tour-stats" id="tourStats"></div>
        </div>

        <div class="main-area">
            <div class="sidebar">
                <div class="sidebar-title">Fachberater</div>
                <div id="fachberaterList" class="fb-list"></div>
                
                <div class="key-list">
                    <div class="sidebar-title">Schlüssel-Suche</div>
                    <div id="keyResultList"></div>
                </div>
            </div>

            <div class="content">
                <table class="data-table">
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
                            <th>Maps</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { 
    const n = document.createElement(tag); 
    if (cls) n.className = cls; 
    if (txt !== undefined) n.textContent = txt; 
    return n; 
};

const buildTableRow = kunde => {
    const tr = el('tr');
    tr.className = 'hidden';
    
    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
    const schluessel = kunde.schluessel || '-';
    
    // Suchtext für Filterung
    const suchtext = `${kunde.name} ${kunde.strasse} ${plz} ${kunde.ort} ${csb} ${sap} ${kunde.fachberater} ${schluessel} ${kunde.touren.map(t => t.tournummer).join(' ')}`.toLowerCase();
    tr.dataset.search = suchtext;
    tr.dataset.key = schluessel.toLowerCase();
    tr.dataset.tours = kunde.touren.map(t => t.tournummer).join(',');
    tr.dataset.fachberater = kunde.fachberater?.toLowerCase() || '';
    
    // CSB
    const csbTd = el('td');
    const csbSpan = el('span', 'csb-cell', csb);
    csbSpan.addEventListener('click', () => {
        $('#globalSearch').value = csb;
        $('#globalSearch').dispatchEvent(new Event('input'));
    });
    csbTd.appendChild(csbSpan);
    
    // SAP
    const sapTd = el('td', '', sap);
    
    // Name
    const nameTd = el('td', '', kunde.name);
    
    // Straße
    const strasseTd = el('td', '', kunde.strasse);
    
    // PLZ
    const plzTd = el('td', '', plz);
    
    // Ort
    const ortTd = el('td', '', kunde.ort);
    
    // Schlüssel
    const keyTd = el('td', 'key-cell', schluessel);
    
    // Touren
    const tourTd = el('td', 'tour-cell');
    kunde.touren.forEach(t => {
        const tag = el('span', 'tour-tag', `${t.tournummer} (${t.liefertag.substring(0,2)})`);
        tag.addEventListener('click', () => {
            $('#tourSearch').value = t.tournummer;
            $('#tourSearch').dispatchEvent(new Event('input'));
        });
        tourTd.appendChild(tag);
    });
    
    // Fachberater
    const fbTd = el('td', '', kunde.fachberater);
    
    // Maps
    const mapsTd = el('td');
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;
    const mapsLink = el('a', 'maps-link', 'Maps');
    mapsLink.href = mapsUrl;
    mapsLink.target = '_blank';
    mapsTd.appendChild(mapsLink);
    
    tr.append(csbTd, sapTd, nameTd, strasseTd, plzTd, ortTd, keyTd, tourTd, fbTd, mapsTd);
    
    return tr;
};

// Main
const tableBody = $('#tableBody');
const treffer = $('#trefferInfo');
const kundenMap = new Map();
const allRows = [];

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    // Kundendaten aufbauen
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
        });
    }

    // Tabelle aufbauen
    kundenMap.forEach(k => {
        const row = buildTableRow(k);
        allRows.push(row);
        tableBody.appendChild(row);
    });

    // Fachberater-Liste
    const fachberaterCounts = {};
    kundenMap.forEach(k => {
        const fb = k.fachberater;
        if (fb) {
            fachberaterCounts[fb] = (fachberaterCounts[fb] || 0) + 1;
        }
    });
    
    const fbList = $('#fachberaterList');
    Object.entries(fachberaterCounts).sort((a, b) => a[0].localeCompare(b[0])).forEach(([fb, count]) => {
        const item = el('div', 'fb-item');
        item.innerHTML = `${fb} <span class="fb-count">${count}</span>`;
        item.addEventListener('click', () => {
            $('#globalSearch').value = fb;
            $('#globalSearch').dispatchEvent(new Event('input'));
        });
        fbList.appendChild(item);
    });

    // Filter-Funktion
    const applyFilters = () => {
        const searchVal = $('#globalSearch').value.trim().toLowerCase();
        const keyVal = $('#keySearch').value.trim().toLowerCase();
        const tourVal = $('#tourSearch').value.trim();
        
        let hits = 0;
        const tourSection = $('#tourSection');
        const tourHeader = $('#tourHeader');
        const tourStats = $('#tourStats');
        
        // Tour-Sektion
        if (tourVal.match(/^\\d{4}$/)) {
            const tourKunden = [];
            allRows.forEach(row => {
                if (row.dataset.tours.includes(tourVal)) {
                    tourKunden.push(row);
                }
            });
            
            if (tourKunden.length > 0) {
                const dayCount = {};
                tourKunden.forEach(row => {
                    // Liefertage zählen (aus den Tour-Tags extrahieren)
                    const tags = row.querySelector('.tour-cell').textContent;
                    const matches = tags.match(/\\((\\w+)\\)/g);
                    if (matches) {
                        matches.forEach(m => {
                            const day = m.slice(1, -1);
                            dayCount[day] = (dayCount[day] || 0) + 1;
                        });
                    }
                });
                
                tourHeader.textContent = `Tour ${tourVal}: ${tourKunden.length} Kunden`;
                tourStats.innerHTML = Object.entries(dayCount).map(([day, count]) => 
                    `<span>${day}: ${count}</span>`
                ).join('');
                tourSection.classList.add('show');
            } else {
                tourSection.classList.remove('show');
            }
        } else {
            tourSection.classList.remove('show');
        }
        
        // Schlüssel-Ergebnisse
        const keyResultList = $('#keyResultList');
        keyResultList.innerHTML = '';
        
        if (keyVal) {
            allRows.forEach(row => {
                if (row.dataset.key.includes(keyVal)) {
                    const csb = row.querySelector('.csb-cell').textContent;
                    const name = row.children[2].textContent;
                    const key = row.children[6].textContent;
                    
                    const item = el('div', 'key-item');
                    item.innerHTML = `<span>${key}</span><span>${csb}</span>`;
                    item.addEventListener('click', () => {
                        $('#globalSearch').value = csb;
                        $('#globalSearch').dispatchEvent(new Event('input'));
                    });
                    keyResultList.appendChild(item);
                }
            });
        }
        
        // Zeilen filtern
        allRows.forEach(row => {
            let show = true;
            
            if (searchVal && !row.dataset.search.includes(searchVal)) show = false;
            if (keyVal && !row.dataset.key.includes(keyVal)) show = false;
            if (tourVal && !row.dataset.tours.includes(tourVal)) show = false;
            
            row.classList.toggle('hidden', !show);
            row.classList.toggle('highlighted', show && (searchVal || keyVal || tourVal));
            if (show) hits++;
        });
        
        treffer.textContent = `${hits} Treffer`;
    };

    // Event Listener
    $('#globalSearch').addEventListener('input', applyFilters);
    $('#keySearch').addEventListener('input', applyFilters);
    $('#tourSearch').addEventListener('input', applyFilters);
    
    $('#resetBtn').addEventListener('click', () => {
        $('#globalSearch').value = '';
        $('#keySearch').value = '';
        $('#tourSearch').value = '';
        $('#keyResultList').innerHTML = '';
        $('#tourSection').classList.remove('show');
        applyFilters();
    });
    
    // Initial anzeigen
    applyFilters();
    
} else {
    tableBody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 40px;">Keine Daten geladen</td></tr>';
}
</script>

</body>
</html>
"""

st.title("Kunden-Suchseite (Listenansicht)")
st.markdown("Kompakte Listenansicht mit separater Schlüsselsuche")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("Schlüsseldatei (CSB/Schlüssel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x): return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", ".")); i = int(f)
        return str(i) if f == i else s
    except Exception:
        return s

def build_key_map(key_df):
    if key_df.shape[1] < 6:
        st.warning("Schlüsseldatei hat weniger als 6 Spalten.")
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
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}

        try:
            with st.spinner("Verarbeite Dateien..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

                tour_dict = {}
                def kunden_sammeln(df):
                    for _, row in df.iterrows():
                        for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                            if spaltenname not in df.columns: continue
                            tournr_raw = str(row[spaltenname]).strip()
                            if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit(): continue
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
                st.error("Keine Daten gefunden")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=2, ensure_ascii=False)
            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Touren", len(sorted_tours))
            with col2:
                st.metric("Kunden", total_customers)
            with col3:
                st.metric("Schlüssel", len(key_map))
            
            st.download_button(
                "⬇️ Download HTML", 
                data=final_html.encode("utf-8"), 
                file_name="kundenliste.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte beide Dateien hochladen")
    
    with st.expander("Features"):
        st.markdown("""
        - **Kompakte Listenansicht** statt Karten
        - **Drei separate Suchfelder**: Allgemein, Schlüssel, Tour
        - **Keine Overlays/Modals** - Tour-Info direkt über der Tabelle
        - **Fachberater-Liste** in der Seitenleiste
        - **Schlüssel-Ergebnisse** in der Seitenleiste
        - **Sortierte Tabelle** mit allen wichtigen Daten
        - **Klickbare Elemente** für schnelle Navigation
        """)
