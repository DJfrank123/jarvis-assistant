# Jarvis - Personal AI Computer Assistant

A voice-controlled, AI-powered personal assistant for your computer, inspired by Jarvis from Iron Man.

## Features

✨ **Core Capabilities:**
- 🎤 **Voice Commands**: Speak to control your computer
- 🤖 **Hand Detection & 3D Visualization**: Real-time hand tracking with 3D robotic hand overlay
- 🚀 **App Launcher**: Open applications by voice command
- 🧠 **AI Brain**: Powered by OpenAI GPT-4 or local LLM
- 📊 **Engineering & Math Support**: Assistance with calculations, problem-solving
- 🎨 **3D Modeling**: Generate and visualize 3D models
- 💬 **Natural Conversation**: Chat with your AI assistant
- ⚙️ **System Control**: Execute system commands safely

## Project Structure

```
jarvis-assistant/
├── backend/
│   ├── app.py                 # FastAPI server
│   ├── voice_handler.py       # Speech recognition
│   ├── hand_detection.py      # MediaPipe hand tracking
│   ├── ai_brain.py            # LLM integration (OpenAI/Local)
│   ├── app_launcher.py        # Application control
│   ├── system_commands.py     # Safe system execution
│   ├── config.py              # Configuration
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Main UI
│   ├── css/
│   │   └── style.css          # Styling
│   ├── js/
│   │   ├── app.js             # Main app logic
│   │   ├── voice.js           # Voice control
│   │   ├── camera.js          # Camera/hand detection
│   │   ├── 3d-model.js        # 3D visualization (Three.js)
│   │   └── api-client.js      # Backend communication
│   └── models/
│       └── robotic_hand.json   # 3D hand model
├── models/
│   └── hand_model.pkl         # ML model data
├── config.json                # Global configuration
├── .env.example               # Environment template
└── docs/
    ├── SETUP.md               # Installation guide
    ├── USAGE.md               # How to use
    └── ARCHITECTURE.md        # System architecture
```

## Quick Start

### 1. Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- Webcam (for hand detection)
- Microphone (for voice commands)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/DJfrank123/jarvis-assistant.git
cd jarvis-assistant

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key or local LLM setup

# Start backend
python app.py
```

### 3. Access Frontend

Open your browser to `http://localhost:8000`

## Configuration

Edit `config.json` to customize:
- Voice recognition language
- Hand detection sensitivity
- App launcher shortcuts
- LLM preferences (OpenAI, Ollama, etc.)
- 3D model settings

## Voice Commands Examples

```
"Jarvis, open Chrome"
"Jarvis, show my robotic hand"
"Jarvis, help me with calculus"
"Jarvis, create a 3D model of a sphere"
"Jarvis, what's the weather?"
"Jarvis, solve 2x + 5 = 15"
```

## Architecture

### Backend (Python/FastAPI)
- **Voice Handler**: Converts speech to text (Google Speech-to-Text)
- **AI Brain**: Processes commands and generates responses (OpenAI/Local LLM)
- **Hand Detection**: Real-time hand tracking (MediaPipe)
- **App Launcher**: Safely launches applications
- **System Commands**: Controlled execution of OS commands

### Frontend (Web-based)
- **Voice Interface**: Microphone input, text display
- **Camera Feed**: Real-time video with hand overlay
- **3D Visualization**: Three.js for 3D rendering
- **Chat UI**: Conversation display and input

## API Endpoints

```
POST /api/command         - Process voice/text command
GET  /api/status          - Get system status
WS   /ws/camera           - WebSocket for live camera feed
WS   /ws/audio            - WebSocket for audio streaming
GET  /api/apps            - List available apps
POST /api/3d-model        - Generate 3D model
GET  /api/hand-data       - Get hand tracking data
```

## Technologies Used

- **Backend**: Python, FastAPI, OpenAI API
- **Frontend**: HTML5, CSS3, JavaScript, Three.js
- **Computer Vision**: MediaPipe, OpenCV
- **Voice**: Google Speech-to-Text, Web Audio API
- **LLM**: OpenAI GPT-4 / Local Ollama
- **3D Rendering**: Three.js

## Roadmap

- ✅ Basic project structure
- ⏳ Voice recognition integration
- ⏳ Hand detection + 3D visualization
- ⏳ App launcher
- ⏳ LLM integration
- ⏳ Web UI dashboard
- ⏳ Advanced 3D modeling
- ⏳ Custom action scripting
- ⏳ Desktop app packaging (Electron)
- ⏳ Multi-language support

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Author

Built with ❤️ by DJfrank123

---

**Inspired by Jarvis from Iron Man** 🤖
