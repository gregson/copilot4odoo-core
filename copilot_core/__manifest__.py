{
    'name': 'Copilot AI Core',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Central AI engine for Odoo copilots - AI tokens and models management',
    'description': """
Copilot AI Core - Central Infrastructure
=======================================

COMPATIBLE WITH ODOO 18+ ONLY

This module is the mandatory central core for all specialized AI copilots.

Main features:
* Centralized management of AI tokens and quotas
* Choice of AI models (GPT-4, Claude, Mixtral, etc.)
* Secure configuration interface
* Discovery hub for available copilot modules
* Tracking and history of AI requests
* Multi-engine support (OpenRouter, OpenAI, Ollama)

This module does not contain direct business AI functions.
It serves as infrastructure for specialized modules:
- Copilot CRM (sales, leads, quotes)
- Copilot HR (employees, leaves, contracts)
- Copilot Stock (inventory, supply)
- Copilot Accounting (invoices, balance sheet)

Required installation to use any other copilot module.
    """,
    'author': 'Copilot4Odoo',
    'website': 'https://www.copilot4odoo.com',
    'license': 'LGPL-3',
    'support': 'support@copilot4odoo.com',
    'price': 0.0,
    'currency': 'EUR',
    'live_test_url': 'https://www.copilot4odoo.com/demo',
    'repository': 'https://github.com/gregson/copilot_core.git',
    'icon': 'static/description/icon.png',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/copilot_config_views.xml',
        'views/copilot_dashboard_views.xml',
        'views/copilot_menu.xml',
        'data/copilot_models_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'copilot_core/static/src/js/copilot_widget.js',
            'copilot_core/static/src/css/copilot_style.css',
            'copilot_core/static/src/xml/copilot_widget.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,
    'images': [
        'static/description/banner.jpg',
        'static/description/copilot_core.jpg',
        # Emplacements pour les futures images de screenshots
         'static/description/screenshot_1.png',
        'static/description/screenshot_2.png',
        'static/description/screenshot_3.png',
    ],
}

