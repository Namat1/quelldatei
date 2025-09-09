input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.style.display = 'none';
        fachberaterBox.style.display = 'none';

        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const tourKunden = [];
            const list = [];
            
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    tourKunden.push(k);
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', mapsUrl });
                }
            });

            if (tourKunden.length > 0) {
                lastTourSearchQuery = tourN;
                
                // Wechsel zur Tour-Übersicht-Screen
                mainScreen.classList.add('hidden');
                tourResultScreen.classList.add('show');
                tourResultTitle.textContent = `Tour ${tourN} (${tourKunden.length} Kunden)`;
                
                const { summary, list: customersList } = buildTourResultView(tourN, tourKunden);
                tourSummary.innerHTML = '';
                tourCustomersList.innerHTML = '';
                tourSummary.appendChild(summary);
                tourCustomersList.appendChild(customersList);
                
                return;
            }
        }

        // Normale Suche weiter
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
                    fachberaterList.appendChild(buildFachberaterEntry(kunde, i % 2 !== 0));
                });
                fachberaterBox.style.display = 'block';
            }
        }

        document.querySelectorAll('.kunde').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) { c.classList.add('highlighted'); hits++; }
            else { c.classList.remove('highlighted'); }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    // Tour Result Back Button
    tourResultBack.addEventListener('click', () => {
        mainScreen.classList.remove('hidden');
        tourResultScreen.classList.remove('show');
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
    });

    document.querySelector('#backBtn').addEventListener('click', () => {
        if (lastTourSearchQuery) {
            input.value = lastTourSearchQuery;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            document.import streamlit as st
import pandas as pd
import json

# --- HTML-Vorlage orientiert am ursprünglichen Design ---
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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
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

    const input                = document.querySelector('#globalSearch');
    const tourBox              = document.querySelector('#tourBox');
    const tourList             = document.querySelector('#tourList');
    const tourNumLbl           = document.querySelector('#tourNumSpan');
    const fachberaterBox       = document.querySelector('#fachberaterBox');
    const fachberaterList      = document.querySelector('#fachberaterList');
    const fachberaterNameSpan  = document.querySelector('#fachberaterNameSpan');
    const fachberaterCountSpan = document.querySelector('#fachberaterCountSpan');
    const tourResultOverlay    = document.querySelector('#tourResultOverlay');
    const tourResultTitle      = document.querySelector('#tourResultTitle');
    const tourSummary          = document.querySelector('#tourSummary');
    const tourCustomersGrid    = document.querySelector('#tourCustomersGrid');
    const closeTourResult      = document.querySelector('#closeTourResult');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.style.display = 'none';
        fachberaterBox.style.display = 'none';

        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const tourKunden = [];
            const list = [];
            
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    tourKunden.push(k);
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', mapsUrl });
                }
            });

            if (tourKunden.length > 0) {
                lastTourSearchQuery = tourN;
                
                // Wechsel zur Tour-Übersicht-Screen
                mainScreen.classList.add('hidden');
                tourResultScreen.classList.add('show');
                tourResultTitle.textContent = `Tour ${tourN} (${tourKunden.length} Kunden)`;
                
                const { summary, list: customersList } = buildTourResultView(tourN, tourKunden);
                tourSummary.innerHTML = '';
                tourCustomersList.innerHTML = '';
                tourSummary.appendChild(summary);
                tourCustomersList.appendChild(customersList);
                
                return;
            }
        }

        // Normale Suche weiter
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
                    fachberaterList.appendChild(buildFachberaterEntry(kunde, i % 2 !== 0));
                });
                fachberaterBox.style.display = 'block';
            }
        }

        document.querySelectorAll('.kunde').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) { c.classList.add('highlighted'); hits++; }
            else { c.classList.remove('highlighted'); }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    // Tour Result Back Button
    tourResultBack.addEventListener('click', () => {
        mainScreen.classList.remove('hidden');
        tourResultScreen.classList.remove('show');
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
    });

    document.querySelector('#backBtn').addEventListener('click', () => {
        if (lastTourSearchQuery) {
            input.value = lastTourSearchQuery;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            document.querySelector('#backBtn').style.display = 'none';
        }
    });

    document.querySelector('#resetBtn').addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        mainScreen.classList.remove('hidden');
        tourResultScreen.classList.remove('show');
    });
} else {
    document.querySelector('#results').textContent = 'Keine Kundendaten gefunden. Stellen Sie sicher, dass die "tourkundenData" korrekt geladen wird.';
}
</script>

</body>
</html>
"""

st.title("🚛 Kunden-Datenbank als HTML-Seite exportieren")
st.markdown("""
Laden Sie zwei Excel-Dateien hoch:
1. Quelldatei mit den Kundendaten (mehrere Blätter)
2. Schlüsseldatei mit CSB in Spalte A und Schlüsselnummer in Spalte F

Ich erstelle daraus eine interaktive HTML-Suchseite mit robuster Tour-Übersicht.
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

def build_key_map(key_df):
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
    if st.button("Robuste HTML-Seite erzeugen", type="primary"):
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

            with st.spinner("📥 Lese und verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht in der Datei gefunden. Wird übersprungen.")

            if not tour_dict:
                st.error("Es konnten keine gültigen Kundendaten gefunden werden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            st.success(f"✅ Erfolgreich! {len(sorted_tours)} Touren verarbeitet. Die robuste HTML-Seite ist fertig.")
            st.download_button("📥 Robuste suche.html herunterladen", data=final_html.encode("utf-8"), file_name="suche.html", mime="text/html")

        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("Bitte zusätzlich die Schlüsseldatei hochladen.")
elif key_file and not excel_file:
    st.info("Bitte zusätzlich die Quelldatei hochladen.")
else:
    st.warning("Bitte beide Dateien hochladen, um fortzufahren.")
    st.markdown("""
    ### ✨ Robuste Features:
    - Single-Screen Darstellung ohne Overlays
    - Tour-Übersicht wechselt kompletten Bildschirm
    - Klare Navigation zwischen Haupt- und Tour-Ansicht
    - Kompakte Listendarstellung für bessere Übersicht
    - Alle ursprünglichen Funktionen bleiben erhalten
    - Robuste und stabile Performance
    """)
} else {
    document.querySelector('#results').textContent = 'Keine Kundendaten gefunden. Stellen Sie sicher, dass die "tourkundenData" korrekt geladen wird.';
}
</script>

</body>
</html>
"""

st.title("🚛 Kunden-Datenbank als HTML-Seite exportieren")
st.markdown("""
Laden Sie zwei Excel-Dateien hoch:
1. Quelldatei mit den Kundendaten (mehrere Blätter)
2. Schlüsseldatei mit CSB in Spalte A und Schlüsselnummer in Spalte F

Ich erstelle daraus eine interaktive HTML-Suchseite mit Tour-Übersicht bei Eingabe einer Tournummer.
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

def build_key_map(key_df):
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
    if st.button("Interaktive HTML-Seite erzeugen", type="primary"):
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

            with st.spinner("📥 Lese und verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht in der Datei gefunden. Wird übersprungen.")

            if not tour_dict:
                st.error("Es konnten keine gültigen Kundendaten gefunden werden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            st.success(f"✅ Erfolgreich! {len(sorted_tours)} Touren verarbeitet. Die HTML-Seite ist fertig.")
            st.download_button("📥 Interaktive suche.html herunterladen", data=final_html.encode("utf-8"), file_name="suche.html", mime="text/html")

        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("Bitte zusätzlich die Schlüsseldatei hochladen.")
elif key_file and not excel_file:
    st.info("Bitte zusätzlich die Quelldatei hochladen.")
else:
    st.warning("Bitte beide Dateien hochladen, um fortzufahren.")
    st.markdown("""
    ### ✨ Features:
    - Zentrale Tour-Übersicht bei Eingabe einer 4-stelligen Tournummer
    - Beibehaltung des ursprünglichen Designs und Layouts
    - RAL 1021 (Rapsgelb) und RAL 5010 (Enzianblau) Farbschema
    - Vollbild-Overlay für detaillierte Tour-Ansicht
    - Alle ursprünglichen Suchfunktionen bleiben erhalten
    - Mobile-optimiert und responsive
    """); 
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
            color: #0E294B; 
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
            border-color: #F3DA0B; 
            box-shadow: 0 0 0 3px rgba(243,218,11,.2); 
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
            background-color: #F3DA0B; 
            color: #0E294B; 
            font-weight: 700;
        } 
        #backBtn:hover { 
            background-color: #F8E555; 
        }
        #trefferInfo { 
            font-size: .8rem; 
            color: #6c757d; 
            margin-top: 6px; 
            font-weight: 500; 
        }

        /* Tour Result Overlay */
        .tour-result-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(14, 41, 75, 0.85);
            z-index: 1000;
            overflow-y: auto;
            padding: 20px;
            display: none;
        }

        .tour-result-overlay.show {
            display: block;
        }

        .tour-result-container {
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            border: 2px solid #F3DA0B;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,.15);
            overflow: hidden;
        }

        .tour-result-header {
            padding: 16px 20px;
            background: #0E294B;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tour-result-title {
            font-size: 1.3rem;
            font-weight: 700;
        }

        .tour-result-close {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s ease;
        }

        .tour-result-close:hover {
            background: rgba(255,255,255,0.3);
        }

        .tour-result-content {
            padding: 20px;
        }

        .tour-summary {
            background: #f8f9fa;
            border-left: 4px solid #F3DA0B;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
        }

        .tour-summary-title {
            font-weight: 700;
            font-size: 1rem;
            background: #e9ecef;
            color: #495057;
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 12px;
        }

        .tour-summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            font-size: 0.85rem;
        }

        .tour-stat {
            text-align: center;
            padding: 8px;
            background: #ffffff;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }

        .tour-stat-number {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0E294B;
        }

        .tour-stat-label {
            color: #6c757d;
            font-weight: 500;
        }

        .tour-customers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
        }

        .tour-customer-card {
            background: #fff;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 1px 2px rgba(0,0,0,.05);
            transition: transform .2s ease, box-shadow .2s ease;
        }

        .tour-customer-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,.08);
        }

        .tour-customer-card.highlighted {
            border-left: 4px solid #F3DA0B;
            background: #fffbf0;
        }

        .tour-customer-name {
            font-size: 1rem;
            margin-bottom: 8px;
            color: #212529;
            font-weight: 700;
        }

        .tour-customer-details {
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 8px;
        }

        .tour-customer-address {
            background: #f8f9fa;
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            color: #495057;
        }

        .tour-customer-actions {
            display: flex;
            gap: 6px;
        }

        .tour-action-btn {
            padding: 6px 10px;
            font-size: 0.75rem;
            font-weight: 600;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .tour-maps-btn {
            background: #F3DA0B;
            color: #0E294B;
        }

        .tour-maps-btn:hover {
            background: #F8E555;
        }

        .tour-details-btn {
            background: #0E294B;
            color: white;
        }

        .tour-details-btn:hover {
            background: #1E3A5F;
        }

        #tourBox { 
            margin: 16px 0 24px 0; 
            display: none; 
            background: #f8f9fa; 
            border-left: 4px solid #0E294B; 
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
        .tour-entry > div { 
            display: grid; 
            grid-template-columns: 80px 140px 1fr 1.5fr 1.5fr auto; 
            align-items: center; 
            gap: .75rem; 
            background: #ffffff; 
            padding: 4px 6px; 
            border-radius: 4px; 
        }
        .tour-entry.alt > div { 
            background: #f8f9fa; 
        }
        .key-col { 
            font-weight: 700; 
            color: #0E294B; 
            cursor: pointer; 
            text-decoration: underline; 
        }
        .skl-col { 
            font-weight: 700; 
            color: #57606a; 
            font-family: inherit; 
        }
        .ort-col { 
            font-weight: 700; 
            color: #343a40; 
            font-family: inherit; 
        }
        .str-col { 
            font-weight: 500; 
            color: #343a40; 
            font-family: inherit; 
        }
        .name-col { 
            font-weight: 600; 
            color: #343a40; 
            font-family: inherit; 
        }
        .btn-col a { 
            display:inline-block;
            padding:1px 4px;
            background:#F3DA0B;
            color:#0E294B;
            text-decoration:none;
            border-radius:4px;
            font-size:.70rem;
            font-weight:600; 
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
            border-left: 4px solid #F3DA0B; 
            background: #fffbf0; 
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
            border-left: 4px solid #F3DA0B; 
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
            grid-template-columns: 80px 140px 1fr 1.5fr 1.5fr auto; 
            align-items: center; 
            gap: .75rem; 
            background: #ffffff; 
            padding: 4px 6px; 
            border-radius: 4px; 
        }
        .fb-entry.alt > div { 
            background: #f8f9fa; 
        }
        .hidden { 
            display: none; 
        }
        @media(max-width: 768px) {
            body { 
                padding: 12px; 
            }
            .main-wrapper { 
                padding: 12px; 
                box-shadow: none; 
                border: 1px solid #d1d9e2; 
            }
            input[type="text"], button { 
                width: 100%; 
                box-sizing: border-box; 
            }
            h1 { 
                font-size: 1.2rem; 
            }
            .kunde { 
                font-size: .85rem; 
                padding: 10px; 
            }
            .tour-entry > div, .fb-entry > div { 
                grid-template-columns: 70px 120px 1fr 1fr 1fr auto; 
                gap: 8px; 
                font-size: .8rem; 
            }
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
        
        <div id="fachberaterBox">
            <div id="fachberaterBoxTitle">👤 Fachberater: <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span> Märkte)</div>
            <div id="fachberaterList"></div>
        </div>

        <div id="results"></div>

        <!-- Tour Result Overlay -->
        <div id="tourResultOverlay" class="tour-result-overlay">
            <div class="tour-result-container">
                <div class="tour-result-header">
                    <div class="tour-result-title">
                        🚚 <span id="tourResultTitle"></span>
                    </div>
                    <button class="tour-result-close" id="closeTourResult">✕</button>
                </div>
                <div class="tour-result-content">
                    <div class="tour-summary" id="tourSummary"></div>
                    <div class="tour-customers-grid" id="tourCustomersGrid"></div>
                </div>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt, wichtig: Semikolon!

// Helpers
const $  = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

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
        const tour = el('div'); tour.style.cssText = 'padding:6px 10px; font-weight:600; font-family:monospace;';
        const link = el('a', null, t.tournummer);
        link.href = '#'; link.style.cssText = 'display:inline-block;color:#0E294B;font-weight:600;font-family:monospace;text-decoration:none;cursor:pointer;';
        link.addEventListener('click', e => { e.preventDefault(); $('#globalSearch').value = t.tournummer; $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true })); window.scrollTo({ top: 0, behavior: 'smooth' }); $('#backBtn').style.display = 'inline-block'; });
        tour.appendChild(link);
        const day = el('div', null, t.liefertag); day.style.cssText = 'padding:6px 10px;color:#6c757d;';
        row.append(tour, day); box.appendChild(row);
    });
    return box;
};

const buildCustomerCard = kunde => {
    const card = el('div', 'kunde hidden');
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${(kunde.schluessel||'')} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    card.appendChild(el('div', 'row1', '🏪 ' + kunde.name + (kunde.schluessel ? ' — Schlüssel: ' + kunde.schluessel : '')));

    const grid = el('div'); grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:8px;font-size:.85rem;'; card.appendChild(grid);

    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;

    const addr = el('div'); addr.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;';
    addr.append(el('div', null, kunde.strasse), el('div', null, `${plz} ${kunde.ort}`));
    const mapBtn = el('a', null, '🗺️ Google Maps öffnen'); mapBtn.href = mapsUrl; mapBtn.target = '_blank';
    mapBtn.style.cssText = 'display:inline-block;padding:6px 12px;background:#F3DA0B;color:#0E294B;text-decoration:none;border-radius:4px;font-weight:600;font-size:.8rem;margin-top:10px;';
    addr.appendChild(mapBtn); grid.appendChild(addr);

    const idBox = el('div'); idBox.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;color:#495057;';
    idBox.append(el('div', null, `🆔 CSB: ${csb}`), el('div', null, `🔢 SAP: ${sap}`), el('div', null, `👤 Fachberater: ${kunde.fachberater}`), el('div', null, `🔑 Schlüssel: ${kunde.schluessel || '-'}`));
    grid.appendChild(idBox);

    const tours = el('div'); tours.style.cssText = 'background:#f8f9fa;padding:12px;border-radius:6px;border:1px solid #e9ecef;grid-column:1/-1;color:#495057;';
    const title = el('div', null, '🚛 Tourenübersicht'); title.style.cssText = 'font-weight:600;margin-bottom:10px;color:#212529;';
    tours.append(title, buildTourGrid(kunde.touren)); grid.appendChild(tours);

    return card;
};

const buildTourResultView = (tourNumber, kunden) => {
    // Summary erstellen
    const summary = el('div');
    const summaryTitle = el('div', 'tour-summary-title', `🚚 Tour ${tourNumber} - Übersicht`);
    const summaryStats = el('div', 'tour-summary-stats');
    
    const totalStat = el('div', 'tour-stat');
    totalStat.innerHTML = `<div class="tour-stat-number">${kunden.length}</div><div class="tour-stat-label">Gesamt Kunden</div>`;
    
    const dayGroups = {};
    kunden.forEach(k => {
        k.touren.forEach(t => {
            if (t.tournummer === tourNumber) {
                dayGroups[t.liefertag] = (dayGroups[t.liefertag] || 0) + 1;
            }
        });
    });
    
    Object.entries(dayGroups).forEach(([day, count]) => {
        const dayStat = el('div', 'tour-stat');
        dayStat.innerHTML = `<div class="tour-stat-number">${count}</div><div class="tour-stat-label">${day}</div>`;
        summaryStats.appendChild(dayStat);
    });
    
    summaryStats.appendChild(totalStat);
    summary.append(summaryTitle, summaryStats);
    
    // Kunden-Grid erstellen
    const grid = el('div', 'tour-customers-grid');
    
    kunden.sort((a, b) => {
        const csbA = parseInt(a.csb_nummer?.toString().replace(/\\.0$/, '') || '0');
        const csbB = parseInt(b.csb_nummer?.toString().replace(/\\.0$/, '') || '0');
        return csbA - csbB;
    }).forEach(kunde => {
        const card = el('div', 'tour-customer-card');
        
        const name = el('div', 'tour-customer-name', '🏪 ' + kunde.name);
        const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
        const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
        const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
        
        const details = el('div', 'tour-customer-details');
        details.innerHTML = `🆔 CSB: ${csb} | 🔢 SAP: ${sap} | 👤 ${kunde.fachberater} | 🔑 ${kunde.schluessel || '-'}`;
        
        const address = el('div', 'tour-customer-address');
        address.innerHTML = `📍 ${kunde.strasse}, ${plz} ${kunde.ort}`;
        
        const actions = el('div', 'tour-customer-actions');
        
        const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;
        const mapsBtn = el('a', 'tour-action-btn tour-maps-btn', '📍 Maps');
        mapsBtn.href = mapsUrl;
        mapsBtn.target = '_blank';
        
        const detailsBtn = el('button', 'tour-action-btn tour-details-btn', '🔍 Details');
        detailsBtn.addEventListener('click', () => {
            $('#globalSearch').value = csb;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            $('#tourResultOverlay').classList.remove('show');
            $('#backBtn').style.display = 'inline-block';
        });
        
        actions.append(mapsBtn, detailsBtn);
        card.append(name, details, address, actions);
        grid.appendChild(card);
    });
    
    return { summary, grid };
};

/* ==== Tour-Übersicht: CSB | Schlüssel | Ort | Straße | Name | Button ==== */
const buildTourEntry = (ort, name, strasse, csbNummer, schluessel, mapsUrl, bgAlt) => {
    const entry = el('div', 'tour-entry' + (bgAlt ? ' alt' : ''));
    const row = el('div');

    const csbDiv  = el('div', 'key-col', csbNummer);
    csbDiv.title = `Kundenkarte für ${csbNummer} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-block';
    });

    const sklText = schluessel && schluessel.trim() !== '' ? `Schlüssel: ${schluessel}` : 'Schlüssel: -';
    const sklDiv  = el('div', 'skl-col', sklText);

    const ortDiv  = el('div', 'ort-col', ort);
    const strDiv  = el('div', 'str-col', strasse);
    const nameDiv = el('div', 'name-col', name);

    const btnDiv = el('div', 'btn-col');
    const link = el('a', null, '📍 Maps'); link.href = mapsUrl; link.target = '_blank';
    btnDiv.appendChild(link);

    row.append(csbDiv, sklDiv, ortDiv, strDiv, nameDiv, btnDiv);
    entry.appendChild(row);
    return entry;
};

/* ==== Fachberater-Übersicht: CSB | Schlüssel | Ort | Straße | Name | Button ==== */
const buildFachberaterEntry = (kunde, bgAlt) => {
    const entry = el('div', 'fb-entry' + (bgAlt ? ' alt' : ''));
    const row = el('div');

    const csbDiv  = el('div', 'key-col', kunde.csb);
    csbDiv.title = `Kundenkarte für CSB ${kunde.csb} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = kunde.csb;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-block';
    });

    const sklText = kunde.schluessel && kunde.schluessel.trim() !== '' ? `Schlüssel: ${kunde.schluessel}` : 'Schlüssel: -';
    const sklDiv  = el('div', 'skl-col', sklText);

    const ortDiv  = el('div', 'ort-col', kunde.ort);
    const strDiv  = el('div', 'str-col', kunde.strasse);
    const nameDiv = el('div', 'name-col', kunde.name);

    const btnDiv = el('div', 'btn-col');
    const link = el('a', null, '📍 Maps'); link.href = kunde.mapsUrl; link.target = '_blank';
    btnDiv.appendChild(link);

    row.append(csbDiv, sklDiv, ortDiv, strDiv, nameDiv, btnDiv);
    entry.appendChild(row);
    return entry;
};

// Main
let lastTourSearchQuery = '';
const results  = $('#results');
const treffer  = $('#trefferInfo');
const kundenMap = new Map();

if
