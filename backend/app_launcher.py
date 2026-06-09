import subprocess
import platform
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AppLauncher:
    """Manages application launching"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.system = platform.system()
        self.app_paths = self._get_app_paths()
        logger.info(f"AppLauncher initialized for {self.system}")
    
    def _get_app_paths(self) -> Dict[str, str]:
        """Get common application paths for the system"""
        if self.system == "Windows":
            return {
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "vscode": r"C:\Program Files\Microsoft VS Code\Code.exe",
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "explorer": "explorer.exe",
            }
        elif self.system == "Darwin":  # macOS
            return {
                "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
                "vscode": "/Applications/Visual Studio Code.app/Contents/MacOS/Code",
                "safari": "/Applications/Safari.app/Contents/MacOS/Safari",
            }
        else:  # Linux
            return {
                "chrome": "/usr/bin/google-chrome",
                "firefox": "/usr/bin/firefox",
                "vscode": "/usr/bin/code",
            }
    
    def launch(self, app_name: str) -> bool:
        """
        Launch an application by name
        """
        app_name = app_name.lower().strip()
        logger.info(f"Attempting to launch: {app_name}")
        
        try:
            # Check if app is in our known paths
            if app_name in self.app_paths:
                app_path = self.app_paths[app_name]
                if os.path.exists(app_path) or self.system != "Windows":
                    if self.system == "Windows":
                        subprocess.Popen(app_path)
                    elif self.system == "Darwin":
                        subprocess.Popen(["open", "-a", app_path])
                    else:
                        subprocess.Popen(app_path)
                    logger.info(f"✅ Launched {app_name}")
                    return True
            
            # Try to launch directly by name (system search)
            if self.system == "Windows":
                subprocess.Popen(f"start {app_name}", shell=True)
            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen(app_name)
            
            logger.info(f"✅ Launched {app_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to launch {app_name}: {str(e)}")
            return False
    
    def get_available_apps(self) -> List[str]:
        """
        Get list of available applications
        """
        available = []
        for app_name, app_path in self.app_paths.items():
            if self.system == "Windows":
                if os.path.exists(app_path):
                    available.append(app_name)
            else:
                # For macOS and Linux, assume common apps are available
                available.append(app_name)
        
        return available
