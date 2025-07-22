# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CopilotUsage(models.Model):
    _name = 'copilot.usage'
    _description = _('AI Copilot Usage History')
    _order = 'create_date desc'
    _rec_name = 'display_name'

    # Relation with config
    config_id = fields.Many2one('copilot.config', string=_('Configuration'), required=True, ondelete='cascade')
    
    # Request details
    prompt = fields.Text(string=_('Sent Prompt'), required=True)
    response = fields.Text(string=_('AI Response'))
    
    # Metadata
    tokens_used = fields.Integer(string=_('Tokens Consumed'), default=0)
    model_used = fields.Char(string=_('AI Model Used'))
    module_name = fields.Char(string=_('Calling Module'))
    
    # Technical context
    user_id = fields.Many2one('res.users', string=_('User'), default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string=_('Company'), default=lambda self: self.env.company)
    created_at = fields.Datetime(string=_('Creation Date'), default=fields.Datetime.now, required=True)
    
    # Status
    status = fields.Selection([
        ('success', _('Success')),
        ('error', _('Error')),
        ('quota_exceeded', _('Quota Exceeded')),
    ], string=_('Status'), default='success')
    
    error_message = fields.Text(string=_('Error Message'))
    
    # Response time
    response_time = fields.Float(string=_('Response Time (s)'), help=_('Duration in seconds'))
    
    # Display name
    display_name = fields.Char(string=_('Name'), compute='_compute_display_name', store=True)
    
    @api.depends('module_name', 'model_used', 'create_date')
    def _compute_display_name(self):
        for record in self:
            module_part = record.module_name or 'Core'
            model_part = record.model_used or 'IA'
            date_part = record.create_date.strftime('%d/%m %H:%M') if record.create_date else ''
            record.display_name = f'{module_part} - {model_part} ({date_part})'
    
    @api.model
    def get_usage_stats(self, days=30):
        """Retourne les statistiques d'usage des derniers jours"""
        domain = [
            ('create_date', '>=', fields.Datetime.now() - fields.timedelta(days=days))
        ]
        
        records = self.search(domain)
        
        stats = {
            'total_requests': len(records),
            'total_tokens': sum(records.mapped('tokens_used')),
            'success_rate': len(records.filtered(lambda r: r.status == 'success')) / len(records) * 100 if records else 0,
            'avg_response_time': sum(records.mapped('response_time')) / len(records) if records else 0,
            'by_module': {},
            'by_model': {},
        }
        
        # Statistiques par module
        for module in records.mapped('module_name'):
            if module:
                module_records = records.filtered(lambda r: r.module_name == module)
                stats['by_module'][module] = {
                    'requests': len(module_records),
                    'tokens': sum(module_records.mapped('tokens_used')),
                }
        
        # Statistiques par modèle
        for model in records.mapped('model_used'):
            if model:
                model_records = records.filtered(lambda r: r.model_used == model)
                stats['by_model'][model] = {
                    'requests': len(model_records),
                    'tokens': sum(model_records.mapped('tokens_used')),
                }
        
        return stats
    
    def action_view_details(self):
        """Action pour voir les détails d'une requête"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Détails de la Requête IA'),
            'res_model': 'copilot.usage',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    @api.model
    def cleanup_old_records(self, days=90):
        """Nettoie les anciens enregistrements d'usage"""
        cutoff_date = fields.Datetime.now() - fields.timedelta(days=days)
        old_records = self.search([('create_date', '<', cutoff_date)])
        count = len(old_records)
        old_records.unlink()
        return count
