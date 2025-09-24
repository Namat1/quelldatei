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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800;900&family=Inter+Tight:wght@700;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f3f6fb; --surface:#ffffff; --alt:#f9fbff;
  --grid:#cfd7e6; --grid-2:#bfc9dd; --head-grid:#b3bfd6;
  --txt:#0c1220; --muted:#293346;

  --accent:#2563eb; --accent-2:#1f4fd3;

  --pill-yellow-bg:#fff3b0; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#4a3001;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#ffe4e6;   --pill-red-bd:#fb7185;  --pill-red-tx:#7f1d1d;

  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;

  --row-sep:#e6edff;

  --radius:6px; --radius-pill:999px;
  --fs-10:10px; --fs-11:11px; --fs-12:12px;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg);
  font-family:"Inter Tight", Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color:var(--txt); font-size:var(--fs-12); line-height:1.35; font-weight:800; letter-spacing:.1px;
}

/* Frame */
.page{min-height:100vh; display:flex; justify-content:center; padding:10px}
.container{width:100%; max-width:1480px}
.card{background:var(--surface); border:1px solid var(--grid); border-radius:8px; overflow:hidden}

/* Header */
.header{
  padding:10px 12px;
  background:linear-gradient(180deg,#ffffff 0%, #f4f7fe 100%);
  color:#0b1226; display:flex; align-items:center; justify-content:center; gap:10px;
  border-bottom:1px solid var(--grid);
}
.brand-logo{height:56px; width:auto}
.title{font-weight:900; letter-spacing:.35px; font-size:13px; text-transform:uppercase}

/* Searchbar */
.searchbar{
  padding:8px 12px; display:grid; grid-template-columns:1fr 260px auto auto; gap:8px; align-items:center;
  border-bottom:1px solid var(--grid); background:var(--surface);
}
@media(max-width:1100px){ .searchbar{grid-template-columns:1fr 1fr} }
@media(max-width:680px){ .searchbar{grid-template-columns:1fr} }
.field{display:grid; grid-template-columns:74px 1fr; gap:6px; align-items:center}
.label{font-weight:900; color:var(--muted); font-size:var(--fs-11); text-transform:uppercase; letter-spacing:.35px}
.input{
  width:100%; padding:7px 9px; border:1px solid var(--grid); border-radius:6px; background:#fff;
  font-size:var(--fs-12); font-weight:900;
}
.input:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 2px rgba(37,99,235,.16)}

/* Buttons */
.btn{padding:7px 10px; border:1px solid var(--grid); background:#fff; color:#0f172a; border-radius:6px; cursor:pointer; font-weight:900; font-size:var(--fs-12)}
.btn:hover{background:#f2f5f9}
.btn-danger{border-color:#d7263d; background:#d7263d; color:#fff}
.btn-danger:hover{background:#bf1f33}
.btn-back{border-color:var(--accent); color:var(--accent-2); background:#eef2ff}
.btn-back:hover{background:#e2e8ff}

/* Tour-Banner */
.tour-wrap{display:none; padding:10px 12px 0}
.tour-banner{display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0; background:transparent; border:none;}
.tour-pill{
  display:inline-flex; align-items:center; gap:10px;
  background:#ffedd5; color:#7c2d12;
  border:2px solid #fb923c; border-radius:999px; padding:8px 14px;
  font-weight:900; font-size:13px; letter-spacing:.2px;
  box-shadow:0 0 0 3px rgba(251,146,60,.18) inset;
}
.tour-stats{font-weight:900; font-size:11px; color:#334155}

/* Tabelle */
.table-section{padding:6px 12px 14px; overflow-x:auto}
table{width:100%; border-collapse:separate; border-spacing:0; table-layout:fixed; font-size:var(--fs-12); min-width:920px}
thead th{
  position:sticky; top:0; z-index:2;
  background:linear-gradient(180deg,#f7f9fe,#eef2f8);
  color:#0f172a; font-weight:900; text-transform:uppercase; letter-spacing:.25px;
  border-bottom:2px solid var(--head-grid); border-right:1px solid var(--head-grid);
  padding:8px 9px; white-space:nowrap; text-align:left;
}
thead th:last-child{border-right:none}
tbody td{
  padding:8px 9px; vertical-align:top; font-weight:800;
  border-bottom:1px solid var(--grid); border-right:1px solid var(--grid);
  background:#fff;
}
tbody td:last-child{border-right:none}

/* Zeilen */
tbody tr:nth-child(odd) td{background:#f8fbff}
tbody tr:nth-child(even) td{background:#ffffff}
tbody tr+tr td{border-top:6px solid var(--row-sep)}
tbody tr:hover td{background:#eef4ff}

/* Zellen */
.cell{display:flex; flex-direction:column; gap:4px; min-height:38px; width:100%}
.cell-top,.cell-sub{max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}

/* Monospace Zahlen */
.mono{font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-weight:700}

/* ID-Chips */
a.id-chip{
  display:inline-flex; align-items:center; gap:6px;
  background:var(--pill-yellow-bg); color:var(--pill-yellow-tx);
  border:1.5px solid var(--pill-yellow-bd); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); text-decoration:none; line-height:1;
  box-shadow:0 0 0 2px rgba(245,158,11,.12) inset;
}
a.id-chip:hover{filter:brightness(.97)}
.id-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}

/* Schlüssel */
.badge-key{
  display:inline-block; background:var(--pill-green-bg); border:1.5px solid var(--pill-green-bd);
  color:var(--pill-green-tx); border-radius:var(--radius-pill); padding:3px 9px;
  font-weight:900; font-size:var(--fs-11); line-height:1;
  box-shadow:0 0 0 2px rgba(16,185,129,.12) inset;
}

/* Touren */
.tour-inline{display:flex; flex-wrap:wrap; gap:6px}
.tour-btn{
  display:inline-block; background:var(--pill-red-bg); border:1.5px solid var(--pill-red-bd); color:var(--pill-red-tx);
  padding:3px 9px; border-radius:var(--radius-pill); font-weight:900; font-size:var(--fs-10); cursor:pointer; line-height:1.25; letter-spacing:.15px;
  box-shadow:0 0 0 2px rgba(251,113,133,.12) inset;
}
.tour-btn:hover{filter:brightness(.97)}

/* Telefon-/Mail-Chips */
.phone-col{display:flex; flex-direction:column; gap:6px}
a.phone-chip, a.mail-chip{
  display:inline-flex; align-items:center; gap:6px; border-radius:var(--radius-pill);
  padding:3px 9px; font-weight:900; font-size:var(--fs-11); line-height:1; text-decoration:none; cursor:pointer; width:max-content; max-width:100%;
}
a.phone-chip.chip-fb{background:var(--chip-fb-bg); color:var(--chip-fb-tx); border:1.5px solid var(--chip-fb-bd)}
a.phone-chip.chip-market{background:var(--chip-mk-bg); color:var(--chip-mk-tx); border:1.5px solid var(--chip-mk-bd)}
a.mail-chip{background:#e6f7f4; color:#065f46; border:1.5px solid #10b981; max-width:100%}
a.phone-chip:hover, a.mail-chip:hover{filter:brightness(.97)}
.chip-tag{font-size:var(--fs-10); font-weight:900; text-transform:uppercase; letter-spacing:.35px; opacity:.95}
.mail-chip .txt{white-space:normal; word-break:break-all; line-height:1.2}

/* Adresse-Pill */
a.addr-chip{
  display:inline-flex; align-items:center; gap:8px; max-width:100%;
  background:#e0ecff; color:#0b3a8a; border:1.5px solid #60a5fa; border-radius:999px; padding:4px 10px;
  text-decoration:none; font-weight:900; font-size:var(--fs-11);
}
.addr-chip .txt{white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%}
.addr-dot{width:6px; height:6px; background:#ff2d55; border-radius:999px; display:inline-block}

/* ========================= */
/* Portrait full-width cards */
/* ========================= */
@media (orientation: portrait) {
  body{ font-size:11px; }
  .page{ padding:0 }
  .container{ max-width:none; width:100% }
  .card{ border-left:none; border-right:none; border-radius:0 }

  .header{
    padding:8px max(12px, env(safe-area-inset-right))
             8px max(12px, env(safe-area-inset-left));
  }
  .brand-logo{ height:40px }

  .searchbar{
    position:sticky; top:0; z-index:5;
    grid-template-columns:1fr; gap:6px;
    padding:8px max(12px, env(safe-area-inset-right))
            8px max(12px, env(safe-area-inset-left));
    border-bottom:1px solid var(--grid);
    background:var(--surface);
  }
  .label{ font-size:10px }
  .input{ padding:6px 8px; font-size:11px }
  .btn{ padding:6px 8px; font-size:11px }

  .tour-wrap{
    padding:6px max(12px, env(safe-area-inset-right))
            0   max(12px, env(safe-area-inset-left));
  }
  .tour-banner{ gap:8px }
  .tour-pill{ padding:5px 10px; font-size:11px }
  .tour-stats{ font-size:10px }

  .table-section{
    padding:8px max(12px, env(safe-area-inset-right))
            12px max(12px, env(safe-area-inset-left));
    overflow:visible;
  }
  table{ width:100%; min-width:0; border-spacing:0; table-layout:auto }
  thead{ display:none }

  tbody tr{
    display:block;
    margin:10px 0;
    background:#fff;
    border:1px solid var(--grid);
    border-radius:10px;
    box-shadow:0 1px 0 rgba(0,0,0,.02);
    overflow:hidden;
  }
  tbody tr:nth-child(odd) td,
  tbody tr:nth-child(even) td{ background:#fff }
  tbody tr+tr td{ border-top:none }

  tbody td{
    display:flex;
    gap:10px;
    align-items:flex-start;
    justify-content:space-between;
    padding:8px 10px;
    border:none;
    border-bottom:1px solid var(--grid);
  }
  tbody td:last-child{ border-bottom:none }

  tbody td::before{
    content:attr(data-label);
    flex:0 0 88px;
    margin-right:8px;
    white-space:nowrap;
    font-weight:900; color:var(--muted);
    text-transform:uppercase; letter-spacing:.3px;
    font-size:10px; line-height:1.2;
  }

  .cell{ gap:3px; min-height:auto }
  .cell-top,.cell-sub{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis }
  .tour-inline{ gap:4px; row-gap:6px }
  .tour-btn{ font-size:10px; padding:2px 6px; line-height:1.2 }
  .badge-key{ font-size:10px; padding:2px 7px }
  a.phone-chip, a.mail-chip{ font-size:10px; padding:3px 7px; max-width:100%; white-space:normal; line-height:1.25 }
  .mail-chip .txt{ white-space:normal; word-break:break-word }
  a.addr-chip{ font-size:10px; padding:3px 8px; max-width:100%; white-space:normal }
}
</style>
</head>
<body>
<!-- hier kommt dein JS/HTML Code mit rowFor() usw. rein -->
</body>
</html>
"""

# ===== Streamlit Wrapper (gekürzt, bleibt wie gehabt) =====
st.title("Kunden-Suche – Tech-Lab")
st.caption("Portrait: full width cards, Landscape: Tabelle")

# ... dein File-Upload und Processing-Code bleibt identisch ...
