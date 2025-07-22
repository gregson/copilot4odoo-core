# 🤖 Copilot AI Core for Odoo

> **IMPORTANT: Compatible with Odoo 18+ only**

## Description

Copilot AI Core is the central module that brings artificial intelligence directly into your Odoo ERP. It provides the necessary infrastructure for all specialized Copilot modules and allows you to easily manage your interactions with different AI models.

## ✨ Main Features

### 🧠 Multi-AI Models
- Support for GPT-4, GPT-3.5, Claude 3, Mixtral, Mistral, Command R
- Free open-source models for testing
- Flexible choice based on your needs and budget

### 🔐 Security & Privacy
- Secure token storage in Odoo
- Support for on-premise models (Ollama)
- GDPR compliance
- No data stored on the editor side

### 💰 Quota Management
- Transparent token system
- Real-time quota alerts
- Complete consumption history
- Integrated credit purchase

### 📊 Intuitive Interface
- Complete dashboard with statistics
- Simple and guided configuration
- Integrated store to discover modules
- Widget in the system bar

## 🚀 Installation

📋 **[Detailed Installation Guide](INSTALLATION.md)** - Check this guide for step-by-step installation with common troubleshooting.

### Quick Installation

1. **Install Python Dependencies**
   ```bash
   pip install psutil rjsmin
   ```

2. **Copy the Module**
   ```bash
   # Linux/Mac
   cp -r copilot_core /path/to/odoo/addons/
   
   # Windows
   xcopy copilot_core C:\odoo18\server\odoo\addons\copilot_core /E /I /Y
   ```

3. **Restart Odoo and Install**
   - Restart your Odoo server
   - Go to Apps > Search for "Copilot AI Core"
   - Click on "Activate"

4. **Initial Configuration**
   - Go to Copilot AI > Configuration
   - Enter your client token (obtained from copilot4odoo.com)
   - Choose your preferred AI model
   - Test the connection

## 🔧 Configuration

### Getting an AI Token

1. Visit [copilot4odoo.com](https://copilot4odoo.com)
2. Create an account or log in
3. Purchase an AI token pack
4. Copy your unique client token

### AI Model Selection

| Model | Provider | Cost | Recommended Use |
|--------|-------------|------|------------------|
| GPT-4 Turbo | OpenAI | €€€ | Complex tasks, analysis |
| GPT-3.5 Turbo | OpenAI | € | General use, fast |
| Claude 3 Opus | Anthropic | €€€ | Reasoning, analysis |
| Claude 3 Sonnet | Anthropic | €€ | Balance performance/cost |
| Mixtral 8x7B | Mistral | € | Open-source, economical |
| Nous Capybara | Open Source | Free | Testing, demos |

## 📦 Available Copilot Modules

### Copilot CRM (399€)
- Automatic prospect summaries
- Intelligent quote generation
- Lead scoring
- Sales action suggestions

### Copilot HR (399€)
- Employee profile analysis
- Contract generation
- Intelligent leave management
- HR file summaries

### Copilot Stock (399€)
- Stockout prediction
- Replenishment suggestions
- Trend analysis
- Stock optimization

### Copilot Accounting (399€)
- Automatic invoice generation
- Accounting anomaly detection
- Financial analysis
- Cash flow predictions

## 🛠️ API for Developers

### Basic Usage

```python
# In a specialized Copilot module
config = self.env['copilot.config'].get_config()
response = config.ask_ai(
    prompt="Summarize this customer",
    context={'client_name': 'Smith Inc', 'revenue': 50000},
    module_name='crm'
)
```

### Availability Check

```python
# Check if AI is available
from copilot_core.models.copilot_config import CopilotConfig

if config.status == 'active' and config.tokens_remaining > 0:
    # Use AI
    pass
```

### Context Formatting

```javascript
// JavaScript side
import { CopilotUtils } from '@copilot_core/js/copilot_widget';

const context = CopilotUtils.formatContext(record, ['name', 'email', 'phone']);
const response = await CopilotUtils.askAI(orm, prompt, context, 'crm');
```

## 📊 Monitoring and Analytics

### Dashboard
- Consumed vs available tokens
- Distribution by module
- Request history
- Average response time

### History
- All AI requests are tracked
- Prompts and responses preserved
- Technical metadata
- Automatic cleanup after 90 days

## 🔒 Security

### Data Storage
- Tokens stored in `ir.config_parameter` (encrypted)
- No sensitive data transmitted to the editor
- Local logs only

### Best Practices
- Use tokens with limited quotas
- Monitor your consumption
- Enable quota alerts
- Test with free models first

## 🆘 Support

### Documentation
- [Complete Documentation](https://copilot4odoo.com/docs)
- [Installation Guide](https://copilot4odoo.com/docs/installation)
- [API Reference](https://copilot4odoo.com/docs/api)

### Technical Support
- Email: support@copilot4odoo.com
- Discord: [Copilot4Odoo Community](https://discord.gg/copilot4odoo)
- GitHub: [Issues and bugs](https://github.com/copilot4odoo/core)

### FAQ

**Q: Is the Core module free?**
A: Yes, the Core module is completely free. You only pay for AI tokens and specialized modules.

**Q: Can I use my own API keys?**
A: No, to simplify management and ensure security, we manage AI calls through our proxy.

**Q: Is the data secure?**
A: Yes, your data never leaves your Odoo instance except for necessary AI calls.

**Q: Can I use on-premise models?**
A: Yes, with the "LLM Local" option you can connect Ollama or other local endpoints.

## 📄 License

This module is distributed under the LGPL-3 license. See the LICENSE file for more details.

## 🤝 Contribution

Contributions are welcome! Check out our [contribution guide](https://copilot4odoo.com/docs/contributing) to get started.

---

**Developed with ❤️ by the Copilot4Odoo team**

[Website](https://copilot4odoo.com) | [Documentation](https://copilot4odoo.com/docs) | [Support](https://copilot4odoo.com/support)
