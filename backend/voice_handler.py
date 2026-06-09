import speech_recognition as sr
import logging
from typing import Optional, Dict
import io

logger = logging.getLogger(__name__)

class VoiceHandler:
    """Handles speech recognition and voice processing"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.language = config.get("voice_language", "en-US")
        logger.info(f"VoiceHandler initialized with language: {self.language}")
    
    def transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """
        Transcribe audio bytes to text
        """
        try:
            # Convert bytes to audio data
            audio = sr.AudioData(audio_data, 16000, 2)
            
            # Use Google Speech Recognition (free, no API key required)
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Transcribed: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return None
    
    def transcribe_audio_stream(self, audio_chunk: bytes) -> Optional[str]:
        """
        Transcribe a chunk of audio from a stream
        """
        try:
            audio = sr.AudioData(audio_chunk, 16000, 2)
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except:
            return None
    
    def get_microphone_input(self, timeout: int = 10) -> Optional[str]:
        """
        Get voice input from microphone
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening for voice command...")
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Voice command: {text}")
                return text
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except Exception as e:
            logger.error(f"Microphone input error: {str(e)}")
            return None
