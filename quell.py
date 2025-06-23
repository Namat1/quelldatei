import streamlit as st
import pandas as pd
import json

st.title("📦 Gesamte Kundendatenbank aus Excel erzeugen (für Webabfrage)")

excel_file = st.file_uploader("Excel-Datei mit Blättern 'Direkt' und 'MK'", type=["xlsx"])

if excel_file:
    if st.button("JSON-Datei mit allen Kunden erzeugen"):
        try:
            # Wochentage und Spaltenindex (0-basiert)
            liefertage = {
                "Montag": 5,
                "Dienstag": 6,
                "Mittwoch": 7,
                "Donnerstag": 8,
                "Freitag": 9,
                "Samstag": 10
            }

            # Alle Kunden sammeln
            kunden_liste = []

            def verarbeite_blatt(df):
                for _, row in df.iterrows():
                    kunden_liste.append({
                        "kundennummer": str(row[0]),
                        "name": row[1],
                        "strasse": row[2],
                        "postleitzahl": str(row[3]),
                        "ort": row[4],
                        "touren": {
                            tag: int(row[idx]) if pd.notna(row[idx]) else None
                            for tag, idx in liefertage.items()
                        }
                    })

            df_direkt = pd.read_excel(excel_file, sheet_name="Direkt")
            df_mk = pd.read_excel(excel_file, sheet_name="MK")

            verarbeite_blatt(df_direkt)
            verarbeite_blatt(df_mk)

            json_data = json.dumps(kunden_liste, indent=4, ensure_ascii=False)

            st.success(f"{len(kunden_liste)} Kunden verarbeitet.")

            st.download_button(
                label="📥 Vollständige JSON-Datei herunterladen",
                data=json_data.encode("utf-8"),
                file_name="alle_kunden.json",
                mime="application/json"
            )

            st.json(kunden_liste[:5])  # Vorschau der ersten 5

        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der Datei: {e}")
