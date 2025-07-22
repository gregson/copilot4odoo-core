/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Widget Copilot IA pour l'interface utilisateur
 */
class CopilotWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        
        this.state = useState({
            isVisible: false,
            isLoading: false,
            config: null,
            quotaPercentage: 0,
            statusColor: 'success',
        });
        
        onMounted(() => {
            this.loadConfig();
            this.logModuleVersion();
        });
    }
    
    /**
     * Affiche la version du module dans les logs
     */
    async logModuleVersion() {
        try {
            const result = await this.orm.call(
                "copilot.config",
                "get_module_version",
                []
            );
            console.log(`Widget Copilot IA v${result} chargé et enregistré dans le systray`);
        } catch (error) {
            console.log("Widget Copilot IA chargé et enregistré dans le systray (version non disponible)");
        }
    }
    
    /**
     * Charge la configuration Copilot
     */
    async loadConfig() {
        try {
            const configs = await this.orm.searchRead(
                "copilot.config",
                [],
                ["user_token", "tokens_total", "tokens_used", "tokens_remaining", "status", "selected_model"],
                { limit: 1 }
            );
            
        if (configs.length > 0) {
            console.log("Configuration Copilot chargée :", configs[0]);
            this.state.config = configs[0];
            this.updateQuotaDisplay();
            console.log("user_token récupéré :", this.state.config.user_token);
        } else {
            console.log("Aucune configuration Copilot trouvée.");
        }
        } catch (error) {
            console.error("Erreur lors du chargement de la config Copilot:", error);
        }
    }
    
    /**
     * Met à jour l'affichage du quota
     */
    updateQuotaDisplay() {
        if (!this.state.config) return;
        
        const { tokens_total, tokens_used } = this.state.config;
        if (tokens_total > 0) {
            this.state.quotaPercentage = (tokens_used / tokens_total) * 100;
            
            // Couleur selon le pourcentage utilisé
            if (this.state.quotaPercentage < 50) {
                this.state.statusColor = 'success';
            } else if (this.state.quotaPercentage < 80) {
                this.state.statusColor = 'warning';
            } else {
                this.state.statusColor = 'danger';
            }
        }
    }
    
    /**
     * Teste la connexion IA
     */
    async testConnection() {
        console.log("Appel de la méthode testConnection()");
        if (!this.state.config) {
            console.log("Aucune configuration Copilot trouvée.");
            return;
        }
        
        console.log("Démarrage du chargement...");
        this.state.isLoading = true;
        try {
            console.log("Appel de la méthode test_connection() sur le serveur...");
            const result = await this.orm.call("copilot.config", "test_connection", [this.state.config.id]);
            console.log("Résultat de l'appel test_connection() :", result);
            console.log("Affichage de la notification de succès...");
            this.notification.add("Connexion IA réussie !", { type: "success" });
            await this.loadConfig(); // Recharge les données
        } catch (error) {
            console.error("Erreur lors de l'appel test_connection() :", error);
            this.notification.add("Erreur de connexion IA: " + error.message, { type: "danger" });
        } finally {
            console.log("Fin du chargement.");
            this.state.isLoading = false;
        }
    }
    
    /**
     * Synchronise le quota
     */
    async syncQuota() {
        console.log("Appel de la méthode syncQuota()");
        if (!this.state.config) {
            console.log("Aucune configuration Copilot trouvée.");
            return;
        }
        
        console.log("Démarrage de la synchronisation du quota...");
        this.state.isLoading = true;
        try {
            console.log("Appel de la méthode sync_quota() sur le serveur...");
            await this.orm.call("copilot.config", "sync_quota", [this.state.config.id]);
            console.log("Synchronisation du quota réussie.");
            this.notification.add("Quota synchronisé !", { type: "success" });
            await this.loadConfig();
        } catch (error) {
            console.error("Erreur lors de l'appel sync_quota() :", error);
            this.notification.add("Erreur de synchronisation: " + error.message, { type: "danger" });
        } finally {
            console.log("Fin de la synchronisation du quota.");
            this.state.isLoading = false;
        }
    }
    
    /**
     * Ouvre la page d'achat de crédits
     */
    async buyCredits() {
        if (!this.state.config) return;
        
        try {
            const action = await this.orm.call("copilot.config", "open_buy_credits", [this.state.config.id]);
            this.action.doAction(action);
        } catch (error) {
            this.notification.add("Erreur lors de l'ouverture de la page d'achat", { type: "danger" });
        }
    }
    
    /**
     * Ouvre le store des modules
     */
    async openStore() {
        if (!this.state.config) return;
        
        try {
            const action = await this.orm.call("copilot.config", "open_copilot_store", [this.state.config.id]);
            this.action.doAction(action);
        } catch (error) {
            this.notification.add("Erreur lors de l'ouverture du store", { type: "danger" });
        }
    }
    
    /**
     * Ouvre le dashboard Copilot
     */
    openDashboard() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Dashboard Copilot IA',
            res_model: 'copilot.config',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'current',
            context: { 'form_view_initial_mode': 'readonly' }
        });
    }
    
    /**
     * Toggle la visibilité du widget
     */
    toggleVisibility() {
        this.state.isVisible = !this.state.isVisible;
    }
    
    /**
     * Formate le nombre de tokens
     */
    formatTokens(tokens) {
        if (tokens >= 1000000) {
            return (tokens / 1000000).toFixed(1) + 'M';
        } else if (tokens >= 1000) {
            return (tokens / 1000).toFixed(1) + 'K';
        }
        return tokens.toString();
    }
    
    /**
     * Retourne la classe CSS pour le statut
     */
    getStatusClass() {
        if (!this.state.config) return 'secondary';
        
        switch (this.state.config.status) {
            case 'active': return 'success';
            case 'expired': return 'danger';
            case 'quota_exceeded': return 'warning';
            case 'invalid_token': return 'danger';
            default: return 'secondary';
        }
    }
}

CopilotWidget.template = "copilot_core.CopilotWidget";

// Enregistrement du composant dans le systray
registry.category("systray").add("CopilotWidget", {
    Component: CopilotWidget,
    isDisplayed: () => true,
});

// Version affichée dynamiquement dans logModuleVersion()

/**
 * Fonctions utilitaires pour les autres modules Copilot
 */
export class CopilotUtils {
    
    /**
     * Appelle l'IA avec un prompt et un contexte
     */
    static async askAI(orm, prompt, context = {}, moduleName = 'core') {
        try {
            const configs = await orm.searchRead("copilot.config", [], [], { limit: 1 });
            if (configs.length === 0) {
                throw new Error("Configuration Copilot non trouvée");
            }
            
            const response = await orm.call(
                "copilot.config", 
                "ask_ai", 
                [configs[0].id, prompt, context, moduleName]
            );
            
            return response;
        } catch (error) {
            console.error("Erreur appel IA:", error);
            throw error;
        }
    }
    
    /**
     * Vérifie si le service IA est disponible
     */
    static async isAIAvailable(orm) {
        try {
            const configs = await orm.searchRead(
                "copilot.config", 
                [['status', '=', 'active']], 
                ['tokens_remaining'], 
                { limit: 1 }
            );
            
            return configs.length > 0 && configs[0].tokens_remaining > 0;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Formate un contexte Odoo pour l'IA
     */
    static formatContext(record, fields = []) {
        if (!record) return {};
        
        const context = {
            model: record._name || 'unknown',
            id: record.id,
            display_name: record.display_name || record.name || 'Sans nom',
        };
        
        // Ajoute les champs spécifiés
        fields.forEach(field => {
            if (record[field] !== undefined) {
                context[field] = record[field];
            }
        });
        
        return context;
    }
    
    /**
     * Affiche une notification avec style Copilot
     */
    static showNotification(notification, message, type = 'info') {
        const title = type === 'success' ? '🤖 Copilot IA' : 
                     type === 'warning' ? '⚠️ Copilot IA' :
                     type === 'danger' ? '❌ Copilot IA' : 
                     '💡 Copilot IA';
        
        notification.add(message, {
            title: title,
            type: type,
            sticky: type === 'danger',
        });
    }
}

// Export pour utilisation dans d'autres modules
export { CopilotWidget, CopilotUtils };
