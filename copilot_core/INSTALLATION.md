# Installation Guide - Copilot AI Core

## Prerequisites

1. **Odoo 18** installed and functional
2. **Python 3.8+** with pip
3. **Administrator access** to your Odoo server

## Automatic Installation (Recommended)

### Step 1: Download the module
```bash
# Download copilot_core from copilot4odoo.com and unzip the file

https://www.copilot4odoo.com/download
```

### Step 2: Install Python dependencies
```bash
# Install the required dependencies
pip install psutil rjsmin
```

### Step 3: Copy the module into Odoo
```bash
# Copy the module into Odoo's addons directory
# Replace /path/to/odoo with your Odoo installation path
cp -r copilot_core /path/to/odoo/addons/

# Or on Windows:
xcopy copilot_core C:\odoo18\server\odoo\addons\copilot_core /E /I /Y
```

### Step 4: Restart Odoo
```bash
# Restart your Odoo server
# Example for a standard installation:
cd /path/to/odoo
python odoo-bin -c odoo.conf -d your_database --stop-after-init

# Then restart normally:
python odoo-bin -c odoo.conf -d your_database
```

### Step 5: Install the module
1. Log in to your Odoo interface
2. Go to **Apps**
3. Search for "**Copilot AI Core**"
4. Click on **Activate**

## Manual Installation

### Step 1: Prepare the environment
```bash
# Create a virtual environment (recommended)
python -m venv copilot_env
source copilot_env/bin/activate  # Linux/Mac
copilot_env\Scripts\activate     # Windows

# Install dependencies
pip install psutil rjsmin requests
```

### Step 2: Clone the repository
```bash
# Clone the repository from GitHub
git clone https://github.com/copilot4odoo/copilot_core.git

# Or download manually from copilot4odoo.com
```

### Step 3: Module configuration
```bash
# Copy the module to Odoo's addons directory
cp -r copilot_core /path/to/odoo/addons/

# Make sure permissions are correct
chmod -R 755 /path/to/odoo/addons/copilot_core

# Or on Windows:
xcopy copilot_core C:\odoo18\server\odoo\addons\copilot_core /E /I /Y
```

### Step 4: Update the module list
1. Start Odoo in development mode
```bash
python odoo-bin -c odoo.conf -d your_database --dev=all
```

2. Log in to Odoo
3. Activate developer mode
4. Go to **Apps > Update Apps List**
5. Search for "Copilot AI Core"
6. Install the module

## Troubleshooting

### Issue: The module does not appear in the list
- Check that the module is correctly placed in the addons directory
- Update the apps list in developer mode
- Check folder permissions

### Issue: Error during installation
- Check the required Python dependencies
- Check Odoo logs for more details
- Make sure your Odoo version is 18 or higher

### Issue: Missing widget after installation
- Completely restart Odoo
- Clear your browser cache
- Try installing with the `--dev=all` option

## Post-Installation Configuration

### Step 1: Get a Client Token
1. Register on [copilot4odoo.com](https://copilot4odoo.com)
2. Purchase an initial token pack
3. Copy your unique client token

### Step 2: Configure the Module
1. In Odoo, go to the **Copilot AI > Configuration** menu
2. Paste your client token in the appropriate field
3. Select your preferred AI model
4. Click on "Validate Token" to verify the connection
5. Save your settings

### Step 3: Verify the Installation
1. Access the **Copilot Dashboard**
2. Check that your token balance is displayed correctly
3. Test the connection with the "Test AI" button
4. Verify that the Copilot widget is visible in the top right

## Module Update

### Automatic update
1. In Odoo, go to **Apps**
2. Click on **Update** next to Copilot AI Core

### Manual update
```bash
# Stop Odoo
# Replace module files
rm -rf /path/to/odoo/addons/copilot_core/*
cp -r /path/to/new/copilot_core/* /path/to/odoo/addons/copilot_core/

# Restart Odoo with module update
python odoo-bin -c odoo.conf -d your_database -u copilot_core
```

## Support and Resources

- **Complete documentation**: [docs.copilot4odoo.com](https://docs.copilot4odoo.com)
- **Technical support**: [support@copilot4odoo.com](mailto:support@copilot4odoo.com)
- **Community**: [forum.copilot4odoo.com](https://forum.copilot4odoo.com)
- **Video tutorials**: [youtube.com/copilot4odoo](https://youtube.com/copilot4odoo)

## Useful Commands

```bash
# Install the module via command line
python odoo-bin -c odoo.conf -d your_database -i copilot_core

# Update the module
python odoo-bin -c odoo.conf -d your_database -u copilot_core

# Uninstall the module
python odoo-bin -c odoo.conf -d your_database --uninstall copilot_core

# Debug mode with detailed logs
python odoo-bin -c odoo.conf -d your_database --log-level=debug
