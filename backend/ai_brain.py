import openai
import requests
import logging
from typing import Dict, Optional
import json
import asyncio

logger = logging.getLogger(__name__)

class AIBrain:
    """AI Brain - processes commands and generates responses"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.use_local_llm = config.get("use_local_llm", False)
        self.conversation_history = []
        self.max_history = 20
        
        if not self.use_local_llm:
            openai.api_key = config.get("openai_api_key")
            self.model = config.get("openai_model", "gpt-4")
        else:
            self.local_url = config.get("local_llm_url", "http://localhost:11434")
            self.local_model = config.get("local_llm_model", "llama2")
        
        logger.info(f"AIBrain initialized - Using {'Local LLM' if self.use_local_llm else 'OpenAI'}")
    
    async def initialize(self):
        """Initialize AI brain"""
        logger.info("Initializing AI Brain...")
        # Test connection
        if self.use_local_llm:
            try:
                response = requests.get(f"{self.local_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Connected to Local LLM")
                else:
                    logger.warning("⚠️  Local LLM connection failed")
            except:
                logger.warning("⚠️  Could not connect to Local LLM")
        else:
            logger.info("✅ OpenAI API configured")
    
    async def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up AI Brain")
    
    def is_connected(self) -> bool:
        """Check if AI brain is connected"""
        if self.use_local_llm:
            try:
                response = requests.get(f"{self.local_url}/api/tags", timeout=2)
                return response.status_code == 200
            except:
                return False
        else:
            return self.config.get("openai_api_key") is not None
    
    async def process_command(self, user_input: str) -> Dict:
        """
        Process user command and generate response with actions
        """
        logger.info(f"Processing command: {user_input}")
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Keep history size manageable
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        try:
            system_prompt = self._get_system_prompt()
            
            if self.use_local_llm:
                response = await self._query_local_llm(user_input, system_prompt)
            else:
                response = await self._query_openai(user_input, system_prompt)
            
            # Parse response for actions
            parsed_response = self._parse_response(response)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return parsed_response
        
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return {
                "text": f"Sorry, I encountered an error: {str(e)}",
                "action": None
            }
    
    async def _query_openai(self, user_input: str, system_prompt: str) -> str:
        """Query OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _query_local_llm(self, user_input: str, system_prompt: str) -> str:
        """Query Local LLM (Ollama)"""
        try:
            prompt = f"{system_prompt}\n\nUser: {user_input}\n\nAssistant:"
            response = requests.post(
                f"{self.local_url}/api/generate",
                json={
                    "model": self.local_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception("Local LLM error")
        except Exception as e:
            logger.error(f"Local LLM error: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the AI"""
        return """You are Jarvis, an AI personal computer assistant inspired by Iron Man's Jarvis.
        
You help the user with:
- Opening applications (respond with action: launch_app)
- Executing safe system commands (respond with action: system_command)
- Providing math and engineering help
- Creating 3D models (respond with action: 3d_model)
- General conversation and assistance

When you need to perform an action, format your response as JSON like:
{"text": "Your spoken response", "action": "launch_app", "app_name": "chrome"}

Always be helpful, professional, and prioritize user safety. Never execute dangerous commands."""
    
    def _parse_response(self, response: str) -> Dict:
        """
        Parse AI response to extract text and actions
        """
        try:
            # Try to parse as JSON
            parsed = json.loads(response)
            return parsed
        except:
            # If not JSON, return as plain text
            return {
                "text": response,
                "action": None
            }
