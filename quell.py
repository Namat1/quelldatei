import streamlit as st
import pandas as pd
import json

# --- HTML-Vorlage mit modernem Design ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Kunden-Suche</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --secondary: #64748b;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --background: #f8fafc;
            --surface: #ffffff;
            --surface-hover: #f1f5f9;
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --radius: 12px;
            --radius-sm: 8px;
        }

        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }

        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--text-primary);
            line-height: 1.6;
        }

        .main-wrapper { 
            max-width: 1200px; 
            width: 100%; 
            margin: 0 auto;
            background: var(--surface);
            border-radius: var(--radius);
            box-shadow: var(--shadow-lg);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            padding: 32px;
            color: white;
            text-align: center;
        }

        .header h1 { 
            font-size: 2.5rem; 
            font-weight: 700; 
            margin-bottom: 8px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 400;
        }

        .content {
            padding: 32px;
        }

        .search-section {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }

        .search-container { 
            display: flex; 
            flex-direction: column; 
            gap: 16px; 
        }

        .search-input-wrapper {
            position: relative;
        }

        .search-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 1.2rem;
        }

        input[type="text"] { 
            width: 100%;
            padding: 16px 16px 16px 50px; 
            font-size: 1.1rem; 
            border: 2px solid var(--border); 
            border-radius: var(--radius-sm); 
            background: var(--surface); 
            color: var(--text-primary); 
            font-weight: 500; 
            transition: all 0.2s ease;
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: var(--primary); 
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); 
        }

        .search-hint {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: -8px;
        }

        .button-group { 
            display: flex; 
            gap: 12px; 
            flex-wrap: wrap; 
        }

        button { 
            padding: 12px 20px; 
            font-size: 0.95rem; 
            font-weight: 600; 
            border: none; 
            border-radius: var(--radius-sm); 
            cursor: pointer; 
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        #resetBtn { 
            background: var(--secondary); 
            color: white; 
        } 
        #resetBtn:hover { 
            background: #475569; 
            transform: translateY(-1px);
        }

        #backBtn { 
            display: none; 
            background: var(--success); 
            color: white; 
        } 
        #backBtn:hover { 
            background: #059669; 
            transform: translateY(-1px);
        }

        .stats-info { 
            font-size: 0.9rem; 
            color: var(--text-secondary); 
            font-weight: 500; 
            padding: 12px 16px;
            background: var(--surface-hover);
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-light);
        }

        .info-box { 
            margin-bottom: 24px; 
            background: var(--surface); 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            display: none;
        }

        .info-box-header { 
            padding: 16px 20px; 
            font-weight: 700; 
            font-size: 1.1rem; 
            background: var(--surface-hover); 
            color: var(--text-primary); 
            border-bottom: 1px solid var(--border);
        }

        .info-box-content {
            max-height: 400px;
            overflow-y: auto;
        }

        .entry { 
            padding: 12px 0; 
            border-bottom: 1px solid var(--border-light); 
        }

        .entry:last-child {
            border-bottom: none;
        }

        .entry-row { 
            display: grid; 
            grid-template-columns: 100px 160px 1fr 1.5fr 1.5fr auto; 
            align-items: center; 
            gap: 16px; 
            padding: 12px 20px; 
            transition: background-color 0.2s ease;
        }

        .entry-row:hover {
            background: var(--surface-hover);
        }

        .entry.alt .entry-row { 
            background: #fafafa; 
        }

        .csb-col { 
            font-weight: 700; 
            color: var(--primary); 
            cursor: pointer; 
            text-decoration: none;
            padding: 4px 8px;
            border-radius: 4px;
            transition: all 0.2s ease;
        }

        .csb-col:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-1px);
        }

        .key-col { 
            font-weight: 600; 
            color: var(--text-secondary); 
            font-size: 0.9rem;
        }

        .location-col { 
            font-weight: 600; 
            color: var(--text-primary); 
        }

        .street-col { 
            font-weight: 500; 
            color: var(--text-secondary); 
        }

        .name-col { 
            font-weight: 600; 
            color: var(--text-primary); 
        }

        .action-col a { 
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 6px 12px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: var(--radius-sm);
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .action-col a:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
        }

        #results { 
            display: grid;
            gap: 20px;
        }

        .customer-card { 
            background: var(--surface); 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            box-shadow: var(--shadow-sm); 
            transition: all 0.3s ease;
            overflow: hidden;
        }

        .customer-card:hover { 
            transform: translateY(-4px); 
            box-shadow: var(--shadow-md); 
        }

        .customer-card.highlighted { 
            border-left: 4px solid var(--primary); 
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        }

        .card-header {
            padding: 20px;
            background: var(--surface-hover);
            border-bottom: 1px solid var(--border);
        }

        .card-title { 
            font-size: 1.3rem; 
            font-weight: 700; 
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .card-subtitle {
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        .card-content {
            padding: 20px;
        }

        .card-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
        }

        .info-panel { 
            background: var(--surface-hover); 
            padding: 16px; 
            border-radius: var(--radius-sm); 
            border: 1px solid var(--border); 
        }

        .info-panel h4 {
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .info-panel .detail {
            margin-bottom: 8px;
            color: var(--text-secondary);
        }

        .info-panel .detail:last-child {
            margin-bottom: 0;
        }

        .maps-button { 
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: var(--radius-sm);
            font-weight: 600;
            font-size: 0.9rem;
            margin-top: 12px;
            transition: all 0.2s ease;
        }

        .maps-button:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
        }

        .tours-panel {
            grid-column: 1 / -1;
        }

        .tour-grid {
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            overflow: hidden;
            margin-top: 12px;
        }

        .tour-grid-header {
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: var(--surface-hover);
            font-weight: 600;
            color: var(--text-primary);
        }

        .tour-grid-header > div {
            padding: 12px 16px;
            border-right: 1px solid var(--border);
        }

        .tour-grid-header > div:last-child {
            border-right: none;
        }

        .tour-grid-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            border-top: 1px solid var(--border);
        }

        .tour-grid-cell {
            padding: 12px 16px;
            border-right: 1px solid var(--border);
        }

        .tour-grid-cell:last-child {
            border-right: none;
            color: var(--text-secondary);
        }

        .tour-link {
            color: var(--primary);
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .tour-link:hover {
            color: var(--primary-dark);
            text-decoration: underline;
        }

        .hidden { 
            display: none !important; 
        }

        /* Mobile Responsive */
        @media(max-width: 768px) {
            body { 
                padding: 12px; 
            }
            
            .header {
                padding: 24px 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .search-section {
                padding: 20px;
            }
            
            input[type="text"] { 
                padding: 14px 14px 14px 45px;
                font-size: 1rem;
            }
            
            button { 
                width: 100%; 
                justify-content: center;
            }
            
            .card-grid { 
                grid-template-columns: 1fr; 
            }
            
            .entry-row { 
                grid-template-columns: 80px 120px 1fr 1fr 1fr auto; 
                gap: 8px; 
                font-size: 0.9rem; 
            }
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--border-light);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--text-muted);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="header">
            <h1>🔍 Kunden-Suche</h1>
            <p>Intelligente Suche nach Kunden, Touren und Fachberatern</p>
        </div>
        
        <div class="content">
            <div class="search-section">
                <div class="search-container">
                    <div class="search-input-wrapper">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße eingeben...">
                    </div>
                    <p class="search-hint">💡 Suche nach Name, Ort, Straße, Tournummer, CSB, SAP, Liefertag oder Fachberater</p>
                    
                    <div class="button-group">
                        <button id="resetBtn">
                            <span>🔄</span>
                            Suche zurücksetzen
                        </button>
                        <button id="backBtn">
                            <span>⬅️</span>
                            Zurück zur Tour-Übersicht
                        </button>
                    </div>
                    
                    <div class="stats-info" id="trefferInfo">
                        🔎 0 Ergebnisse gefunden
                    </div>
                </div>
            </div>

            <div id="tourBox" class="info-box">
                <div class="info-box-header">
                    🚚 Tour <span id="tourNumSpan"></span>
                </div>
                <div class="info-box-content" id="tourList"></div>
            </div>
            
            <div id="fachberaterBox" class="info-box">
                <div class="info-box-header">
                    👤 Fachberater: <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span> Märkte)
                </div>
                <div class="info-box-content" id="fachberaterList"></div>
            </div>

            <div id="results"></div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt, wichtig: Semikolon!

// Helpers
const $  = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

const buildTourGrid = touren => {
    const box = el('div', 'tour-grid');
    
    const head = el('div', 'tour-grid-header');
    head.appendChild(el('div', null, '🚛 Tour'));
    head.appendChild(el('div', null, '📦 Liefertag'));
    box.appendChild(head);
    
    touren.forEach(t => {
        const row = el('div', 'tour-grid-row');
        
        const tourCell = el('div', 'tour-grid-cell');
        const link = el('a', 'tour-link', t.tournummer);
        link.href = '#';
        link.addEventListener('click', e => { 
            e.preventDefault(); 
            $('#globalSearch').value = t.tournummer; 
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true })); 
            window.scrollTo({ top: 0, behavior: 'smooth' }); 
            $('#backBtn').style.display = 'inline-flex'; 
        });
        tourCell.appendChild(link);
        
        const dayCell = el('div', 'tour-grid-cell', t.liefertag);
        
        row.append(tourCell, dayCell); 
        box.appendChild(row);
    });
    
    return box;
};

const buildCustomerCard = kunde => {
    const card = el('div', 'customer-card hidden');
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${(kunde.schluessel||'')} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    const cardHeader = el('div', 'card-header');
    const cardTitle = el('div', 'card-title', '🏪 ' + kunde.name);
    const cardSubtitle = el('div', 'card-subtitle', 
        kunde.schluessel ? `Schlüssel: ${kunde.schluessel}` : 'Kein Schlüssel hinterlegt'
    );
    cardHeader.appendChild(cardTitle);
    cardHeader.appendChild(cardSubtitle);
    card.appendChild(cardHeader);

    const cardContent = el('div', 'card-content');
    const grid = el('div', 'card-grid');

    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;

    // Adresse Panel
    const addrPanel = el('div', 'info-panel');
    const addrTitle = el('h4', null, '📍 Adresse');
    addrPanel.appendChild(addrTitle);
    addrPanel.appendChild(el('div', 'detail', kunde.strasse));
    addrPanel.appendChild(el('div', 'detail', `${plz} ${kunde.ort}`));
    const mapBtn = el('a', 'maps-button', '🗺️ Google Maps öffnen'); 
    mapBtn.href = mapsUrl; 
    mapBtn.target = '_blank';
    addrPanel.appendChild(mapBtn);
    grid.appendChild(addrPanel);

    // Stammdaten Panel
    const dataPanel = el('div', 'info-panel');
    const dataTitle = el('h4', null, '📊 Stammdaten');
    dataPanel.appendChild(dataTitle);
    dataPanel.appendChild(el('div', 'detail', `🆔 CSB: ${csb}`));
    dataPanel.appendChild(el('div', 'detail', `🔢 SAP: ${sap}`));
    dataPanel.appendChild(el('div', 'detail', `👤 Fachberater: ${kunde.fachberater}`));
    dataPanel.appendChild(el('div', 'detail', `🔑 Schlüssel: ${kunde.schluessel || '-'}`));
    grid.appendChild(dataPanel);

    // Touren Panel
    const toursPanel = el('div', 'info-panel tours-panel');
    const toursTitle = el('h4', null, '🚛 Tourenübersicht');
    toursPanel.appendChild(toursTitle);
    toursPanel.appendChild(buildTourGrid(kunde.touren));
    grid.appendChild(toursPanel);

    cardContent.appendChild(grid);
    card.appendChild(cardContent);

    return card;
};

const buildTourEntry = (ort, name, strasse, csbNummer, schluessel, mapsUrl, bgAlt) => {
    const entry = el('div', 'entry' + (bgAlt ? ' alt' : ''));
    const row = el('div', 'entry-row');

    const csbDiv = el('div', 'csb-col', csbNummer);
    csbDiv.title = `Kundenkarte für ${csbNummer} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = csbNummer;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-flex';
    });

    const sklText = schluessel && schluessel.trim() !== '' ? `Schlüssel: ${schluessel}` : 'Schlüssel: -';
    const sklDiv = el('div', 'key-col', sklText);

    const ortDiv = el('div', 'location-col', ort);
    const strDiv = el('div', 'street-col', strasse);
    const nameDiv = el('div', 'name-col', name);

    const btnDiv = el('div', 'action-col');
    const link = el('a', null, '📍 Maps'); 
    link.href = mapsUrl; 
    link.target = '_blank';
    btnDiv.appendChild(link);

    row.append(csbDiv, sklDiv, ortDiv, strDiv, nameDiv, btnDiv);
    entry.appendChild(row);
    return entry;
};

const buildFachberaterEntry = (kunde, bgAlt) => {
    const entry = el('div', 'entry' + (bgAlt ? ' alt' : ''));
    const row = el('div', 'entry-row');

    const csbDiv = el('div', 'csb-col', kunde.csb);
    csbDiv.title = `Kundenkarte für CSB ${kunde.csb} anzeigen`;
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = kunde.csb;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $('#backBtn').style.display = 'inline-flex';
    });

    const sklText = kunde.schluessel && kunde.schluessel.trim() !== '' ? `Schlüssel: ${kunde.schluessel}` : 'Schlüssel: -';
    const sklDiv = el('div', 'key-col', sklText);

    const ortDiv = el('div', 'location-col', kunde.ort);
    const strDiv = el('div', 'street-col', kunde.strasse);
    const nameDiv = el('div', 'name-col', kunde.name);

    const btnDiv = el('div', 'action-col');
    const link = el('a', null, '📍 Maps'); 
    link.href = kunde.mapsUrl; 
    link.target = '_blank';
    btnDiv.appendChild(link);

    row.append(csbDiv, sklDiv, ortDiv, strDiv, nameDiv, btnDiv);
    entry.appendChild(row);
    return entry;
};

// Main
let lastTourSearchQuery = '';
const results = $('#results');
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

    const allCards = [];
    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        results.appendChild(card);
        allCards.push(card);
    });

    const input = $('#globalSearch');
    const tourBox = $('#tourBox');
    const tourList = $('#tourList');
    const tourNumLbl = $('#tourNumSpan');
    const fachberaterBox = $('#fachberaterBox');
    const fachberaterList = $('#fachberaterList');
    const fachberaterNameSpan = $('#fachberaterNameSpan');
    const fachberaterCountSpan = $('#fachberaterCountSpan');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        tourBox.style.display = 'none';
        fachberaterBox.style.display = 'none';

        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const list = [];
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    list.push({ ort: k.ort, name: k.name, strasse: k.strasse, csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', schluessel: k.schluessel || '', mapsUrl });
                }
            });

            if (list.length > 0) {
                lastTourSearchQuery = tourN;
                tourList.innerHTML = '';
                tourNumLbl.textContent = `${tourN} - ${list.length} Kunde${list.length === 1 ? '' : 'n'}`;
                list.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach((kunde, i) => {
                    tourList.appendChild(buildTourEntry(kunde.ort, kunde.name, kunde.strasse, kunde.csb, kunde.schluessel, kunde.mapsUrl, i % 2 !== 0));
                });
                tourBox.style.display = 'block';
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
                    fachberaterList.appendChild(buildFachberaterEntry(kunde, i % 2 !== 0));
                });
                fachberaterBox.style.display = 'block';
            }
        }

        document.querySelectorAll('.customer-card').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            if (match) { c.classList.add('highlighted'); hits++; }
            else { c.classList.remove('highlighted'); }
        });

        treffer.textContent = `🔎 ${hits} Ergebnis${hits === 1 ? '' : 'se'} gefunden`;
    });

    document.querySelector('#backBtn').addEventListener('click', () => {
        if (lastTourSearchQuery) {
            input.value = lastTourSearchQuery;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            document.querySelector('#backBtn').style.display = 'none';
        }
    });

    document.querySelector('#resetBtn').addEventListener('click', () => {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        document.querySelector('#backBtn').style.display = 'none';
    });
} else {
    document.querySelector('#results').innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><h3>❌ Keine Kundendaten gefunden</h3><p>Stellen Sie sicher, dass die "tourkundenData" korrekt geladen wird.</p></div>';
}
</script>

</body>
</html>
"""

# --- UI Setup ---
st.title("🚛 Kunden-Datenbank als HTML-Seite exportieren")
st.markdown("""
Laden Sie **zwei** Excel-Dateien hoch:
1) **Quelldatei** mit den Kundendaten (mehrere Blätter)  
2) **Schlüsseldatei** mit *CSB in Spalte A* und *Schlüsselnummer in Spalte F*.

Ich erstelle daraus eine interaktive **HTML-Suchseite** (`suche.html`) mit modernem Design und verbesserter Benutzerfreundlichkeit.
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
    if st.button("🎨 Moderne HTML-Seite erzeugen", type="primary"):
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
                st.success(f"✅ {len(key_map)} Schlüsselzuordnungen geladen")

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

            with st.spinner("📥 Lese und verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                        st.info(f"✓ Blatt '{blatt}' verarbeitet")
                    except ValueError:
                        st.warning(f"⚠️ Blatt '{blatt}' nicht in der Datei gefunden. Wird übersprungen.")

            if not tour_dict:
                st.error("❌ Es konnten keine gültigen Kundendaten gefunden werden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            st.success(f"🎉 Erfolgreich! {len(sorted_tours)} Touren mit modernem Design verarbeitet.")
            
            # Statistiken anzeigen
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            st.info(f"📊 **Statistiken:** {len(sorted_tours)} Touren • {total_customers} Kundeneinträge • {len(key_map)} Schlüsselzuordnungen")
            
            st.download_button(
                "📥 Moderne `suche.html` herunterladen", 
                data=final_html.encode("utf-8"), 
                file_name="suche.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"❌ Ein unerwarteter Fehler ist aufgetreten: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("📁 Bitte zusätzlich die **Schlüsseldatei** (A=CSB, F=Schlüssel) hochladen.")
elif key_file and not excel_file:
    st.info("📁 Bitte zusätzlich die **Quelldatei** (Kundendaten) hochladen.")
else:
    st.info("📋 Bitte beide Dateien hochladen, um mit der Verarbeitung zu beginnen.")
    st.markdown("""
    ### ✨ Neue Features des modernen Designs:
    - **Gradient-Header** mit verbesserter Typografie
    - **Glassmorphism-Effekte** und moderne Schatten
    - **Verbesserte Farbpalette** mit CSS Custom Properties
    - **Responsive Grid-Layout** für alle Bildschirmgrößen  
    - **Micro-Animations** bei Hover-Effekten
    - **Optimierte Benutzerführung** mit visuellen Cues
    - **Bessere Zugänglichkeit** und Kontraste
    """)
