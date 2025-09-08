import streamlit as st
import pandas as pd
import json
import io

# --- HTML-Vorlage (mit Schlüsselnummer in Karten + Übersichten) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Suche</title>
    <style>
        * { box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f4f5f7;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            color: #333;
            font-weight: 500;
        }

        .main-wrapper {
            max-width: 1200px;
            width: 100%;
            background: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,.05);
            border: 1px solid #d1d9e2;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 16px;
            color: #007bff;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 700;
        }

        .suche-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
        }

        input[type="text"] {
            padding: 10px 12px;
            font-size: 1rem;
            border: 1px solid #ced4da;
            border-radius: 6px;
            background: #fff;
            color: #495057;
            font-weight: 500;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 3px rgba(0,123,255,.2);
        }

        .button-group {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        button {
            padding: 10px 16px;
            font-size: .95rem;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background .2s ease;
        }

        #resetBtn {
            background: #6c757d;
            color: #ffffff;
        }

        #resetBtn:hover {
            background: #5a6268;
        }

        #backBtn {
            display: none;
            background-color: #28a745;
            color: white;
        }

        #backBtn:hover {
            background-color: #218838;
        }

        #trefferInfo {
            font-size: .8rem;
            color: #6c757d;
            margin-top: 6px;
            font-weight: 500;
        }

        #tourBox {
            margin: 16px 0 24px 0;
            display: none;
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: .75rem;
            font-weight: 500;
            border: 1px solid #e9ecef;
        }

        #tourBoxTitle {
            margin-bottom: 6px;
            font-weight: 700;
            font-size: .85rem;
            background: #e9ecef;
            color: #495057;
            padding: 6px 10px;
            border-radius: 4px;
        }

        #tourList {
            border-top: 1px solid #dee2e6;
        }

        .tour-entry {
            padding: 6px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .tour-entry > div {
            display: grid;
            grid-template-columns: 80px 1fr auto; /* Schlüssel, Name, Buttons */
            align-items: center;
            gap: 12px;
            background: #ffffff;
            padding: 4px 6px;
            border-radius: 4px;
        }

        .tour-entry .name-field {
            font-weight: 600;
            color: #343a40;
            display: flex;
            align-items: center;
            gap: .5rem;
        }

        .tour-entry .key-field {
            font-family: monospace;
            color: #6c757d;
            font-weight: 700;
            cursor: pointer;
            text-decoration: underline;
        }

        #results {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .kunde {
            background: #fff;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 1px 2px rgba(0,0,0,.05);
            transition: transform .2s ease, box-shadow .2s ease;
        }

        .kunde:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,.08);
        }

        .kunde.highlighted {
            border-left: 4px solid #007bff;
            background: #e7f3ff;
        }

        .row1 {
            font-size: 1rem;
            margin-bottom: 8px;
            color: #212529;
            font-weight: 700;
        }

        #fachberaterBox {
            margin: 16px 0 24px 0;
            background: #f8f9fa;
            border-left: 4px solid #28a745;
            border-radius: 6px;
            padding: 10px 14px;
            border: 1px solid #e9ecef;
            display: none;
        }

        #fachberaterBoxTitle {
            margin-bottom: 6px;
            font-weight: 700;
            font-size: .85rem;
            background: #e9ecef;
            color: #495057;
            padding: 6px 10px;
            border-radius: 4px;
        }

        #fachberaterList {
            border-top: 1px solid #dee2e6;
        }

        .fb-entry {
            padding: 6px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .fb-entry > div {
            display: grid;
            grid-template-columns: 80px 1fr auto; /* Schlüssel, Name, Buttons */
            align-items: center;
            gap: 12px;
            background: #ffffff;
            padding: 4px 6px;
            border-radius: 4px;
        }

        .fb-entry .name-field {
            font-weight: 600;
            color: #343a40;
            display: flex;
            align-items: center;
            gap: .5rem;
        }

        .fb-entry .key-field {
            font-family: monospace;
            color: #6c757d;
            font-weight: 700;
            cursor: pointer;
            text-decoration: underline;
        }

        .hidden {
            display: none;
        }

        .badge {
            font-size: .72rem;
            padding: 2px 6px;
            border: 1px solid #d0d7de;
            border-radius: 999px;
            background: #f6f8fa;
            color: #57606a;
            font-weight: 600;
        }

        @media(max-width: 850px) {
            body { padding: 12px; }
            .main-wrapper { padding: 12px; box-shadow: none; border: 1px solid #d1d9e2; }
            input[type="text"], button { width: 100%; box-sizing: border-box; }
            h1 { font-size: 1.2rem; }
            .kunde { font-size: .85rem; padding: 10px; }

            .tour-entry > div,
            .fb-entry > div {
                grid-template-columns: 70px 1fr auto !important;
                gap: 8px !important;
                font-size: .8rem !important;
            }

            /* Sichtbar lassen (Name + Schlüssel + Buttons) */
            .tour-entry div:first-child > div:nth-child(2),
            .tour-entry div:first-child > div:nth-child(3),
            .fb-entry div:first-child > div:nth-child(2),
            .fb-entry div:first-child > div:nth-child(3) {
                display: initial;
            }
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <h1>🔍 Suche</h1>
        <div class="suche-container">
            <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße, Schlüssel...">
            <p style="font-size:.8rem;color:#6c757d;margin:-2px 0 8px 0;">🔤 Suche nach Name, Ort, Straße, Tournummer, CSB, SAP, Schlüssel, Liefertag oder Fachberater</p>

            <div class="button-group">
                <button id="resetBtn">Suche zurücksetzen</button>
                <button id="backBtn">Zurück zur Tour-Übersicht</button>
            </div>

            <p id="trefferInfo">🔎 0 Ergebnisse</p>
        </div>

        <div id="tourBox">
            <div id="tourBoxTitle">🚚 Tour <span id="tourNumSpan"></span></div>
            <div id="tourList"></div>
        </div>

        <div id="fachberaterBox">
            <div id="fachberaterBoxTitle">👤 Fachberater: <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span> Märkte)</div>
            <div id="fachberaterList"></div>
        </div>

        <div id="results"></div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt, wichtig: Semikolon!

// ---------- Hilfsfunktionen ----------
const $  = sel => document.querySelector(sel);
const $$ = sel => document.querySelectorAll(sel);
const el = (tag, cls, txt) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined) n.textContent = txt;
    return n;
};

const buildTourGrid = touren => {
    const box = el('div');
    box.style.cssText = 'border:1px solid #dee2e6;border-radius:6px;overflow:hidden;font-size:.85rem;';

    const head = el('div');
    head.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;background:#f8f9fa;font-weight:600;color:#495057;';
    head.appendChild(el('div', null, '🚛 Tour'));
    head.appendChild(el('div', null, '📦 Liefertag'));
    box.appendChild(head);

    touren.forEach(t => {
        const row  = el('div');
        row.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #dee2e6;';

        const tour = el('div');
        tour.style.cssText = 'padding:6px 10px; font-weight:600; font-family:monospace;';

        const link = el('a', null, t.tournummer);
        link.href = '#';
        link.style.cssText = `
            display:inline-block;
            color:#007bff;
            font-weight:600;
            font-family:monospace;
            text-decoration:none;
            cursor:pointer;
            transition:color .2s ease, text-decoration .2s ease;
        `;
        link.addEventListener('mouseover', () => link.style.textDecoration = 'underline');
        link.addEventListener('mouseout',  () => link.style.textDecoration = 'none');
        link.addEventListener('click', e => {
            e.preventDefault();
            $('#globalSearch').value = t.tournummer;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            window.scrollTo({ top: 0, behavior: 'smooth' });
            $('#backBtn').style.display = 'inline-block';
        });

        tour.appendChild(link);

        const day = el('div', null, t.liefertag);
        day.style.cssText = 'padding:6px 10px;color:#6c757d;';

        row.append(tour, day);
        box.appendChild(row);
    });

    return box;
};

const buildCustomerCard = kunde => {
    const card = el('div', 'kunde hidden');

    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${kunde.schluessel||''} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    const nameLine = '🏪 ' + kunde.name + (kunde.schluessel ? ' — Schlüssel: ' + kunde.schluessel : '');
    card.appendChild(el('div', 'row1', nameLine));

    const grid = el('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:8px;font-size:.85rem;';
    card.appendChild(grid);

    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;

    const addr = el('div');
    addr.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;';
    addr.append(el('div', null, kunde.strasse), el('div', null, `${plz} ${kunde.ort}`));
    const mapBtn = el('a', null, '🗺️ Google Maps öffnen');
    mapBtn.href = mapsUrl;
    mapBtn.target = '_blank';
    mapBtn.style.cssText = 'display:inline-block;padding:6px 12px;background:#007bff;color:#ffffff;text-decoration:none;border-radius:4px;font-weight:600;font-size:.8rem;margin-top:10px;';
    addr.appendChild(mapBtn);
    grid.appendChild(addr);

    const idBox = el('div');
    idBox.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;color:#495057;';
    idBox.append(
        el('div', null, `🆔 CSB: ${csb}`),
        el('div', null, `🔢 SAP: ${sap}`),
        el('div', null, `👤 Fachberater: ${kunde.fachberater}`)
    );
    grid.appendChild(idBox);

    const tours = el('div');
    tours.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;grid-column:1/-1;color:#495057;';
    const title = el('div', null, '🚛 Tourenübersicht');
    title.style.cssText = 'font-weight:600;margin-bottom:10px;color:#212529;';
    tours.append(title, buildTourGrid(kunde.touren));
    grid.appendChild(tours);

    return card;
};

// Tour-Übersicht: Schlüssel (CSB) | Name(+Schlüssel-Badge) | Buttons
const buildTourEntry = (csbNummer, name, mapsUrl, schluessel) => {
    const entry = el('div', 'tour-entry');
    const row = el('div');

    const keyDiv = el('div', 'key-field', csbNummer);
    keyDiv.title = `Kundenkarte für ${csbNummer} anzeigen`;
    keyDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-block';
    });

    const nameWrap = el('div', 'name-field');
    nameWrap.appendChild(el('span', null, name));
    if (schluessel && schluessel.trim() !== '') {
        nameWrap.appendChild(el('span', 'badge', `Schlüssel: ${schluessel}`));
    }

    const btnWrap = el('div');
    const link = el('a', null, '📍 Maps');
    link.href = mapsUrl;
    link.target = '_blank';
    link.style.cssText = 'display:inline-block;padding:2px 8px;background:#007bff;color:#ffffff;text-decoration:none;border-radius:4px;font-size:.80rem;font-weight:600;';
    btnWrap.appendChild(link);

    row.append(keyDiv, nameWrap, btnWrap);
    entry.appendChild(row);
    return entry;
};

// Fachberater-Übersicht: Schlüssel (CSB) | Name(+Schlüssel-Badge) | Buttons
const buildFachberaterEntry = (kunde) => {
    const entry = el('div', 'fb-entry');
    const row = el('div');

    const keyDiv = el('div', 'key-field', kunde.csb);
    keyDiv.title = `Kundenkarte für CSB ${kunde.csb} anzeigen`;
    keyDiv.addEventListener('click', () => {
        $('#globalSearch').value = kunde.csb;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-block';
    });

    const nameWrap = el('div', 'name-field');
    nameWrap.appendChild(el('span', null, kunde.name));
    if (kunde.schluessel && kunde.schluessel.trim() !== '') {
        nameWrap.appendChild(el('span', 'badge', `Schlüssel: ${kunde.schluessel}`));
    }

    const btnWrap = el('div');
    const link = el('a', null, '📍 Maps');
    link.href = kunde.mapsUrl;
    link.target = '_blank';
    link.style.cssText = 'display:inline-block;padding:2px 8px;background:#007bff;color:#ffffff;text-decoration:none;border-radius:4px;font-size:.80rem;font-weight:600;';
    btnWrap.appendChild(link);

    row.append(keyDiv, nameWrap, btnWrap);
    entry.appendChild(row);
    return entry;
};

// ---------- Hauptlogik ----------
let lastTourSearchQuery = '';
const results  = $('#results');
const treffer  = $('#trefferInfo');
const kundenMap = new Map();

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    // Kunden zusammenführen: CSB = Schlüssel
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
        });
    }

    const allCards = [];
    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        results.appendChild(card);
        allCards.push(card);
    });

    const input                = $('#globalSearch');
    const tourBox              = $('#tourBox');
    const tourList             = $('#tourList');
    const tourNumLbl           = $('#tourNumSpan');
    const fachberaterBox       = $('#fachberaterBox');
    const fachberaterList      = $('#fachberaterList');
    const fachberaterNameSpan  = $('#fachberaterNameSpan');
    const fachberaterCountSpan = $('#fachberaterCountSpan');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.style.display = 'none';
        fachberaterBox.style.display = 'none';

        // Touren-Suche (genau 4 Ziffern)
        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const list = [];
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({
                        csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-',
                        name: k.name,
                        mapsUrl,
                        schluessel: k.schluessel || ''
                    });
                }
            });

            if (list.length > 0) {
                lastTourSearchQuery = tourN;
                tourList.innerHTML = '';
                tourNumLbl.textContent = `${tourN} - ${list.length} Kunde${list.length === 1 ? '' : 'n'}`;
                list.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach(kunde => {
                    tourList.appendChild(
                        buildTourEntry(kunde.csb, kunde.name, kunde.mapsUrl, kunde.schluessel)
                    );
                });
                tourBox.style.display = 'block';
            }
        }

        // Fachberater-Suche (ab 3 Zeichen, contains)
        const matchedFachberater = q.length > 2 ? alleFachberater.find(fb => fb.includes(q)) : null;
        if (matchedFachberater) {
            const kundenDesBeraters = [];
            let beraterName = '';
            kundenMap.forEach(k => {
                if (k.fachberater?.toLowerCase() === matchedFachberater) {
                    if (!beraterName) beraterName = k.fachberater;
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    kundenDesBeraters.push({
                        csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-',
                        name: k.name,
                        mapsUrl,
                        schluessel: k.schluessel || ''
                    });
                }
            });

            if (kundenDesBeraters.length > 0) {
                fachberaterNameSpan.textContent = beraterName;
                fachberaterCountSpan.textContent = kundenDesBeraters.length;
                fachberaterList.innerHTML = '';
                kundenDesBeraters.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach(kunde => {
                    fachberaterList.appendChild(buildFachberaterEntry(kunde));
                });
                fachberaterBox.style.display = 'block';
            }
        }

        // Karten filtern
        const anyQuery = q !== '';
        allCards.forEach(c => {
            const match = anyQuery && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) {
                c.classList.add('highlighted');
                hits++;
            } else {
                c.classList.remove('highlighted');
            }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    // Buttons
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
    });
} else {
    document.querySelector('#results').textContent = 'Keine Kundendaten gefunden. Stellen Sie sicher, dass die "tourkundenData" korrekt geladen wird.';
}
</script>

</body>
</html>
"""

# ---------- UI ----------
st.title("🚛 Kunden-Datenbank als HTML-Seite exportieren")
st.markdown("""
Laden Sie **zwei** Excel-Dateien hoch:
1) **Quelldatei** mit den Kundendaten (mehrere Blätter)  
2) **Schlüsseldatei** mit *CSB-Nummer in Spalte A* und *Schlüsselnummer in Spalte F*

Ich erstelle daraus eine interaktive **`suche.html`**, in der die Schlüsselnummer hinter dem Kundennamen angezeigt wird.
""")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("📄 Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("🔑 Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])

# ---------- Helpers ----------
def norm_str_num(x):
    """Normalisiert Nummern (auch aus float/str) auf saubere String-Darstellung ohne '.0'."""
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
    """
    Erzeugt Mapping: CSB -> Schlüsselnummer
    Erwartung: CSB in Spalte A (Index 0), Schlüssel in Spalte F (Index 5).
    Robust: nimmt erste und sechste Spalte der Datei, Header egal.
    """
    if key_df.shape[1] < 6:
        st.warning("⚠️ Schlüsseldatei hat weniger als 6 Spalten. Es werden vorhandene Spalten verwendet.")
    csb_col = 0
    key_col = 5 if key_df.shape[1] > 5 else key_df.shape[1] - 1

    mapping = {}
    for _, row in key_df.iterrows():
        csb_raw = row.iloc[csb_col] if key_df.shape[1] > 0 else None
        key_raw = row.iloc[key_col] if key_df.shape[1] > 0 else None
        csb = norm_str_num(csb_raw)
        key = "" if pd.isna(key_raw) else str(key_raw).strip()
        if csb:
            mapping[csb] = key
    return mapping

if excel_file and key_file:
    if st.button("🛠️ Interaktive HTML-Seite erzeugen"):
        # --- KONFIGURATION ---
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {
            "Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt",
            "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"
        }
        SPALTEN_MAPPING = {
            "csb_nummer": "Nr",
            "sap_nummer": "SAP-Nr.",
            "name": "Name",
            "strasse": "Strasse",
            "postleitzahl": "Plz",
            "ort": "Ort",
            "fachberater": "Fachberater"
        }

        try:
            # Schlüsseldatei lesen (erstes Blatt)
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
                        if spaltenname not in df.columns:
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit():
                            continue
                        tournr = str(int(float(tournr_raw)))

                        # Eintrag füllen
                        eintrag = {
                            json_key: str(row.get(excel_col, "")).strip()
                            for json_key, excel_col in SPALTEN_MAPPING.items()
                        }

                        # CSB normalisieren und Schlüssel ergänzen
                        csb_clean = norm_str_num(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        eintrag["schluessel"] = key_map.get(csb_clean, "")

                        eintrag["liefertag"] = tag
                        tour_dict.setdefault(tournr, []).append(eintrag)

            with st.spinner("📥 Lese und verarbeite Quelldatei..."):
                verarbeitete_blaetter = []
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                        verarbeitete_blaetter.append(blatt)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht in der Datei gefunden. Wird übersprungen.")
                        continue

            if not tour_dict:
                st.error("Es konnten keine gültigen Kundendaten gefunden werden.")
                st.stop()

            # --- DATEN SORTIEREN UND IN JSON KONVERTIEREN ---
            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            # --- HTML erzeugen ---
            final_html = HTML_TEMPLATE.replace(
                "const tourkundenData = {  }",
                f"const tourkundenData = {json_data_string};"
            )

            # --- Download ---
            st.success(f"✅ Erfolgreich! {len(sorted_tours)} Touren verarbeitet. Die HTML-Seite ist fertig.")
            st.download_button(
                label="📥 Interaktive `suche.html` herunterladen",
                data=final_html.encode("utf-8"),
                file_name="suche.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            st.exception(e)

elif excel_file and not key_file:
    st.info("Bitte zusätzlich die **Schlüsseldatei** (A=CSB, F=Schlüssel) hochladen.")
elif key_file and not excel_file:
    st.info("Bitte zusätzlich die **Quelldatei** (Kundendaten) hochladen.")
else:
    st.warning("Bitte beide Dateien hochladen, um fortzufahren.")
