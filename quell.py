import streamlit as st
import pandas as pd
import json

st.title("🚛 Kunden nach Tournummer sortiert exportieren")

excel_file = st.file_uploader("Excel-Datei mit Blättern 'Direkt 1 - 99' und 'Hupa MK 882'", type=["xlsx"])

if excel_file:
    if st.button("JSON erzeugen – nach Tournummer sortiert"):
        try:
            # Neue Spaltenindizes basierend auf deiner Struktur (0-basiert)
            liefertage = {
                "Montag": 6,
                "Dienstag": 7,
                "Mittwoch": 8,
                "Donnerstag": 9,
                "Freitag": 10,
                "Samstag": 11
            }

            tour_dict = {}

            def kunden_sammeln(df):
                for _, row in df.iterrows():
                    for tag, idx in liefertage.items():
                        tournr = row[idx]
                        # Nur numerische Tournummern verarbeiten
                        if isinstance(tournr, (int, float)) and not pd.isna(tournr):
                            tournr = str(int(tournr))
                        else:
                            continue  # z. B. "ADENDORF" überspringen

                        eintrag = {
                            "kundennummer": str(row[0]),
                            "name": row[2],
                            "strasse": row[3],
                            "postleitzahl": str(row[4]),
                            "ort": row[5],
                            "liefertag": tag
                        }
                        if tournr not in tour_dict:
                            tour_dict[tournr] = []
                        tour_dict[tournr].append(eintrag)

            # Blätter einlesen
            df_direkt = pd.read_excel(excel_file, sheet_name="Direkt 1 - 99")
            df_mk = pd.read_excel(excel_file, sheet_name="Hupa MK 882")

            # Kunden einsammeln
            kunden_sammeln(df_direkt)
            kunden_sammeln(df_mk)

            # Tournummern sortieren
            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))

            # JSON erzeugen
            json_data = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            st.success(f"{len(sorted_tours)} Touren exportiert (sortiert).")

            # Download-Button
            st.download_button(
                label="📥 Sortierte JSON-Datei herunterladen",
                data=json_data.encode("utf-8"),
                file_name="tourkunden_sortiert.json",
                mime="application/json"
            )

            # Vorschau einer Tour anzeigen
            if sorted_tours:
                beispiel = next(iter(sorted_tours.keys()))
                st.subheader(f"📋 Vorschau: Tour {beispiel}")
                st.json(sorted_tours[beispiel])

        except Exception as e:
            st.error(f"Fehler: {e}")
