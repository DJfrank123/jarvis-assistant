class ChatInterface {
    constructor() {
        this.messages = document.getElementById('messages');
        this.commandInput = document.getElementById('commandInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.historyList = document.getElementById('historyList');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.commandHistory = [];
        
        this.init();
    }

    init() {
        this.sendBtn.addEventListener('click', () => this.handleSendCommand());
        this.commandInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSendCommand();
        });
        
        // Quick action buttons
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => this.handleAction(btn));
        });
        
        // Update status
        this.updateStatus();
        setInterval(() => this.updateStatus(), 5000);
    }

    async handleSendCommand() {
        const command = this.commandInput.value.trim();
        if (!command) return;
        
        // Add user message to chat
        this.addMessage(command, 'user');
        this.commandInput.value = '';
        
        // Send command to backend
        await this.sendCommand(command, 'text');
    }

    async sendCommand(command, type = 'text') {
        const result = await apiClient.processCommand(command, type);
        
        if (result.success) {
            const response = result.response || result.data?.text || 'Command processed';
            this.addMessage(response, 'assistant');
            
            // Add to history
            this.addToHistory(command);
            
            // Handle actions
            if (result.action) {
                await this.handleAction(result);
            }
            
            // Handle 3D model requests
            if (result.data && result.data['3d_model_data']) {
                model3DViewer.createModel(result.data['3d_model_data'].type);
            }
        } else {
            this.addMessage(`❌ ${result.error || 'Command failed'}`, 'assistant');
        }
    }

    async handleAction(source) {
        let action, appName;
        
        if (source instanceof Event) {
            // Click from button
            action = source.currentTarget.dataset.action;
            appName = source.currentTarget.dataset.app;
        } else {
            // From API response
            action = source.action;
            appName = source.data?.app_name;
        }
        
        if (action === 'launch_app' && appName) {
            const result = await apiClient.launchApp(appName);
            if (result.success) {
                this.addMessage(`✅ Launched ${appName}`, 'assistant');
            } else {
                this.addMessage(`❌ Failed to launch ${appName}`, 'assistant');
            }
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `<p>${this.escapeHtml(text)}</p>`;
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }

    addToHistory(command) {
        this.commandHistory.unshift(command);
        if (this.commandHistory.length > 10) {
            this.commandHistory.pop();
        }
        
        // Update UI
        const li = document.createElement('li');
        li.textContent = command.substring(0, 30) + (command.length > 30 ? '...' : '');
        this.historyList.insertBefore(li, this.historyList.firstChild);
        
        // Keep only last 5 visible
        while (this.historyList.children.length > 5) {
            this.historyList.removeChild(this.historyList.lastChild);
        }
    }

    async updateStatus() {
        const status = await apiClient.getStatus();
        
        if (status) {
            this.statusDot.classList.add('online');
            this.statusText.textContent = 'Online';
            
            // Update individual statuses
            document.getElementById('voiceStatus').textContent = status.voice_enabled ? '✓' : '✗';
            document.getElementById('handDetectionStatus').textContent = status.hand_detection_enabled ? '✓' : '✗';
            document.getElementById('aiBrainStatus').textContent = status.ai_brain_connected ? '✓' : '✗';
        } else {
            this.statusDot.classList.remove('online');
            this.statusText.textContent = 'Offline';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global chat interface
let chatInterface;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    chatInterface = new ChatInterface();
    console.log('🤖 Jarvis AI Assistant UI loaded');
});
