# -*- coding: utf-8 -*-
{
    'name': 'Copilot HR',
    'version': '18.0.1.0.49',
    'category': 'Human Resources/Productivity',
    'summary': 'Module HR pour Copilot4Odoo',
    'description': '''
Copilot HR - Version v18.0.1.0.49
============================================

Module HR v18.0.1.0.49 pour Copilot4Odoo compatible avec Odoo 18.
Améliorations: contexte société et KPIs injectés dans le rapport IA, et détection module côté API via module_name='copilot_hr'.
    ''',
    'author': 'Copilot4Odoo Team',
    'website': 'https://www.copilot4odoo.com/modules',
    'license': 'OPL-1',
    'icon': '/copilot_hr/static/description/icon.png',  # Icône locale pour le chatter
    'depends': [
        'base',
        'hr',
        'copilot_core',
        'hr_recruitment',
        'hr_contract',
    ],
    'suggests': [],
    'data': [
        'security/hr_ai_security.xml',
        'security/ir.model.access.csv',
        'data/copilot_data.xml',
        'data/ir_cron.xml',
        'views/hr_employee_views.xml',
        'views/hr_applicant_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_report_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 399.0,
    'currency': 'EUR',
    'images': [
        'static/description/banner.gif',
        'static/description/copilot_hr.jpg',
 
    ],
    'post_init_hook': 'post_init_hook',
}
