import streamlit as st
import pandas as pd
import json

# --- Kompakte HTML-Vorlage mit RAL-Farben ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Kunden-Suche</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --ral-1021: #F3DA0B;      /* Rapsgelb */
            --ral-5010: #0E294B;      /* Enzianblau */
            --ral-1021-light: #F8E555; /* Aufgehelltes Rapsgelb */
            --ral-5010-light: #1E3A5F; /* Aufgehelltes Enzianblau */
            --background: #fafbfc;
            --surface: #ffffff;
            --surface-alt: #f8f9fa;
            --border: #e1e5e9;
            --text-primary: #2c3e50;
            --text-secondary: #546e7a;
            --text-muted: #78909c;
            --shadow: 0 1px 3px rgba(0,0,0,0.08);
        }

        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.4;
            font-size: 14px;
        }

        .container { 
            max-width: 1400px; 
            margin: 0 auto;
            padding: 12px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: linear-gradient(135deg, var(--ral-5010) 0%, var(--ral-5010-light) 100%);
            color: white;
            padding: 16px 20px;
            border-radius: 6px;
            margin-bottom: 12px;
            text-align: center;
        }

        .header h1 { 
            font-size: 1.5rem; 
            font-weight: 700; 
            margin-bottom: 4px;
        }

        .header p {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        .search-bar {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: var(--shadow);
        }

        .search-input-row {
            display: flex;
            gap: 8px;
            margin-bottom: 8px;
        }

        input[type="text"] { 
            flex: 1;
            padding: 8px 12px; 
            border: 1px solid var(--border); 
            border-radius: 4px; 
            font-size: 14px;
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: var(--ral-5010); 
            box-shadow: 0 0 0 2px rgba(14, 41, 75, 0.1); 
        }

        .btn-group {
            display: flex;
            gap: 6px;
        }

        button { 
            padding: 8px 12px; 
            font-size: 13px; 
            font-weight: 500; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            transition: all 0.15s ease;
        }

        #resetBtn { 
            background: var(--text-muted); 
            color: white; 
        } 
        #resetBtn:hover { 
            background: var(--text-secondary); 
        }

        #backBtn { 
            display: none; 
            background: var(--ral-1021); 
            color: var(--ral-5010); 
            font-weight: 600;
        } 
        #backBtn:hover { 
            background: var(--ral-1021-light); 
        }

        .stats { 
            font-size: 12px; 
            color: var(--text-secondary); 
            margin-top: 4px;
        }

        .content-area {
            flex: 1;
            display: flex;
            gap: 12px;
            min-height: 0;
        }

        .sidebar {
            width: 350px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .main-content {
            flex: 1;
            min-height: 0;
        }

        .info-box { 
            background: var(--surface); 
            border: 1px solid var(--border); 
            border-radius: 6px; 
            overflow: hidden;
            box-shadow: var(--shadow);
            display: none;
            max-height: 400px;
            display: flex;
            flex-direction: column;
        }

        .info-header { 
            padding: 8px 12px; 
            font-weight: 600; 
            font-size: 13px; 
            background: var(--surface-alt); 
            border-bottom: 1px solid var(--border);
            color: var(--ral-5010);
        }

        .info-content {
            flex: 1;
            overflow-y: auto;
            min-height: 0;
        }

        .list-item { 
            padding: 4px 0; 
            border-bottom: 1px solid #f0f0f0; 
        }

        .list-item:last-child {
            border-bottom: none;
        }

        .list-row { 
            display: grid; 
            grid-template-columns: 70px 120px 1fr 1fr auto; 
            align-items: center; 
            gap: 8px; 
            padding: 4px 12px; 
            font-size: 12px;
        }

        .list-row:hover {
            background: var(--surface-alt);
        }

        .csb-link { 
            font-weight: 600; 
            color: var(--ral-5010); 
            cursor: pointer; 
            text-decoration: none;
            padding: 2px 4px;
            border-radius: 3px;
        }

        .csb-link:hover {
            background: var(--ral-5010);
            color: white;
        }

        .key-info { 
            font-size: 11px;
            color: var(--text-muted); 
        }

        .location { 
            font-weight: 500; 
            color: var(--text-primary); 
        }

        .street { 
            color: var(--text-secondary); 
        }

        .maps-link { 
            padding: 2px 6px;
            background: var(--ral-1021);
            color: var(--ral-5010);
            text-decoration: none;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }

        .maps-link:hover {
            background: var(--ral-1021-light);
        }

        #results { 
            height: calc(100vh - 140px);
            overflow-y: auto;
            padding-right: 4px;
        }

        .customer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 8px;
            padding: 4px;
        }

        .customer-card { 
            background: var(--surface); 
            border: 1px solid var(--border); 
            border-radius: 6px; 
            box-shadow: var(--shadow); 
            transition: all 0.15s ease;
            height: fit-content;
        }

        .customer-card:hover { 
            transform: translateY(-1px); 
            box-shadow: 0 2px 8px rgba(0,0,0,0.12); 
        }

        .customer-card.highlighted { 
            border-left: 3px solid var(--ral-1021); 
            background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
        }

        .card-header {
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
            background: var(--surface-alt);
        }

        .card-title { 
            font-size: 14px; 
            font-weight: 600; 
            color: var(--ral-5010);
            margin-bottom: 2px;
        }

        .card-subtitle {
            font-size: 11px;
            color: var(--text-muted);
        }

        .card-body {
            padding: 10px 12px;
        }

        .card-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 8px;
            font-size: 12px;
        }

        .card-row:last-child {
            margin-bottom: 0;
        }

        .info-item {
            color: var(--text-secondary);
        }

        .info-label {
            font-weight: 500;
            color: var(--text-primary);
        }

        .tours-section {
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid var(--border);
        }

        .tours-title {
            font-size: 11px;
            font-weight: 600;
            color: var(--ral-5010);
            margin-bottom: 4px;
        }

        .tour-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }

        .tour-tag {
            background: var(--ral-5010);
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .tour-tag:hover {
            background: var(--ral-5010-light);
        }

        .card-maps {
            margin-top: 8px;
        }

        .card-maps-btn {
            display: inline-block;
            padding: 4px 8px;
            background: var(--ral-1021);
            color: var(--ral-5010);
            text-decoration: none;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }

        .card-maps-btn:hover {
            background: var(--ral-1021-light);
        }

        .hidden { 
            display: none !important; 
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--surface-alt);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        /* Mobile */
        @media(max-width: 768px) {
            .container { 
                padding: 8px; 
            }
            
            .content-area {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                order: 2;
            }
            
            .customer-grid {
                grid-template-columns: 1fr;
            }
            
            .search-input-row {
                flex-direction: column;
            }
            
            .btn-group {
                flex-wrap: wrap;
            }
            
            button {
                flex: 1;
                min-width: 120px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Kunden-Suche</h1>
            <p>Kompakte Übersicht aller Kunden und Touren</p>
        </div>
        
        <div class="search-bar">
            <div class="search-input-row">
                <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße...">
                <div class="btn-group">
                    <button id="resetBtn">🔄 Reset</button>
                    <button id="backBtn">⬅️ Zurück</button>
                </div>
            </div>
            <div class="stats" id="trefferInfo">🔎 0 Ergebnisse</div>
        </div>

        <div class="content-area">
            <div class="sidebar">
                <div id="tourBox" class="info-box">
                    <div class="info-header">
                        🚚 Tour <span id="tourNumSpan"></span>
                    </div>
                    <div class="info-content" id="tourList"></div>
                </div>
                
                <div id="fachberaterBox" class="info-box">
                    <div class="info-header">
                        👤 <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span>)
                    </div>
                    <div class="info-content" id="fachberaterList"></div>
                </div>
            </div>

            <div class="main-content">
                <div id="results">
                    <div class="customer-grid" id="customerGrid"></div>
                </div>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

const buildCustomerCard = kunde => {
    const card = el('div', 'customer-card hidden');
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${(kunde.schluessel||'')} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    const header = el('div', 'card-header');
    const title = el('div', 'card-title', '🏪 ' + kunde.name);
    const subtitle = el('div', 'card-subtitle', kunde.schluessel ? `Schlüssel: ${kunde.schluessel}` : 'Kein Schlüssel');
    header.append(title, subtitle);

    const body = el('div', 'card-body');
    
    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';

    const row1 = el('div', 'card-row');
    row1.innerHTML = `<div class="info-item"><span class="info-label">CSB:</span> ${csb}</div><div class="info-item"><span class="info-label">SAP:</span> ${sap}</div>`;
    
    const row2 = el('div', 'card-row');
    row2.innerHTML = `<div class="info-item"><span class="info-label">Ort:</span> ${kunde.ort}</div><div class="info-item"><span class="info-label">PLZ:</span> ${plz}</div>`;
    
    const row3 = el('div', 'card-row');
    row3.innerHTML = `<div class="info-item" style="grid-column: 1/-1;"><span class="info-label">Straße:</span> ${kunde.strasse}</div>`;
    
    const row4 = el('div', 'card-row');
    row4.innerHTML = `<div class="info-item" style="grid-column: 1/-1;"><span class="info-label">Fachberater:</span> ${kunde.fachberater}</div>`;

    const toursSection = el('div', 'tours-section');
    const toursTitle = el('div', 'tours-title', '🚛 Touren:');
    const tourTags = el('div', 'tour-tags');
    
    kunde.touren.forEach(t => {
        const tag = el('span', 'tour-tag', `${t.tournummer} (${t.liefertag})`);
        tag.addEventListener('click', () => {
            $('#globalSearch').value = t.tournummer;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            $('#backBtn').style.display = 'inline-block';
        });
        tourTags.appendChild(tag);
    });
    
    toursSection.append(toursTitle, tourTags);

    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;
    const mapsDiv = el('div', 'card-maps');
    const mapsBtn = el('a', 'card-maps-btn', '📍 Maps');
    mapsBtn.href = mapsUrl;
    mapsBtn.target = '_blank';
    mapsDiv.appendChild(mapsBtn);

    body.append(row1, row2, row3, row4, toursSection, mapsDiv);
    card.append(header, body);

    return card;
};

const buildListEntry = (ort, name, strasse, csbNummer, schluessel, mapsUrl, isAlt) => {
    const item = el('div', 'list-item' + (isAlt ? ' alt' : ''));
    const row = el('div', 'list-row');

    const csbDiv = el('div', 'csb-link', csbNummer);
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        $('#backBtn').style.display = 'inline-block';
    });

    const keyDiv = el('div', 'key-info', schluessel ? `S: ${schluessel}` : 'S: -');
    const ortDiv = el('div', 'location', ort);
    const nameDiv = el('div', 'street', name);
    
    const linkDiv = el('div');
    const link = el('a', 'maps-link', '📍');
    link.href = mapsUrl;
    link.target = '_blank';
    linkDiv.appendChild(link);

    row.append(csbDiv, keyDiv, ortDiv, nameDiv, linkDiv);
    item.appendChild(row);
    return item;
};

// Main
let lastTourSearchQuery = '';
const results = $('#results');
const customerGrid = $('#customerGrid');
const treffer = $('#trefferInfo');
const kundenMap = new Map();

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
        });
    }

    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        customerGrid.appendChild(card);
    });

    const input = $('#globalSearch');
    const tourBox = $('#tourBox');
    const tourList = $('#tourList');
    const tourNumLbl = $('#tourNumSpan');
    const fachberaterBox = $('#fachberaterBox');
    const fachberaterList = $('#fachberaterList');
    const fachberaterNameSpan = $('#fachberaterNameSpan');
    const fachberaterCountSpan = $('#fachberaterCountSpan');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.style.display = 'none';
        fachberaterBox.style.display = 'none';

        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const list = [];
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', mapsUrl });
                }
            });

            if (list.length > 0) {
                lastTourSearchQuery = tourN;
                tourList.innerHTML = '';
                tourNumLbl.textContent = `${tourN} (${list.length})`;
                list.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    tourList.appendChild(buildListEntry(kunde.ort, kunde.name, kunde.strasse, kunde.csb, kunde.schluessel, kunde.mapsUrl, i % 2 !== 0));
                });
                tourBox.style.display = 'flex';
            }
        }

        const matchedFachberater = q.length > 2 ? alleFachberater.find(fb => fb.includes(q)) : null;
        if (matchedFachberater) {
            const kundenDesBeraters = [];
            let beraterName = '';
            kundenMap.forEach(k => {
                if (k.fachberater?.toLowerCase() === matchedFachberater) {
                    if (!beraterName) beraterName = k.fachberater;
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    kundenDesBeraters.push({ csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', name: k.name, ort: k.ort, strasse: k.strasse, mapsUrl });
                }
            });

            if (kundenDesBeraters.length > 0) {
                fachberaterNameSpan.textContent = beraterName;
                fachberaterCountSpan.textContent = kundenDesBeraters.length;
                fachberaterList.innerHTML = '';
                kundenDesBeraters.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    fachberaterList.appendChild(buildListEntry(kunde.ort, kunde.name, kunde.strasse, kunde.csb, kunde.schluessel, kunde.mapsUrl, i % 2 !== 0));
                });
                fachberaterBox.style.display = 'flex';
            }
        }

        document.querySelectorAll('.customer-card').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) { c.classList.add('highlighted'); hits++; }
            else { c.classList.remove('highlighted'); }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    $('#backBtn').addEventListener('click', () => {
        if (lastTourSearchQuery) {
            input.value = lastTourSearchQuery;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            $('#backBtn').style.display = 'none';
        }
    });

    $('#resetBtn').addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        $('#backBtn').style.display = 'none';
    });
} else {
    customerGrid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><h3>❌ Keine Daten</h3><p>Kundendaten konnten nicht geladen werden.</p></div>';
}
</script>

</body>
</html>
"""

# --- UI Setup ---
st.title("🚛 Kompakte Kunden-Suchseite")
st.markdown("""
Laden Sie **zwei** Excel-Dateien hoch:
1) **Quelldatei** mit den Kundendaten (mehrere Blätter)  
2) **Schlüsseldatei** mit *CSB in Spalte A* und *Schlüsselnummer in Spalte F*.

Erstellt eine **kompakte HTML-Suchseite** in RAL 1021 (Rapsgelb) und RAL 5010 (Enzianblau).
""")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("📄 Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("🔑 Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])

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
        st.warning("⚠️ Schlüsseldatei hat weniger als 6 Spalten. Es werden die vorhandenen Spalten genutzt.")
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
    if st.button("🎨 Kompakte HTML-Seite erzeugen", type="primary"):
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}

        try:
            with st.spinner("🔑 Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            tour_dict = {}
            def kunden_sammeln(df: pd.DataFrame):
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

            with st.spinner("📥 Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht gefunden.")

            if not tour_dict:
                st.error("❌ Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            st.success(f"✅ Kompakte Seite erstellt! {len(sorted_tours)} Touren verarbeitet.")
            
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            st.info(f"📊 {len(sorted_tours)} Touren • {total_customers} Kunden • {len(key_map)} Schlüssel")
            
            st.download_button(
                "📥 Kompakte `suche.html` herunterladen", 
                data=final_html.encode("utf-8"), 
                file_name="suche.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"❌ Fehler: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("📁 Bitte noch die **Schlüsseldatei** hochladen.")
elif key_file and not excel_file:
    st.info("📁 Bitte noch die **Quelldatei** hochladen.")
else:
    st.info("📋 Bitte beide Dateien hochladen.")
    st.markdown("""
    ### ✨ Kompaktes Design Features:
    - **RAL 1021 (Rapsgelb)** und **RAL 5010 (Enzianblau)** in dezenter Anwendung
    - **Minimale Abstände** für maximale Informationsdichte
    - **Sidebar-Layout** mit fester Höhe - kein vertikales Scrollen
    - **Grid-basierte Kundenkarten** für optimale Raumnutzung
    - **Kompakte Schriftgrößen** und reduzierte Paddings
    - **Zweispalten-Layout** für Desktop-Ansichten
    - **Mobile-optimiert** mit angepasstem Layout
    """)
