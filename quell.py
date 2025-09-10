# Create a simple mockup "screenshot" of the app layout using matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig_w, fig_h = 12, 7
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, 120)
ax.set_ylim(0, 70)
ax.axis('off')

def draw_box(x, y, w, h, label, fc='#ffffff', ec='#cccccc', label_color='#111111', fontsize=10, lw=1.5):
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x+2, y+h-4, label, fontsize=fontsize, color=label_color, va='top', ha='left')

# Background
draw_box(2, 2, 116, 66, '', fc='#f6f7f9', ec='#f6f7f9', lw=0)  # page bg

# Card container
draw_box(6, 6, 108, 58, '', fc='#ffffff', ec='#d9e2ef')

# Header
draw_box(6, 58, 108, 6, 'Header: Logo + "Kunden-Suche"', fc='#ffffff', ec='#d9e2ef')
# Logo
draw_box(10, 58.5, 12, 5, 'Logo', fc='#eaf2ff', ec='#a9c3ff')
# Title text
ax.text(30, 61, 'Kunden-Suche (Titel)', fontsize=12, color='#344054', va='center')

# Searchbar
draw_box(6, 50.5, 108, 7, 'Suchleiste', fc='#ffffff', ec='#d9e2ef')
# Fields
draw_box(8, 51.2, 55, 5.5, 'Suche: Name / Ort / CSB / SAP / Tour / Fachberater / Telefon …', fc='#fbfcfe', ec='#e6eaf0')
draw_box(64.5, 51.2, 28, 5.5, 'Schlüssel (exakt)', fc='#fbfcfe', ec='#e6eaf0')
draw_box(94, 51.2, 18, 5.5, 'Zurücksetzen', fc='#ffffff', ec='#e6eaf0')

# Tour banner
draw_box(6, 45, 108, 4.5, 'Tour-Banner: "Tour 1234 — 24 Kunden"   |   Mo:8 • Di:5 • Mi:4 • Do:3 • Fr:4', fc='#f2f5fa', ec='#d9e2ef')

# Table header
draw_box(6, 41, 108, 4, '', fc='#f2f5fa', ec='#e6edf5')
headers = ["CSB / SAP", "Name / Straße", "PLZ / Ort", "Schlüssel / Touren", "Fachberater / Markt Telefon", "Aktion"]
x_positions = [6.5, 24, 49, 64, 86, 110]
widths = [16, 23, 14, 20, 22, 4]
for x, w, h in zip(x_positions, widths, headers):
    ax.text(x+1, 43.5, h, fontsize=9, color='#344054', va='center')

# Table rows (2-line layout per row; no wrapping in cells)
row_y = 36.5
row_h = 4.5
for i in range(6):  # draw two example rows
    y = row_y - i*row_h
    fc = '#ffffff' if i%2==0 else '#f5f8fc'
    draw_box(6, y, 108, row_h, '', fc=fc, ec='#e6edf5')
    # Column separators (visual guides)
    # CSB/SAP
    ax.text(7.5, y+3.2, "CSB: 30391", fontsize=9, color='#0b3a8a', va='center')
    ax.text(7.5, y+1.3, "SAP: 123456", fontsize=8.5, color='#64748b', va='center')
    # Name/Strasse
    ax.text(25.5, y+3.2, "EDEKA Muster Markt", fontsize=9, color='#111', va='center')
    ax.text(25.5, y+1.3, "Hauptstr. 1", fontsize=8.5, color='#64748b', va='center')
    # PLZ/Ort
    ax.text(50.5, y+3.2, "23552", fontsize=9, color='#111', va='center')
    ax.text(50.5, y+1.3, "Lübeck", fontsize=8.5, color='#64748b', va='center')
    # Schlüssel/Touren
    ax.text(65, y+3.2, "Schlüssel: 40", fontsize=9, color='#92400e', va='center')
    ax.text(65, y+1.3, "Touren: 1234(Mo) 5678(Fr)", fontsize=8.5, color='#065f46', va='center')
    # Fachberater/Markt Telefon
    ax.text(87, y+3.2, "Max Mustermann  ☎ 0451-123456", fontsize=9, color='#111', va='center')
    ax.text(87, y+1.3, "☎ 0451-987654", fontsize=8.5, color='#64748b', va='center')
    # Aktion
    draw_box(110.5, y+0.9, 3.5, 2.7, "Map", fc='#2563eb', ec='#1d4ed8')
    
# Save image
out_path = "/mnt/data/app_layout_mock.png"
fig.savefig(out_path, dpi=160, bbox_inches='tight')
out_path
