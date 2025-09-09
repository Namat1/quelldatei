import streamlit as st
import pandas as pd
import json

# --- Kompaktes Listen-HTML mit Buttons und exakter Suche ---
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
            padding: 15px;
            margin-bottom: 10px;
        }

        .search-row {
            display: flex;
            gap: 15px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .search-group {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .search-label {
            font-weight: 600;
            color: #666;
            min-width: 60px;
        }

        input[type="text"] { 
            padding: 6px 10px; 
            border: 1px solid #ccc; 
            font-size: 13px;
            width: 180px;
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: #0066cc; 
        }

        .btn { 
            padding: 6px 16px; 
            font-size: 13px; 
            border: 1px solid #0066cc; 
            background: #0066cc;
            color: white;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.2s;
        }

        .btn:hover { 
            background: #0052a3;
        }

        .btn-secondary {
            background: white;
            color: #333;
            border: 1px solid #ccc;
        }

        .btn-secondary:hover {
            background: #f0f0f0;
        }

        .btn-danger {
            background: #dc3545;
            border-color: #dc3545;
        }

        .btn-danger:hover {
            background: #c82333;
        }

        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .stats { 
            font-size: 14px; 
            color: #666;
            font-weight: 600;
            padding: 10px;
            background: #f8f8f8;
            border-top: 1px solid #ddd;
        }

        /* Hauptbereich */
        .main-area {
            display: flex;
            gap: 10px;
        }

        .sidebar {
            width: 280px;
            background: white;
            border: 1px solid #ddd;
            display: none;
        }

        .sidebar.show {
            display: block;
        }

        .sidebar-section {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        .sidebar-title {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .content {
            flex: 1;
            background: white;
            border: 1px solid #ddd;
            min-height: 400px;
        }

        /* Startbildschirm */
        .welcome-screen {
            padding: 80px 20px;
            text-align: center;
            color: #666;
        }

        .welcome-screen h2 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #333;
        }

        .welcome-screen p {
            font-size: 14px;
            margin-bottom: 5px;
        }

        /* Tabelle */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            display: none;
        }

        .data-table.show {
            display: table;
        }

        .data-table thead {
            background: #f8f8f8;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .data-table th {
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            white-space: nowrap;
        }

        .data-table td {
            padding: 8px;
            border-bottom: 1px solid #eee;
        }

        .data-table tbody tr:hover {
            background: #f9f9f9;
        }

        /* Zellentypen */
        .csb-btn {
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            padding: 2px 8px;
            cursor: pointer;
            font-weight: 600;
            color: #0066cc;
            font-size: 12px;
        }

        .csb-btn:hover {
            background: #cce5ff;
        }

        .key-badge {
            background: #fff3cd;
            color: #856404;
            padding: 2px 6px;
            border: 1px solid #ffeaa7;
            font-weight: 600;
            display: inline-block;
        }

        .tour-btn {
            display: inline-block;
            background: white;
            border: 1px solid #28a745;
            color: #28a745;
            padding: 2px 6px;
            margin: 1px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 500;
        }

        .tour-btn:hover {
            background: #28a745;
            color: white;
        }

        .maps-btn {
            background: #6c757d;
            color: white;
            padding: 3px 10px;
            border: none;
            cursor: pointer;
            font-size: 11px;
            text-decoration: none;
            display: inline-block;
        }

        .maps-btn:hover {
            background: #5a6268;
        }

        /* Tour-Info */
        .tour-info {
            padding: 15px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            margin-bottom: 10px;
            display: none;
        }

        .tour-info.show {
            display: block;
        }

        .tour-info-header {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 8px;
            color: #155724;
        }

        .tour-info-stats {
            display: flex;
            gap: 20px;
            font-size: 14px;
        }

        /* Fachberater Liste */
        .fb-item {
            padding: 6px 10px;
            border: 1px solid #ddd;
            margin-bottom: 5px;
            cursor: pointer;
            background: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .fb-item:hover {
            background: #e7f3ff;
            border-color: #0066cc;
        }

        .fb-count {
            background: #6c757d;
            color: white;
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 11px;
        }

        /* Schlüssel-Liste */
        .key-result {
            padding: 8px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            margin-bottom: 5px;
            cursor: pointer;
        }

        .key-result:hover {
            background: #ffe69c;
        }

        .key-result-number {
            font-weight: 600;
            color: #856404;
            font-size: 14px;
        }

        .key-result-info {
            font-size: 12px;
            color: #666;
            margin-top: 2px;
        }

        /* Allgemeine Buttons */
        .action-buttons {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }

        .clear-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 20px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
        }

        .clear-btn:hover {
            background: #c82333;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #999;
        }

        /* Mobile */
        @media(max-width: 768px) {
            .main-area {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
            }
            
            .search-row {
                flex-direction: column;
            }
            
            .search-group {
                width: 100%;
            }
            
            input[type="text"] {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-bar">
            <div class="search-row">
                <div class="search-group">
                    <span class="search-label">Allgemein:</span>
                    <input type="text" id="globalSearch" placeholder="Name, Ort, CSB, SAP...">
                    <button class="btn" onclick="searchGeneral()">Suchen</button>
                </div>
                <div class="search-group">
                    <span class="search-label">Schlüssel:</span>
                    <input type="text" id="keySearch" placeholder="Exakte Nummer">
                    <button class="btn" onclick="searchKey()">Suchen</button>
                </div>
                <div class="search-group">
                    <span class="search-label">Tour:</span>
                    <input type="text" id="tourSearch" placeholder="4-stellig">
                    <button class="btn" onclick="searchTour()">Anzeigen</button>
                </div>
            </div>
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showAllCustomers()">Alle Kunden anzeigen</button>
                <button class="btn btn-secondary" onclick="showFachberater()">Fachberater-Liste</button>
                <button class="btn btn-danger" onclick="clearAll()">Zurücksetzen</button>
            </div>
            <div class="stats" id="trefferInfo">Bereit für Suche</div>
        </div>

        <div id="tourInfo" class="tour-info">
            <div class="tour-info-header" id="tourInfoHeader"></div>
            <div class="tour-info-stats" id="tourInfoStats"></div>
        </div>

        <div class="main-area">
            <div id="sidebar" class="sidebar">
                <div id="fachberaterSection" class="sidebar-section" style="display:none;">
                    <div class="sidebar-title">Fachberater</div>
                    <div id="fachberaterList"></div>
                </div>
                
                <div id="keySection" class="sidebar-section" style="display:none;">
                    <div class="sidebar-title">Schlüssel-Ergebnisse</div>
                    <div id="keyResultList"></div>
                </div>
            </div>

            <div class="content">
                <div id="welcomeScreen" class="welcome-screen">
                    <h2>Willkommen zur Kundensuche</h2>
                    <p>Nutzen Sie die Suchfelder oben für:</p>
                    <p>• Allgemeine Suche nach Name, Ort, CSB oder SAP</p>
                    <p>• Exakte Schlüsselsuche</p>
                    <p>• Tour-Anzeige (4-stellige Nummer)</p>
                    <p style="margin-top: 20px;">Oder klicken Sie auf "Alle Kunden anzeigen"</p>
                </div>
                
                <table id="dataTable" class="data-table">
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
                    <tbody id="tableBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);
const $$ = sel => document.querySelectorAll(sel);

// Globale Variablen
let allCustomers = [];
let currentView = 'welcome';

// Kundendaten aufbereiten
function initializeData() {
    const kundenMap = new Map();
    
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) {
                kundenMap.set(key, { ...k, touren: [] });
            }
            kundenMap.get(key).touren.push({ 
                tournummer: tour, 
                liefertag: k.liefertag 
            });
        });
    }
    
    allCustomers = Array.from(kundenMap.values());
}

// Tabellen-Zeile erstellen
function createTableRow(kunde) {
    const tr = document.createElement('tr');
    
    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
    const schluessel = kunde.schluessel || '-';
    
    // CSB als Button
    const csbTd = document.createElement('td');
    const csbBtn = document.createElement('button');
    csbBtn.className = 'csb-btn';
    csbBtn.textContent = csb;
    csbBtn.onclick = () => {
        $('#globalSearch').value = csb;
        searchGeneral();
    };
    csbTd.appendChild(csbBtn);
    
    // SAP
    const sapTd = document.createElement('td');
    sapTd.textContent = sap;
    
    // Name
    const nameTd = document.createElement('td');
    nameTd.textContent = kunde.name;
    
    // Straße
    const strasseTd = document.createElement('td');
    strasseTd.textContent = kunde.strasse;
    
    // PLZ
    const plzTd = document.createElement('td');
    plzTd.textContent = plz;
    
    // Ort
    const ortTd = document.createElement('td');
    ortTd.textContent = kunde.ort;
    
    // Schlüssel
    const keyTd = document.createElement('td');
    if (schluessel !== '-') {
        const keyBadge = document.createElement('span');
        keyBadge.className = 'key-badge';
        keyBadge.textContent = schluessel;
        keyTd.appendChild(keyBadge);
    } else {
        keyTd.textContent = '-';
    }
    
    // Touren als Buttons
    const tourTd = document.createElement('td');
    kunde.touren.forEach(t => {
        const tourBtn = document.createElement('button');
        tourBtn.className = 'tour-btn';
        tourBtn.textContent = `${t.tournummer} (${t.liefertag.substring(0,2)})`;
        tourBtn.onclick = () => {
            $('#tourSearch').value = t.tournummer;
            searchTour();
        };
        tourTd.appendChild(tourBtn);
    });
    
    // Fachberater
    const fbTd = document.createElement('td');
    fbTd.textContent = kunde.fachberater;
    
    // Maps Button
    const actionTd = document.createElement('td');
    const mapsBtn = document.createElement('a');
    mapsBtn.className = 'maps-btn';
    mapsBtn.textContent = 'Maps';
    mapsBtn.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort
    )}`;
    mapsBtn.target = '_blank';
    actionTd.appendChild(mapsBtn);
    
    tr.append(csbTd, sapTd, nameTd, strasseTd, plzTd, ortTd, keyTd, tourTd, fbTd, actionTd);
    
    return tr;
}

// Ansicht aktualisieren
function updateView(customers, message) {
    const welcomeScreen = $('#welcomeScreen');
    const dataTable = $('#dataTable');
    const tableBody = $('#tableBody');
    const trefferInfo = $('#trefferInfo');
    
    // Welcome Screen ausblenden
    welcomeScreen.style.display = 'none';
    
    // Tabelle leeren und füllen
    tableBody.innerHTML = '';
    
    if (customers.length > 0) {
        dataTable.classList.add('show');
        customers.forEach(kunde => {
            tableBody.appendChild(createTableRow(kunde));
        });
        trefferInfo.textContent = `${customers.length} Kunde${customers.length === 1 ? '' : 'n'} gefunden`;
    } else {
        dataTable.classList.remove('show');
        welcomeScreen.style.display = 'block';
        welcomeScreen.innerHTML = `<h2>Keine Ergebnisse</h2><p>${message || 'Keine Kunden gefunden'}</p>`;
        trefferInfo.textContent = 'Keine Treffer';
    }
}

// Suchfunktionen
function searchGeneral() {
    const query = $('#globalSearch').value.trim().toLowerCase();
    if (!query) return;
    
    clearSidebar();
    $('#tourInfo').classList.remove('show');
    
    const results = allCustomers.filter(kunde => {
        const searchText = `${kunde.name} ${kunde.strasse} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater}`.toLowerCase();
        return searchText.includes(query);
    });
    
    updateView(results, `Keine Kunden für "${query}" gefunden`);
}

function searchKey() {
    const query = $('#keySearch').value.trim();
    if (!query) return;
    
    clearSidebar();
    $('#tourInfo').classList.remove('show');
    
    // Exakte Suche nach Schlüssel
    const results = allCustomers.filter(kunde => {
        return kunde.schluessel === query;
    });
    
    // Sidebar mit Ergebnissen anzeigen
    if (results.length > 0) {
        $('#sidebar').classList.add('show');
        $('#keySection').style.display = 'block';
        const keyResultList = $('#keyResultList');
        keyResultList.innerHTML = '';
        
        results.forEach(kunde => {
            const item = document.createElement('div');
            item.className = 'key-result';
            item.innerHTML = `
                <div class="key-result-number">Schlüssel: ${kunde.schluessel}</div>
                <div class="key-result-info">CSB: ${kunde.csb_nummer} - ${kunde.name}</div>
            `;
            item.onclick = () => {
                $('#globalSearch').value = kunde.csb_nummer;
                searchGeneral();
            };
            keyResultList.appendChild(item);
        });
    }
    
    updateView(results, `Kein Kunde mit Schlüssel "${query}" gefunden`);
}

function searchTour() {
    const query = $('#tourSearch').value.trim();
    if (!query.match(/^\\d{4}$/)) {
        alert('Bitte geben Sie eine 4-stellige Tournummer ein');
        return;
    }
    
    clearSidebar();
    
    const results = allCustomers.filter(kunde => {
        return kunde.touren.some(t => t.tournummer === query);
    });
    
    if (results.length > 0) {
        // Tour-Info anzeigen
        const tourInfo = $('#tourInfo');
        const tourInfoHeader = $('#tourInfoHeader');
        const tourInfoStats = $('#tourInfoStats');
        
        const dayCount = {};
        results.forEach(kunde => {
            kunde.touren.forEach(t => {
                if (t.tournummer === query) {
                    dayCount[t.liefertag] = (dayCount[t.liefertag] || 0) + 1;
                }
            });
        });
        
        tourInfoHeader.textContent = `Tour ${query}: ${results.length} Kunden`;
        tourInfoStats.innerHTML = Object.entries(dayCount)
            .map(([day, count]) => `<span><strong>${day}:</strong> ${count} Kunden</span>`)
            .join('');
        
        tourInfo.classList.add('show');
    } else {
        $('#tourInfo').classList.remove('show');
    }
    
    updateView(results, `Tour "${query}" nicht gefunden`);
}

function showAllCustomers() {
    clearSidebar();
    $('#tourInfo').classList.remove('show');
    updateView(allCustomers, '');
}

function showFachberater() {
    clearAll();
    
    // Fachberater zählen
    const fbCount = {};
    allCustomers.forEach(kunde => {
        const fb = kunde.fachberater;
        if (fb) {
            fbCount[fb] = (fbCount[fb] || 0) + 1;
        }
    });
    
    // Sidebar anzeigen
    $('#sidebar').classList.add('show');
    $('#fachberaterSection').style.display = 'block';
    const fbList = $('#fachberaterList');
    fbList.innerHTML = '';
    
    Object.entries(fbCount)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .forEach(([fb, count]) => {
            const item = document.createElement('div');
            item.className = 'fb-item';
            item.innerHTML = `
                <span>${fb}</span>
                <span class="fb-count">${count}</span>
            `;
            item.onclick = () => {
                $('#globalSearch').value = fb;
                searchGeneral();
            };
            fbList.appendChild(item);
        });
}

function clearSidebar() {
    $('#sidebar').classList.remove('show');
    $('#fachberaterSection').style.display = 'none';
    $('#keySection').style.display = 'none';
}

function clearAll() {
    $('#globalSearch').value = '';
    $('#keySearch').value = '';
    $('#tourSearch').value = '';
    $('#tourInfo').classList.remove('show');
    $('#dataTable').classList.remove('show');
    $('#welcomeScreen').style.display = 'block';
    $('#welcomeScreen').innerHTML = `
        <h2>Willkommen zur Kundensuche</h2>
        <p>Nutzen Sie die Suchfelder oben für:</p>
        <p>• Allgemeine Suche nach Name, Ort, CSB oder SAP</p>
        <p>• Exakte Schlüsselsuche</p>
        <p>• Tour-Anzeige (4-stellige Nummer)</p>
        <p style="margin-top: 20px;">Oder klicken Sie auf "Alle Kunden anzeigen"</p>
    `;
    $('#trefferInfo').textContent = 'Bereit für Suche';
    clearSidebar();
}

// Enter-Taste für Suche
document.addEventListener('DOMContentLoaded', () => {
    $('#globalSearch').addEventListener('keypress', e => {
        if (e.key === 'Enter') searchGeneral();
    });
    $('#keySearch').addEventListener('keypress', e => {
        if (e.key === 'Enter') searchKey();
    });
    $('#tourSearch').addEventListener('keypress', e => {
        if (e.key === 'Enter') searchTour();
    });
});

// Initialisierung
if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    initializeData();
} else {
    $('#welcomeScreen').innerHTML = '<h2>Fehler</h2><p>Keine Kundendaten geladen</p>';
}
</script>

</body>
</html>
"""

st.title("Kunden-Suchseite")
st.markdown("Kompakte Listenansicht mit separaten Suchfunktionen")

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
    
    with st.expander("Neue Features"):
        st.markdown("""
        ✅ **Leerer Startbildschirm** - Willkommensseite statt direkt alle Daten
        
        ✅ **Exakte Schlüsselsuche** - Nur exakte Treffer (54 findet nur 54, nicht 154)
        
        ✅ **Mehr Buttons** - Alle Aktionen als Buttons statt Links
        
        ✅ **Separate Suchen** - Jede Suche startet neu, keine Kombination
        
        ✅ **Verbesserte Navigation**:
        - CSB-Nummern als klickbare Buttons
        - Tour-Nummern als grüne Buttons
        - Schlüssel als gelbe Badges
        - Maps als graue Buttons
        
        ✅ **Übersichtliche Steuerung**:
        - "Alle Kunden anzeigen" Button
        - "Fachberater-Liste" Button
        - "Zurücksetzen" Button in Rot
        """)
