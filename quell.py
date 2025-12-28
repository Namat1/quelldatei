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

# ---------------- STREAMLIT ----------------
st.title("Kunden-Suche – Raised Darkmode")
logo = st.file_uploader("Logo", type=["png","jpg","jpeg"])
if logo:
    b64 = base64.b64encode(logo.read()).decode()
    html = HTML_TEMPLATE.replace("__LOGO_DATA_URL__", f"data:image/png;base64,{b64}")
    st.download_button("HTML herunterladen", html, "suche.html", "text/html")
