import streamlit as st
import pandas as pd
import json

st.title("🚛 Kunden nach Tournummer sortiert exportieren")

excel_file = st.file_uploader(
    "Excel-Datei mit Blättern 'Direkt 1 - 99', 'Hupa MK 882', 'Hupa 2221-4444', 'Hupa 7773-7779'",
    type=["xlsx"]
)

if excel_file:
    if st.button("JSON erzeugen – nach Tournummer sortiert"):
        try:
            # Wochentag → Spaltenname (wie in den Blättern)
            liefertage = {
                "Montag": "Mo",
                "Dienstag": "Die",
                "Mittwoch": "Mitt",
                "Donnerstag": "Don",
                "Freitag": "Fr",
                "Samstag": "Sam"
            }

            tour_dict = {}

            def kunden_sammeln(df):
                for _, row in df.iterrows():
                    for tag, spaltenname in liefertage.items():
                        if spaltenname not in df.columns:
                            continue  # Spalte fehlt im Blatt
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw.replace('.', '').isdigit():
                            continue  # kein gültiger Wert

                        tournr = str(int(float(tournr_raw)))

                        eintrag = {
                            "csb_nummer": str(row.get("Nr", "")).strip(),
                            "sap_nummer": str(row.get("SAP-Nr.", "")).strip(),
                            "name": str(row.get("Name", "")).strip(),
                            "strasse": str(row.get("Strasse", "")).strip(),
                            "postleitzahl": str(row.get("Plz", "")).strip(),
                            "ort": str(row.get("Ort", "")).strip(),
                            "liefertag": tag,
                            "fachberater": str(row.get("Fachberater", "")).strip()
                        }

                        if tournr not in tour_dict:
                            tour_dict[tournr] = []
                        tour_dict[tournr].append(eintrag)

            # Blätter einlesen
            blattnamen = [
                "Direkt 1 - 99",
                "Hupa MK 882",
                "Hupa 2221-4444",
                "Hupa 7773-7779"
            ]

            for blatt in blattnamen:
                df = pd.read_excel(excel_file, sheet_name=blatt)
                kunden_sammeln(df)

            # Nach Tournummer sortieren
            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))

            # JSON erzeugen
            json_data = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            st.success(f"{len(sorted_tours)} Touren exportiert (sortiert).")

            st.download_button(
                label="📥 Sortierte JSON-Datei herunterladen",
                data=json_data.encode("utf-8"),
                file_name="tourkunden_sortiert.json",
                mime="application/json"
            )

            # Vorschau anzeigen
            if sorted_tours:
                beispiel = next(iter(sorted_tours.keys()))
                st.subheader(f"📋 Vorschau: Tour {beispiel}")
                st.json(sorted_tours[beispiel])

        except Exception as e:
            st.error(f"Fehler: {e}")
