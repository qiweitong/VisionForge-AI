import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

import torch
from model.config import DEVICE
from model.predict import ResNetPredictor
from model.models.yolo import YOLOPredictor


class ModelManager:
    def __init__(self):
        self._predictors = {}
        self._current_model_name = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return

        resnet_path = project_root / "model" / "output" / "weights" / "best.pth"
        yolo_path = project_root / "model" / "runs" / "yolo11n_steel" / "weights" / "best.pt"

        if resnet_path.exists():
            try:
                predictor = ResNetPredictor(weight_path=str(resnet_path), device=DEVICE)
                self.register_model(
                    name="resnet50",
                    predictor=predictor,
                    display_name="ResNet50 钢材分类",
                    task_type="classification"
                )
                print("[ModelManager] ResNet50 已加载")
            except Exception as e:
                print(f"[ModelManager] ResNet50 加载失败: {e}")
        else:
            print(f"[ModelManager] ResNet50 权重不存在: {resnet_path}")

        if yolo_path.exists():
            try:
                predictor = YOLOPredictor(weight_path=str(yolo_path), device=DEVICE)
                self.register_model(
                    name="yolo11",
                    predictor=predictor,
                    display_name="YOLO11 钢材检测",
                    task_type="detection"
                )
                print("[ModelManager] YOLO11 已加载")
            except Exception as e:
                print(f"[ModelManager] YOLO11 加载失败: {e}")
        else:
            print(f"[ModelManager] YOLO11 权重不存在: {yolo_path}")

        if self._predictors:
            first_model = list(self._predictors.keys())[0]
            self._current_model_name = first_model
            print(f"[ModelManager] 当前激活模型: {self.get_current_model_info()['display_name']}")
        else:
            print("[ModelManager] 警告: 没有可用的模型")

        self._initialized = True

    def register_model(self, name, predictor, display_name="", task_type="classification"):
        self._predictors[name] = {
            "predictor": predictor,
            "display_name": display_name or name,
            "task_type": task_type
        }

    def set_model(self, name: str) -> bool:
        if name not in self._predictors:
            return False
        self._current_model_name = name
        return True

    def get_model(self, name: str = None):
        name = name or self._current_model_name
        if name and name in self._predictors:
            return self._predictors[name]["predictor"]
        return None

    def get_predictor(self, name: str = None):
        return self.get_model(name)

    def get_current_model_info(self) -> dict:
        if not self._current_model_name or self._current_model_name not in self._predictors:
            return {"name": None, "display_name": None, "task_type": None}
        info = self._predictors[self._current_model_name]
        return {
            "name": self._current_model_name,
            "display_name": info["display_name"],
            "task_type": info["task_type"]
        }

    def list_models(self) -> list:
        result = []
        for name, info in self._predictors.items():
            result.append({
                "name": name,
                "display_name": info["display_name"],
                "task_type": info["task_type"],
                "is_current": name == self._current_model_name
            })
        return result

    def get_current_model_name(self) -> str:
        return self._current_model_name

    def get_current_task_type(self) -> str:
        if self._current_model_name and self._current_model_name in self._predictors:
            return self._predictors[self._current_model_name]["task_type"]
        return "unknown"

    def reload_yolo(self) -> bool:
        yolo_path = project_root / "model" / "runs" / "yolo11n_steel" / "weights" / "best.pt"
        if not yolo_path.exists():
            return False
        try:
            predictor = YOLOPredictor(weight_path=str(yolo_path), device=DEVICE)
            self.register_model(
                name="yolo11",
                predictor=predictor,
                display_name="YOLO11 钢材检测",
                task_type="detection"
            )
            print("[ModelManager] YOLO11 权重已重新加载")
            return True
        except Exception as e:
            print(f"[ModelManager] YOLO11 重新加载失败: {e}")
            return False


model_manager = ModelManager()
