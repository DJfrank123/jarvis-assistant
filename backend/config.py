import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.json and environment variables
    """
    config = {
        # Voice Configuration
        "voice_enabled": os.getenv("VOICE_ENABLED", "true").lower() == "true",
        "voice_language": os.getenv("VOICE_LANGUAGE", "en-US"),
        
        # Hand Detection Configuration
        "hand_detection_enabled": os.getenv("HAND_DETECTION_ENABLED", "true").lower() == "true",
        "hand_detection_confidence": float(os.getenv("HAND_DETECTION_CONFIDENCE", "0.7")),
        
        # AI Brain Configuration
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
        "use_local_llm": os.getenv("USE_LOCAL_LLM", "false").lower() == "true",
        "local_llm_url": os.getenv("LOCAL_LLM_URL", "http://localhost:11434"),
        "local_llm_model": os.getenv("LOCAL_LLM_MODEL", "llama2"),
        
        # System Configuration
        "allow_system_commands": os.getenv("ALLOW_SYSTEM_COMMANDS", "true").lower() == "true",
        "safe_mode": os.getenv("SAFE_MODE", "true").lower() == "true",
        
        # Server Configuration
        "server_host": os.getenv("SERVER_HOST", "0.0.0.0"),
        "server_port": int(os.getenv("SERVER_PORT", "8000")),
        "debug": os.getenv("DEBUG", "true").lower() == "true",
    }
    
    # Try to load from config.json if it exists
    try:
        if os.path.exists("../config.json"):
            with open("../config.json", "r") as f:
                file_config = json.load(f)
                config.update(file_config)
                logger.info("Loaded configuration from config.json")
    except Exception as e:
        logger.warning(f"Could not load config.json: {str(e)}")
    
    return config
