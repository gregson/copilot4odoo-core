---
# Poster dans le chatter avec l'auteur "Copilot IA"

Ce guide explique comment publier un message dans le chatter Odoo sous le nom "Copilot IA" (au lieu d'OdooBot) et comment réutiliser cette méthode dans vos modules.

## 1) Pré-requis: créer le partenaire "Copilot IA"
Créez un partenaire technique réutilisable par tous les modules. Idéalement dans `copilot_core` pour qu'il soit centralisé.

Exemple `data/copilot_data.xml`:
```xml
<odoo>
  <data noupdate="1">
    <record id="partner_copilot" model="res.partner">
      <field name="name">Copilot IA</field>
      <field name="email">no-reply@copilot.local</field>
      <field name="is_company" eval="False"/>
      <field name="active" eval="True"/>
    </record>
  </data>
</odoo>
```

- External ID recommandé: `copilot_core.partner_copilot` (si placé dans `copilot_core`).
- Si vous avez déjà un partenaire dans un autre module (ex: `copilot_hr.partner_copilot`), vous pouvez le réutiliser tel quel.

## 2) Poster un message dans le chatter avec cet auteur
Dans vos modèles, utilisez `message_post` en passant `author_id` avec le `partner_id` du partenaire "Copilot IA". Utilisez `sudo()` pour éviter des restrictions d'accès lors de l'imputation de l'auteur.

Exemple Python:
```python
from odoo import models, _, fields

class AnyModel(models.Model):
    _name = 'your.model'

    def post_copilot_message(self, body_html, subject=None):
        # 1. Récupérer le partenaire "Copilot IA"
        partner = self.env.ref('copilot_core.partner_copilot', raise_if_not_found=False)

        # 2. Poster dans le chatter avec cet auteur (fallback sur auteur courant si partenaire introuvable)
        self.sudo().message_post(
            body=body_html,
            subject=subject or _('Copilot IA'),
            author_id=partner.id if partner else False,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
```

Notes:
- `author_id` attend un `res.partner`.
- `message_type='comment'` et `subtype_xmlid='mail.mt_note'` postent une note simple.
- `sudo()` est conseillé pour garantir l'affectation de l'auteur.

## 3) Programmer une activité pour un utilisateur (optionnel)
Vous pouvez compléter par une activité assignée à un responsable.

```python
if getattr(record, 'user_id', False):
    record.activity_schedule(
        'mail.mail_activity_data_todo',
        user_id=record.user_id.id,
        summary=_('Action requise par Copilot IA'),
        note=_('Veuillez examiner la recommandation postée par Copilot IA.'),
        date_deadline=fields.Date.today(),
    )
```

## 4) Bonnes pratiques
- **Centraliser le partenaire** dans `copilot_core` et référencer: `self.env.ref('copilot_core.partner_copilot')`.
- **Fallback**: si le partenaire n'existe pas, poster sans `author_id` pour éviter une exception.
- **i18n**: utiliser `_()` pour les libellés.
- **Sécurité**: privilégier `sudo()` au moment du `message_post`.

## 5) Exemple complet (inspiré de `copilot_hr`)
```python
partner = self.env.ref('copilot_core.partner_copilot', raise_if_not_found=False)
msg = _("⚠️ Turnover risk alert for %s: score %s (level: %s).") % (self.name, int(score), level)
self.sudo().message_post(
    body=msg,
    subject=_('Turnover risk alert'),
    author_id=partner.id if partner else False,
    message_type='comment',
    subtype_xmlid='mail.mt_note',
)
```

En appliquant ce patron, tous vos modules peuvent publier des messages au nom de "Copilot IA" de façon homogène.
