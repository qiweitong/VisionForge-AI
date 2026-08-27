from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from model.predict import Predictor

weight_path = r"E:\VisionForge AI\model\output\weights\best.pth"

device = "cpu"

predictor = Predictor(weight_path, device)

def predict(frame):
    return predictor.predict_frame(frame)