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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Inter+Tight:wght@700;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f1f5f9; --surface:#ffffff; --alt:#f8fafc;
  --grid:#e2e8f0; --grid-2:#cbd5e1; --head-grid:#94a3b8;
  --txt:#0f172a; --muted:#475569; --muted-light:#64748b;

  --accent:#2563eb; --accent-2:#1d4ed8; --accent-light:#3b82f6;
  --success:#10b981; --warning:#f59e0b; --danger:#ef4444;

  --pill-yellow-bg:#fef3c7; --pill-yellow-bd:#f59e0b; --pill-yellow-tx:#92400e;
  --pill-green-bg:#d1fae5; --pill-green-bd:#10b981; --pill-green-tx:#065f46;
  --pill-red-bg:#fee2e2;   --pill-red-bd:#ef4444;  --pill-red-tx:#991b1b;
  --pill-blue-bg:#dbeafe; --pill-blue-bd:#3b82f6; --pill-blue-tx:#1e40af;

  --chip-fb-bg:#e0f2ff; --chip-fb-bd:#3b82f6; --chip-fb-tx:#0b3b93;
  --chip-mk-bg:#ede9fe; --chip-mk-bd:#8b5cf6; --chip-mk-tx:#2c1973;

  --row-sep:#e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

  --radius: 8px; --radius-sm: 6px; --radius-pill: 999px;
  --fs-09: 9px; --fs-10: 10px; --fs-11: 11px; --fs-12: 12px; --fs-13: 13px; --fs-14: 14px;
}

/* Reset & Base */
*, *::before, *::after { box-sizing: border-box; }
html, body { height: 100%; }
body {
  margin: 0; background: var(--bg);
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  color: var(--txt); font-size: var(--fs-12); line-height: 1.5; font-weight: 500;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}

/* Smooth Transitions */
* {
  transition: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
              color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Layout */
.page {
  min-height: 100vh; display: flex; justify-content: center; 
  padding: 20px 12px;
}
.container {
  width: 100%; max-width: 1600px;
}
.card {
  background: var(--surface); border-radius: var(--radius);
  box-shadow: var(--shadow-lg); overflow: hidden;
}

/* Header */
.header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  color: var(--txt); display: flex; align-items: center; justify-content: center; gap: 12px;
  border-bottom: 1px solid var(--grid);
}
.brand-logo { 
  height: 64px; width: auto; 
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

/* Search Section */
.searchbar {
  padding: 20px; 
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid var(--grid);
}

.search-grid {
  display: grid; 
  grid-template-columns: 1fr 300px auto auto; 
  gap: 16px; 
  align-items: end;
}

@media(max-width: 1200px) { 
  .search-grid { grid-template-columns: 1fr 1fr auto auto; } 
}
@media(max-width: 768px) { 
  .search-grid { grid-template-columns: 1fr; gap: 12px; } 
  .searchbar { padding: 16px; }
}

.field {
  display: flex; flex-direction: column; gap: 6px;
  position: relative;
}

.label {
  font-weight: 600; color: var(--muted); font-size: var(--fs-11); 
  text-transform: uppercase; letter-spacing: 0.5px;
}

.input-wrapper {
  position: relative;
}

.input {
  width: 100%; padding: 12px 16px; 
  border: 2px solid var(--grid); border-radius: var(--radius-sm); 
  background: #fff; font-size: var(--fs-13); font-weight: 500;
  color: var(--txt);
}

.input:focus {
  outline: none; 
  border-color: var(--accent); 
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  transform: translateY(-1px);
}

.input:not(:placeholder-shown) + .clear-btn {
  display: block;
}

.clear-btn {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  background: none; border: none; color: var(--muted-light); cursor: pointer;
  font-size: 16px; display: none; padding: 4px;
  border-radius: 4px;
}

.clear-btn:hover {
  background: var(--alt); color: var(--muted);
}

/* Buttons */
.btn {
  padding: 12px 20px; border: 2px solid var(--grid); background: #fff; 
  color: var(--txt); border-radius: var(--radius-sm); cursor: pointer; 
  font-weight: 600; font-size: var(--fs-12); 
  display: inline-flex; align-items: center; gap: 8px;
  white-space: nowrap;
}

.btn:hover {
  background: var(--alt); transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px;
}

.btn-danger {
  border-color: var(--danger); background: var(--danger); color: #fff;
}
.btn-danger:hover {
  background: #dc2626; border-color: #dc2626;
}

.btn-back {
  border-color: var(--accent); color: var(--accent); background: var(--pill-blue-bg);
}
.btn-back:hover {
  background: #bfdbfe; border-color: var(--accent-2);
}

/* Tour Banner */
.tour-wrap {
  display: none; padding: 16px 20px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-bottom: 1px solid var(--warning);
}

.tour-banner {
  display: flex; align-items: center; justify-content: space-between; 
  gap: 16px; flex-wrap: wrap;
}

.tour-pill {
  display: inline-flex; align-items: center; gap: 12px;
  background: var(--pill-yellow-bg); color: var(--pill-yellow-tx);
  border: 2px solid var(--pill-yellow-bd); border-radius: var(--radius-pill); 
  padding: 10px 20px; font-weight: 700; font-size: var(--fs-13); 
  letter-spacing: 0.25px;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15) inset;
}

.tour-stats {
  font-weight: 600; font-size: var(--fs-11); color: var(--muted);
  background: rgba(255, 255, 255, 0.8); padding: 6px 12px;
  border-radius: var(--radius-sm);
}

/* Table Section */
.table-section {
  padding: 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.table-container {
  border-radius: var(--radius-sm);
  border: 1px solid var(--grid);
  overflow: hidden;
  box-shadow: var(--shadow);
}

table {
  width: 100%; border-collapse: separate; border-spacing: 0; 
  table-layout: fixed; font-size: var(--fs-12);
  background: var(--surface);
}

/* Table Header */
thead th {
  position: sticky; top: 0; z-index: 10;
  background: linear-gradient(180deg, #f1f5f9, #e2e8f0);
  color: var(--txt); font-weight: 700; text-transform: uppercase; 
  letter-spacing: 0.5px; font-size: var(--fs-10);
  border-bottom: 2px solid var(--head-grid); 
  border-right: 1px solid var(--head-grid);
  padding: 16px 12px; white-space: nowrap; text-align: left;
  line-height: 1.3;
}

thead th:last-child { border-right: none; }

/* Table Body */
tbody td {
  padding: 16px 12px; vertical-align: top; 
  border-bottom: 1px solid var(--grid); 
  border-right: 1px solid var(--grid);
  background: #fff;
}

tbody td:last-child { border-right: none; }

tbody tr:nth-child(odd) td { background: #f8fafc; }
tbody tr:nth-child(even) td { background: #ffffff; }

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

tbody tr:hover td {
  background: #eef4ff !important;
}

tbody tr + tr td {
  border-top: 4px solid var(--row-sep);
}

/* Table Columns */
.col-csb { width: 210px; }
.col-name { width: 520px; }
.col-tours { width: 260px; }
.col-key { width: 105px; }
.col-contact { width: 418px; }

/* Cell Content */
.cell {
  display: flex; flex-direction: column; gap: 6px; 
  min-height: 40px; width: 100%;
}

.cell-top, .cell-sub {
  max-width: 100%; white-space: nowrap; 
  overflow: hidden; text-overflow: ellipsis;
}

.cell-top {
  font-size: var(--fs-13); font-weight: 700; color: var(--txt);
}

.cell-sub {
  font-size: var(--fs-11); color: var(--muted); font-weight: 500;
}

/* Monospace */
.mono {
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; 
  font-weight: 600;
}

/* ID Chips */
a.id-chip {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--pill-yellow-bg); color: var(--pill-yellow-tx);
  border: 2px solid var(--pill-yellow-bd); border-radius: var(--radius-pill); 
  padding: 6px 12px; font-weight: 700; font-size: var(--fs-11); 
  text-decoration: none; line-height: 1;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.1) inset;
}

a.id-chip:hover {
  filter: brightness(0.97); transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

a.id-chip:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 1px;
}

.id-tag {
  font-size: var(--fs-09); font-weight: 700; 
  text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;
}

/* Key Badge */
.badge-key {
  display: inline-block; background: var(--pill-green-bg); 
  border: 2px solid var(--pill-green-bd); color: var(--pill-green-tx); 
  border-radius: var(--radius-pill); padding: 6px 12px;
  font-weight: 700; font-size: var(--fs-11); line-height: 1;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1) inset;
}

/* Tour Buttons */
.tour-inline {
  display: flex; flex-wrap: wrap; gap: 6px;
}

.tour-btn {
  display: inline-block; background: var(--pill-red-bg); 
  border: 2px solid var(--pill-red-bd); color: var(--pill-red-tx);
  padding: 4px 10px; border-radius: var(--radius-pill); 
  font-weight: 700; font-size: var(--fs-10); cursor: pointer; 
  line-height: 1.3; letter-spacing: 0.25px;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.1) inset;
}

.tour-btn:hover {
  filter: brightness(0.97); transform: translateY(-1px);
}

/* Contact Chips */
.phone-col {
  display: flex; flex-direction: column; gap: 8px;
}

a.phone-chip, a.mail-chip {
  display: inline-flex; align-items: center; gap: 6px; 
  border-radius: var(--radius-pill); padding: 6px 12px; 
  font-weight: 700; font-size: var(--fs-11); line-height: 1; 
  text-decoration: none; cursor: pointer; width: max-content; 
  max-width: 100%; border: 2px solid;
}

a.phone-chip.chip-fb {
  background: var(--chip-fb-bg); color: var(--chip-fb-tx); 
  border-color: var(--chip-fb-bd);
}

a.phone-chip.chip-market {
  background: var(--chip-mk-bg); color: var(--chip-mk-tx); 
  border-color: var(--chip-mk-bd);
}

a.mail-chip {
  background: #ecfdf5; color: #065f46; border-color: #10b981; 
  max-width: 100%;
}

a.phone-chip:hover, a.mail-chip:hover {
  filter: brightness(0.97); transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

a.phone-chip:focus-visible, a.mail-chip:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 1px;
}

.chip-tag {
  font-size: var(--fs-09); font-weight: 700; 
  text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;
}

.mail-chip .txt {
  white-space: normal; word-break: break-all; line-height: 1.2;
}

/* Address Chip */
a.addr-chip {
  display: inline-flex; align-items: center; gap: 8px; max-width: 100%;
  background: var(--pill-blue-bg); color: var(--pill-blue-tx); 
  border: 2px solid var(--pill-blue-bd); border-radius: var(--radius-pill); 
  padding: 6px 12px; text-decoration: none; font-weight: 700; 
  font-size: var(--fs-11);
}

.addr-chip:hover {
  filter: brightness(0.97); transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.addr-chip:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 1px;
}

.addr-chip .txt {
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; 
  max-width: 100%;
}

.addr-dot {
  width: 6px; height: 6px; background: var(--danger); 
  border-radius: 50%; display: inline-block;
}

/* Loading Animation */
.loading::after {
  content: "";
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid var(--accent);
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
  margin-left: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Search Suggestions */
.search-suggestions {
  position: absolute; top: 100%; left: 0; right: 0;
  background: var(--surface); border: 1px solid var(--grid);
  border-radius: var(--radius-sm); margin-top: 4px; z-index: 20;
  max-height: 200px; overflow-y: auto; display: none;
  box-shadow: var(--shadow-md);
}

.suggestion-item {
  padding: 10px 12px; cursor: pointer; font-size: var(--fs-12);
  border-bottom: 1px solid var(--alt); color: var(--txt);
  display: flex; align-items: center; gap: 8px;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background: var(--alt);
}

.suggestion-type {
  font-size: var(--fs-10); color: var(--muted); 
  background: var(--alt); padding: 2px 6px; 
  border-radius: var(--radius-sm); font-weight: 600;
}

/* Empty State */
.empty-state {
  text-align: center; padding: 60px 20px; color: var(--muted);
}

.empty-state-icon {
  font-size: 48px; margin-bottom: 16px; opacity: 0.5;
}

.empty-state-title {
  font-size: var(--fs-14); font-weight: 600; margin-bottom: 8px;
}

.empty-state-text {
  font-size: var(--fs-12); line-height: 1.5;
}

/* Results Counter */
.results-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; padding: 0 4px;
}

.results-count {
  font-size: var(--fs-12); color: var(--muted); font-weight: 600;
}

.results-actions {
  display: flex; gap: 8px;
}

.action-btn {
  padding: 6px 12px; background: var(--alt); border: 1px solid var(--grid);
  border-radius: var(--radius-sm); font-size: var(--fs-11); 
  cursor: pointer; color: var(--muted); font-weight: 600;
}

.action-btn:hover {
  background: var(--grid); color: var(--txt);
}

/* Mobile Responsive Table */
@media(max-width: 768px) {
  .table-container {
    border: none; box-shadow: none;
  }
  
  table, thead, tbody, th, td, tr {
    display: block;
  }
  
  thead tr {
    position: absolute; top: -9999px; left: -9999px;
  }
  
  tbody tr {
    border: 1px solid var(--grid);
    margin-bottom: 16px;
    border-radius: var(--radius);
    background: var(--surface);
    padding: 16px;
    box-shadow: var(--shadow);
  }
  
  tbody tr:hover {
    transform: none;
    box-shadow: var(--shadow-md);
  }
  
  tbody td {
    border: none !important;
    padding: 8px 0 !important;
    position: relative;
    padding-left: 30% !important;
    background: transparent !important;
  }
  
  tbody td:before {
    content: attr(data-label) ": ";
    position: absolute; left: 0; top: 8px;
    width: 25%; padding-right: 10px;
    white-space: nowrap; font-weight: 700;
    color: var(--muted); font-size: var(--fs-11);
    text-transform: uppercase; letter-spacing: 0.5px;
  }
  
  .cell {
    min-height: auto;
  }
  
  .tour-inline {
    flex-direction: column; align-items: flex-start;
  }
  
  .phone-col {
    align-items: flex-start;
  }
}

/* Scroll Improvements */
.table-section {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
}

.table-section::-webkit-scrollbar {
  width: 8px;
}

.table-section::-webkit-scrollbar-track {
  background: var(--alt);
}

.table-section::-webkit-scrollbar-thumb {
  background: var(--grid-2);
  border-radius: 4px;
}

.table-section::-webkit-scrollbar-thumb:hover {
  background: var(--muted-light);
}

/* Print Styles */
@media print {
  .page { padding: 0; }
  .searchbar, .tour-wrap { display: none !important; }
  .card { box-shadow: none; border: 1px solid var(--grid); }
  tbody tr:hover { transform: none; box-shadow: none; }
  tbody tr:hover td { background: inherit !important; }
}
</style>
</head>
<body>
<div class="page">
  <div class="container">
    <div class="card">
      <!-- Header -->
      <div class="header">
        <img class="brand-logo" alt="Logo" src="__LOGO_DATA_URL__">
      </div>

      <!-- Search Section -->
      <div class="searchbar">
        <div class="search-grid">
          <div class="field">
            <div class="label">🔍 Intelligente Suche</div>
            <div class="input-wrapper">
              <input class="input" id="smartSearch" 
                     placeholder="Name, Ort, CSB, SAP, Tour, Fachberater, Telefon..."
                     autocomplete="off">
              <button class="clear-btn" id="clearSmart" title="Leeren">×</button>
              <div class="search-suggestions" id="smartSuggestions"></div>
            </div>
          </div>
          
          <div class="field">
            <div class="label">🔑 Schlüssel (exakt)</div>
            <div class="input-wrapper">
              <input class="input" id="keySearch" placeholder="z.B. 40">
              <button class="clear-btn" id="clearKey" title="Leeren">×</button>
            </div>
          </div>
          
          <button class="btn btn-back" id="btnBack" style="display:none;">
            ← Zurück
          </button>
          
          <button class="btn btn-danger" id="btnReset">
            🗑️ Reset
          </button>
        </div>
      </div>

      <!-- Tour Banner -->
      <div class="tour-wrap" id="tourWrap">
        <div class="tour-banner">
          <span class="tour-pill" id="tourTitle"></span>
          <small class="tour-stats" id="tourExtra"></small>
        </div>
      </div>

      <!-- Table Section -->
      <div class="table-section">
        <div class="results-header" id="resultsHeader" style="display:none;">
          <span class="results-count" id="resultsCount"></span>
          <div class="results-actions">
            <button class="action-btn" onclick="exportResults()">📊 Export</button>
            <button class="action-btn" onclick="printResults()">🖨️ Drucken</button>
          </div>
        </div>
        
        <div class="empty-state" id="emptyState">
          <div class="empty-state-icon">🔍</div>
          <div class="empty-state-title">Keine Ergebnisse</div>
          <div class="empty-state-text">
            Geben Sie einen Suchbegriff ein, um Kunden zu finden.<br>
            Sie können nach Name, Ort, CSB, SAP, Tour, Fachberater oder Telefon suchen.
          </div>
        </div>

        <div class="table-container" id="tableContainer" style="display:none;">
          <table id="resultTable">
            <colgroup>
              <col class="col-csb">
              <col class="col-name">
              <col class="col-tours">
              <col class="col-key">
              <col class="col-contact">
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
</div>

<script>
// Data containers
const tourkundenData   = {  };
const keyIndex         = {  };
const beraterIndex     = {  };
const beraterCSBIndex  = {  };

// Utility functions
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const el = (t,c,txt) => {
  const n = document.createElement(t); 
  if(c) n.className = c; 
  if(txt !== undefined) n.textContent = txt; 
  return n;
};

// State
let allCustomers = [];
let currentResults = [];
let prevQuery = null;
const DIAL_SCHEME = 'tel';

// Search suggestions data
let searchSuggestions = [];

// Utility functions
function sanitizePhone(num) { 
  return (num || '').toString().trim().replace(/[^\\d+]/g, ''); 
}

function normDE(s) {
  if (!s) return '';
  let x = s.toLowerCase();
  x = x.replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
  return x.replace(/\\s+/g, ' ').trim();
}

function normalizeDigits(v) {
  if (v == null) return '';
  let s = String(v).trim().replace(/\\.0$/, '');
  s = s.replace(/[^0-9]/g, '').replace(/^0+(\\d)/, '$1');
  return s;
}

function normalizeNameKey(s) {
  if (!s) return '';
  let x = s.replace(/[\\u200B-\\u200D\\uFEFF]/g, '').replace(/\\u00A0/g, ' ')
    .replace(/[–—]/g, '-').toLowerCase();
  x = x.replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss');
  x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
    .replace(/\\(.*?\\)/g, ' ');
  x = x.replace(/[./,;:+*_#|]/g, ' ').replace(/-/g, ' ')
    .replace(/[^a-z\\s]/g, ' ').replace(/\\s+/g, ' ').trim();
  return x;
}

function nameVariants(s) {
  const base = normalizeNameKey(s); 
  if (!base) return [];
  const parts = base.split(' ').filter(Boolean);
  const out = new Set([base]);
  if (parts.length >= 2) { 
    const f = parts[0], l = parts[parts.length - 1]; 
    out.add(`${f} ${l}`); 
    out.add(`${l} ${f}`); 
  }
  return Array.from(out);
}

function fbEmailFromName(name) {
  const parts = normalizeNameKey(name).split(' ').filter(Boolean);
  if (parts.length < 2) return '';
  const vor = parts[0], nach = parts[parts.length - 1];
  return `${vor}.${nach}@edeka.de`.replace(/\s+/g, '');
}

function pickBeraterPhone(name) {
  if (!name) return '';
  const variants = nameVariants(name);
  for (const v of variants) { 
    if (beraterIndex[v]) return beraterIndex[v]; 
  }
  const keys = Object.keys(beraterIndex);
  for (const v of variants) {
    const parts = v.split(' ').filter(Boolean);
    for (const k of keys) { 
      if (parts.every(p => k.includes(p))) return beraterIndex[k]; 
    }
  }
  return '';
}

function dedupByCSB(list) {
  const seen = new Set(), out = [];
  for (const k of list) { 
    const csb = normalizeDigits(k.csb_nummer); 
    if (!seen.has(csb)) { 
      seen.add(csb); 
      out.push(k); 
    } 
  }
  return out;
}

// Build search suggestions
function buildSearchSuggestions() {
  const suggestions = new Set();
  
  allCustomers.forEach(customer => {
    // Names
    if (customer.name) {
      suggestions.add({
        value: customer.name,
        type: 'Name',
        category: 'customer'
      });
    }
    
    // Cities
    if (customer.ort) {
      suggestions.add({
        value: customer.ort,
        type: 'Ort',
        category: 'location'
      });
    }
    
    // Fachberater
    if (customer.fachberater) {
      suggestions.add({
        value: customer.fachberater,
        type: 'Fachberater',
        category: 'contact'
      });
    }
    
    // Tours
    customer.touren?.forEach(tour => {
      if (tour.tournummer) {
        suggestions.add({
          value: tour.tournummer,
          type: 'Tour',
          category: 'tour'
        });
      }
    });
  });
  
  searchSuggestions = Array.from(suggestions);
}

// Search suggestions UI
function showSuggestions(query, inputId) {
  const input = $(`#${inputId}`);
  const container = input.parentElement.querySelector('.search-suggestions');
  
  if (!query || query.length < 2) {
    container.style.display = 'none';
    return;
  }
  
  const filtered = searchSuggestions
    .filter(item => normDE(item.value).includes(normDE(query)))
    .slice(0, 8);
  
  if (filtered.length === 0) {
    container.style.display = 'none';
    return;
  }
  
  container.innerHTML = '';
  filtered.forEach(item => {
    const div = el('div', 'suggestion-item');
    div.innerHTML = `
      <span class="suggestion-type">${item.type}</span>
      <span>${item.value}</span>
    `;
    div.addEventListener('click', () => {
      input.value = item.value;
      container.style.display = 'none';
      if (inputId === 'smartSearch') onSmart();
      else if (inputId === 'keySearch') onKey();
    });
    container.appendChild(div);
  });
  
  container.style.display = 'block';
}

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.input-wrapper')) {
    $$('.search-suggestions').forEach(el => el.style.display = 'none');
  }
});

// Data building
function buildData() {
  const map = new Map();
  for (const [tour, list] of Object.entries(tourkundenData)) {
    const tourN = normalizeDigits(tour);
    list.forEach(k => {
      const csb = normalizeDigits(k.csb_nummer); 
      if (!csb) return;
      if (!map.has(csb)) {
        const rec = { ...k };
        rec.csb_nummer = csb;
        rec.sap_nummer = normalizeDigits(rec.sap_nummer);
        rec.postleitzahl = normalizeDigits(rec.postleitzahl);
        rec.touren = [];
        rec.schluessel = normalizeDigits(rec.schluessel) || (keyIndex[csb] || '');
        if (beraterCSBIndex[csb] && beraterCSBIndex[csb].name) { 
          rec.fachberater = beraterCSBIndex[csb].name; 
        }
        rec.fb_phone = rec.fachberater ? pickBeraterPhone(rec.fachberater) : '';
        rec.market_phone = (beraterCSBIndex[csb] && beraterCSBIndex[csb].telefon) ? 
          beraterCSBIndex[csb].telefon : '';
        rec.market_email = (beraterCSBIndex[csb] && beraterCSBIndex[csb].email) ? 
          beraterCSBIndex[csb].email : '';
        map.set(csb, rec);
      }
      map.get(csb).touren.push({ tournummer: tourN, liefertag: k.liefertag });
    });
  }
  allCustomers = Array.from(map.values());
  buildSearchSuggestions();
}

// Previous query management
function pushPrevQuery() { 
  const v = $('#smartSearch').value.trim(); 
  if (v) { 
    prevQuery = v; 
    $('#btnBack').style.display = 'inline-block'; 
  } 
}

function popPrevQuery() { 
  if (prevQuery) { 
    $('#smartSearch').value = prevQuery; 
    prevQuery = null; 
    $('#btnBack').style.display = 'none'; 
    onSmart(); 
  } 
}

// Chip creation functions
function makePhoneChip(label, num, cls) {
  if (!num) return null;
  const a = document.createElement('a');
  a.className = 'phone-chip ' + cls;
  a.href = `${DIAL_SCHEME}:${sanitizePhone(num)}`;
  a.append(
    el('span', 'chip-tag', label), 
    el('span', 'mono', ' ' + num)
  );
  return a;
}

function makeMailChip(label, addr) {
  if (!addr) return null;
  const a = document.createElement('a');
  a.className = 'mail-chip';
  a.href = `mailto:${addr}`;
  const txt = document.createElement('span'); 
  txt.className = 'txt mono'; 
  txt.textContent = ' ' + addr;
  a.append(el('span', 'chip-tag', label), txt);
  return a;
}

function makeIdChip(label, value) {
  const a = document.createElement('a'); 
  a.className = 'id-chip'; 
  a.href = 'javascript:void(0)'; 
  a.title = label + ' ' + value + ' suchen';
  a.addEventListener('click', () => { 
    pushPrevQuery(); 
    $('#smartSearch').value = value; 
    onSmart(); 
  });
  a.append(
    el('span', 'id-tag', label), 
    el('span', 'mono', ' ' + value)
  ); 
  return a;
}

function makeAddressChip(name, strasse, plz, ort) {
  const txt = `${strasse || ''}, ${plz || ''} ${ort || ''}`.replace(/^,\\s*/, '').trim();
  const url = 'https://www.google.com/maps/search/?api=1&query=' + 
    encodeURIComponent(`${name || ''}, ${txt}`);
  const a = document.createElement('a'); 
  a.className = 'addr-chip'; 
  a.href = url; 
  a.target = '_blank'; 
  a.title = 'Adresse in Google Maps öffnen';
  
  const txtSpan = document.createElement('span');
  txtSpan.className = 'txt';
  txtSpan.textContent = ' ' + txt;
  
  a.append(
    el('span', 'addr-dot', ''), 
    el('span', 'chip-tag', 'Adresse'), 
    txtSpan
  );
  return a;
}

// Table row creation
function rowFor(k) {
  const tr = document.createElement('tr');
  const csb = k.csb_nummer || '-', sap = k.sap_nummer || '-', plz = k.postleitzahl || '-';

  // CSB/SAP Column
  const td1 = document.createElement('td');
  td1.setAttribute('data-label', 'CSB / SAP');
  const c1 = el('div', 'cell');
  const l1 = el('div', 'cell-top'); 
  l1.appendChild(makeIdChip('CSB', csb));
  const l2 = el('div', 'cell-sub'); 
  l2.appendChild(makeIdChip('SAP', sap));
  c1.append(l1, l2); 
  td1.append(c1); 
  tr.append(td1);

  // Name/Address Column
  const td2 = document.createElement('td');
  td2.setAttribute('data-label', 'Name / Adresse');
  const c2 = el('div', 'cell');
  c2.append(el('div', 'cell-top', k.name || '-'));
  const addrPill = makeAddressChip(k.name || '', k.strasse || '', plz, k.ort || '');
  const line2 = el('div', 'cell-sub'); 
  line2.appendChild(addrPill);
  c2.append(line2);
  td2.append(c2); 
  tr.append(td2);

  // Tours Column
  const td3 = document.createElement('td');
  td3.setAttribute('data-label', 'Touren');
  const c3 = el('div', 'cell'); 
  const tours = el('div', 'tour-inline');
  (k.touren || []).forEach(t => { 
    const tnum = (t.tournummer || ''); 
    const b = el('span', 'tour-btn', tnum + ' (' + t.liefertag.substring(0, 2) + ')'); 
    b.title = 'Tour ' + tnum; 
    b.onclick = () => { 
      pushPrevQuery(); 
      $('#smartSearch').value = tnum; 
      onSmart(); 
    }; 
    tours.appendChild(b); 
  });
  c3.appendChild(tours); 
  td3.appendChild(c3); 
  tr.append(td3);

  // Key Column
  const td4 = document.createElement('td');
  td4.setAttribute('data-label', 'Schlüssel');
  const key = (k.schluessel || '') || (keyIndex[csb] || '');
  td4.appendChild(key ? el('span', 'badge-key', key) : el('span', '', '-')); 
  tr.append(td4);

  // Contact Column
  const td5 = document.createElement('td');
  td5.setAttribute('data-label', 'Kontakt');
  const col = el('div', 'phone-col');
  const fbPhone = k.fb_phone;
  const fbMail = k.fachberater ? fbEmailFromName(k.fachberater) : '';
  const mkPhone = k.market_phone;
  const mkMail = k.market_email || '';
  
  const p1 = makePhoneChip('FB', fbPhone, 'chip-fb');      
  if (p1) col.appendChild(p1);
  const m1 = makeMailChip('FB Mail', fbMail);              
  if (m1) col.appendChild(m1);
  const p2 = makePhoneChip('Markt', mkPhone, 'chip-market');
  if (p2) col.appendChild(p2);
  const m2 = makeMailChip('Mail', mkMail);                 
  if (m2) col.appendChild(m2);
  
  if (!col.childNodes.length) col.textContent = '-';
  td5.appendChild(col); 
  tr.append(td5);

  return tr;
}

// Table rendering with performance optimization
function renderTable(list) {
  const body = $('#tableBody');
  const container = $('#tableContainer');
  const emptyState = $('#emptyState');
  const resultsHeader = $('#resultsHeader');
  const resultsCount = $('#resultsCount');
  
  currentResults = list;
  body.innerHTML = '';
  
  if (list.length === 0) {
    container.style.display = 'none';
    resultsHeader.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }
  
  // Update results count
  resultsCount.textContent = `${list.length} ${list.length === 1 ? 'Kunde' : 'Kunden'} gefunden`;
  resultsHeader.style.display = 'flex';
  emptyState.style.display = 'none';
  
  // Virtual scrolling for large datasets
  if (list.length > 100) {
    renderVirtualTable(list);
  } else {
    list.forEach(k => body.appendChild(rowFor(k)));
  }
  
  container.style.display = 'block';
}

// Virtual table rendering for performance
function renderVirtualTable(list) {
  const body = $('#tableBody');
  const BATCH_SIZE = 50;
  let rendered = 0;
  
  function renderBatch() {
    const batch = list.slice(rendered, rendered + BATCH_SIZE);
    batch.forEach(k => body.appendChild(rowFor(k)));
    rendered += BATCH_SIZE;
    
    if (rendered < list.length) {
      requestAnimationFrame(renderBatch);
    }
  }
  
  renderBatch();
}

// Tour banner rendering
function renderTourTop(list, query, isExact) {
  const wrap = $('#tourWrap'), title = $('#tourTitle'), extra = $('#tourExtra');
  
  if (!list.length) { 
    wrap.style.display = 'none'; 
    title.textContent = ''; 
    extra.textContent = ''; 
    return; 
  }
  
  if (query.startsWith('Schluessel ')) { 
    const key = query.replace(/^Schluessel\\s+/, ''); 
    title.textContent = '🔑 Schlüssel ' + key + ' — ' + list.length + ' ' + 
      (list.length === 1 ? 'Kunde' : 'Kunden'); 
  } else { 
    title.textContent = '🚛 ' + (isExact ? ('Tour ' + query) : ('Tour-Prefix ' + query + '*')) + 
      ' — ' + list.length + ' ' + (list.length === 1 ? 'Kunde' : 'Kunden'); 
  }
  
  const dayCount = {}; 
  list.forEach(k => (k.touren || []).forEach(t => { 
    const tnum = t.tournummer || ''; 
    const cond = isExact ? (tnum === query) : tnum.startsWith(query.replace('Schluessel ', '')); 
    if (cond || query.startsWith('Schluessel ')) { 
      dayCount[t.liefertag] = (dayCount[t.liefertag] || 0) + 1; 
    }
  }));
  
  extra.textContent = Object.entries(dayCount).sort()
    .map(([d, c]) => d + ': ' + c).join('  •  ');
  wrap.style.display = 'block';
}

function closeTourTop() { 
  $('#tourWrap').style.display = 'none'; 
  $('#tourTitle').textContent = ''; 
  $('#tourExtra').textContent = ''; 
}

// Search functions
function onSmart() {
  const qRaw = $('#smartSearch').value.trim(); 
  closeTourTop(); 
  
  if (!qRaw) { 
    renderTable([]); 
    return; 
  }
  
  // Tour searches
  if (/^\\d{1,3}$/.test(qRaw)) { 
    const n = qRaw.replace(/^0+(\\d)/, '$1'); 
    const r = allCustomers.filter(k => (k.touren || [])
      .some(t => (t.tournummer || '').startsWith(n))); 
    renderTourTop(r, n, false); 
    renderTable(r); 
    return; 
  }
  
  if (/^\\d{4}$/.test(qRaw)) {
    const n = qRaw.replace(/^0+(\\d)/, '$1'); 
    const tr = allCustomers.filter(k => (k.touren || [])
      .some(t => (t.tournummer || '') === n)); 
    const cr = allCustomers.filter(k => (k.csb_nummer || '') === n); 
    const r = dedupByCSB([...tr, ...cr]);
    if (tr.length) renderTourTop(tr, n, true); 
    else closeTourTop(); 
    renderTable(r); 
    return;
  }
  
  // General search
  const q = normDE(qRaw);
  const r = allCustomers.filter(k => { 
    const fb = k.fachberater || ''; 
    const text = (k.name + ' ' + k.strasse + ' ' + k.ort + ' ' + k.csb_nummer + ' ' + 
      k.sap_nummer + ' ' + fb + ' ' + (k.schluessel || '') + ' ' + (k.fb_phone || '') + ' ' + 
      (k.market_phone || '') + ' ' + (k.market_email || '')); 
    return normDE(text).includes(q); 
  });
  
  renderTable(r);
}

function onKey() {
  const q = $('#keySearch').value.trim(); 
  closeTourTop(); 
  
  if (!q) { 
    renderTable([]); 
    return; 
  }
  
  const n = q.replace(/[^0-9]/g, '').replace(/^0+(\\d)/, '$1'); 
  const r = []; 
  
  for (const k of allCustomers) { 
    const key = (k.schluessel || '') || (keyIndex[k.csb_nummer] || ''); 
    if (key === n) r.push(k); 
  }
  
  if (r.length) renderTourTop(r, 'Schluessel ' + n, true); 
  renderTable(r);
}

// Utility functions
function debounce(fn, d = 200) { 
  let t; 
  return (...a) => { 
    clearTimeout(t); 
    t = setTimeout(() => fn(...a), d); 
  }; 
}

// Export functions
function exportResults() {
  if (!currentResults.length) return;
  
  const csv = [
    ['CSB', 'SAP', 'Name', 'Straße', 'PLZ', 'Ort', 'Fachberater', 'Tour', 'Schlüssel'].join(';')
  ];
  
  currentResults.forEach(customer => {
    const tours = customer.touren?.map(t => t.tournummer).join(',') || '';
    csv.push([
      customer.csb_nummer || '',
      customer.sap_nummer || '',
      customer.name || '',
      customer.strasse || '',
      customer.postleitzahl || '',
      customer.ort || '',
      customer.fachberater || '',
      tours,
      customer.schluessel || ''
    ].join(';'));
  });
  
  const blob = new Blob([csv.join('\\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'kunden_export.csv';
  a.click();
  URL.revokeObjectURL(url);
}

function printResults() {
  window.print();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Cmd/Ctrl + K for search focus
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    $('#smartSearch').focus();
  }
  
  // Escape to clear search
  if (e.key === 'Escape') {
    $('#smartSearch').value = '';
    $('#keySearch').value = '';
    closeTourTop();
    renderTable([]);
    $$('.search-suggestions').forEach(el => el.style.display = 'none');
  }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  if (Object.keys(tourkundenData).length > 0) { 
    buildData(); 
  }
  
  // Search event listeners
  $('#smartSearch').addEventListener('input', debounce((e) => {
    onSmart();
    showSuggestions(e.target.value, 'smartSearch');
  }, 200));
  
  $('#keySearch').addEventListener('input', debounce((e) => {
    onKey();
    showSuggestions(e.target.value, 'keySearch');
  }, 200));
  
  // Clear button listeners
  $('#clearSmart').addEventListener('click', () => {
    $('#smartSearch').value = '';
    closeTourTop();
    renderTable([]);
    $$('.search-suggestions').forEach(el => el.style.display = 'none');
  });
  
  $('#clearKey').addEventListener('click', () => {
    $('#keySearch').value = '';
    closeTourTop();
    renderTable([]);
  });
  
  // Control button listeners
  $('#btnReset').addEventListener('click', () => { 
    $('#smartSearch').value = ''; 
    $('#keySearch').value = ''; 
    closeTourTop(); 
    renderTable([]); 
    prevQuery = null; 
    $('#btnBack').style.display = 'none';
    $$('.search-suggestions').forEach(el => el.style.display = 'none');
  });
  
  $('#btnBack').addEventListener('click', () => { 
    popPrevQuery(); 
  });
  
  // Show/hide clear buttons based on input content
  ['smartSearch', 'keySearch'].forEach(id => {
    const input = $(`#${id}`);
    const clearBtn = $(`#clear${id.replace('Search', '').replace('smart', 'Smart').replace('key', 'Key')}`);
    
    input.addEventListener('input', () => {
      clearBtn.style.display = input.value ? 'block' : 'none';
    });
  });
});
</script>
</body>
</html>
"""

# ===== Streamlit-Wrapper =====
st.set_page_config(
    page_title="Verbesserte Kunden-Suche",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Kunden-Suche – Tech-Lab Premium")
st.caption("Erweiterte Features: Intelligente Suche • Auto-Vervollständigung • Export • Responsive Design • Keyboard Shortcuts")

# Upload section with improved layout
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Datenquellen")
        excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"], key="excel")
        key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"], key="keys")
        berater_file = st.file_uploader("OPTIONAL: Fachberater-Telefonliste (A=Vorname, B=Nachname, C=Nummer)", type=["xlsx"], key="berater")
    
    with col2:
        st.subheader("🎨 Anpassung")
        logo_file = st.file_uploader("Logo (PNG/JPG)", type=["png","jpg","jpeg"], key="logo")
        berater_csb_file = st.file_uploader("Fachberater–CSB-Zuordnung (A=Fachberater, I=CSB, O=Markt-Tel, X=Markt-Mail)", type=["xlsx"], key="berater_csb")

# Helper functions (same as before but with improved error handling)
def normalize_digits_py(v) -> str:
    if pd.isna(v): return ""
    s = str(v).strip().replace(".0","")
    s = "".join(ch for ch in s if ch.isdigit())
    if not s: return ""
    s = s.lstrip("0")
    return s if s else "0"

def norm_de_py(s: str) -> str:
    if not s: return ""
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
        st.warning(f"⚠️ Schlüsseldatei hat nur {df.shape[1]} Spalten – nehme letzte vorhandene Spalte als Schlüssel.")
    csb_col = 0
    key_col = 5 if df.shape[1] > 5 else df.shape[1] - 1
    out = {}
    for _, row in df.iterrows():
        csb = normalize_digits_py(row.iloc[csb_col] if df.shape[1] > 0 else "")
        key = normalize_digits_py(row.iloc[key_col] if df.shape[1] > 0 else "")
        if csb: out[csb] = key
    return out

def build_berater_map(df: pd.DataFrame) -> dict:
    out = {}
    for _, row in df.iterrows():
        v = ("" if df.shape[1] < 1 or pd.isna(row.iloc[0]) else str(row.iloc[0])).strip()
        n = ("" if df.shape[1] < 2 or pd.isna(row.iloc[1]) else str(row.iloc[1])).strip()
        t = ("" if df.shape[1] < 3 or pd.isna(row.iloc[2]) else str(row.iloc[2])).strip()
        if not t: continue
        k1 = norm_de_py(f"{v} {n}")
        k2 = norm_de_py(f"{n} {v}")
        for k in {k1, k2}:
            if k and k not in out:
                out[k] = t
    return out

def build_berater_csb_map(df: pd.DataFrame) -> dict:
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

# Processing
if excel_file and key_file:
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    if st.button("🚀 Erweiterte HTML-Anwendung erstellen", type="primary", use_container_width=True):
        if logo_file is None:
            st.error("❌ Bitte Logo (PNG/JPG) hochladen.")
            st.stop()
            
        try:
            status_text.text("📋 Bereite Logo vor...")
            progress_bar.progress(10)
            logo_data_url = to_data_url(logo_file)

            BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
            SPALTEN_MAPPING = {
                "csb_nummer":"Nr","sap_nummer":"SAP-Nr.","name":"Name","strasse":"Strasse",
                "postleitzahl":"Plz","ort":"Ort","fachberater":"Fachberater"
            }
            LIEFERTAGE_MAPPING = {"Montag":"Mo","Dienstag":"Die","Mittwoch":"Mitt","Donnerstag":"Don","Freitag":"Fr","Samstag":"Sam"}

            status_text.text("🔑 Verarbeite Schlüsseldatei...")
            progress_bar.progress(20)
            key_df = pd.read_excel(key_file, sheet_name=0, header=0)
            if key_df.shape[1] < 2:
                key_file.seek(0)
                key_df = pd.read_excel(key_file, sheet_name=0, header=None)
            key_map = build_key_map(key_df)

            berater_map = {}
            if berater_file is not None:
                status_text.text("📞 Verarbeite Fachberater-Telefonliste...")
                progress_bar.progress(30)
                berater_file.seek(0)
                bf = pd.read_excel(berater_file, sheet_name=0, header=None)
                bf = bf.rename(columns={0:"Vorname",1:"Nachname",2:"Nummer"}).dropna(how="all")
                berater_map = build_berater_map(bf)

            berater_csb_map = {}
            if berater_csb_file is not None:
                status_text.text("🔗 Verarbeite Fachberater–CSB-Zuordnung...")
                progress_bar.progress(40)
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
                        if spaltenname not in df.columns: continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit(): continue
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

            status_text.text("📊 Verarbeite Kundendatei...")
            progress_bar.progress(60)
            
            processed_sheets = 0
            for blatt in BLATTNAMEN:
                try:
                    df = pd.read_excel(excel_file, sheet_name=blatt)
                    kunden_sammeln(df)
                    processed_sheets += 1
                    status_text.text(f"📊 Verarbeitet: {blatt}")
                except ValueError:
                    pass

            if not tour_dict:
                st.error("❌ Keine gültigen Kundendaten gefunden.")
                st.stop()

            status_text.text("🔄 Sortiere und optimiere Daten...")
            progress_bar.progress(80)
            sorted_tours = dict(sorted(tour_dict.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0))

            status_text.text("🏗️ Erstelle HTML-Anwendung...")
            progress_bar.progress(90)
            
            final_html = (HTML_TEMPLATE
              .replace("const tourkundenData   = {  }", f"const tourkundenData   = {json.dumps(sorted_tours, ensure_ascii=False)}")
              .replace("const keyIndex         = {  }", f"const keyIndex         = {json.dumps(key_map, ensure_ascii=False)}")
              .replace("const beraterIndex     = {  }", f"const beraterIndex     = {json.dumps(berater_map, ensure_ascii=False)}")
              .replace("const beraterCSBIndex  = {  }", f"const beraterCSBIndex  = {json.dumps(berater_csb_map, ensure_ascii=False)}")
              .replace("__LOGO_DATA_URL__", logo_data_url)
            )

            progress_bar.progress(100)
            status_text.text("✅ Erfolgreich erstellt!")

            # Statistics
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            unique_customers = len(set(k.get('csb_nummer') for customers in sorted_tours.values() for k in customers if k.get('csb_nummer')))
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Touren", len(sorted_tours))
            with col2:
                st.metric("Kunden (total)", total_customers)
            with col3:
                st.metric("Kunden (unique)", unique_customers)
            with col4:
                st.metric("Verarbeitete Blätter", processed_sheets)

            st.success("🎉 Erweiterte HTML-Anwendung erfolgreich erstellt!")
            
            # Feature overview
            with st.expander("🚀 Neue Features in dieser Version"):
                st.markdown("""
                **🔍 Erweiterte Suche:**
                - Auto-Vervollständigung mit Kategorien
                - Intelligente Suchvorschläge
                - Keyboard-Shortcuts (Cmd/Ctrl+K, ESC)
                
                **📱 Bessere UX:**
                - Vollständig responsive Design
                - Moderne Micro-Animations
                - Verbesserte Touch-Bedienung
                - Performance-Optimierungen
                
                **📊 Export & Tools:**
                - CSV-Export Funktion
                - Drucken-Option
                - Ergebnis-Counter
                - Clear-Buttons für Inputs
                
                **🎨 Design-Verbesserungen:**
                - Modernere Farbpalette
                - Bessere Typography
                - Verbesserte Accessibility
                - Smooth Transitions
                """)

            st.download_button(
                "📥 Erweiterte HTML-Anwendung herunterladen",
                data=final_html.encode("utf-8"),
                file_name="kunden_suche_premium.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Fehler beim Verarbeiten: {str(e)}")
            st.exception(e)
        finally:
            progress_bar.empty()
            status_text.empty()
else:
    st.info("💡 Bitte laden Sie mindestens die Quelldatei, Schlüsseldatei und ein Logo hoch, um zu beginnen.")
    
    with st.expander("📖 Anleitung"):
        st.markdown("""
        **Erforderliche Dateien:**
        - **Quelldatei (Excel):** Kundendaten mit den Blättern 'Direkt 1 - 99', 'Hupa MK 882', 'Hupa 2221-4444', 'Hupa 7773-7779'
        - **Schlüsseldatei (Excel):** CSB-Nummern in Spalte A, Schlüssel in Spalte F
        - **Logo (PNG/JPG):** Ihr Unternehmenslogo
        
        **Optionale Dateien:**
        - **Fachberater-Telefonliste:** Vorname (A), Nachname (B), Telefonnummer (C)
        - **Fachberater-CSB-Zuordnung:** Fachberater (A), CSB (I), Markt-Tel (O), Markt-Mail (X)
        """)
