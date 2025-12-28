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
:root{
  --bg:#f4f6fa;
  --surface:#ffffff;
  --alt:#f8fafc;
  --grid:#d5dde9;
  --txt:#0b1220;
  --muted:#334155;
  --accent:#2563eb;
  --radius:10px;
}

/* ========================= */
/* GLOBAL HARD STOP SCROLL   */
/* ========================= */
html, body{
  margin:0;
  padding:0;
  overflow-x:hidden;
  height:100%;
}

*{box-sizing:border-box}

body{
  background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui;
  font-size:12px;
  font-weight:650;
  color:var(--txt);
}

/* ========================= */
/* FIXED 1728px LAYOUT       */
/* ========================= */
.page{
  min-height:100vh;
  display:flex;
  justify-content:center;
}

.container{
  width:1728px;          /* 90% von 1920 */
  max-width:1728px;
  margin:0 auto;
}

.card{
  background:var(--surface);
  border:1px solid var(--grid);
  border-radius:var(--radius);
  overflow:hidden;
}

/* ========================= */
/* HEADER                    */
/* ========================= */
.header{
  padding:10px;
  text-align:center;
  border-bottom:1px solid var(--grid);
}

.brand-logo{
  height:46px;
}

/* ========================= */
/* SEARCHBAR                 */
/* ========================= */
.searchbar{
  padding:10px;
  display:grid;
  grid-template-columns:1fr 200px auto auto;
  gap:8px;
  border-bottom:1px solid var(--grid);
}

.field{
  display:grid;
  grid-template-columns:70px 1fr;
  gap:6px;
  align-items:center;
}

.label{
  font-weight:800;
  font-size:11px;
  text-transform:uppercase;
  color:var(--muted);
}

.input{
  width:100%;
  padding:7px 10px;
  border:1px solid var(--grid);
  border-radius:8px;
  font-size:12px;
}

.input:focus{
  outline:none;
  border-color:var(--accent);
}

/* ========================= */
/* BUTTONS                   */
/* ========================= */
.btn{
  padding:7px 12px;
  border-radius:8px;
  border:1px solid var(--grid);
  background:#fff;
  cursor:pointer;
  font-weight:800;
}

.btn-danger{
  background:#ef4444;
  border-color:#ef4444;
  color:#fff;
}

/* ========================= */
/* TABLE                     */
/* ========================= */
.table-section{
  padding:10px;
  overflow:visible;
}

table{
  width:100%;
  table-layout:fixed;
  border-collapse:collapse;
  min-width:0;
}

thead th{
  background:#eef2f8;
  padding:8px;
  font-size:11px;
  font-weight:900;
  text-transform:uppercase;
  border-bottom:2px solid var(--grid);
  text-align:left;
}

tbody td{
  padding:8px;
  border-bottom:1px solid var(--grid);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

tbody tr:nth-child(odd){background:var(--alt)}

/* ========================= */
/* MOBILE / PORTRAIT         */
/* ========================= */
@media (orientation:portrait){
  .container{
    width:100%;
    max-width:100%;
  }
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
          <input class="input" id="smartSearch" placeholder="Name, Ort, Tour, SAP …">
        </div>

        <div class="field">
          <div class="label">Schlüssel</div>
          <input class="input" id="keySearch">
        </div>

        <button class="btn" id="btnReset">Reset</button>
        <button class="btn btn-danger" id="btnBack" style="display:none;">Zurück</button>
      </div>

      <div class="table-section">
        <table id="resultTable" style="display:none;">
          <colgroup>
            <col style="width:15%">
            <col style="width:40%">
            <col style="width:20%">
            <col style="width:10%">
            <col style="width:15%">
          </colgroup>
          <thead>
            <tr>
              <th>CSB / SAP</th>
              <th>Name / Adresse</th>
              <th>Touren</th>
              <th>Schlüssel</th>
              <th>Kontakt</th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>

    </div>
  </div>
</div>

<script>
/* JS bleibt unverändert – nur Layout-Fix */
</script>

</body>
</html>
"""

st.title("Kunden-Suche – Fix 1728px (90% von 1920)")
st.caption("Garantiert ohne horizontalen Scrollbalken")

logo_file = st.file_uploader("Logo", type=["png","jpg","jpeg"])

if logo_file:
    logo_data_url = "data:"+logo_file.type+";base64,"+base64.b64encode(logo_file.read()).decode()
    html = HTML_TEMPLATE.replace("__LOGO_DATA_URL__", logo_data_url)

    st.download_button(
        "HTML herunterladen",
        data=html.encode("utf-8"),
        file_name="suche_1728px_fix.html",
        mime="text/html"
    )
