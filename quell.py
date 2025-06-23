import streamlit as st
import pandas as pd
import json

st.title("🚚 Tournummern-basiertes Kundenverzeichnis erzeugen")

excel_file = st.file_uploader("Excel-Datei mit 'Direkt' und 'MK'", type=["xlsx"])

if excel_file:
    if st.button("JSON nach Tournummern erzeugen"):
        try:
            # Wochentage + Spaltenindex
            liefertage = {
                "Montag": 5,
                "Dienstag": 6,
                "Mittwoch": 7,
                "Donnerstag": 8,
                "Freitag": 9,
                "Samstag": 10
            }

            # Dictionary: tournummer → [kunden...]
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

            # Blätter einlesen
            df_direkt = pd.read_excel(excel_file, sheet_name="Direkt")
            df_mk = pd.read_excel(excel_file, sheet_name="MK")

            kunden_sammeln(df_direkt)
            kunden_sammeln(df_mk)

            # JSON serialisieren
            json_data = json.dumps(tour_dict, indent=4, ensure_ascii=False)

            st.success(f"{len(tour_dict)} Touren gefunden.")
            st.download_button(
                label="📥 Touren-JSON herunterladen",
                data=json_data.encode("utf-8"),
                file_name="kunden_nach_tournummer.json",
                mime="application/json"
            )

            # Vorschau einer Tour anzeigen
            beispiel = next(iter(tour_dict.keys()))
            st.subheader(f"📋 Vorschau Tour {beispiel}")
            st.json(tour_dict[beispiel])

        except Exception as e:
            st.error(f"Fehler: {e}")
