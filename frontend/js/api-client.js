class APIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.isConnected = false;
        this.checkConnection();
    }

    async checkConnection() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            this.isConnected = response.ok;
            console.log('✅ Connected to Jarvis backend');
        } catch (error) {
            this.isConnected = false;
            console.error('❌ Cannot connect to backend:', error);
        }
    }

    async getStatus() {
        try {
            const response = await fetch(`${this.baseURL}/api/status`);
            return await response.json();
        } catch (error) {
            console.error('Error getting status:', error);
            return null;
        }
    }

    async processCommand(command, type = 'text') {
        try {
            const response = await fetch(`${this.baseURL}/api/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, type })
            });
            return await response.json();
        } catch (error) {
            console.error('Error processing command:', error);
            return { success: false, error: error.message };
        }
    }

    async getAvailableApps() {
        try {
            const response = await fetch(`${this.baseURL}/api/apps`);
            return await response.json();
        } catch (error) {
            console.error('Error getting apps:', error);
            return { apps: [] };
        }
    }

    async launchApp(appName) {
        try {
            const response = await fetch(`${this.baseURL}/api/launch-app`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ app_name: appName })
            });
            return await response.json();
        } catch (error) {
            console.error('Error launching app:', error);
            return { success: false, error: error.message };
        }
    }

    async getHandData() {
        try {
            const response = await fetch(`${this.baseURL}/api/hand-data`);
            return await response.json();
        } catch (error) {
            console.error('Error getting hand data:', error);
            return null;
        }
    }

    async uploadVoice(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('file', audioBlob);
            const response = await fetch(`${this.baseURL}/api/voice-upload`, {
                method: 'POST',
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error('Error uploading voice:', error);
            return { success: false, error: error.message };
        }
    }

    connectWebSocket(path) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsURL = `${protocol}//${window.location.host}${path}`;
        return new WebSocket(wsURL);
    }
}

// Global API client instance
const apiClient = new APIClient();
