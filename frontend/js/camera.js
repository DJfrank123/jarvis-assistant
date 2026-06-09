class CameraController {
    constructor() {
        this.canvas = document.getElementById('cameraCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.ws = null;
        this.isConnected = false;
        this.init();
    }

    init() {
        this.connectWebSocket();
    }

    connectWebSocket() {
        try {
            this.ws = apiClient.connectWebSocket('/ws/camera');
            
            this.ws.onopen = () => {
                console.log('✅ Camera WebSocket connected');
                this.isConnected = true;
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'frame') {
                    this.renderFrame(data.data);
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
            
            this.ws.onclose = () => {
                console.log('Camera WebSocket closed');
                this.isConnected = false;
                // Reconnect after 3 seconds
                setTimeout(() => this.connectWebSocket(), 3000);
            };
        } catch (error) {
            console.error('Failed to connect camera WebSocket:', error);
        }
    }

    renderFrame(frameData) {
        if (!frameData.frame) return;
        
        const img = new Image();
        img.src = 'data:image/jpeg;base64,' + frameData.frame;
        
        img.onload = () => {
            this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
            
            // Draw hand detection data if available
            if (frameData.hand_data && frameData.hand_data.hands) {
                this.drawHandData(frameData.hand_data);
            }
        };
    }

    drawHandData(handData) {
        const handCount = document.getElementById('handCount');
        handCount.textContent = handData.hands.length;
        
        handData.hands.forEach((hand, idx) => {
            hand.landmarks.forEach((landmark, i) => {
                const x = landmark.x * this.canvas.width;
                const y = landmark.y * this.canvas.height;
                
                this.ctx.fillStyle = '#00ff00';
                this.ctx.beginPath();
                this.ctx.arc(x, y, 4, 0, Math.PI * 2);
                this.ctx.fill();
            });
        });
    }
}

const cameraController = new CameraController();
