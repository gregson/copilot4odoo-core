# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CopilotModels(models.Model):
    _name = 'copilot.models'
    _description = _('Available AI Models')
    _order = 'sequence, name'

    name = fields.Char(string=_('Technical Name'), required=True)
    display_name = fields.Char(string=_('Display Name'), required=True)
    provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('mistral', 'Mistral'),
        ('cohere', 'Cohere'),
        ('opensource', 'Open Source'),
    ], string=_('Provider'), required=True)
    
    description = fields.Text(string=_('Description'))
    
    # Technical characteristics
    context_length = fields.Integer(string=_('Context Length'), help=_('Maximum number of input tokens'))
    cost_per_1k_input = fields.Float(string=_('Cost / 1K tokens (input)'), digits=(10, 6))
    cost_per_1k_output = fields.Float(string=_('Cost / 1K tokens (output)'), digits=(10, 6))
    
    # Capabilities
    supports_function_calling = fields.Boolean(string=_('Supports Function Calling'), default=False)
    supports_vision = fields.Boolean(string=_('Supports Vision'), default=False)
    supports_code = fields.Boolean(string=_('Code Optimized'), default=False)
    
    # Status
    is_active = fields.Boolean(string=_('Active'), default=True)
    is_recommended = fields.Boolean(string=_('Recommended'), default=False)
    sequence = fields.Integer(string=_('Sequence'), default=10)
    
    # Metadata
    release_date = fields.Date(string=_('Release Date'))
    last_update = fields.Datetime(string=_('Last Update'), default=fields.Datetime.now)
    
    @api.model
    def get_active_models(self):
        """Retourne la liste des modèles actifs pour les sélections"""
        models = self.search([('is_active', '=', True)])
        return [(model.name, f'{model.display_name} ({model.provider})') for model in models]
    
    @api.model
    def get_recommended_model(self):
        """Retourne le modèle recommandé par défaut"""
        recommended = self.search([('is_recommended', '=', True), ('is_active', '=', True)], limit=1)
        if recommended:
            return recommended.name
        
        # Fallback sur le premier modèle actif
        first_active = self.search([('is_active', '=', True)], limit=1)
        return first_active.name if first_active else 'gpt-3.5-turbo'
    
    def estimate_cost(self, input_tokens, output_tokens):
        """Estime le coût d'une requête"""
        self.ensure_one()
        input_cost = (input_tokens / 1000) * self.cost_per_1k_input
        output_cost = (output_tokens / 1000) * self.cost_per_1k_output
        return input_cost + output_cost
    
    @api.model
    def sync_from_api(self, models_data):
        """Synchronise les modèles depuis l'API externe"""
        for model_data in models_data:
            existing = self.search([('name', '=', model_data.get('name'))], limit=1)
            
            values = {
                'name': model_data.get('name'),
                'display_name': model_data.get('display_name'),
                'provider': model_data.get('provider'),
                'description': model_data.get('description'),
                'context_length': model_data.get('context_length', 0),
                'cost_per_1k_input': model_data.get('cost_per_1k_input', 0),
                'cost_per_1k_output': model_data.get('cost_per_1k_output', 0),
                'supports_function_calling': model_data.get('supports_function_calling', False),
                'supports_vision': model_data.get('supports_vision', False),
                'supports_code': model_data.get('supports_code', False),
                'is_active': model_data.get('is_active', True),
                'last_update': fields.Datetime.now(),
            }
            
            if existing:
                existing.write(values)
            else:
                self.create(values)
