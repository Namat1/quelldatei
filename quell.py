import streamlit as st
import pandas as pd
import json
import base64
import unicodedata
import re

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Kunden-Suche</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&family=Inter+Tight:wght@500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">

<style>
/* =========================================================
   LIGHT THEME (Default)
   ========================================================= */
:root{
  --bg:#f4f6fa;
  --surface:#ffffff;
  --alt:#f8fafc;

  --grid:#d5dde9;
  --grid-2:#c6d0e3;
  --head-grid:#b8c4da;
  --row-sep:#edf2fb;

  --txt:#0b1220;
  --muted:#334155;
  --muted-2:#64748b;

  --accent:#2563eb;
  --accent-2:#1e4fd1;

  --chip-neutral-bg:#f8fafc;
  --chip-neutral-bd:#cbd5e1;
  --chip-neutral-tx:#334155;

  --chip-tour-bg:#ffe4e6;
  --chip-tour-bd:#fb7185;
  --chip-tour-tx:#7f1d1d;

  --chip-key-bg:#dcfce7;
  --chip-key-bd:#22c55e;
  --chip-key-tx:#14532d;

  --chip-addr-bg:#e7f0ff;
  --chip-addr-bd:#7aa7ff;
  --chip-addr-tx:#0b3a8a;

  --shadow-soft:0 1px 0 rgba(15,23,42,.04), 0 8px 24px rgba(15,23,42,.06);

  --radius:10px;
  --radius-pill:999px;
}

/* =========================================================
   DARK THEME – RAISED / HELLER / KONTRASTREICH
   ========================================================= */
:root[data-theme="dark"]{
  --bg:#0a1020;
  --surface:#121b2f;
  --alt:#0f1930;

  --grid:#2a3a5a;
  --grid-2:#33466d;
  --head-grid:#3b5280;
  --row-sep:#0a1224;

  --txt:#f1f5f9;
  --muted:#d7e0ea;
  --muted-2:#a6b4c8;

  --accent:#7dd3fc;
  --accent-2:#a5b4fc;

  --chip-neutral-bg:#172543;
  --chip-neutral-bd:#3a4f7d;
  --chip-neutral-tx:#e6eef8;

  --chip-tour-bg:#3a1020;
  --chip-tour-bd:#fb7185;
  --chip-tour-tx:#ffe4e6;

  --chip-key-bg:#06301c;
  --chip-key-bd:#22c55e;
  --chip-key-tx:#dcfce7;

  --chip-addr-bg:#13264a;
  --chip-addr-bd:#60a5fa;
  --chip-addr-tx:#dbeafe;

  --shadow-soft:
    0 1px 0 rgba(255,255,255,.06),
    0 16px 34px rgba(0,0,0,.35);
}

/* ========================================================= */

*{box-sizing:border-box}
html,body{height:100%; overflow-x:hidden}

body{
  margin:0;
  background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt);
  font-size:12px;
  line-height:1.35;
  font-weight:650;
}

/* Layout */
.page{min-height:100vh; display:flex; justify-content:center}
.container{
  width:90vw;
  max-width:1728px;
  margin:0 auto;
}
.card{
  background:var(--surface);
  border:1px solid var(--grid);
  border-radius:var(--radius);
  box-shadow:var(--shadow-soft);
  overflow:hidden;
}

/* Header */
.header{
  padding:10px 12px;
  border-bottom:1px solid var(--grid);
  display:flex;
  justify-content:center;
}
.brand-logo{height:46px}

/* Searchbar */
.searchbar{
  padding:10px 12px;
  display:grid;
  grid-template-columns:1fr 220px auto auto auto auto;
  gap:8px;
  align-items:center;
  border-bottom:1px solid var(--grid);
}
@media(max-width:900px){ .searchbar{grid-template-columns:1fr} }

.field{display:grid; grid-template-columns:70px 1fr; gap:6px}
.label{
  font-size:11px;
  font-weight:900;
  color:var(--muted);
  text-transform:uppercase;
}

.input{
  padding:7px 10px;
  border:1px solid var(--grid);
  border-radius:8px;
  background:var(--surface);
  color:var(--txt);
}
:root[data-theme="dark"] .input{
  background:rgba(255,255,255,.06);
  border-color:rgba(148,163,184,.35);
}

/* Buttons */
.btn{
  padding:7px 10px;
  border-radius:8px;
  border:1px solid var(--grid);
  background:var(--surface);
  font-weight:800;
  cursor:pointer;
  color:var(--txt);
}
:root[data-theme="dark"] .btn{
  background:rgba(255,255,255,.06);
  border-color:rgba(148,163,184,.35);
}
.btn-danger{background:#ef4444;color:#fff;border-color:#ef4444}
.btn-back{border-color:var(--accent); color:var(--accent)}

/* Toggle */
.btn-toggle{display:flex;gap:8px;align-items:center}
.toggle-dot{
  width:10px;height:10px;border-radius:50%;
  background:var(--muted-2);
}
:root[data-theme="dark"] .toggle-dot{background:var(--accent)}

/* Tabelle */
.table-section{padding:8px 12px}
table{width:100%; table-layout:fixed; border-collapse:separate; border-spacing:0}

thead th{
  position:sticky; top:0;
  background:var(--surface);
  border-bottom:2px solid var(--head-grid);
  padding:8px;
  font-size:11px;
  text-transform:uppercase;
}

tbody td{
  padding:7px 8px;
  border-bottom:1px solid var(--grid);
}
tbody tr:nth-child(odd) td{background:var(--alt)}

/* Chips allgemein */
a.phone-chip,a.mail-chip{
  display:inline-flex;
  gap:6px;
  padding:3px 9px;
  border-radius:999px;
  font-size:11px;
  text-decoration:none;
  border:1px solid var(--grid-2);
  background:var(--surface);
  color:var(--txt);
}

/* === DARK MODE GLOW FÜR PILLs === */
:root[data-theme="dark"] a.phone-chip,
:root[data-theme="dark"] a.mail-chip{
  background:rgba(255,255,255,.07);
  border-color:rgba(148,163,184,.45);
  color:#f8fafc;
  box-shadow:
    0 0 0 1px rgba(255,255,255,.08) inset,
    0 12px 26px rgba(0,0,0,.45);
}
:root[data-theme="dark"] a.phone-chip.chip-fb{
  background:rgba(96,165,250,.22);
  border-color:rgba(96,165,250,.65);
}
:root[data-theme="dark"] a.phone-chip.chip-market{
  background:rgba(167,139,250,.22);
  border-color:rgba(167,139,250,.65);
}
:root[data-theme="dark"] a.mail-chip{
  background:rgba(34,197,94,.20);
  border-color:rgba(34,197,94,.65);
}
</style>
</head>

<body>
<div class="page">
  <div class="container">
    <div class="card">

      <div class="header">
        <img class="brand-logo" src="__LOGO_DATA_URL__">
      </div>

      <div class="searchbar">
        <div class="field">
          <div class="label">Suche</div>
          <input id="smartSearch" class="input">
        </div>
        <div class="field">
          <div class="label">Key</div>
          <input id="keySearch" class="input">
        </div>

        <button class="btn btn-toggle" id="btnTheme">
          <span class="toggle-dot"></span>
          <span id="themeLabel">Dark</span>
        </button>

        <button class="btn btn-back" id="btnBack" style="display:none">Zurück</button>
        <button class="btn btn-danger" id="btnReset">Reset</button>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none">
          <thead>
            <tr>
              <th>CSB</th>
              <th>Name</th>
              <th>Touren</th>
              <th>Schlüssel</th>
              <th>Fachberater / Markt</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>

    </div>
  </div>
</div>

<script>
const THEME_KEY='kunden_suche_theme';

function applyTheme(t){
  if(t==='dark'){
    document.documentElement.setAttribute('data-theme','dark');
    themeLabel.textContent='Light';
  }else{
    document.documentElement.removeAttribute('data-theme');
    themeLabel.textContent='Dark';
  }
}
(function initTheme(){
  const s=localStorage.getItem(THEME_KEY);
  if(s){applyTheme(s);return;}
  applyTheme(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
})();
btnTheme.onclick=()=>{
  const d=document.documentElement.getAttribute('data-theme')==='dark';
  const n=d?'light':'dark';
  localStorage.setItem(THEME_KEY,n);
  applyTheme(n);
};
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.title("Kunden-Suche – V3 (Dispo UI, 90% von 1920 + Darkmode)")
st.caption("Ruhiges Dispo-Theme • Darkmode Toggle • 90% Breite (max 1728) • Portrait: Cards • Landscape: Tabelle")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with c2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])
with c3:
    logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

berater_file = st.file_uploader("OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"])
berater_csb_file = st.file_uploader("Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Tel, X=Markt-Mail)", type=["xlsx"])

def normalize_digits_py(v) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip().replace(".0", "")
    s = "".join(ch for ch in s if ch.isdigit())
    if not s:
        return ""
    s = s.lstrip("0")
    return s if s else "0"

def norm_de_py(s: str) -> str:
    if not s:
        return ""
    x = s.replace("\u200b","").replace("\u200c","").replace("\u200d","").replace("\ufeff","")
    x = x.replace("\u00A0"," ").replace("–","-").replace("—","-").lower()
    x = x.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    x = unicodedata.normalize("NFD", x)
    x = "".join(ch for ch in x if unicodedata.category(ch) != "Mn")
    x = re.sub(r"\(.*?\)", " ", x)
    x = re.sub(r"[./,;:+*_#|]", " ", x)
    x = re.sub(r"-", " ", x)
    x = re.sub(r"[^a-z\s]", " ", x)
    x = " ".join(x.split())
    return x

def build_key_map(df: pd.DataFrame) -> dict:
    if df.shape[1] < 6:
        st.warning("Schlüsseldatei hat < 6 Spalten – nehme letzte vorhandene Spalte als Schlüssel.")
    csb_col = 0
    key_col = 5 if df.shape[1] > 5 else df.shape[1] - 1
    out = {}
    for _, row in df.iterrows():
        csb = normalize_digits_py(row.iloc[csb_col] if df.shape[1] > 0 else "")
        key = normalize_digits_py(row.iloc[key_col] if df.shape[1] > 0 else "")
        if csb:
            out[csb] = key
    return out

def build_berater_map(df: pd.DataFrame) -> dict:
    out = {}
    for _, row in df.iterrows():
        v = ("" if df.shape[1] < 1 or pd.isna(row.iloc[0]) else str(row.iloc[0])).strip()
        n = ("" if df.shape[1] < 2 or pd.isna(row.iloc[1]) else str(row.iloc[1])).strip()
        t = ("" if df.shape[1] < 3 or pd.isna(row.iloc[2]) else str(row.iloc[2])).strip()
        if not t:
            continue
        k1 = norm_de_py(f"{v} {n}")
        k2 = norm_de_py(f"{n} {v}")
        for k in {k1, k2}:
            if k and k not in out:
                out[k] = t
    return out

def build_berater_csb_map(df: pd.DataFrame) -> dict:
    # A = Fachberater, I = CSB, O = Markt-Tel, X = Markt-Mail
    out = {}
    for _, row in df.iterrows():
        fach = str(row.iloc[0]).strip() if df.shape[1] > 0 and not pd.isna(row.iloc[0]) else ""
        csb  = normalize_digits_py(row.iloc[8]) if df.shape[1] > 8 and not pd.isna(row.iloc[8]) else ""
        tel  = str(row.iloc[14]).strip() if df.shape[1] > 14 and not pd.isna(row.iloc[14]) else ""
        mail = str(row.iloc[23]).strip() if df.shape[1] > 23 and not pd.isna(row.iloc[23]) else ""
        if csb:
            out[csb] = {"name": fach, "telefon": tel, "email": mail}
    return out

def to_data_url(file) -> str:
    mime = file.type or ("image/png" if file.name.lower().endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(file.read()).decode("utf-8")

if excel_file and key_file:
    if st.button("HTML erzeugen", type="primary"):
        if logo_file is None:
            st.error("Bitte Logo (PNG/JPG) hochladen.")
            st.stop()

        logo_data_url = to_data_url(logo_file)

        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        SPALTEN_MAPPING = {
            "csb_nummer": "Nr",
            "sap_nummer": "SAP-Nr.",
            "name": "Name",
            "strasse": "Strasse",
            "postleitzahl": "Plz",
            "ort": "Ort",
            "fachberater": "Fachberater"
        }
        LIEFERTAGE_MAPPING = {
            "Montag": "Mo",
            "Dienstag": "Die",
            "Mittwoch": "Mitt",
            "Donnerstag": "Don",
            "Freitag": "Fr",
            "Samstag": "Sam"
        }

        try:
            with st.spinner("Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            berater_map = {}
            if berater_file is not None:
                with st.spinner("Lese Fachberater-Telefonliste..."):
                    berater_file.seek(0)
                    bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                    bf = bf.rename(columns={0: "Vorname", 1: "Nachname", 2: "Nummer"}).dropna(how="all")
                    berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                with st.spinner("Lese Fachberater–CSB-Zuordnung..."):
                    try:
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=0)
                    except Exception:
                        berater_csb_file.seek(0)
                        bcf = pd.read_excel(berater_csb_file, sheet_name=0, header=None)
                    berater_csb_map = build_berater_csb_map(bcf)

            tour_dict = {}

            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns:
                            continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit():
                            continue

                        tournr = normalize_digits_py(tournr_raw)

                        entry = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean = normalize_digits_py(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        entry["csb_nummer"] = csb_clean
                        entry["sap_nummer"] = normalize_digits_py(entry.get("sap_nummer", ""))
                        entry["postleitzahl"] = normalize_digits_py(entry.get("postleitzahl", ""))
                        entry["schluessel"] = key_map.get(csb_clean, "")
                        entry["liefertag"] = tag

                        if csb_clean and csb_clean in berater_csb_map and berater_csb_map[csb_clean].get("name"):
                            entry["fachberater"] = berater_csb_map[csb_clean]["name"]

                        tour_dict.setdefault(tournr, []).append(entry)

            with st.spinner("Verarbeite Kundendatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        pass

            if not tour_dict:
                st.error("Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(
                tour_dict.items(),
                key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0
            ))

            final_html = (
                HTML_TEMPLATE
                .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
                .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
                .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
                .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
                .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            st.download_button(
                "Download HTML",
                data=final_html.encode("utf-8"),
                file_name="suche.html",
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"Fehler: {e}")
else:
    st.info("Bitte Quelldatei, Schlüsseldatei und Logo hochladen. Optional: Fachberater-Telefonliste & CSB-Zuordnung.")
