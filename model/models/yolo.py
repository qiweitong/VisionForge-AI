import time
import sys
from pathlib import Path

current_folder = Path(__file__).parent.parent
sys.path.insert(0, str(current_folder))

from ultralytics import YOLO

CLASS_CN_MAP = {
    "crazing": "裂纹",
    "inclusion": "夹杂",
    "patches": "斑块",
    "pitted_surface": "点蚀",
    "rolled-in_scale": "轧制氧化皮",
    "scratches": "划痕"
}

CLASS_EN_MAP = {
    0: "Cr",
    1: "In",
    2: "Pa",
    3: "PS",
    4: "RS",
    5: "Sc"
}


class YOLOPredictor:
    def __init__(self, weight_path, device="cpu"):
        self.model = YOLO(weight_path)
        self.device = device
        self.class_names = self.model.names
        self.class_cn_map = CLASS_CN_MAP
        self.class_en_map = CLASS_EN_MAP

    def predict(self, image):
        start = time.time()
        results = self.model(image, verbose=False)
        result = results[0]
        end = time.time()
        inference_time = round((end - start) * 1000, 2)

        detections = []
        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                cls_id = int(box.cls.item())
                conf = float(box.conf.item())
                xyxy = box.xyxy[0].tolist()
                detections.append({
                    "class_id": cls_id,
                    "class_name": self.class_names.get(cls_id, f"class_{cls_id}"),
                    "class_cn": self.class_cn_map.get(
                        self.class_names.get(cls_id, ""),
                        "未知缺陷"
                    ),
                    "confidence": round(conf, 4),
                    "bbox": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                })

        return {
            "task_type": "detection",
            "detections": detections,
            "inference": inference_time
        }

    def predict_frame(self, frame):
        return self.predict(frame)
