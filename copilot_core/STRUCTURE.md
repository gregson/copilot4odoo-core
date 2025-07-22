# Copilot AI Core Module Structure

```
copilot_core/
├── __init__.py                          # Module entry point
├── __manifest__.py                      # Module metadata and configuration
├── README.md                           # Complete documentation
├── STRUCTURE.md                        # This file - project structure
│
├── models/                             # Data models
│   ├── __init__.py                     # Models import
│   ├── copilot_config.py              # Main configuration and AI API
│   ├── copilot_usage.py               # Token usage history
│   └── copilot_models.py              # Available AI models catalog
│
├── views/                              # XML user interfaces
│   ├── copilot_config_views.xml       # Configuration views
│   ├── copilot_dashboard_views.xml    # Main dashboard
│   └── copilot_menu.xml               # Menu structure
│
├── security/                           # Access rights
│   └── ir.model.access.csv            # Permissions by user group
│
├── data/                               # Base data
│   └── copilot_models_data.xml        # Pre-configured AI models
│
└── static/                             # Static resources
    ├── description/                    # Module description
    │   ├── index.html                  # Presentation page
    │   └── icon.png                    # Module icon (to be created)
    │
    └── src/                            # Frontend code
        ├── css/
        │   └── copilot_style.css       # Custom CSS styles
        └── js/
            └── copilot_widget.js       # JavaScript widget and utilities
```

## 📋 Component Description

### 🗂️ Data Models

#### `copilot_config.py`
- **Role**: Central configuration of the AI system
- **Key functions**:
  - Client token management
  - API calls to AI models
  - Quota synchronization
  - Connection testing
  - Store opening and credit purchase

#### `copilot_usage.py`
- **Role**: Token usage tracking
- **Key functions**:
  - Recording AI requests
  - Cost calculation by model
  - Detailed interaction history
  - Usage reports
  - Quota alerts

#### `copilot_models.py`
- **Role**: Management of available AI models
- **Key functions**:
  - Definition of supported models
  - Default parameters
  - Costs and limits
  - Specific capabilities
  - Usage recommendations

### 🖥️ Interfaces Utilisateur

#### `copilot_config_views.xml`
- **Role**: Configuration interface
- **Main elements**:
  - Configuration form
  - API token fields
  - AI model selector
  - Advanced parameters
  - Test button

#### `copilot_dashboard_views.xml`
- **Role**: Main dashboard
- **Main elements**:
  - Statistics
  - Available modules cards
  - Quick actions
  - System information

#### `copilot_menu.xml`
- **Role**: Menu structure
- **Main elements**:
  - Main menu "Copilot AI"
  - Sub-menus (Dashboard, Configuration, etc.)
  - Associated actions
  - Security groups

### 📝 Development Notes

- The module is compatible only with Odoo 18+
- Uses the new JavaScript APIs of Odoo 18
- Requires Python 3.10+ for certain asynchronous features
- Follows Odoo code standards (OCA guidelines)

#### `copilot_widget.js`
- **Role**: JavaScript widget and utilities
- **Main functions**:
  - Widget in the system bar
  - Utilities for other modules
  - Client-side AI call management
  - Notifications and interactions

### 🔐 Security

#### `ir.model.access.csv`
- **Role**: Access rights management
- **Main elements**:
  - Read/write permissions by model
  - User/administrator separation
  - Protection of sensitive data

### 📂 Data de Base

#### `copilot_models_data.xml`
- **Role**: Pre-configured AI models
- **Main elements**:
  - Pre-configured models (GPT, Claude, Mixtral, etc.)
  - Costs and technical characteristics
  - Status and recommendations

## 🔄 Flux de Données

### 1. Configuration Initiale
```
User → Configuration → AI Token → Test Connection → Sync Quota
```

### Data Flow
1. **AI Request**: Specialized module → Core → External API
2. **Response**: External API → Core → Specialized module
3. **Tracking**: Recording in `copilot.usage`
4. **Quotas**: Verification and decrement

## 📈 Évolutivité

### Extensions Possibles
- Support de nouveaux modèles IA
- Intégration RAG (documents)
- Chat vocal (Whisper + TTS)
- Analytics avancés
- API webhooks

### Modular Architecture
- Core = Infrastructure
- Specialized modules = Business features
- API Proxy = Centralized token management
- Store = Distribution and monetization

## 🎯 Points Clés
### ✅ Avantages de cette Architecture
- **Séparation des responsabilités** : Core vs modules métier
- **Réutilisabilité** : API commune pour tous les modules
- **Sécurité** : Gestion centralisée des tokens
- **Monétisation** : Hub commercial intégré
- **Évolutivité** : Ajout facile de nouveaux modèles/modules

### 🔧 Maintenance
- **Logs centralisés** : Debugging facilité
- **Monitoring intégré** : Surveillance des performances
- **Updates automatiques** : Sync des modèles disponibles
- **Nettoyage automatique** : Gestion de l'espace disque

Cette architecture permet de créer un écosystème IA complet et évolutif pour Odoo, avec une expérience utilisateur fluide et une monétisation efficace.
