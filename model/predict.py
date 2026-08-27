import torch
import time
from PIL import Image
import sys
import cv2
from pathlib import Path

current_folder = Path(__file__).parent
sys.path.append(str(current_folder))

from models.resnet import build_model
from datasets.dataset import get_val_transforms

CLASS_CN_MAP = {
    "Cr": "裂纹",
    "In": "夹杂",
    "Pa": "斑块",
    "PS": "点蚀",
    "RS": "轧制氧化皮",
    "Sc": "划痕"
}


class ResNetPredictor:
    def __init__(self, weight_path, device="cpu", num_classes=6):
        self.class_names = ["Cr", "In", "Pa", "PS", "RS", "Sc"]
        self.class_cn_map = CLASS_CN_MAP
        self.device = device
        self.transform = get_val_transforms()
        self.model = build_model(num_classes=num_classes)
        self.model.load_state_dict(
            torch.load(weight_path, map_location=device, weights_only=True)
        )
        self.model.to(device)
        self.model.eval()

    def preprocess(self, image):
        if isinstance(image, str):
            image = Image.open(image)
        if isinstance(image, Image.Image):
            image = image.convert("RGB")
        else:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
        image = self.transform(image)
        image = image.unsqueeze(0)
        return image.to(self.device)

    def predict(self, image):
        start = time.time()
        image_tensor = self.preprocess(image)
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, dim=1)
        end = time.time()
        inference_time = round((end - start) * 1000, 2)
        class_id = predicted.item()
        class_name = self.class_names[class_id]
        return {
            "task_type": "classification",
            "class_id": class_id,
            "class_name": class_name,
            "class_cn": self.class_cn_map.get(class_name, "未知缺陷"),
            "confidence": round(confidence.item(), 4),
            "inference": inference_time
        }

    def predict_frame(self, frame):
        return self.predict(frame)
