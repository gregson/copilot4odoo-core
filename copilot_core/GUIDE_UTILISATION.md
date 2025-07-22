# 🚀 User Guide - Copilot AI Core

## What you should see after installation

Once the Copilot AI Core module is properly installed and configured, here is what you should see in your Odoo interface:

### 1. 📋 Main Menu "Copilot AI"

In the main Odoo navigation bar, you should see a new menu **"Copilot AI"** with the following sub-menus:

- **📊 Dashboard** - Main dashboard
- **⚙️ Configuration** - Settings and configuration
- **📈 Usage** - History and statistics
- **🛍️ Store** - Available Copilot modules

### 2. 🤖 Copilot Widget in the system bar

In the top right corner of your Odoo interface, next to other system icons, you should see:
- **Copilot Icon** (🤖) - Quick access to AI features
- **Token Indicator** - Display of remaining tokens
- **Connection Status** - Green if connected, red if there's an issue

### 3. 📊 Copilot Dashboard

Accessible via the main menu, the dashboard displays:

#### General Statistics
- **Available Tokens** vs **Consumed Tokens**
- **Number of requests** this month
- **Average response time** of AIs
- **Active modules** using AI

#### Charts
- **Daily consumption** (line chart)
- **Distribution by module** (pie chart)
- **Performance evolution** (trend chart)

#### Quick Actions
- **Test AI connection**
- **Purchase tokens**
- **Configure a new model**
- **View detailed history**

### 4. ⚙️ Configuration

In the Configuration section, you will find:

#### General Settings
- **Client Token** - Your unique access key
- **Selected AI Model** - GPT-4, Claude, Mixtral, etc.
- **API Endpoint** - Service URL (automatic)
- **Timeout** - Request timeout period

#### Token Management
- **Current Balance** - Available tokens
- **Purchase History** - Past transactions
- **Alerts** - Notification thresholds
- **Auto-recharge** - Automatic token purchase

#### Available Models
List of AI models with:
- **Name and provider**
- **Cost per token**
- **Response speed**
- **Recommended use cases**

### 5. 📈 Usage

The Usage section allows you to:

- **View the complete history** of AI interactions
- **Filter by module** (CRM, HR, Stock, etc.)
- **Filter by period** (day, week, month)
- **Analyze costs** by department/user
- **Export data** (CSV, XLS)

#### Filters and Search
- **By date** (today, this week, this month)
- **By module** (CRM, HR, Accounting, etc.)
- **By user**
- **By AI model used**

### 6. 🛍️ Store

The Copilot Store allows you to:

- **Discover** available specialized modules
- **Purchase** new modules directly
- **Update** your existing modules
- **Manage your licenses** and subscriptions

#### For each module
- **Detailed description**
- **Main features**
- **Price and conditions**
- **Installation button**
- **Online demo**

### 7. 🔧 Integrations into Existing Modules

Once configured, you will see AI buttons in:

#### CRM Module
- **"Summarize this lead"** on lead sheets
- **"Generate a quote"** automatically
- **"Score this lead"** with AI
- **"Suggest actions"** commercially

#### HR Module
- **"Analyze this employee profile"**
- **"Generate a contract"** automatically
- **"Summarize evaluations"**
- **"Predict vacations"**

#### Stock Module
- **"Predict stockouts"**
- **"Optimize orders"**
- **"Analyze trends"**

## 🚨 Troubleshooting Current Issue

If you see an error "Missing template: copilot_core.CopilotWidget", it means that Odoo has not yet reloaded the JavaScript/XML assets.

### Recommended Solution

1. **Completely stop Odoo**
   ```bash
   # Stop the Odoo process
   Ctrl+C in the terminal where Odoo is running
   ```

2. **Restart Odoo forcing asset update**
   ```bash
   cd C:\odoo18\server
   python odoo-bin -c odoo.conf -d odoo -u copilot_core --dev=reload
   ```

3. **Alternative: Clear asset cache**
   ```bash
   # Remove asset cache
   rm -rf C:\odoo18\server\odoo\addons\web\static\src\legacy\js\libs\
   
   # Then restart normally
   python odoo-bin -c odoo.conf -d odoo
   ```

4. **As a last resort: Developer Mode**
   - Activate developer mode in Odoo
   - Go to **Settings > Technical > User Interface > Views**
   - Search for "copilot" and delete views in error
   - Update the module

### Verification of Proper Functioning

Once the issue is resolved, you should:

1. ✅ **See the "Copilot AI" menu** in the navigation
2. ✅ **Access the dashboard** without error
3. ✅ **See the Copilot widget** in the top right
4. ✅ **Be able to configure** your API token
5. ✅ **Test the connection** with the AI

## 📞 Support

If the issue persists:

- **Email**: support@copilot4odoo.com
- **Documentation**: [Detailed Installation Guide](INSTALLATION.md)
- **Odoo Logs**: Check logs for specific errors

## 🎯 Next Steps

Once the module is configured, it brings artificial intelligence directly into your Odoo business processes!

## Main Features

### 🔑 Token Management

1. **Get a Client Token**
   - Register on [copilot4odoo.com](https://copilot4odoo.com)
   - Purchase an initial token pack
   - Copy your unique client token

2. **Configure the Token**
   - Paste your token in the Configuration section
   - Click on "Validate Token"
   - Verify that the status turns green

3. **Manage your Balance**
   - Monitor your consumption in the Dashboard
   - Configure low threshold alerts
   - Purchase additional tokens as needed
