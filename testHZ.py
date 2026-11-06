import random
from nicegui import ui

# --- State / Daten ---
assets = [
    {"name": "Bitcoin (BTC)", "price": 95000, "change": 1.2},
    {"name": "Ethereum (ETH)", "price": 3200, "change": -0.5},
    {"name": "Solana (SOL)", "price": 210, "change": 5.4},
]

# Historische Daten für den Chart initialisieren
chart_data = {asset["name"]: [asset["price"] * (1 + random.uniform(-0.02, 0.02)) for _ in range(10)] for asset in assets}

# --- Funktionen / Logik ---
def update_prices():
    """Simuliert eine Preisänderung und aktualisiert die UI-Elemente."""
    for asset in assets:
        change_pct = random.uniform(-3.0, 3.0)
        asset["price"] = round(asset["price"] * (1 + change_pct / 100), 2)
        asset["change"] = round(change_pct, 2)
        
        # Chart-Daten aktualisieren (letzten Wert rollieren)
        chart_data[asset["name"]].pop(0)
        chart_data[asset["name"]].append(asset["price"])
    
    # UI-Komponenten aktualisieren
    grid_cards.refresh()
    table.update()
    update_chart()
    ui.notify("Kurse aktualisiert!", type="positive", color="teal")

def update_chart():
    """Aktualisiert die Linien im EChart."""
    crypto_chart.options['series'] = [
        {'name': name, 'type': 'line', 'data': data} for name, data in chart_data.items()
    ]
    crypto_chart.update()

# --- UI Layout ---
ui.query('body').classes('bg-slate-50 dark:bg-slate-900 transition-colors duration-300')

# Header Bar
with ui.header().classes('bg-gradient-to-r from-blue-600 to-indigo-700 text-white items-center justify-between shadow-lg px-6 py-3'):
    with ui.row().classes('items-center gap-3'):
        ui.icon('monitoring', size='md')
        ui.label('ApexAsset Dashboard').classes('text-2xl font-black tracking-wider')
    
    with ui.row().classes('items-center gap-4'):
        ui.button('Kurse aktualisieren', on_click=update_prices, icon='refresh').props('elevated color=amber text-color=black')
        # Dark Mode Switcher
        dark = ui.dark_mode()
        ui.button(icon='dark_mode', on_click=dark.toggle).props('flat round color=white')

# Hauptbereich mit Tabs
with ui.tabs().classes('w-full justify-center mt-6 text-indigo-600 dark:text-indigo-400') as tabs:
    tab_overview = ui.tab('Übersicht', icon='dashboard')
    tab_analytics = ui.tab('Analyse & Charts', icon='show_chart')

with ui.tab_panels(tabs, value=tab_overview).classes('w-full max-w-5xl mx-auto bg-transparent mt-4'):
    
    # --- TAB 1: ÜBERSICHT ---
    with ui.tab_panel(tab_overview):
        # Dynamische Grid-Karten (Reaktionsfähig via @ui.refreshable)
        @ui.refreshable
        def grid_cards():
            with ui.row().classes('w-full justify-between gap-6'):
                for asset in assets:
                    color = "emerald" if asset["change"] >= 0 else "rose"
                    icon = "trending_up" if asset["change"] >= 0 else "trending_down"
                    sign = "+" if asset["change"] >= 0 else ""
                    
                    with ui.card().classes('flex-1 min-w-[250px] p-6 rounded-2xl shadow-md border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-800 transition-all hover:scale-[1.02]'):
                        ui.label(asset["name"]).classes('text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider')
                        ui.label(f"${asset['price']:,}").classes('text-3xl font-bold my-2 text-slate-800 dark:text-slate-100')
                        
                        with ui.row().classes(f'items-center text-{color}-500 font-bold bg-{color}-50 dark:bg-{color}-950/30 px-3 py-1 rounded-full text-sm'):
                            ui.icon(icon, size='xs')
                            ui.label(f"{sign}{asset['change']}% (24h)")
        
        grid_cards()
        
        # Interaktive Datentabelle
        ui.label('Alle Vermögenswerte').classes('text-xl font-bold mt-10 mb-4 text-slate-800 dark:text-slate-100')
        columns = [
            {'name': 'name', 'label': 'Asset', 'field': 'name', 'required': True, 'align': 'left'},
            {'name': 'price', 'label': 'Preis (USD)', 'field': 'price', 'sortable': True},
            {'name': 'change', 'label': 'Veränderung', 'field': 'change', 'sortable': True},
        ]
        table = ui.table(columns=columns, rows=assets, row_key='name').classes('w-full shadow-md rounded-xl bg-white dark:bg-slate-800')
        # Customizing Table cells via slots
        table.add_slot('body-cell-change', '''
            <q-td :props="props">
                <q-chip :color="props.value >= 0 ? 'emerald-1' : 'rose-1'" :text-color="props.value >= 0 ? 'emerald-9' : 'rose-9'" icon="fiber_manual_record" dense>
                    {{ props.value >= 0 ? '+' : '' }}{{ props.value }}%
                </q-chip>
            </q-td>
        ''')

    # --- TAB 2: ANALYSE ---
    with ui.tab_panel(tab_analytics):
        with ui.card().classes('w-full p-6 rounded-2xl shadow-md bg-white dark:bg-slate-800'):
            ui.label('Preisentwicklung (Simulierte Ticks)').classes('text-lg font-bold text-slate-800 dark:text-slate-100 mb-4')
            
            # Leistungsstarkes Apache EChart integrieren
            crypto_chart = ui.echart({
                'tooltip': {'trigger': 'axis'},
                'legend': {'data': [asset["name"] for asset in assets], 'bottom': 0},
                'xAxis': {'type': 'category', 'boundaryGap': False},
                'yAxis': {'type': 'value', 'scale': True},
                'series': []
            }).classes('w-full h-80')
            update_chart()

# Startet den Server automatisch im Hot-Reload-Modus
ui.run(title='ApexAsset Dashboard', port=8080)
