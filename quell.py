import streamlit as st
import pandas as pd
import json

st.title("🚛 Tourkunden aus Excel extrahieren")

# Datei-Upload
excel_file = st.file_uploader("Excel-Datei hochladen (.xlsx)", type=["xlsx"])

if excel_file:
    # Eingabe der Tournummer
    tournummer = st.number_input("Tournummer eingeben (z. B. 1001)", min_value=1000, max_value=9999, step=1)

    if st.button("Kunden filtern und JSON erzeugen"):
        # Wochentags-Zuordnung
        liefertage = {
            "Montag": 5,
            "Dienstag": 6,
            "Mittwoch": 7,
            "Donnerstag": 8,
            "Freitag": 9,
            "Samstag": 10
        }

        def kunden_finden(df, tournummer):
            kunden = []
            for tag, idx in liefertage.items():
                gefiltert = df[df.iloc[:, idx] == tournummer]
                for _, row in gefiltert.iterrows():
                    kunden.append({
                        "kundennummer": str(row[0]),
                        "name": row[1],
                        "strasse": row[2],
                        "postleitzahl": str(row[3]),
                        "ort": row[4],
                        "liefertag": tag
                    })
            return kunden

        try:
            df_direkt = pd.read_excel(excel_file, sheet_name="Direkt")
            df_mk = pd.read_excel(excel_file, sheet_name="MK")

            kunden = kunden_finden(df_direkt, tournummer) + kunden_finden(df_mk, tournummer)

            if kunden:
                json_data = json.dumps(kunden, indent=4, ensure_ascii=False)
                st.success(f"{len(kunden)} Kunden gefunden.")

                st.download_button(
                    label="📥 JSON-Datei herunterladen",
                    data=json_data.encode("utf-8"),
                    file_name="tourkunden.json",
                    mime="application/json"
                )

                st.json(kunden)
            else:
                st.warning("Keine Kunden mit dieser Tournummer gefunden.")
        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der Datei: {e}")
