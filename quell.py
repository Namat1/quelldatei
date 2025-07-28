import streamlit as st
import pandas as pd
import json

# --- HTML-Vorlage ---
# Die von Ihnen bereitgestellte HTML-Datei wird hier als String gespeichert.
# Der Platzhalter "const tourkundenData = {  }" wird später ersetzt.
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
            max-width: 900px;
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
            font-weight: 600;
            font-family: monospace;
            color: #343a40;
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

        .hidden {
            display: none;
        }

        @media(max-width: 768px) {
            body { padding: 12px; }
            .main-wrapper { padding: 12px; box-shadow: none; border: 1px solid #d1d9e2; }
            input[type="text"], button { width: 100%; box-sizing: border-box; }
            h1 { font-size: 1.2rem; }
            .kunde { font-size: .85rem; padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <h1>🔍 Suche</h1>
        <div class="suche-container">
            <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße...">
            <p style="font-size:.8rem;color:#6c757d;margin:-2px 0 8px 0;">🔤 Suche nach Name, Ort, Straße, Tournummer, CSB, SAP, Liefertag oder Fachberater</p>
            
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
        
        <div id="fachberaterBox" style="display: none;">
            <div id="fachberaterBoxTitle">👤 Fachberater: <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span> Märkte)</div>
            <div id="fachberaterList"></div>
        </div>

        <div id="results"></div>
    </div>

<script>
const tourkundenData = {  }

// Der Rest des Skripts bleibt unverändert, da es die Daten aus tourkundenData liest.
// =======================================================================


// ---------- Hilfsfunktionen ----------
const $ = sel => document.querySelector(sel);
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
        const row = el('div');
        row.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #dee2e6;';
        const tour = el('div');
        tour.style.cssText = 'padding:6px 10px;';
        const link = el('span', null, t.tournummer);
        link.style.cssText = 'cursor:pointer;color:#007bff;text-decoration:underline;';
        link.addEventListener('click', () => {
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
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    card.appendChild(el('div', 'row1', '🏪 ' + kunde.name));
    const grid = el('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:8px;font-size:.85rem;';
    card.appendChild(grid);

    const csb = kunde.csb_nummer?.toString().replace(/\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\.0$/, '') || '-';
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
    idBox.append(el('div', null, `🆔 CSB: ${csb}`), el('div', null, `🔢 SAP: ${sap}`), el('div', null, `👤 Fachberater: ${kunde.fachberater}`));
    grid.appendChild(idBox);

    const tours = el('div');
    tours.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;grid-column:1/-1;color:#495057;';
    const title = el('div', null, '🚛 Tourenübersicht');
    title.style.cssText = 'font-weight:600;margin-bottom:10px;color:#212529;';
    tours.append(title, buildTourGrid(kunde.touren));
    grid.appendChild(tours);

    return card;
};

const buildTourEntry = (ort, name, strasse, csbNummer, mapsUrl, bgAlt) => {
    const entry = el('div', 'tour-entry');
    const row = el('div');
    row.style.cssText = `display:flex; align-items:center; gap:.75rem; background:${bgAlt ? '#f8f9fa' : '#ffffff'}; padding:4px 6px; border-radius:4px; font-size:.85rem; color:#343a40;`;

    const csbDiv = el('div');
    csbDiv.style.cssText = 'flex:0 0 70px; font-weight:700; color:#990033; cursor:pointer; text-decoration:underline;';
    csbDiv.textContent = csbNummer;
    csbDiv.title = `Kundenkarte für ${csbNummer} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-block';
    });

    const ortDiv = el('div', null, ort);
    ortDiv.style.cssText = 'flex:1; font-weight:700;';
    const nameDiv = el('div', null, name);
    nameDiv.style.cssText = 'flex:1.5;';
    const strDiv = el('div', null, strasse);
    strDiv.style.cssText = 'flex:1.5;';

    const linkDiv = el('div');
    const link = el('a', null, '📍 Maps');
    link.href = mapsUrl;
    link.target = '_blank';
    link.style.cssText = 'display:inline-block;padding:1px 4px;background:#007bff;color:#ffffff;text-decoration:none;border-radius:4px;font-size:.70rem;font-weight:600;';
    linkDiv.appendChild(link);

    row.append(csbDiv, ortDiv, strDiv, nameDiv, linkDiv);
    entry.appendChild(row);
    return entry;
};

const buildFachberaterEntry = (kunde, bgAlt) => {
    const entry = el('div', 'fb-entry');
    const row = el('div');
    row.style.cssText = `display:flex; align-items:center; gap:.75rem; background:${bgAlt ? '#f8f9fa' : '#ffffff'}; padding:4px 6px; border-radius:4px; font-size:.85rem; color:#343a40;`;

    const csbDiv = el('div', null, kunde.csb);
    csbDiv.style.cssText = 'flex:0 0 70px; font-weight:700; color:#990033; cursor:pointer; text-decoration:underline;';
    csbDiv.title = `Kundenkarte für CSB ${kunde.csb} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = kunde.csb;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
    });

    const ortDiv = el('div', null, kunde.ort);
    ortDiv.style.cssText = 'flex:1; font-weight:700;';
    const strDiv = el('div', null, kunde.strasse);
    strDiv.style.cssText = 'flex:1.5;';
    const nameDiv = el('div', null, kunde.name);
    nameDiv.style.cssText = 'flex:1.5;';
    const linkDiv = el('div');
    const link = el('a', null, '📍 Maps');
    link.href = kunde.mapsUrl;
    link.target = '_blank';
    link.style.cssText = 'display:inline-block;padding:1px 4px;background:#007bff;color:#ffffff;text-decoration:none;border-radius:4px;font-size:.70rem;font-weight:600;';
    linkDiv.appendChild(link);

    row.append(csbDiv, ortDiv, strDiv, nameDiv, linkDiv);
    entry.appendChild(row);
    return entry;
};

// ---------- Hauptlogik (mit Sortierung nach Kundennummer für alle Übersichten) ----------
let lastTourSearchQuery = ''; 
const results = $('#results');
const treffer = $('#trefferInfo');
const kundenMap = new Map();

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({
                tournummer: tour,
                liefertag: k.liefertag
            });
        });
    }

    const allCards = [];
    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        results.appendChild(card);
        allCards.push(card);
    });

    // ---------- Suche ----------
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
        
        const tourMatch = q.match(/^\d{4}$/);
        
        if (tourMatch) {
            const tourN = tourMatch[0];
            const list = [];
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    const plz = k.postleitzahl?.toString().replace(/\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\.0$/, '') || '-', mapsUrl: mapsUrl });
                }
            });

            if (list.length > 0) {
                lastTourSearchQuery = tourN;
                tourList.innerHTML = '';
                tourNumLbl.textContent = `${tourN} - ${list.length} Kunde${list.length === 1 ? '' : 'n'}`;
                
                // HIER IST DIE GEÄNDERTE SORTIERUNG FÜR TOUREN
                list.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    tourList.appendChild(buildTourEntry(kunde.ort, kunde.name, kunde.strasse, kunde.csb, kunde.mapsUrl, i % 2 !== 0));
                });
                tourBox.style.display = 'block';
            }
        }
        
        const matchedFachberater = alleFachberater.find(fb => fb.includes(q));
        if (q.length > 2 && matchedFachberater) {
            const kundenDesBeraters = [];
            let beraterName = '';
            kundenMap.forEach(k => {
                if (k.fachberater?.toLowerCase() === matchedFachberater) {
                    if (!beraterName) beraterName = k.fachberater;
                    const plz = k.postleitzahl?.toString().replace(/\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    kundenDesBeraters.push({
                        csb: k.csb_nummer?.toString().replace(/\.0$/, '') || '-',
                        name: k.name,
                        ort: k.ort,
                        strasse: k.strasse,
                        mapsUrl: mapsUrl
                    });
                }
            });

            if (kundenDesBeraters.length > 0) {
                fachberaterNameSpan.textContent = beraterName;
                fachberaterCountSpan.textContent = kundenDesBeraters.length;
                fachberaterList.innerHTML = '';
                kundenDesBeraters.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    fachberaterList.appendChild(buildFachberaterEntry(kunde, i % 2 !== 0));
                });
                fachberaterBox.style.display = 'block';
            }
        }

        allCards.forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
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

    // --- BUTTON-LOGIK ---
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
    results.textContent = 'Keine Kundendaten gefunden. Stellen Sie sicher, dass die "tourkundenData" korrekt geladen wird.';
}
</script>

</body>
</html>
"""

# --- UI Setup ---
st.title("🚛 Kunden-Datenbank als HTML-Seite exportieren")
st.markdown("""
Laden Sie eine Excel-Datei hoch, um eine **interaktive HTML-Suchseite** (`suche.html`) zu erstellen.
Die Seite enthält alle Kundendaten, gruppiert nach Touren und durchsuchbar.
""")

excel_file = st.file_uploader(
    "Wählen Sie Ihre Excel-Datei",
    type=["xlsx"]
)

if excel_file:
    if st.button("Interaktive HTML-Seite erzeugen"):
        
        # --- KONFIGURATION (unverändert) ---
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}
        
        try:
            tour_dict = {}
            verarbeitete_blaetter = []

            def kunden_sammeln(df):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns:
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit():
                            continue
                        tournr = str(int(float(tournr_raw)))
                        eintrag = {json_key: str(row.get(excel_col, "")).strip() for json_key, excel_col in SPALTEN_MAPPING.items()}
                        eintrag["liefertag"] = tag
                        if tournr not in tour_dict:
                            tour_dict[tournr] = []
                        tour_dict[tournr].append(eintrag)

            with st.spinner("Lese und verarbeite Excel-Datei..."):
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

            # --- HTML-DATEI ERZEUGEN ---
            # Ersetzt den Platzhalter im Template mit den tatsächlichen JSON-Daten.
            final_html = HTML_TEMPLATE.replace(
                "const tourkundenData = {  }",
                f"const tourkundenData = {json_data_string}"
            )

            # --- ERGEBNISSE ANZEIGEN UND DOWNLOAD ANBIETEN ---
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
            

