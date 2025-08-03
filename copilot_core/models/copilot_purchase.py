# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CopilotPurchase(models.Model):
    _name = 'copilot.purchase'
    _description = _('AI Copilot Token Purchases')
    _order = 'create_date desc'
    _rec_name = 'display_name'

    # Relation with config
    config_id = fields.Many2one('copilot.config', string=_('Configuration'), required=True, ondelete='cascade')
    
    # Purchase details
    tokens_purchased = fields.Integer(string=_('Tokens Purchased'), required=True)
    amount_eur = fields.Float(string=_('Amount (EUR)'), digits=(10, 2))
    
    # Payment info
    payment_reference = fields.Char(string=_('Payment Reference'))
    
    # Status
    status = fields.Selection([
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ], string=_('Status'), default='completed', required=True)
    
    # Dates
    created_at = fields.Datetime(string=_('Creation Date'), default=fields.Datetime.now, required=True)
    completed_at = fields.Datetime(string=_('Completion Date'))
    
    # Technical context
    user_id = fields.Many2one('res.users', string=_('User'), default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string=_('Company'), default=lambda self: self.env.company)
    
    # Display name
    display_name = fields.Char(string=_('Name'), compute='_compute_display_name', store=True)
    
    @api.depends('tokens_purchased', 'status', 'created_at')
    def _compute_display_name(self):
        for record in self:
            status_part = dict(record._fields['status'].selection).get(record.status)
            date_part = record.created_at.strftime('%d/%m/%Y') if record.created_at else ''
            record.display_name = f'{record.tokens_purchased} tokens - {status_part} ({date_part})'
