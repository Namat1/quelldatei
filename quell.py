// Modal Event Listeners
    closeTourResult.addEventListener('click', () => {
        tourResultOverlay.classList.remove('show');
        document.body.style.overflow = 'auto';
    });

    tourResultOverlay.addEventListener('click', (e) => {
        if (e.target === tourResultOverlay) {
            tourResultOverlay.classList.remove('show');
            document.body.style.overflow = 'auto';
        }import streamlit as st
import pandas as pd
import json

# --- Fancy Minimal HTML mit fester Tour-Übersicht ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Kunden-Suche</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --ral-1021: #F3DA0B;
            --ral-5010: #0E294B;
            --ral-1021-light: #F8E555;
            --ral-5010-light: #1E3A5F;
            --ral-1021-soft: rgba(243, 218, 11, 0.1);
            --ral-5010-soft: rgba(14, 41, 75, 0.05);
            --background: #fafbfc;
            --surface: #ffffff;
            --surface-alt: #f8f9fa;
            --border: #e1e5e9;
            --text-primary: #2c3e50;
            --text-secondary: #546e7a;
            --text-muted: #78909c;
            --shadow: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-hover: 0 4px 12px rgba(0,0,0,0.15);
            --glow: 0 0 20px rgba(243, 218, 11, 0.3);
        }

        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: var(--text-primary);
            line-height: 1.4;
            font-size: 14px;
            overflow-x: hidden;
        }

        .container { 
            max-width: 1600px; 
            margin: 0 auto;
            padding: 8px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: linear-gradient(135deg, var(--ral-5010) 0%, var(--ral-5010-light) 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 8px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(180deg); }
        }

        .header h1 { 
            font-size: 1.4rem; 
            font-weight: 700; 
            margin-bottom: 2px;
            position: relative;
            z-index: 1;
        }

        .header p {
            font-size: 0.85rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        .search-bar {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .search-bar:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-1px);
        }

        .search-input-row {
            display: flex;
            gap: 6px;
            margin-bottom: 6px;
        }

        input[type="text"] { 
            flex: 1;
            padding: 8px 12px; 
            border: 2px solid var(--border); 
            border-radius: 6px; 
            font-size: 13px;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: var(--ral-1021); 
            box-shadow: var(--glow);
            transform: scale(1.01);
        }

        .btn-group {
            display: flex;
            gap: 4px;
        }

        button { 
            padding: 8px 12px; 
            font-size: 12px; 
            font-weight: 600; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255,255,255,0.3);
            border-radius: 50%;
            transition: all 0.3s ease;
            transform: translate(-50%, -50%);
        }

        button:hover::before {
            width: 100px;
            height: 100px;
        }

        #resetBtn { 
            background: linear-gradient(135deg, var(--text-muted) 0%, var(--text-secondary) 100%); 
            color: white; 
        } 
        #resetBtn:hover { 
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        #backBtn { 
            display: none; 
            background: linear-gradient(135deg, var(--ral-1021) 0%, var(--ral-1021-light) 100%); 
            color: var(--ral-5010); 
            font-weight: 700;
        } 
        #backBtn:hover { 
            transform: translateY(-2px) scale(1.05);
            box-shadow: var(--glow);
        }

        .stats { 
            font-size: 11px; 
            color: var(--text-secondary); 
            margin-top: 2px;
            font-weight: 500;
        }

        .content-area {
            flex: 1;
            display: flex;
            gap: 8px;
            min-height: 0;
        }

        .sidebar {
            width: 320px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .main-content {
            flex: 1;
            min-height: 0;
        }

        .info-box { 
            background: var(--surface); 
            border: 1px solid var(--border); 
            border-radius: 8px; 
            overflow: hidden;
            box-shadow: var(--shadow);
            display: none;
            flex-direction: column;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .info-box:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-1px);
        }

        .info-box.show {
            display: flex;
        }

        .info-header { 
            padding: 8px 12px; 
            font-weight: 700; 
            font-size: 12px; 
            background: linear-gradient(135deg, var(--ral-5010-soft) 0%, var(--surface-alt) 100%); 
            border-bottom: 1px solid var(--border);
            color: var(--ral-5010);
            position: relative;
        }

        .info-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--ral-1021) 0%, transparent 100%);
        }

        .tour-overview {
            height: 280px;
            overflow: hidden;
            padding: 8px;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
        }

        .tour-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 4px;
            height: 100%;
        }

        .tour-item {
            background: linear-gradient(135deg, var(--surface) 0%, var(--ral-5010-soft) 100%);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .tour-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(243, 218, 11, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .tour-item:hover::before {
            left: 100%;
        }

        .tour-item:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: var(--glow);
            border-color: var(--ral-1021);
        }

        .tour-number {
            font-weight: 700;
            font-size: 13px;
            color: var(--ral-5010);
            margin-bottom: 2px;
        }

        .tour-day {
            font-size: 10px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .fachberater-content {
            max-height: 300px;
            overflow-y: auto;
            padding: 4px;
        }

        .list-item { 
            padding: 3px 0; 
            border-bottom: 1px solid #f5f5f5; 
        }

        .list-item:last-child {
            border-bottom: none;
        }

        .list-row { 
            display: grid; 
            grid-template-columns: 60px 100px 1fr auto; 
            align-items: center; 
            gap: 6px; 
            padding: 4px 8px; 
            font-size: 11px;
            border-radius: 4px;
            transition: all 0.2s ease;
        }

        .list-row:hover {
            background: linear-gradient(135deg, var(--ral-1021-soft) 0%, var(--surface-alt) 100%);
            transform: translateX(2px);
        }

        .csb-link { 
            font-weight: 700; 
            color: var(--ral-5010); 
            cursor: pointer; 
            text-decoration: none;
            padding: 2px 4px;
            border-radius: 3px;
            transition: all 0.2s ease;
        }

        .csb-link:hover {
            background: var(--ral-5010);
            color: white;
            transform: scale(1.1);
        }

        .key-info { 
            font-size: 10px;
            color: var(--text-muted); 
            font-weight: 500;
        }

        .location { 
            font-weight: 600; 
            color: var(--text-primary); 
        }

        .maps-link { 
            padding: 2px 6px;
            background: linear-gradient(135deg, var(--ral-1021) 0%, var(--ral-1021-light) 100%);
            color: var(--ral-5010);
            text-decoration: none;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
            transition: all 0.2s ease;
        }

        .maps-link:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 8px rgba(243, 218, 11, 0.4);
        }

        #results { 
            height: calc(100vh - 120px);
            overflow-y: auto;
            padding-right: 4px;
        }

        .customer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 6px;
            padding: 4px;
        }

        .customer-card { 
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%); 
            border: 1px solid var(--border); 
            border-radius: 8px; 
            box-shadow: var(--shadow); 
            transition: all 0.3s ease;
            height: fit-content;
            position: relative;
            overflow: hidden;
        }

        .customer-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--ral-1021) 0%, var(--ral-5010) 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .customer-card:hover::before {
            transform: scaleX(1);
        }

        .customer-card:hover { 
            transform: translateY(-3px) scale(1.02); 
            box-shadow: var(--shadow-hover); 
        }

        .customer-card.highlighted { 
            border-color: var(--ral-1021); 
            background: linear-gradient(135deg, var(--ral-1021-soft) 0%, var(--surface) 100%);
            box-shadow: var(--glow);
        }

        .customer-card.highlighted::before {
            transform: scaleX(1);
        }

        .card-header {
            padding: 8px 10px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(135deg, var(--surface-alt) 0%, var(--surface) 100%);
        }

        .card-title { 
            font-size: 13px; 
            font-weight: 700; 
            color: var(--ral-5010);
            margin-bottom: 1px;
        }

        .card-subtitle {
            font-size: 10px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .card-body {
            padding: 8px 10px;
        }

        .card-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 6px;
            font-size: 11px;
        }

        .card-row:last-child {
            margin-bottom: 0;
        }

        .info-item {
            color: var(--text-secondary);
        }

        .info-label {
            font-weight: 600;
            color: var(--ral-5010);
        }

        .tours-section {
            margin-top: 6px;
            padding-top: 6px;
            border-top: 1px solid var(--border);
        }

        .tours-title {
            font-size: 10px;
            font-weight: 700;
            color: var(--ral-5010);
            margin-bottom: 4px;
        }

        .tour-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 3px;
        }

        .tour-tag {
            background: linear-gradient(135deg, var(--ral-5010) 0%, var(--ral-5010-light) 100%);
            color: white;
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .tour-tag::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.3s ease;
        }

        .tour-tag:hover::before {
            left: 100%;
        }

        .tour-tag:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 8px rgba(14, 41, 75, 0.3);
        }

        .card-maps {
            margin-top: 6px;
        }

        .card-maps-btn {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            background: linear-gradient(135deg, var(--ral-1021) 0%, var(--ral-1021-light) 100%);
            color: var(--ral-5010);
            text-decoration: none;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
            transition: all 0.3s ease;
        }

        .card-maps-btn:hover {
            transform: scale(1.05);
            box-shadow: var(--glow);
        }

        .hidden { 
            display: none !important; 
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 4px;
        }

        ::-webkit-scrollbar-track {
            background: var(--surface-alt);
            border-radius: 2px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--ral-1021) 0%, var(--ral-5010) 100%);
            border-radius: 2px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--ral-5010) 0%, var(--ral-1021) 100%);
        }

        /* Mobile */
        @media(max-width: 768px) {
            .container { 
                padding: 6px; 
            }
            
            .content-area {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                order: 2;
            }
            
            .customer-grid {
                grid-template-columns: 1fr;
            }
            
            .search-input-row {
                flex-direction: column;
            }
            
            .btn-group {
                flex-wrap: wrap;
            }
            
            button {
                flex: 1;
                min-width: 100px;
            }

            .tour-grid {
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Kunden-Suche</h1>
            <p>Intelligente Übersicht mit Stil</p>
        </div>
        
        <div class="search-bar">
            <div class="search-input-row">
                <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße...">
                <div class="btn-group">
                    <button id="resetBtn">🔄 Reset</button>
                    <button id="backBtn">⬅️ Zurück</button>
                </div>
            </div>
            <div class="stats" id="trefferInfo">🔎 0 Ergebnisse</div>
        </div>

        <div class="content-area">
            <div class="sidebar">
                <div id="tourBox" class="info-box">
                    <div class="info-header">
                        🚚 Tour <span id="tourNumSpan"></span>
                    </div>
                    <div class="tour-overview" id="tourOverview"></div>
                </div>
                
                <div id="fachberaterBox" class="info-box">
                    <div class="info-header">
                        👤 <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span>)
                    </div>
                    <div class="fachberater-content" id="fachberaterList"></div>
                </div>
            </div>

            <div class="main-content">
                <div id="results">
                    <div class="customer-grid" id="customerGrid"></div>
                </div>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

const buildCustomerCard = kunde => {
    const card = el('div', 'customer-card hidden');
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${(kunde.schluessel||'')} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    const header = el('div', 'card-header');
    const title = el('div', 'card-title', '🏪 ' + kunde.name);
    const subtitle = el('div', 'card-subtitle', kunde.schluessel ? `Schlüssel: ${kunde.schluessel}` : 'Kein Schlüssel');
    header.append(title, subtitle);

    const body = el('div', 'card-body');
    
    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';

    const row1 = el('div', 'card-row');
    row1.innerHTML = `<div class="info-item"><span class="info-label">CSB:</span> ${csb}</div><div class="info-item"><span class="info-label">SAP:</span> ${sap}</div>`;
    
    const row2 = el('div', 'card-row');
    row2.innerHTML = `<div class="info-item"><span class="info-label">Ort:</span> ${kunde.ort}</div><div class="info-item"><span class="info-label">PLZ:</span> ${plz}</div>`;
    
    const row3 = el('div', 'card-row');
    row3.innerHTML = `<div class="info-item" style="grid-column: 1/-1;"><span class="info-label">Straße:</span> ${kunde.strasse}</div>`;
    
    const row4 = el('div', 'card-row');
    row4.innerHTML = `<div class="info-item" style="grid-column: 1/-1;"><span class="info-label">Fachberater:</span> ${kunde.fachberater}</div>`;

    const toursSection = el('div', 'tours-section');
    const toursTitle = el('div', 'tours-title', '🚛 Touren:');
    const tourTags = el('div', 'tour-tags');
    
    kunde.touren.forEach(t => {
        const tag = el('span', 'tour-tag', `${t.tournummer} (${t.liefertag})`);
        tag.addEventListener('click', () => {
            $('#globalSearch').value = t.tournummer;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            $('#backBtn').style.display = 'inline-block';
        });
        tourTags.appendChild(tag);
    });
    
    toursSection.append(toursTitle, tourTags);

    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;
    const mapsDiv = el('div', 'card-maps');
    const mapsBtn = el('a', 'card-maps-btn', '📍 Maps');
    mapsBtn.href = mapsUrl;
    mapsBtn.target = '_blank';
    mapsDiv.appendChild(mapsBtn);

    body.append(row1, row2, row3, row4, toursSection, mapsDiv);
    card.append(header, body);

    return card;
};

const buildTourGrid = touren => {
    const grid = el('div', 'tour-grid');
    
    touren.forEach(t => {
        const item = el('div', 'tour-item');
        const number = el('div', 'tour-number', t.tournummer);
        const day = el('div', 'tour-day', t.liefertag);
        
        item.addEventListener('click', () => {
            $('#globalSearch').value = t.tournummer;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            $('#backBtn').style.display = 'inline-block';
        });
        
        item.append(number, day);
        grid.appendChild(item);
    });
    
    return grid;
};

const buildListEntry = (ort, name, strasse, csbNummer, schluessel, mapsUrl, isAlt) => {
    const item = el('div', 'list-item' + (isAlt ? ' alt' : ''));
    const row = el('div', 'list-row');

    const csbDiv = el('div', 'csb-link', csbNummer);
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        $('#backBtn').style.display = 'inline-block';
    });

    const keyDiv = el('div', 'key-info', schluessel ? `S: ${schluessel}` : 'S: -');
    const nameDiv = el('div', 'location', name.substring(0, 20) + (name.length > 20 ? '...' : ''));
    
    const linkDiv = el('div');
    const link = el('a', 'maps-link', '📍');
    link.href = mapsUrl;
    link.target = '_blank';
    linkDiv.appendChild(link);

    row.append(csbDiv, keyDiv, nameDiv, linkDiv);
    item.appendChild(row);
    return item;
};

// Main
let lastTourSearchQuery = '';
const results = $('#results');
const customerGrid = $('#customerGrid');
const treffer = $('#trefferInfo');
const kundenMap = new Map();

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
        });
    }

    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        customerGrid.appendChild(card);
    });

    const input = $('#globalSearch');
    const tourBox = $('#tourBox');
    const tourOverview = $('#tourOverview');
    const tourNumLbl = $('#tourNumSpan');
    const fachberaterBox = $('#fachberaterBox');
    const fachberaterList = $('#fachberaterList');
    const fachberaterNameSpan = $('#fachberaterNameSpan');
    const fachberaterCountSpan = $('#fachberaterCountSpan');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.classList.remove('show');
        fachberaterBox.classList.remove('show');

        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const list = [];
            const tourData = [];
            
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', mapsUrl });
                    
                    k.touren.forEach(t => {
                        if (t.tournummer === tourN && !tourData.some(td => td.tournummer === t.tournummer && td.liefertag === t.liefertag)) {
                            tourData.push({ tournummer: t.tournummer, liefertag: t.liefertag });
                        }
                    });
                }
            });

            if (list.length > 0) {
                lastTourSearchQuery = tourN;
                tourOverview.innerHTML = '';
                tourNumLbl.textContent = `${tourN} (${list.length} Kunden)`;
                tourOverview.appendChild(buildTourGrid(tourData));
                tourBox.classList.add('show');
            }
        }

        const matchedFachberater = q.length > 2 ? alleFachberater.find(fb => fb.includes(q)) : null;
        if (matchedFachberater) {
            const kundenDesBeraters = [];
            let beraterName = '';
            kundenMap.forEach(k => {
                if (k.fachberater?.toLowerCase() === matchedFachberater) {
                    if (!beraterName) beraterName = k.fachberater;
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    kundenDesBeraters.push({ csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', name: k.name, ort: k.ort, strasse: k.strasse, mapsUrl });
                }
            });

            if (kundenDesBeraters.length > 0) {
                fachberaterNameSpan.textContent = beraterName;
                fachberaterCountSpan.textContent = kundenDesBeraters.length;
                fachberaterList.innerHTML = '';
                kundenDesBeraters.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    fachberaterList.appendChild(buildListEntry(kunde.ort, kunde.name, kunde.strasse, kunde.csb, kunde.schluessel, kunde.mapsUrl, i % 2 !== 0));
                });
                fachberaterBox.classList.add('show');
            }
        }

        document.querySelectorAll('.customer-card').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) { c.classList.add('highlighted'); hits++; }
            else { c.classList.remove('highlighted'); }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    });

    // Escape key to close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && tourResultOverlay.classList.contains('show')) {
            tourResultOverlay.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    });

    $('#backBtn').addEventListener('click', () => {
        if (lastTourSearchQuery) {
            input.value = lastTourSearchQuery;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            $('#backBtn').style.display = 'none';
        }
    });

    $('#resetBtn').addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        $('#backBtn').style.display = 'none';
        fachberaterBox.classList.remove('show');
        tourResultOverlay.classList.remove('show');
        document.body.style.overflow = 'auto';
    });
} else {
    customerGrid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><h3>❌ Keine Daten</h3><p>Kundendaten konnten nicht geladen werden.</p></div>';
}
</script>

</body>
</html>
"""

# --- UI Setup ---
st.title("🚛 Tour-Übersicht Kunden-Suchseite")
st.markdown("""
Laden Sie **zwei** Excel-Dateien hoch:
1) **Quelldatei** mit den Kundendaten (mehrere Blätter)  
2) **Schlüsseldatei** mit *CSB in Spalte A* und *Schlüsselnummer in Spalte F*

Erstellt eine **Tour-fokussierte HTML-Suchseite** mit zentraler Übersicht bei Tour-Eingabe.
""")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("📄 Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("🔑 Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x): return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", ".")); i = int(f)
        return str(i) if f == i else s
    except Exception:
        return s

def build_key_map(key_df: pd.DataFrame) -> dict:
    if key_df.shape[1] < 6:
        st.warning("⚠️ Schlüsseldatei hat weniger als 6 Spalten. Es werden die vorhandenen Spalten genutzt.")
    csb_col = 0
    key_col = 5 if key_df.shape[1] > 5 else key_df.shape[1] - 1
    mapping = {}
    for _, row in key_df.iterrows():
        csb = norm_str_num(row.iloc[csb_col] if key_df.shape[1] > 0 else "")
        schluessel_raw = row.iloc[key_col] if key_df.shape[1] > 0 else ""
        schluessel = "" if pd.isna(schluessel_raw) else str(schluessel_raw).strip()
        if csb:
            mapping[csb] = schluessel
    return mapping

if excel_file and key_file:
    if st.button("🎯 Tour-Übersicht HTML-Seite erzeugen", type="primary"):
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}

        try:
            with st.spinner("🔑 Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            tour_dict = {}
            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns: continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit(): continue
                        tournr = str(int(float(tournr_raw)))
                        eintrag = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean = norm_str_num(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        eintrag["schluessel"] = key_map.get(csb_clean, "")
                        eintrag["liefertag"] = tag
                        tour_dict.setdefault(tournr, []).append(eintrag)

            with st.spinner("📥 Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht gefunden.")

            if not tour_dict:
                st.error("❌ Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            st.success(f"🎯 Tour-Übersicht Seite erstellt! {len(sorted_tours)} Touren verarbeitet.")
            
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            st.info(f"📊 {len(sorted_tours)} Touren • {total_customers} Kunden • {len(key_map)} Schlüssel")
            
            st.download_button(
                "📥 Tour-Übersicht `suche.html` herunterladen", 
                data=final_html.encode("utf-8"), 
                file_name="suche.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"❌ Fehler: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("📁 Bitte noch die **Schlüsseldatei** hochladen.")
elif key_file and not excel_file:
    st.info("📁 Bitte noch die **Quelldatei** hochladen.")
else:
    st.info("📋 Bitte beide Dateien hochladen.")
    st.markdown("""
    ### 🎯 Tour-Übersicht Features:
    - **Zentrale Tour-Anzeige** bei Eingabe einer 4-stelligen Tournummer
    - **Vollbild-Overlay** mit scrollbarem Inhalt über allem anderen
    - **Detaillierte Kundenkarten** mit allen wichtigen Informationen
    - **Tour-Statistiken** mit Aufschlüsselung nach Liefertagen
    - **Direkte Aktionen** pro Kunde (Google Maps, Details anzeigen)
    - **Sortierte Darstellung** nach CSB-Nummern
    - **Responsive Design** mit eleganten Animationen
    - **ESC-Taste** oder Klick außerhalb schließt die Übersicht
    """)

} else {
    customerGrid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><h3>❌ Keine Daten</h3><p>Kundendaten konnten nicht geladen werden.</p></div>';
}
</script>

</body>
</html>
"""

# --- UI Setup ---
st.title("🚛 Fancy Minimale Kunden-Suchseite")
st.markdown("""
Laden Sie **zwei** Excel-Dateien hoch:
1) **Quelldatei** mit den Kundendaten (mehrere Blätter)  
2) **Schlüsseldatei** mit *CSB in Spalte A* und *Schlüsselnummer in Spalte F*.

Erstellt eine **fancy-minimale HTML-Suchseite** mit fester Tour-Übersicht und eleganten Animationen.
""")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("📄 Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("🔑 Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x): return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", ".")); i = int(f)
        return str(i) if f == i else s
    except Exception:
        return s

def build_key_map(key_df: pd.DataFrame) -> dict:
    if key_df.shape[1] < 6:
        st.warning("⚠️ Schlüsseldatei hat weniger als 6 Spalten. Es werden die vorhandenen Spalten genutzt.")
    csb_col = 0
    key_col = 5 if key_df.shape[1] > 5 else key_df.shape[1] - 1
    mapping = {}
    for _, row in key_df.iterrows():
        csb = norm_str_num(row.iloc[csb_col] if key_df.shape[1] > 0 else "")
        schluessel_raw = row.iloc[key_col] if key_df.shape[1] > 0 else ""
        schluessel = "" if pd.isna(schluessel_raw) else str(schluessel_raw).strip()
        if csb:
            mapping[csb] = schluessel
    return mapping

if excel_file and key_file:
    if st.button("✨ Fancy Minimale HTML-Seite erzeugen", type="primary"):
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}

        try:
            with st.spinner("🔑 Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            tour_dict = {}
            def kunden_sammeln(df: pd.DataFrame):
                for _, row in df.iterrows():
                    for tag, spaltenname in LIEFERTAGE_MAPPING.items():
                        if spaltenname not in df.columns: continue
                        tournr_raw = str(row[spaltenname]).strip()
                        if not tournr_raw or not tournr_raw.replace('.', '', 1).isdigit(): continue
                        tournr = str(int(float(tournr_raw)))
                        eintrag = {k: str(row.get(v, "")).strip() for k, v in SPALTEN_MAPPING.items()}
                        csb_clean = norm_str_num(row.get(SPALTEN_MAPPING["csb_nummer"], ""))
                        eintrag["schluessel"] = key_map.get(csb_clean, "")
                        eintrag["liefertag"] = tag
                        tour_dict.setdefault(tournr, []).append(eintrag)

            with st.spinner("📥 Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht gefunden.")

            if not tour_dict:
                st.error("❌ Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            st.success(f"✨ Fancy minimale Seite erstellt! {len(sorted_tours)} Touren verarbeitet.")
            
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            st.info(f"📊 {len(sorted_tours)} Touren • {total_customers} Kunden • {len(key_map)} Schlüssel")
            
            st.download_button(
                "📥 Fancy Minimale `suche.html` herunterladen", 
                data=final_html.encode("utf-8"), 
                file_name="suche.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"❌ Fehler: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("📁 Bitte noch die **Schlüsseldatei** hochladen.")
elif key_file and not excel_file:
    st.info("📁 Bitte noch die **Quelldatei** hochladen.")
else:
    st.info("📋 Bitte beide Dateien hochladen.")
    st.markdown("""
    ### ✨ Fancy Minimale Features:
    - **RAL 1021 & 5010** in dezenten Gradienten und Glows
    - **Feste Tour-Übersicht** (280px, kein Scrollen) mit Grid-Layout
    - **Animierte Hover-Effekte** und Micro-Interactions
    - **Shimmer-Animationen** im Header und bei Buttons
    - **Gradient-Scrollbars** in Firmenfarben
    - **Glassmorphism-Effekte** mit Backdrop-Filter
    - **Glow-Schatten** für highlighted Elemente
    - **Smooth Transitions** für alle Interaktionen
    """)
