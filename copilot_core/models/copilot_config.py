# -*- coding: utf-8 -*-

import requests
import json
import logging
import hashlib
import inspect
import time
from datetime import datetime
from odoo import models, fields, api, _, release
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CopilotConfig(models.Model):
    _name = 'copilot.config'
    _description = _('AI Copilot Configuration')
    _rec_name = 'user_token'

    # Token and authentication
    user_token = fields.Char(
        string=_('AI Client Token'),
        help=_('Unique token provided by Copilot4Odoo to access AI models'),
        required=True
    )
    
    # Selected AI model
    selected_model = fields.Selection([
        ('gpt-4-turbo', 'GPT-4 Turbo (OpenAI)'),
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo (OpenAI)'),
        ('claude-3-opus', 'Claude 3 Opus (Anthropic)'),
        ('claude-3-sonnet', 'Claude 3 Sonnet (Anthropic)'),
        ('mixtral-8x7b', 'Mixtral 8x7B (Mistral)'),
        ('mistral-7b', 'Mistral 7B (Mistral)'),
        ('command-r', 'Command R (Cohere)'),
        ('nous-capybara', 'Nous Capybara (Open Source)'),
    ], string=_('AI Model'), default='gpt-3.5-turbo', required=True)
    
    # Quota management
    tokens_total = fields.Integer(string=_('Total Tokens'), default=0, readonly=True)
    tokens_used = fields.Integer(string=_('Used Tokens'), default=0, readonly=True)
    tokens_remaining = fields.Integer(
        string=_('Remaining Tokens'),
        compute='_compute_tokens_remaining',
        store=False,
        help=_('Number of remaining tokens')
    )
    
    usage_percentage = fields.Float(
        string=_('Usage Percentage'),
        compute='_compute_usage_percentage',
        store=False,
        help=_('Percentage of tokens used')
    )
    
    expiry_date = fields.Datetime(string=_('Expiry Date'), readonly=True)
    last_sync = fields.Datetime(string=_('Last Synchronization'), readonly=True)
    
    # Advanced parameters
    api_endpoint = fields.Char(
        string=_('API Endpoint'),
        default='https://www.copilot4odoo.com/api',
        help=_('Base URL for AI calls')
    )
    
    # Status
    is_active = fields.Boolean(string=_('Active'), default=True)
    status = fields.Selection([
        ('active', _('Active')),
        ('expired', _('Expired')),
        ('quota_exceeded', _('Quota Exceeded')),
        ('invalid_token', _('Invalid Token')),
    ], string=_('Status'), default='active', readonly=True)
    
    # Installed modules
    installed_modules = fields.Text(
        string=_('Installed Copilot Modules'),
        help=_('List of installed Copilot modules'),
        readonly=True,
        default=_('No Copilot module installed')
    )
    
    installed_modules_html = fields.Html(
        string=_('Installed Copilot Modules (HTML)'),
        help=_('List of installed Copilot modules in HTML format'),
        readonly=True,
        sanitize=False,
        default=_('<p>No Copilot module installed</p>')
    )

    available_modules = fields.Text(
        string=_('Available Copilot Modules'),
        help=_('List of available Copilot modules'),
        readonly=True,
        default=_('Loading available modules...')
    )
    
    # Méthode temporairement supprimée pour permettre l'upgrade
    def _compute_available_modules_html_disabled(self):
        pass
    
    @api.depends('tokens_total', 'tokens_used')
    def _compute_tokens_remaining(self):
        for record in self:
            record.tokens_remaining = record.tokens_total - record.tokens_used
            
    @api.onchange('user_token', 'api_endpoint')
    def _onchange_credentials(self):
        """Sauvegarde automatiquement les modifications du token et de l'endpoint API"""
        if self.id and (self.user_token or self.api_endpoint):
            _logger.info(f"Détection de changement dans token ou endpoint: {self.user_token[:5]}... / {self.api_endpoint}")
            # On ne peut pas utiliser self.write() dans un onchange, on enregistre donc pour traitement différé
            self.env.context = dict(self.env.context, save_token=self.user_token, save_endpoint=self.api_endpoint)
    
    @api.model
    def get_config(self):
        """Récupère la configuration active ou en crée une par défaut"""
        config = self.search([], limit=1)
        if not config:
            config = self.create({
                'user_token': 'demo_token_' + str(self.env.company.id),
                'selected_model': 'gpt-3.5-turbo',
                'api_endpoint': 'https://www.copilot4odoo.com/api',
            })
        
        # Traitement des modifications en attente depuis onchange
        ctx = self.env.context
        if ctx.get('save_token') or ctx.get('save_endpoint'):
            _logger.info(f"Sauvegarde des modifications en attente depuis onchange")
            values = {}
            if ctx.get('save_token'):
                values['user_token'] = ctx.get('save_token')
            if ctx.get('save_endpoint'):
                values['api_endpoint'] = ctx.get('save_endpoint')
                
            if values:
                config.sudo().write(values)
                self.env.cr.commit()
                _logger.info(f"Modifications sauvegardées: {values}")
        
        # Mise à jour de la liste des modules installés si nécessaire
        if not config.installed_modules or ctx.get('refresh_modules'):
            _logger.info("Mise à jour de la liste des modules Copilot installés")
            config.check_installed_copilots()
        
        return config
        
    @api.model
    def save_config(self, values):
        """Sauvegarde les modifications de la configuration"""
        _logger.info(f"Sauvegarde de la configuration: {values}")
        config = self.get_config()
        
        # Sauvegarde des valeurs dans la base de données
        if values:
            config.sudo().write(values)
            _logger.info(f"Configuration sauvegardée avec succès: {values}")
        
        return config
    
    @api.depends('tokens_total', 'tokens_used')
    def _compute_tokens_remaining(self):
        """Calcule le nombre de tokens restants"""
        for record in self:
            record.tokens_remaining = record.tokens_total - record.tokens_used
    
    @api.depends('tokens_total', 'tokens_used')
    def _compute_usage_percentage(self):
        """Calcule le pourcentage d'usage des tokens"""
        for record in self:
            if record.tokens_total > 0:
                record.usage_percentage = (record.tokens_used / record.tokens_total) * 100
            else:
                record.usage_percentage = 0.0
    
    def test_connection(self):
        """Teste la connexion avec le token et récupère les informations du compte"""
        self.ensure_one()
        
        # Vérification du token sans réécriture inutile
        if not self.user_token:
            raise UserError(_('Veuillez saisir un token client valide.'))
        
        # Pas de write() ici pour éviter le refresh de la vue qui fait disparaître l'affichage
        
        try:
            # Logs détaillés pour l'appel API
            _logger.info('='*50)
            _logger.info(f'DÉBUT APPEL API /api/account/info')
            _logger.info(f'Token utilisé: {self.user_token[:5]}...{self.user_token[-5:] if len(self.user_token) > 10 else self.user_token}')
            _logger.info(f'URL complète: {self.api_endpoint}/account/info')
            
            headers = {
                'Authorization': f'Bearer {self.user_token}',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'User-Agent': 'Odoo/Copilot4Odoo-Client'
            }
            
            _logger.info(f'Headers envoyés: {headers}')
            
            # Envoi de la requête avec mesure du temps
            import time
            start_time = time.time()
            
            response = requests.get(
                f'{self.api_endpoint}/account/info',
                headers=headers,
                timeout=10
            )
            
            elapsed_time = time.time() - start_time
            _logger.info(f'Temps de réponse: {elapsed_time:.2f} secondes')
            _logger.info(f'Code de statut: {response.status_code}')
            _logger.info(f'Headers de réponse: {dict(response.headers)}')
            
            # Traitement de la réponse
            if response.status_code == 200:
                _logger.info(f'Réponse brute: {response.text}')
                data = response.json()
                _logger.info(f'Données JSON parsées: {data}')
                
                self.write({
                    'tokens_total': data.get('tokens_total', 0),
                    'tokens_used': data.get('tokens_used', 0),
                    'expiry_date': data.get('expiry_date'),
                    'status': 'active',
                    'last_sync': fields.Datetime.now(),
                })
                
                _logger.info(f'Mise à jour réussie - Tokens total: {data.get("tokens_total", 0)}, utilisés: {data.get("tokens_used", 0)}')
                _logger.info('FIN APPEL API /api/account/info')
                _logger.info('='*50)
                
                # Envoi de la télémétrie après un test de connexion réussi
                try:
                    self.send_telemetry()
                except Exception as telemetry_error:
                    _logger.warning(f'Erreur télémétrie (non bloquante): {telemetry_error}')
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Connexion réussie !'),
                        'message': _('Token valide. Quota: %s tokens restants.') % self.tokens_remaining,
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                self.status = 'invalid_token'
                raise UserError(_('Token invalide ou expiré. Code: %s') % response.status_code)
                
        except requests.exceptions.RequestException as e:
            _logger.error(f'Erreur de connexion API: {e}')
            raise UserError(_('Impossible de se connecter au service IA. Vérifiez votre connexion internet.'))
    
    def sync_quota(self):
        """Synchronise le quota avec le serveur"""
        self.ensure_one()
        
        # Vérification du token (comme dans ask_ai)
        if not self.user_token:
            raise UserError(_('Veuillez saisir un token client valide.'))
        
        try:
            # Logs détaillés pour l'appel API
            _logger.info('='*50)
            _logger.info(f'DÉBUT SYNCHRONISATION QUOTA - APPEL API /api/account/info')
            _logger.info(f'Token utilisé: {self.user_token[:5]}...{self.user_token[-5:] if len(self.user_token) > 10 else self.user_token}')
            _logger.info(f'URL complète: {self.api_endpoint}/account/info')
            _logger.info(f'Méthode: GET')
            
            headers = {
                'Authorization': f'Bearer {self.user_token}',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'User-Agent': 'Odoo/Copilot4Odoo-Client'
            }
            
            _logger.info(f'Headers envoyés: {headers}')
            
            # Envoi de la requête avec mesure du temps
            import time
            start_time = time.time()
            
            response = requests.get(
                f'{self.api_endpoint}/account/info',
                headers=headers,
                timeout=10
            )
            
            elapsed_time = time.time() - start_time
            _logger.info(f'Temps de réponse: {elapsed_time:.2f} secondes')
            _logger.info(f'Code de statut: {response.status_code}')
            _logger.info(f'Headers de réponse: {dict(response.headers)}')
            
            # Traitement de la réponse
            if response.status_code == 200:
                _logger.info(f'Réponse brute: {response.text}')
                data = response.json()
                _logger.info(f'Données JSON parsées: {data}')
                
                # Valeurs avant mise à jour
                old_tokens_total = self.tokens_total
                old_tokens_used = self.tokens_used
                
                # Mise à jour des données (comme dans ask_ai)
                self.write({
                    'tokens_total': data.get('tokens_total', 0),
                    'tokens_used': data.get('tokens_used', 0),
                    'expiry_date': data.get('expiry_date'),
                    'status': 'active',
                    'last_sync': fields.Datetime.now(),
                })
                
                _logger.info(f'Mise à jour réussie:')
                _logger.info(f'- Tokens total: {old_tokens_total} -> {data.get("tokens_total", 0)}')
                _logger.info(f'- Tokens utilisés: {old_tokens_used} -> {data.get("tokens_used", 0)}')
                _logger.info(f'- Tokens restants: {data.get("tokens_total", 0) - data.get("tokens_used", 0)}')
                _logger.info('FIN SYNCHRONISATION QUOTA')
                _logger.info('='*50)
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Synchronisation réussie !'),
                        'message': _('Quota synchronisé. Tokens restants: %s') % self.tokens_remaining,
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                self.status = 'invalid_token'
                raise UserError(_('Token invalide ou expiré. Code: %s') % response.status_code)
                
        except requests.exceptions.RequestException as e:
            _logger.error(f'Erreur de synchronisation du quota: {e}')
            raise UserError(_('Impossible de se connecter au service IA. Vérifiez votre connexion internet.'))
    
    def ask_ai(self, prompt, context=None, module_name=None):
        """
        Méthode principale pour interroger l'IA
        
        :param prompt: Question/instruction pour l'IA
        :param context: Contexte métier (dict avec données Odoo)
        :param module_name: Nom du module appelant (crm, hr, stock, etc.)
        :return: Réponse de l'IA
        """
        self.ensure_one()
        
        if self.status != 'active':
            raise UserError(_('Service IA non disponible. Statut: %s') % self.status)
        
        if self.tokens_remaining <= 0:
            raise UserError(_('Quota de tokens épuisé. Rechargez vos crédits IA.'))
        
        try:
            headers = {
                'Authorization': f'Bearer {self.user_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'token': self.user_token,  # Ajout du token dans le payload
                'model': self.selected_model,
                'messages': [{
                    'role': 'user',
                    'content': prompt
                }],
                'context': context or {},
                'module_name': module_name,  # Utiliser module_name pour cohérence avec le backend
                'odoo_version': release.version,
            }
            
            # Enregistrer le temps de début pour calculer le temps de réponse
            start_time = time.time()
            
            response = requests.post(
                f'{self.api_endpoint}/chat/completion',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Calculer le temps de réponse
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if not isinstance(data, dict):
                        _logger.error(f'Réponse API non-JSON: {response.text[:200]}')
                        raise UserError(_('Réponse API invalide (non-JSON)'))
                except (json.JSONDecodeError, ValueError) as e:
                    _logger.error(f'Erreur parsing JSON: {e}, Réponse: {response.text[:200]}')
                    raise UserError(_('Réponse API invalide (JSON malformé)'))
                
                # Extraction de la réponse IA (format OpenAI standard)
                ai_response = ''
                if 'choices' in data and len(data['choices']) > 0:
                    choice = data['choices'][0]
                    if 'message' in choice and 'content' in choice['message']:
                        ai_response = choice['message']['content']
                
                if not ai_response:
                    # Fallback sur l'ancien format si disponible
                    ai_response = data.get('response', '')
                
                if not ai_response:
                    _logger.error(f'Aucune réponse IA trouvée dans: {data}')
                    raise UserError(_('Réponse IA vide ou format invalide.'))
                
                # Mise à jour du quota (format OpenAI ou ancien format)
                tokens_consumed = 0
                if 'usage' in data:
                    tokens_consumed = data['usage'].get('total_tokens', 0)
                else:
                    tokens_consumed = data.get('tokens_used', 0)
                
                self.tokens_used += tokens_consumed
                
                # Log de l'usage
                # Déterminer le nom du module correctement
                real_module_name = module_name
                if not real_module_name:
                    # Essayer de déterminer le module appelant
                    stack = inspect.stack()
                    for frame in stack:
                        if 'copilot_' in frame.filename and 'copilot_core' not in frame.filename:
                            # Extraire le nom du module depuis le chemin
                            module_path = frame.filename.split('/')[-3] if '/' in frame.filename else frame.filename.split('\\')[-3]
                            if module_path.startswith('copilot_'):
                                real_module_name = module_path.replace('copilot_', '')
                                break
                
                # Créer l'entrée de log avec le module correct et le temps de réponse
                self.env['copilot.usage'].create({
                    'config_id': self.id,
                    'prompt': prompt[:500],  # Tronqué pour la DB
                    'response': ai_response[:1000],
                    'tokens_used': tokens_consumed,
                    'model_used': self.selected_model,
                    'module_name': real_module_name or 'core',  # Utiliser 'core' comme fallback
                    'response_time': response_time,  # Ajouter le temps de réponse en secondes
                })
                
                return ai_response
            
            elif response.status_code == 402:
                self.status = 'quota_exceeded'
                raise UserError(_('Quota de tokens épuisé. Rechargez vos crédits IA.'))
            
            elif response.status_code == 401:
                self.status = 'invalid_token'
                raise UserError(_('Token invalide ou expiré.'))
            
            else:
                raise UserError(_('Erreur API: %s') % response.text)
                
        except requests.exceptions.RequestException as e:
            _logger.error(f'Erreur appel IA: {e}')
            raise UserError(_('Erreur de connexion au service IA.'))
    
    def get_available_models(self):
        """Récupère la liste des modèles disponibles depuis l'API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.user_token}',
                'Content-Type': 'application/json'
            }
            
            
            response = requests.get(
                f'{self.api_endpoint}/auth/verify-token',
                json={'token': self.user_token},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('models', [])
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def check_installed_copilots(self):
        """Vérifie et met à jour la liste des modules Copilot installés et disponibles"""
        self.ensure_one()
        
        try:
            import requests
            import json
            import logging
            _logger = logging.getLogger(__name__)
            
            # Récupération des modules Odoo installés
            installed_modules_obj = self.env['ir.module.module'].search([
                ('name', 'like', 'copilot_%'),
                ('state', '=', 'installed')
            ])
            
            # Formatage de l'affichage des modules installés (texte)
            if installed_modules_obj:
                installed_text = "Modules Copilot installés:\n\n"
                
                for module in installed_modules_obj:
                    installed_text += f"• {module.shortdesc} (v{module.latest_version})\n"
            else:
                installed_text = "Aucun module Copilot installé.\n\nCliquez sur 'Découvrir les Modules' pour explorer les modules disponibles."
            
            # Formatage de l'affichage des modules installés (HTML)
            if installed_modules_obj:
                installed_html = "<div class='alert alert-success'>\n"
                installed_html += "<h4>Modules Copilot installés</h4>\n"
                installed_html += "<ul class='list-group'>\n"
                
                for module in installed_modules_obj:
                    installed_html += f"<li class='list-group-item'><strong>{module.shortdesc}</strong> - Version {module.latest_version}</li>\n"
                
                installed_html += "</ul>\n</div>"
            else:
                installed_html = "<div class='alert alert-warning'>\n"
                installed_html += "<p>Aucun module Copilot installé.</p>\n"
                installed_html += "<p>Cliquez sur 'Découvrir les Modules' pour explorer les modules disponibles.</p>\n"
                installed_html += "</div>"
            
            # Mise à jour des champs des modules installés
            self.write({
                'installed_modules': installed_text,
                'installed_modules_html': installed_html
            })
            
            # Récupération de l'endpoint API configuré ou utilisation d'une valeur par défaut
            endpoint = self.api_endpoint or "https://www.copilot4odoo.com"
            url = f"{endpoint}/api/modules/list"
            
            _logger.info(f"Récupération des modules disponibles depuis {url}")
            
            # Tentative de récupération des modules disponibles depuis l'API
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    available_modules = data.get('modules', [])
                    _logger.info(f"Modules disponibles récupérés: {len(available_modules)}")
                    
                    # Filtrage pour ne pas afficher copilot_core dans les modules disponibles
                    available_modules = [m for m in available_modules if m.get('name') != 'copilot_core']
                    
                    # Formatage de l'affichage des modules disponibles
                    if available_modules:
                        available_text = "Modules Copilot disponibles:\n\n"
                        
                        for module in available_modules:
                            available_text += f"• {module.get('display_name')} - {module.get('description')}\n"
                    else:
                        available_text = "Aucun module Copilot disponible actuellement."
                    
                    # Si le champ available_modules existe, le mettre à jour
                    if hasattr(self, 'available_modules'):
                        self.write({
                            'available_modules': available_text
                        })
                else:
                    _logger.warning(f"Erreur lors de la récupération des modules: {response.status_code}")
            except Exception as e:
                _logger.error(f"Exception lors de la récupération des modules disponibles: {str(e)}")
                # Ne pas bloquer le processus si la récupération des modules disponibles échoue
            
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
            
        except Exception as e:
            _logger.error(f"Exception lors de la récupération des modules installés: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur',
                    'message': f"Exception lors de la récupération des modules: {str(e)}",
                    'type': 'danger',
                }
            }
    
    def open_buy_credits(self):
        """Ouvre la page d'achat de crédits IA"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://www.copilot4odoo.com/buy-credits?token={self.user_token}',
            'target': 'new',
        }
    
    def open_copilot_store(self):
        """Ouvre le store des modules copilot"""
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.copilot4odoo.com/modules',
            'target': 'new',
        }
        
    def refresh_available_modules(self):
        """Récupère la liste des modules Copilot disponibles depuis l'API et met à jour l'affichage"""
        self.ensure_one()
        
        # Récupération de la liste des modules disponibles depuis l'API
        try:
            import requests
            import json
            import logging
            _logger = logging.getLogger(__name__)
            
            # Récupération de l'endpoint API configuré ou utilisation d'une valeur par défaut
            endpoint = self.api_endpoint or "https://www.copilot4odoo.com"
            url = f"{endpoint}/api/modules/list"
            
            _logger.info(f"Récupération des modules disponibles depuis {url}")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                available_modules = data.get('modules', [])
                _logger.info(f"Modules disponibles récupérés: {len(available_modules)}")
                
                # Format de l'affichage
                if available_modules:
                    modules_text = "Modules Copilot disponibles:\n\n"
                    
                    for module in available_modules:
                        if module.get('name') != 'copilot_core':
                            modules_text += f"• {module.get('display_name')} - {module.get('description')}\n"
                    
                    # Mise à jour du champ
                    self.write({'available_modules': modules_text})
                    
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
            else:
                _logger.warning(f"Erreur lors de la récupération des modules: {response.status_code}")
                # Message d'erreur
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Erreur',
                        'message': f"Impossible de récupérer les modules disponibles (code {response.status_code})",
                        'type': 'warning',
                    }
                }
        except Exception as e:
            _logger.error(f"Exception lors de la récupération des modules: {str(e)}")
            # Message d'erreur
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur',
                    'message': f"Exception lors de la récupération des modules: {str(e)}",
                    'type': 'danger',
                }
            }
            
    def get_available_modules(self):
        """Récupère la liste des modules Copilot disponibles depuis l'API"""
        self.ensure_one()
        
        # Récupération de la liste des modules disponibles depuis l'API
        try:
            import requests
            import json
            import logging
            _logger = logging.getLogger(__name__)
            
            # Récupération de l'endpoint API configuré ou utilisation d'une valeur par défaut
            endpoint = self.api_endpoint or "https://www.copilot4odoo.com"
            url = f"{endpoint}/api/modules/list"
            
            _logger.info(f"Récupération des modules disponibles depuis {url}")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                available_modules = data.get('modules', [])
                _logger.info(f"Modules disponibles récupérés: {len(available_modules)}")
                return available_modules
            else:
                _logger.warning(f"Erreur lors de la récupération des modules: {response.status_code}")
                # Fallback sur une liste minimale en cas d'erreur
                return [
                    {
                        'name': 'copilot_crm',
                        'display_name': 'Copilot CRM',
                        'description': 'Assistant pour ventes, leads et devis',
                        'category': 'CRM'
                    },
                    {
                        'name': 'copilot_hr',
                        'display_name': 'Copilot RH',
                        'description': 'Gestion employés, congés et contrats',
                        'category': 'HR'
                    }
                ]
        except Exception as e:
            _logger.error(f"Exception lors de la récupération des modules: {str(e)}")
            # Fallback sur une liste minimale en cas d'erreur
            return [
                {
                    'name': 'copilot_crm',
                    'display_name': 'Copilot CRM',
                    'description': 'Assistant pour ventes, leads et devis',
                    'category': 'CRM'
                },
                {
                    'name': 'copilot_hr',
                    'display_name': 'Copilot RH',
                    'description': 'Gestion employés, congés et contrats',
                    'category': 'HR'
                }
            ]
        
    def check_installed_copilots(self):
        """Vérifie quels modules Copilot sont installés et met à jour le champ installed_modules"""
        self.ensure_one()
        
        # Récupération de la liste des modules disponibles depuis l'API
        try:
            import requests
            import json
            import logging
            _logger = logging.getLogger(__name__)
            
            # Récupération de l'endpoint API configuré ou utilisation d'une valeur par défaut
            endpoint = self.api_endpoint or "https://www.copilot4odoo.com"
            url = f"{endpoint}/api/modules/list"
            
            _logger.info(f"Récupération des modules disponibles depuis {url}")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                copilot_modules = [module['name'] for module in data.get('modules', [])]
                _logger.info(f"Modules disponibles récupérés: {len(copilot_modules)}")
            else:
                _logger.warning(f"Erreur lors de la récupération des modules: {response.status_code}")
                # Fallback sur une liste minimale en cas d'erreur
                copilot_modules = [
                    'copilot_core'
                ]
        except Exception as e:
            _logger.error(f"Exception lors de la récupération des modules: {str(e)}")
            # Fallback sur une liste minimale en cas d'erreur
            copilot_modules = [
                'copilot_core'
            ]
        
        # Vérification des modules installés
        installed_modules = []
        module_obj = self.env['ir.module.module']
        
        for module_name in copilot_modules:
            module = module_obj.search([('name', '=', module_name)], limit=1)
            if module and module.state == 'installed':
                installed_modules.append(module_name)
        
        # Format de l'affichage
        if installed_modules:
            modules_info = "\n".join([f"- {module}" for module in installed_modules])
            modules_count = len(installed_modules)
            modules_text = f"Modules Copilot installés ({modules_count}):\n{modules_info}"
        else:
            modules_text = "Aucun module Copilot supplémentaire installé."
        
        # Mise à jour du champ
        self.write({'installed_modules': modules_text})
        
        return True
    
    def get_module_version(self):
        """Récupère la version du module copilot_core installé"""
        module = self.env['ir.module.module'].search([('name', '=', 'copilot_core'), ('state', '=', 'installed')], limit=1)
        return module.latest_version if module else 'Version non disponible'
    
    @api.model
    def action_open_dashboard(self):
        """Ouvre le dashboard avec l'enregistrement de configuration existant"""
        config = self.get_config()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Dashboard Copilot IA'),
            'res_model': 'copilot.config',
            'res_id': config.id,
            'view_mode': 'form',
            'view_id': self.env.ref('copilot_core.view_copilot_dashboard').id,
            'target': 'current',
            'context': {'form_view_initial_mode': 'readonly'},
        }
    
    def send_telemetry(self):
        """Envoie les données de télémétrie vers l'API du website"""
        try:
            # Collecte des informations système
            odoo_version = release.version
            copilot_version = self.get_module_version()
            
            # Informations utilisateur (si disponibles)
            user = self.env.user
            company = user.company_id
            
            # Hash du token pour identifier les installations sans exposer le token
            user_token_hash = None
            if self.user_token:
                user_token_hash = hashlib.sha256(self.user_token.encode()).hexdigest()
            
            # Préparation des données de télémétrie
            telemetry_data = {
                'odoo_version': odoo_version,
                'copilot_version': copilot_version,
                'user_email': user.email if user.email else None,
                'user_name': user.name if user.name else None,
                'company_name': company.name if company.name else None,
                'company_country': company.country_id.name if company.country_id else None,
                'installation_date': datetime.now().isoformat(),
                'user_token_hash': user_token_hash,
                'server_info': {
                    'database_name': self.env.cr.dbname,
                    'server_version': release.version_info,
                    'language': self.env.context.get('lang', 'en_US'),
                    'timezone': self.env.context.get('tz', 'UTC')
                }
            }
            
            # Envoi vers l'API de télémétrie
            telemetry_url = 'https://copilot4odoo.com/api/telemetry'
            
            _logger.info(f'Envoi des données de télémétrie vers {telemetry_url}')
            _logger.info(f'Données: Odoo v{odoo_version}, Copilot v{copilot_version}, User: {user.email or "N/A"}')
            
            response = requests.post(
                telemetry_url,
                json=telemetry_data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': f'Odoo-Copilot/{copilot_version}'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                _logger.info(f'Télémétrie envoyée avec succès: {result.get("message", "OK")}')
                return True
            else:
                _logger.warning(f'Erreur lors de l\'envoi de la télémétrie: {response.status_code}')
                return False
                
        except Exception as e:
            _logger.error(f'Erreur lors de l\'envoi de la télémétrie: {e}')
            return False
