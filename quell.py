import streamlit as st
import pandas as pd
import json

st.title("🚛 Kunden nach Tournummer sortiert exportieren")

excel_file = st.file_uploader("Excel-Datei mit Blättern 'Direkt' und 'MK'", type=["xlsx"])

if excel_file:
    if st.button("JSON erzeugen – nach Tournummer sortiert"):
        try:
            liefertage = {
                "Montag": 5,
                "Dienstag": 6,
                "Mittwoch": 7,
                "Donnerstag": 8,
                "Freitag": 9,
                "Samstag": 10
            }

            tour_dict = {}

            def kunden_sammeln(df):
                for _, row in df.iterrows():
                    for tag, idx in liefertage.items():
                        tournr = row[idx]
                        if pd.notna(tournr):
                            tournr = str(int(tournr))
                            eintrag = {
                                "kundennummer": str(row[0]),
                                "name": row[1],
                                "strasse": row[2],
                                "postleitzahl": str(row[3]),
                                "ort": row[4],
                                "liefertag": tag
                            }
                            if tournr not in tour_dict:
                                tour_dict[tournr] = []
                            tour_dict[tournr].append(eintrag)

            df_direkt = pd.read_excel(excel_file, sheet_name="Direkt")
            df_mk = pd.read_excel(excel_file, sheet_name="MK")

            kunden_sammeln(df_direkt)
            kunden_sammeln(df_mk)

            # Nach Tournummern numerisch sortieren
            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))

            json_data = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            st.success(f"{len(sorted_tours)} Touren exportiert (sortiert).")
            st.download_button(
                label="📥 Sortierte JSON-Datei herunterladen",
                data=json_data.encode("utf-8"),
                file_name="tourkunden_sortiert.json",
                mime="application/json"
            )

            beispiel = next(iter(sorted_tours.keys()))
            st.subheader(f"📋 Vorschau Tour {beispiel}")
            st.json(sorted_tours[beispiel])

        except Exception as e:
            st.error(f"Fehler: {e}")
