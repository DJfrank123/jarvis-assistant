from fastapi import FastAPI, WebSocket, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import logging
from typing import Dict, List
import json

from voice_handler import VoiceHandler
from hand_detection import HandDetectionManager
from ai_brain import AIBrain
from app_launcher import AppLauncher
from system_commands import SystemCommandExecutor
from config import load_config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Jarvis - AI Computer Assistant",
    description="Voice-controlled personal AI assistant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration
config = load_config()

# Initialize components
voice_handler = VoiceHandler(config)
hand_detection = HandDetectionManager(config)
ai_brain = AIBrain(config)
app_launcher = AppLauncher(config)
system_executor = SystemCommandExecutor(config)

logger.info("Jarvis AI Assistant initialized")

# ==================== API Routes ====================

@app.get("/")
async def root():
    """Serve the main frontend"""
    try:
        with open("../frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except:
        return {"message": "Jarvis AI Assistant Running"}

@app.get("/api/status")
async def get_status() -> Dict:
    """Get system status"""
    return {
        "status": "online",
        "jarvis_version": "1.0.0",
        "voice_enabled": config.get("voice_enabled", True),
        "hand_detection_enabled": config.get("hand_detection_enabled", True),
        "ai_brain_connected": ai_brain.is_connected(),
    }

@app.post("/api/command")
async def process_command(data: Dict) -> Dict:
    """
    Process a voice or text command
    
    Expected input:
    {
        "command": "open chrome",
        "type": "voice" or "text"
    }
    """
    command = data.get("command", "")
    command_type = data.get("type", "text")
    
    logger.info(f"Processing {command_type} command: {command}")
    
    try:
        # Process command through AI brain
        response = await ai_brain.process_command(command)
        
        # Check if it's an action command (app launch, system command, etc.)
        if response.get("action"):
            action = response["action"]
            
            if action == "launch_app":
                app_name = response.get("app_name")
                result = app_launcher.launch(app_name)
                response["execution_result"] = result
            
            elif action == "system_command":
                cmd = response.get("command")
                result = system_executor.execute_safe(cmd)
                response["execution_result"] = result
            
            elif action == "3d_model":
                model_type = response.get("model_type")
                response["3d_model_data"] = {"type": model_type}
        
        return {
            "success": True,
            "command": command,
            "response": response.get("text", ""),
            "action": response.get("action"),
            "data": response
        }
    
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "command": command
        }

@app.get("/api/apps")
async def get_available_apps() -> Dict:
    """Get list of available applications"""
    apps = app_launcher.get_available_apps()
    return {
        "apps": apps,
        "count": len(apps)
    }

@app.post("/api/launch-app")
async def launch_app(data: Dict) -> Dict:
    """Launch an application"""
    app_name = data.get("app_name", "")
    logger.info(f"Launching app: {app_name}")
    
    try:
        result = app_launcher.launch(app_name)
        return {
            "success": result,
            "app_name": app_name,
            "message": f"Launched {app_name}" if result else f"Failed to launch {app_name}"
        }
    except Exception as e:
        logger.error(f"Error launching app: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "app_name": app_name
        }

@app.get("/api/hand-data")
async def get_hand_data() -> Dict:
    """Get latest hand detection data"""
    return hand_detection.get_latest_hand_data()

@app.post("/api/voice-upload")
async def upload_voice(file: UploadFile = File(...)) -> Dict:
    """Upload and process voice file"""
    try:
        content = await file.read()
        # Process audio and convert to text
        text = voice_handler.transcribe_audio(content)
        return {
            "success": True,
            "transcribed_text": text
        }
    except Exception as e:
        logger.error(f"Error processing voice upload: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# ==================== WebSocket Routes ====================

@app.websocket("/ws/camera")
async def websocket_camera(websocket: WebSocket):
    """WebSocket for live camera feed with hand detection"""
    await websocket.accept()
    logger.info("Camera WebSocket connected")
    
    try:
        while True:
            # Get frame with hand detection
            frame_data = hand_detection.get_frame_with_detection()
            if frame_data:
                await websocket.send_json({
                    "type": "frame",
                    "data": frame_data
                })
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """WebSocket for audio streaming and voice commands"""
    await websocket.accept()
    logger.info("Audio WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            # Process audio stream
            text = voice_handler.transcribe_audio_stream(data)
            if text:
                await websocket.send_json({
                    "type": "transcription",
                    "text": text
                })
    except Exception as e:
        logger.error(f"Audio WebSocket error: {str(e)}")
    finally:
        await websocket.close()

# ==================== Health Check ====================

@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "Jarvis AI Assistant"}

# ==================== Startup & Shutdown ====================

@app.on_event("startup")
async def startup_event():
    logger.info("🤖 Jarvis AI Assistant is starting up...")
    try:
        await ai_brain.initialize()
        hand_detection.start()
        logger.info("✅ All systems initialized successfully")
    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🔴 Jarvis AI Assistant is shutting down...")
    hand_detection.stop()
    await ai_brain.cleanup()
    logger.info("✅ Cleanup complete")

# ==================== Static Files ====================

try:
    app.mount("/static", StaticFiles(directory="../frontend"), name="static")
except:
    logger.warning("Could not mount static files")

# ==================== Main ====================

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    logger.info(f"Starting Jarvis on {host}:{port}")
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
