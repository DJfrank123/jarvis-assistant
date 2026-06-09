import subprocess
import logging
import platform
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SystemCommandExecutor:
    """Safely executes system commands"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.safe_mode = config.get("safe_mode", True)
        self.allow_commands = config.get("allow_system_commands", True)
        
        # Commands that are never allowed
        self.blocked_keywords = [
            "rm -rf",
            "format",
            "del /s",
            "sudo rm",
            "dd if=",
            "mkfs",
            "shutdown -h",
            "halt",
            "reboot",
        ]
        
        logger.info(f"SystemCommandExecutor initialized (Safe Mode: {self.safe_mode})")
    
    def execute_safe(self, command: str) -> Dict:
        """
        Execute a system command safely
        """
        if not self.allow_commands:
            return {
                "success": False,
                "error": "System commands are disabled"
            }
        
        if self.safe_mode and self._is_dangerous(command):
            logger.warning(f"Blocked dangerous command: {command}")
            return {
                "success": False,
                "error": "This command is not allowed for safety reasons"
            }
        
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=10,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        
        except subprocess.TimeoutExpired:
            logger.error("Command timeout")
            return {
                "success": False,
                "error": "Command timed out"
            }
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _is_dangerous(self, command: str) -> bool:
        """
        Check if command contains dangerous keywords
        """
        command_lower = command.lower()
        for keyword in self.blocked_keywords:
            if keyword in command_lower:
                return True
        return False
