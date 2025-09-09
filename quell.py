import streamlit as st
import pandas as pd
import json

# --- Modernes, schlichtes HTML-Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Kunden-Suche</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0066cc;
            --primary-hover: #0052a3;
            --secondary: #6c757d;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --bg: #ffffff;
            --bg-secondary: #f8f9fa;
            --border: #dee2e6;
            --text: #212529;
            --text-muted: #6c757d;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow: 0 2px 4px rgba(0,0,0,0.1);
            --radius: 4px;
        }

        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }

        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: var(--bg-secondary);
            color: var(--text);
            line-height: 1.5;
            font-size: 14px;
        }

        .container { 
            max-width: 1400px; 
            margin: 0 auto;
            padding: 16px;
        }

        /* Header */
        .header {
            background: var(--bg);
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 16px;
        }

        .header h1 { 
            font-size: 20px; 
            font-weight: 600; 
            color: var(--text);
        }

        /* Search Bar */
        .search-section {
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
            margin-bottom: 16px;
        }

        .search-row {
            display: flex;
            gap: 8px;
            margin-bottom: 8px;
        }

        input[type="text"] { 
            flex: 1;
            padding: 8px 12px; 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            font-size: 14px;
            background: var(--bg);
        }

        input[type="text"]:focus { 
            outline: none; 
            border-color: var(--primary); 
            box-shadow: 0 0 0 2px rgba(0,102,204,0.1);
        }

        .btn-group {
            display: flex;
            gap: 8px;
        }

        button { 
            padding: 8px 16px; 
            font-size: 14px; 
            font-weight: 500; 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            cursor: pointer; 
            background: var(--bg);
            color: var(--text);
            transition: all 0.2s;
        }

        button:hover { 
            background: var(--bg-secondary);
        }

        button.primary {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        button.primary:hover {
            background: var(--primary-hover);
        }

        #backBtn { 
            display: none; 
        }

        .stats { 
            font-size: 12px; 
            color: var(--text-muted); 
        }

        /* Main Layout */
        .main-layout {
            display: flex;
            gap: 16px;
        }

        .sidebar {
            width: 300px;
            flex-shrink: 0;
        }

        .main-content {
            flex: 1;
            min-width: 0;
        }

        /* Info Box */
        .info-box { 
            background: var(--bg); 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            overflow: hidden;
            display: none;
        }

        .info-box.show {
            display: block;
        }

        .info-header { 
            padding: 12px 16px; 
            font-weight: 600; 
            font-size: 14px; 
            background: var(--bg-secondary); 
            border-bottom: 1px solid var(--border);
        }

        .info-content {
            max-height: 400px;
            overflow-y: auto;
        }

        .list-item { 
            padding: 8px 16px; 
            border-bottom: 1px solid var(--border); 
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13px;
        }

        .list-item:hover {
            background: var(--bg-secondary);
        }

        .csb-link { 
            font-weight: 600; 
            color: var(--primary); 
            cursor: pointer; 
            min-width: 60px;
        }

        .csb-link:hover {
            text-decoration: underline;
        }

        .key-info { 
            font-size: 12px;
            color: var(--text-muted); 
            min-width: 60px;
        }

        .location { 
            flex: 1;
            color: var(--text); 
        }

        .maps-link { 
            padding: 4px 8px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: var(--radius);
            font-size: 12px;
        }

        .maps-link:hover {
            background: var(--primary-hover);
        }

        /* Customer Grid */
        .customer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
        }

        .customer-card { 
            background: var(--bg); 
            border: 1px solid var(--border); 
            border-radius: var(--radius); 
            overflow: hidden;
            transition: box-shadow 0.2s;
        }

        .customer-card:hover { 
            box-shadow: var(--shadow);
        }

        .customer-card.highlighted { 
            border-color: var(--primary); 
            box-shadow: 0 0 0 2px rgba(0,102,204,0.1);
        }

        .card-header {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            background: var(--bg-secondary);
        }

        .card-title { 
            font-size: 14px; 
            font-weight: 600; 
            color: var(--text);
            margin-bottom: 2px;
        }

        .card-subtitle {
            font-size: 12px;
            color: var(--text-muted);
        }

        .card-body {
            padding: 12px 16px;
        }

        .card-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 13px;
        }

        .info-label {
            font-weight: 600;
            color: var(--text-muted);
        }

        .tours-section {
            padding-top: 12px;
            border-top: 1px solid var(--border);
        }

        .tours-title {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .tour-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }

        .tour-tag {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 4px 8px;
            border-radius: var(--radius);
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .tour-tag:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        .card-actions {
            margin-top: 12px;
        }

        .action-btn {
            display: inline-block;
            padding: 6px 12px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: var(--radius);
            font-size: 12px;
            transition: background 0.2s;
        }

        .action-btn:hover {
            background: var(--primary-hover);
        }

        /* Tour Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            overflow-y: auto;
            padding: 32px;
        }

        .modal-overlay.show {
            display: block;
        }

        .modal-content {
            max-width: 1200px;
            margin: 0 auto;
            background: var(--bg);
            border-radius: var(--radius);
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }

        .modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 18px;
            font-weight: 600;
        }

        .modal-close {
            background: transparent;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: var(--text-muted);
            padding: 0;
            width: 32px;
            height: 32px;
        }

        .modal-close:hover {
            color: var(--text);
        }

        .modal-body {
            padding: 24px;
        }

        .tour-summary {
            background: var(--bg-secondary);
            padding: 16px;
            border-radius: var(--radius);
            margin-bottom: 24px;
        }

        .summary-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 24px;
            font-weight: 600;
            color: var(--primary);
        }

        .stat-label {
            font-size: 12px;
            color: var(--text-muted);
        }

        .tour-customers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 16px;
        }

        .tour-customer-card {
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
        }

        .tour-customer-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .tour-customer-key {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 12px;
        }

        .tour-customer-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 13px;
        }

        .tour-customer-address {
            background: var(--bg-secondary);
            padding: 8px;
            border-radius: var(--radius);
            margin-bottom: 12px;
            font-size: 13px;
        }

        .tour-customer-actions {
            display: flex;
            gap: 8px;
        }

        .hidden { 
            display: none !important; 
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: var(--radius);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        /* Mobile */
        @media(max-width: 768px) {
            .container { 
                padding: 8px; 
            }
            
            .main-layout {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
            }
            
            .customer-grid {
                grid-template-columns: 1fr;
            }
            
            .modal-overlay {
                padding: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Kunden-Suche</h1>
    </div>

    <div class="container">
        <div class="search-section">
            <div class="search-row">
                <input type="text" id="globalSearch" placeholder="Name, Ort, Tour, CSB, SAP, Straße...">
                <div class="btn-group">
                    <button id="resetBtn">Zurücksetzen</button>
                    <button id="backBtn" class="primary">Zurück zur Tour</button>
                </div>
            </div>
            <div class="stats" id="trefferInfo">0 Ergebnisse</div>
        </div>

        <div class="main-layout">
            <div class="sidebar">
                <div id="fachberaterBox" class="info-box">
                    <div class="info-header">
                        <span id="fachberaterNameSpan"></span> (<span id="fachberaterCountSpan"></span>)
                    </div>
                    <div class="info-content" id="fachberaterList"></div>
                </div>
            </div>

            <div class="main-content">
                <div class="customer-grid" id="customerGrid"></div>
            </div>
        </div>
    </div>

    <!-- Tour Modal -->
    <div id="tourModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="tourModalTitle"></div>
                <button class="modal-close" id="closeTourModal">×</button>
            </div>
            <div class="modal-body">
                <div class="tour-summary" id="tourSummary"></div>
                <div class="tour-customers-grid" id="tourCustomersGrid"></div>
            </div>
        </div>
    </div>

<script>
const tourkundenData = {  }; // <- wird von Python ersetzt

const $ = sel => document.querySelector(sel);
const el = (tag, cls, txt) => { 
    const n = document.createElement(tag); 
    if (cls) n.className = cls; 
    if (txt !== undefined) n.textContent = txt; 
    return n; 
};

const buildCustomerCard = kunde => {
    const card = el('div', 'customer-card hidden');
    const suchtext = `${kunde.name} ${kunde.strasse} ${kunde.postleitzahl} ${kunde.ort} ${kunde.csb_nummer} ${kunde.sap_nummer} ${kunde.fachberater} ${(kunde.schluessel||'')} ${kunde.touren.map(t => t.tournummer).join(' ')} ${kunde.touren.map(t => t.liefertag).join(' ')}`.toLowerCase();
    card.dataset.search = suchtext;

    const header = el('div', 'card-header');
    const title = el('div', 'card-title', kunde.name);
    const subtitle = el('div', 'card-subtitle', kunde.schluessel ? `Schlüssel: ${kunde.schluessel}` : 'Kein Schlüssel');
    header.append(title, subtitle);

    const body = el('div', 'card-body');
    
    const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
    const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
    const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';

    const info = el('div', 'card-info');
    info.innerHTML = `
        <div><span class="info-label">CSB:</span> ${csb}</div>
        <div><span class="info-label">SAP:</span> ${sap}</div>
        <div><span class="info-label">PLZ:</span> ${plz}</div>
        <div><span class="info-label">Ort:</span> ${kunde.ort}</div>
        <div style="grid-column: 1/-1;"><span class="info-label">Straße:</span> ${kunde.strasse}</div>
        <div style="grid-column: 1/-1;"><span class="info-label">Fachberater:</span> ${kunde.fachberater}</div>
    `;

    const toursSection = el('div', 'tours-section');
    const toursTitle = el('div', 'tours-title', 'Touren:');
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
    const actions = el('div', 'card-actions');
    const mapsBtn = el('a', 'action-btn', 'Google Maps');
    mapsBtn.href = mapsUrl;
    mapsBtn.target = '_blank';
    actions.appendChild(mapsBtn);

    body.append(info, toursSection, actions);
    card.append(header, body);

    return card;
};

const buildTourModal = (tourNumber, kunden) => {
    // Summary
    const summary = el('div');
    const summaryTitle = el('div', 'summary-title', `Tour ${tourNumber} - Übersicht`);
    const summaryStats = el('div', 'summary-stats');
    
    const totalStat = el('div', 'stat-item');
    totalStat.innerHTML = `<div class="stat-number">${kunden.length}</div><div class="stat-label">Gesamt</div>`;
    summaryStats.appendChild(totalStat);
    
    const dayGroups = {};
    kunden.forEach(k => {
        k.touren.forEach(t => {
            if (t.tournummer === tourNumber) {
                dayGroups[t.liefertag] = (dayGroups[t.liefertag] || 0) + 1;
            }
        });
    });
    
    Object.entries(dayGroups).forEach(([day, count]) => {
        const dayStat = el('div', 'stat-item');
        dayStat.innerHTML = `<div class="stat-number">${count}</div><div class="stat-label">${day}</div>`;
        summaryStats.appendChild(dayStat);
    });
    
    summary.append(summaryTitle, summaryStats);
    
    // Customers
    const grid = el('div');
    
    kunden.sort((a, b) => {
        const csbA = parseInt(a.csb_nummer?.toString().replace(/\\.0$/, '') || '0');
        const csbB = parseInt(b.csb_nummer?.toString().replace(/\\.0$/, '') || '0');
        return csbA - csbB;
    }).forEach(kunde => {
        const card = el('div', 'tour-customer-card');
        
        const name = el('div', 'tour-customer-name', kunde.name);
        const key = el('div', 'tour-customer-key', kunde.schluessel ? `Schlüssel: ${kunde.schluessel}` : 'Kein Schlüssel');
        
        const csb = kunde.csb_nummer?.toString().replace(/\\.0$/, '') || '-';
        const sap = kunde.sap_nummer?.toString().replace(/\\.0$/, '') || '-';
        const plz = kunde.postleitzahl?.toString().replace(/\\.0$/, '') || '-';
        
        const info = el('div', 'tour-customer-info');
        info.innerHTML = `
            <div><span class="info-label">CSB:</span> ${csb}</div>
            <div><span class="info-label">SAP:</span> ${sap}</div>
            <div><span class="info-label">PLZ:</span> ${plz}</div>
            <div><span class="info-label">Fachberater:</span> ${kunde.fachberater}</div>
        `;
        
        const address = el('div', 'tour-customer-address');
        address.textContent = `${kunde.strasse}, ${plz} ${kunde.ort}`;
        
        const actions = el('div', 'tour-customer-actions');
        
        const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(kunde.name + ', ' + kunde.strasse + ', ' + plz + ' ' + kunde.ort)}`;
        const mapsBtn = el('a', 'action-btn', 'Google Maps');
        mapsBtn.href = mapsUrl;
        mapsBtn.target = '_blank';
        
        const detailsBtn = el('button', 'action-btn', 'Details');
        detailsBtn.addEventListener('click', () => {
            $('#globalSearch').value = csb;
            $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
            $('#tourModal').classList.remove('show');
            $('#backBtn').style.display = 'inline-block';
        });
        
        actions.append(mapsBtn, detailsBtn);
        card.append(name, key, info, address, actions);
        grid.appendChild(card);
    });
    
    return { summary, grid };
};

const buildListEntry = (kunde) => {
    const item = el('div', 'list-item');
    
    const csbDiv = el('div', 'csb-link', kunde.csb);
    csbDiv.addEventListener('click', () => {
        $('#globalSearch').value = kunde.csb;
        $('#globalSearch').dispatchEvent(new Event('input', { bubbles: true }));
        $('#backBtn').style.display = 'inline-block';
    });

    const keyDiv = el('div', 'key-info', kunde.schluessel ? `S: ${kunde.schluessel}` : 'S: -');
    const nameDiv = el('div', 'location', kunde.name);
    
    const linkDiv = el('a', 'maps-link', 'Maps');
    linkDiv.href = kunde.mapsUrl;
    linkDiv.target = '_blank';

    item.append(csbDiv, keyDiv, nameDiv, linkDiv);
    return item;
};

// Main
let lastTourSearchQuery = '';
const customerGrid = $('#customerGrid');
const treffer = $('#trefferInfo');
const kundenMap = new Map();

if (typeof tourkundenData !== 'undefined' && Object.keys(tourkundenData).length > 0) {
    // Build customer map
    for (const [tour, klist] of Object.entries(tourkundenData)) {
        klist.forEach(k => {
            const key = k.csb_nummer;
            if (!key) return;
            if (!kundenMap.has(key)) kundenMap.set(key, { ...k, touren: [] });
            kundenMap.get(key).touren.push({ tournummer: tour, liefertag: k.liefertag });
        });
    }

    // Create cards
    kundenMap.forEach(k => {
        const card = buildCustomerCard(k);
        customerGrid.appendChild(card);
    });

    const input = $('#globalSearch');
    const fachberaterBox = $('#fachberaterBox');
    const fachberaterList = $('#fachberaterList');
    const fachberaterNameSpan = $('#fachberaterNameSpan');
    const fachberaterCountSpan = $('#fachberaterCountSpan');
    const tourModal = $('#tourModal');
    const tourModalTitle = $('#tourModalTitle');
    const tourSummary = $('#tourSummary');
    const tourCustomersGrid = $('#tourCustomersGrid');
    const closeTourModal = $('#closeTourModal');

    const alleFachberater = [...new Set(Array.from(kundenMap.values()).map(k => k.fachberater?.toLowerCase()))].filter(Boolean);

    // Search handler
    input.addEventListener('input', () => {
        const q = input.value.trim().toLowerCase();
        let hits = 0;

        fachberaterBox.classList.remove('show');
        tourModal.classList.remove('show');

        // Tour search
        const tourMatch = q.match(/^\\d{4}$/);
        if (tourMatch) {
            const tourN = tourMatch[0];
            const tourKunden = [];
            
            kundenMap.forEach(k => {
                if (k.touren.some(t => t.tournummer === tourN)) {
                    tourKunden.push(k);
                }
            });

            if (tourKunden.length > 0) {
                lastTourSearchQuery = tourN;
                tourModalTitle.textContent = `Tour ${tourN} (${tourKunden.length} Kunden)`;
                
                const { summary, grid } = buildTourModal(tourN, tourKunden);
                tourSummary.innerHTML = '';
                tourCustomersGrid.innerHTML = '';
                tourSummary.appendChild(summary);
                tourCustomersGrid.appendChild(grid);
                
                tourModal.classList.add('show');
                return;
            }
        }

        // Fachberater search
        const matchedFachberater = q.length > 2 ? alleFachberater.find(fb => fb.includes(q)) : null;
        if (matchedFachberater) {
            const kundenDesBeraters = [];
            let beraterName = '';
            kundenMap.forEach(k => {
                if (k.fachberater?.toLowerCase() === matchedFachberater) {
                    if (!beraterName) beraterName = k.fachberater;
                    const plz = k.postleitzahl?.toString().replace(/\\.0$/, '') || '';
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(k.name + ', ' + k.strasse + ', ' + plz + ' ' + k.ort)}`;
                    kundenDesBeraters.push({ 
                        csb: k.csb_nummer?.toString().replace(/\\.0$/, '') || '-', 
                        schluessel: k.schluessel || '', 
                        name: k.name, 
                        ort: k.ort, 
                        strasse: k.strasse, 
                        mapsUrl 
                    });
                }
            });

            if (kundenDesBeraters.length > 0) {
                fachberaterNameSpan.textContent = beraterName;
                fachberaterCountSpan.textContent = kundenDesBeraters.length;
                fachberaterList.innerHTML = '';
                kundenDesBeraters.sort((a, b) => Number(a.csb) - Number(b.csb)).forEach(kunde => {
                    fachberaterList.appendChild(buildListEntry(kunde));
                });
                fachberaterBox.classList.add('show');
            }
        }

        // Card search
        document.querySelectorAll('.customer-card').forEach(c => {
            const match = q !== '' && c.dataset.search.includes(q);
            c.classList.toggle('hidden', !match);
            c.classList.toggle('highlighted', match);
            if (match) hits++;
        });

        treffer.textContent = `${hits} Ergebnis${hits === 1 ? '' : 'se'}`;
    });

    // Modal close handlers
    closeTourModal.addEventListener('click', () => {
        tourModal.classList.remove('show');
    });

    tourModal.addEventListener('click', (e) => {
        if (e.target === tourModal) {
            tourModal.classList.remove('show');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && tourModal.classList.contains('show')) {
            tourModal.classList.remove('show');
        }
    });

    // Button handlers
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
        tourModal.classList.remove('show');
    });
} else {
    customerGrid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);"><h3>Keine Daten</h3><p>Kundendaten konnten nicht geladen werden.</p></div>';
}
</script>

</body>
</html>
"""

st.title("Tour-Übersicht Kunden-Suchseite")
st.markdown("""
Laden Sie zwei Excel-Dateien hoch:
1. **Quelldatei** mit den Kundendaten (mehrere Blätter)
2. **Schlüsseldatei** mit CSB in Spalte A und Schlüsselnummer in Spalte F
""")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("Quelldatei (Kundendaten)", type=["xlsx"])
with col2:
    key_file = st.file_uploader("Schlüsseldatei (A=CSB, F=Schlüssel)", type=["xlsx"])

def norm_str_num(x):
    if pd.isna(x): return ""
    s = str(x).strip()
    try:
        f = float(s.replace(",", ".")); i = int(f)
        return str(i) if f == i else s
    except Exception:
        return s

def build_key_map(key_df):
    if key_df.shape[1] < 6:
        st.warning("Schlüsseldatei hat weniger als 6 Spalten. Es werden die vorhandenen Spalten genutzt.")
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
    if st.button("HTML-Seite erzeugen", type="primary"):
        BLATTNAMEN = ["Direkt 1 - 99", "Hupa MK 882", "Hupa 2221-4444", "Hupa 7773-7779"]
        LIEFERTAGE_MAPPING = {"Montag": "Mo", "Dienstag": "Die", "Mittwoch": "Mitt", "Donnerstag": "Don", "Freitag": "Fr", "Samstag": "Sam"}
        SPALTEN_MAPPING = {"csb_nummer": "Nr", "sap_nummer": "SAP-Nr.", "name": "Name", "strasse": "Strasse", "postleitzahl": "Plz", "ort": "Ort", "fachberater": "Fachberater"}

        try:
            with st.spinner("Lese Schlüsseldatei..."):
                key_df = pd.read_excel(key_file, sheet_name=0, header=0)
                if key_df.shape[1] < 2:
                    key_file.seek(0)
                    key_df = pd.read_excel(key_file, sheet_name=0, header=None)
                key_map = build_key_map(key_df)

            tour_dict = {}
            def kunden_sammeln(df):
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

            with st.spinner("Verarbeite Quelldatei..."):
                for blatt in BLATTNAMEN:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=blatt)
                        kunden_sammeln(df)
                    except ValueError:
                        st.warning(f"Blatt '{blatt}' nicht gefunden.")

            if not tour_dict:
                st.error("Keine gültigen Kundendaten gefunden.")
                st.stop()

            sorted_tours = dict(sorted(tour_dict.items(), key=lambda item: int(item[0])))
            json_data_string = json.dumps(sorted_tours, indent=4, ensure_ascii=False)

            final_html = HTML_TEMPLATE.replace("const tourkundenData = {  }", f"const tourkundenData = {json_data_string};")
            
            st.success(f"✓ HTML-Seite erfolgreich erstellt!")
            
            total_customers = sum(len(customers) for customers in sorted_tours.values())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Touren", len(sorted_tours))
            with col2:
                st.metric("Kunden", total_customers)
            with col3:
                st.metric("Schlüssel", len(key_map))
            
            st.download_button(
                "⬇️ HTML-Datei herunterladen", 
                data=final_html.encode("utf-8"), 
                file_name="suche.html", 
                mime="text/html",
                type="primary"
            )

        except Exception as e:
            st.error(f"Fehler: {e}")
            st.exception(e)
elif excel_file and not key_file:
    st.info("Bitte noch die Schlüsseldatei hochladen.")
elif key_file and not excel_file:
    st.info("Bitte noch die Quelldatei hochladen.")
else:
    st.info("Bitte beide Dateien hochladen, um fortzufahren.")
    
    with st.expander("Funktionsübersicht"):
        st.markdown("""
        **Hauptfunktionen:**
        - Zentrale Suche nach Name, Ort, Tour, CSB, SAP oder Straße
        - Tour-Übersicht als Modal bei Eingabe einer 4-stelligen Tournummer
        - Fachberater-Liste in der Seitenleiste
        - Responsive Kunden-Karten mit allen wichtigen Informationen
        - Direkte Google Maps Integration
        - Schnelle Navigation zwischen Tour-Übersicht und Einzelkunden
        """)
