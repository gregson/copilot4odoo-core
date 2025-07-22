# -*- coding: utf-8 -*-

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    _logger.info("Modèle res_company chargé avec succès et hérite de res.company")

    copilot_default_model = fields.Selection([
        ('gpt-4-turbo', 'GPT-4 Turbo (OpenAI)'),
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo (OpenAI)'),
        ('claude-3-opus', 'Claude 3 Opus (Anthropic)'),
        ('claude-3-sonnet', 'Claude 3 Sonnet (Anthropic)'),
        ('mixtral-8x7b', 'Mixtral 8x7B (Mistral)'),
        ('mistral-7b', 'Mistral 7B (Mistral)'),
        ('command-r', 'Command R (Cohere)'),
        ('nous-capybara', 'Nous Capybara (Open Source)'),
    ], string="Modèle IA par défaut", default='gpt-3.5-turbo',
    help="Modèle IA par défaut à utiliser pour les fonctionnalités Copilot")
