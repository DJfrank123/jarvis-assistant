import cv2
import mediapipe as mp
import numpy as np
import logging
from typing import Dict, List, Optional
import threading
import base64

logger = logging.getLogger(__name__)

class HandDetectionManager:
    """Manages hand detection using MediaPipe"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=config.get("hand_detection_confidence", 0.7),
            min_tracking_confidence=0.5
        )
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.current_hand_data = {}
        self.thread = None
        logger.info("HandDetectionManager initialized")
    
    def start(self):
        """Start hand detection from webcam"""
        if self.is_running:
            return
        
        self.cap = cv2.VideoCapture(0)
        self.is_running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        logger.info("Hand detection started")
    
    def stop(self):
        """Stop hand detection"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Hand detection stopped")
    
    def _detection_loop(self):
        """Main detection loop running in a separate thread"""
        while self.is_running and self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                continue
            
            # Flip and process frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect hands
            results = self.hands.process(rgb_frame)
            
            # Store hand data
            if results.multi_hand_landmarks:
                self._process_hand_landmarks(results, frame)
            
            # Draw landmarks on frame
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
            
            # Encode frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            self.current_frame = base64.b64encode(buffer).decode()
    
    def _process_hand_landmarks(self, results, frame):
        """Process detected hand landmarks"""
        hand_data = []
        h, w, c = frame.shape
        
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.append({
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                })
            
            hand_info = {
                "hand_index": idx,
                "landmarks": landmarks,
                "handedness": results.multi_handedness[idx].classification[0].label if results.multi_handedness else "Unknown"
            }
            hand_data.append(hand_info)
        
        self.current_hand_data = {
            "detected": len(hand_data) > 0,
            "hands": hand_data,
            "timestamp": None
        }
    
    def get_frame_with_detection(self) -> Optional[Dict]:
        """Get current frame with hand detection"""
        if self.current_frame is None:
            return None
        
        return {
            "frame": self.current_frame,
            "hand_data": self.current_hand_data
        }
    
    def get_latest_hand_data(self) -> Dict:
        """Get latest hand detection data"""
        return self.current_hand_data
    
    def get_hand_position(self, hand_index: int = 0) -> Optional[Dict]:
        """Get position of a specific hand"""
        if not self.current_hand_data.get("hands"):
            return None
        
        if hand_index >= len(self.current_hand_data["hands"]):
            return None
        
        hand = self.current_hand_data["hands"][hand_index]
        wrist = hand["landmarks"][0]
        
        return {
            "wrist_x": wrist["x"],
            "wrist_y": wrist["y"],
            "wrist_z": wrist["z"]
        }
