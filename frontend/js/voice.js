class VoiceController {
    constructor() {
        this.isListening = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.voiceBtn = document.getElementById('voiceBtn');
        this.voiceTranscript = document.getElementById('voiceTranscript');
        this.init();
    }

    init() {
        this.voiceBtn.addEventListener('click', () => this.toggleListening());
    }

    async toggleListening() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    async startListening() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                await this.processAudio(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };

            this.mediaRecorder.start();
            this.isListening = true;
            this.voiceBtn.classList.add('listening');
            this.voiceBtn.textContent = '🎤 Listening...';
            this.voiceTranscript.textContent = 'Listening for command...';
        } catch (error) {
            console.error('Microphone error:', error);
            this.voiceTranscript.textContent = '❌ Microphone access denied';
        }
    }

    stopListening() {
        if (this.mediaRecorder) {
            this.mediaRecorder.stop();
            this.isListening = false;
            this.voiceBtn.classList.remove('listening');
            this.voiceBtn.textContent = '🎤 Start Listening';
        }
    }

    async processAudio(audioBlob) {
        this.voiceTranscript.textContent = 'Processing audio...';
        const result = await apiClient.uploadVoice(audioBlob);
        
        if (result.success && result.transcribed_text) {
            this.voiceTranscript.textContent = `You said: "${result.transcribed_text}"`;
            // Process the command
            window.chatInterface.sendCommand(result.transcribed_text, 'voice');
        } else {
            this.voiceTranscript.textContent = '❌ Could not understand audio';
        }
    }
}

const voiceController = new VoiceController();
