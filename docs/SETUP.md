# Jarvis AI Assistant - Setup Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Hardware**: Webcam, Microphone

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/DJfrank123/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
# For OpenAI:
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Or for Local LLM (Ollama):
USE_LOCAL_LLM=true
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama2
```

### 5. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:8000`

## OpenAI API Setup (Recommended)

1. Create an account at https://platform.openai.com
2. Generate an API key
3. Add to `.env` file: `OPENAI_API_KEY=your_key`
4. Set model: `OPENAI_MODEL=gpt-4`

## Local LLM Setup (Ollama)

### Install Ollama

1. Download from https://ollama.ai
2. Install and run: `ollama serve`
3. In another terminal: `ollama pull llama2`

### Configure Jarvis

```env
USE_LOCAL_LLM=true
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama2
```

## Troubleshooting

### Microphone Access Denied
- Check browser permissions
- Allow microphone access when prompted
- Restart browser if needed

### Camera Not Working
- Ensure webcam is connected
- Check camera permissions in OS settings
- Try: `cv2.VideoCapture(1)` if using external camera

### OpenAI API Errors
- Verify API key is correct
- Check API usage at https://platform.openai.com/account/usage
- Ensure sufficient credits

### Hand Detection Not Working
- Ensure good lighting
- Position hands clearly in camera view
- Adjust `hand_detection_confidence` in config.json

## First Run Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] OpenAI key or Ollama running
- [ ] Webcam and microphone working
- [ ] Backend server running
- [ ] Browser can access http://localhost:8000
- [ ] Camera feed showing
- [ ] Voice input working

## Next Steps

After setup, check out:
- [USAGE.md](USAGE.md) - How to use Jarvis
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
