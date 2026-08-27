import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.predict_service import predict_service
from services.model_manager import model_manager

router = APIRouter()


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    confidence: float = Form(0.5),
    model: str = Form(None),
):
    if model and not model_manager.set_model(model):
        return JSONResponse(content={"success": False, "error": f"模型 {model} 不存在"}, status_code=400)

    try:
        image_data = file.file.read()
        result = predict_service.predict_image(
            image_data=image_data,
            filename=file.filename,
            confidence=confidence
        )
        return {"success": True, "data": result}
    except ValueError as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.get("/predict/list")
async def predict_list():
    from services.history_service import history_service
    history = history_service.get_history(limit=50)
    return {"success": True, "data": history}


@router.delete("/predict/{record_id}")
async def delete_predict(record_id: int):
    from services.history_service import history_service
    history_service.delete_history(record_id)
    return {"success": True}


@router.delete("/predict")
async def clear_predict():
    from services.history_service import history_service
    model_name = model_manager.get_current_model_name()
    history_service.clear_history(model_name=model_name)
    return {"success": True}
