import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

import cv2
import numpy as np
from services.model_manager import model_manager


class CameraService:
    @staticmethod
    def predict_frame(frame):
        predictor = model_manager.get_predictor()
        if predictor is None:
            return None
        return predictor.predict_frame(frame)


camera_service = CameraService()
