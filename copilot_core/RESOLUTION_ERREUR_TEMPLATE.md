# 🔴 Resolving the Error "Missing template: copilot_core.CopilotWidget"

## Identified Problem

The error `Missing template: "copilot_core.CopilotWidget"` occurs because Odoo has cached the old version of the JavaScript widget that was registered in the systray, but the corresponding XML template has been temporarily disabled.

## ✅ Solutions in Order of Preference

### Solution 1: Complete Odoo Restart (RECOMMENDED)

1. **Stop Odoo completely**:
   ```bash
   # In the terminal where Odoo is running, press Ctrl+C
   # Wait for the process to completely terminate
   ```

2. **Clear the assets cache**:
   ```bash
   cd C:\odoo18\server
   # Remove the assets cache
   rm -rf filestore/odoo/assets/*
   # Or on Windows:
   rmdir /s filestore\odoo\assets
   ```

3. **Restart Odoo with forced update**:
   ```bash
   python odoo-bin -c odoo.conf -d odoo -u copilot_core --dev=reload
   ```

### Solution 2: Odoo Developer Mode

1. **Log in to Odoo** (temporarily ignore the error)
2. **Activate developer mode**:
   - Go to **Settings**
   - Click on **Activate developer mode**
3. **Clear the assets cache**:
   - Go to **Settings > Technical > User Interface > Assets**
   - Delete all assets containing "copilot"
4. **Reload the page** with Ctrl+F5

### Solution 3: Manual Module Update

1. **Go to Apps**
2. **Search for "Copilot AI Core"**
3. **Click on "Update"**
4. **Wait for the update to complete**
5. **Reload the page**

### Solution 4: Complete Reinstallation

1. **Uninstall the module**:
   - Apps > Copilot AI Core > Uninstall
2. **Restart Odoo**:
   ```bash
   python odoo-bin -c odoo.conf -d odoo
   ```
3. **Reinstall the module**:
   - Apps > Search for "Copilot" > Install

## 🔧 Widget Reactivation (After Resolution)

Once the error is resolved, you can reactivate the Copilot widget:

### Step 1: Restore the XML Template

```bash
cd c:\Users\gregs\Downloads\copilot4odoo
move copilot_core\static\src\xml\copilot_widget.xml.backup copilot_core\static\src\xml\copilot_widget.xml
```

### Step 2: Reactivate in the Manifest

Edit `copilot_core/__manifest__.py` and uncomment the line:

```python
'assets': {
    'web.assets_backend': [
        'copilot_core/static/src/js/copilot_widget.js',
        'copilot_core/static/src/css/copilot_style.css',
        'copilot_core/static/src/xml/copilot_widget.xml',  # Reactivated
    ],
},
```

### Step 3: Reactivate in JavaScript

Edit `copilot_core/static/src/js/copilot_widget.js` and uncomment:

```javascript
// Reactivate component registration
registry.category("systray").add("CopilotWidget", {
    Component: CopilotWidget,
    isDisplayed: () => true,
});
```

### Step 4: Update the Module

```bash
cd C:\odoo18\server
python odoo-bin -c odoo.conf -d odoo -u copilot_core
```

## 🎯 Verification of Proper Functioning

After resolution, you should see:

1. ✅ **No errors** in the browser console
2. ✅ **"Copilot AI" menu** in the main navigation
3. ✅ **Copilot widget** in the top right (🤖)
4. ✅ **Dashboard access** without errors
5. ✅ **Functional configuration**

## 📋 What You Should See

### Main Menu
- **Copilot AI** > Dashboard
- **Copilot AI** > Configuration  
- **Copilot AI** > Usage
- **Copilot AI** > Store

### Systray Widget
- 🤖 "Copilot AI" icon 
- Remaining tokens indicator
- Dropdown menu with quick actions

### Functional Dashboard
- Token statistics
- Usage graphs
- Configuration actions
- AI connection tests

## 🔴 If the Problem Persists

### Additional Checks

1. **Odoo Logs** - Check if there are other errors:
   ```bash
   tail -f /var/log/odoo/odoo.log
   ```

2. **File Permissions**:
   ```bash
   chmod -R 755 copilot_core/
   ```

3. **File Syntax** - Check that there are no syntax errors in:
   - `__manifest__.py`
   - `copilot_widget.js`
   - `copilot_widget.xml`

### Contact Support

If no solution works:

- **Email**: support@copilot4odoo.com
- **Include**: Odoo logs, Odoo version, steps already attempted
- **Attach**: Screenshot of the error

## 💡 Future Prevention

To avoid this problem in the future:

1. **Always test** JavaScript widgets before registering them
2. **Use developer mode** during development
3. **Clear the cache** after each asset modification
4. **Restart Odoo** after important changes

---

**Note**: This error is temporary and related to Odoo's cache. The Copilot AI Core module is correctly installed and functional, you just need to clear the cache to solve the problem.
