import sys
import io
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from PIL import Image
from services.model_manager import model_manager
from database.database import insert_history


class PredictService:
    @staticmethod
    def predict_image(image_data: bytes, filename: str = "", confidence: float = 0.5):
        predictor = model_manager.get_predictor()
        if predictor is None:
            raise ValueError("没有可用的模型，请先在模型管理页面加载模型")

        image = Image.open(io.BytesIO(image_data))
        result = predictor.predict(image)

        model_name = model_manager.get_current_model_name()
        record_id = insert_history(
            image_name=filename,
            class_name=result.get("class_name", ""),
            class_cn=result.get("class_cn", result.get("class_name", "")),
            confidence=result.get("confidence", 0.0),
            model_name=model_name
        )

        result["id"] = record_id
        result["model_name"] = model_name
        return result


predict_service = PredictService()
