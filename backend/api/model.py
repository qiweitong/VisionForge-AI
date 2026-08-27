import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import APIRouter
from services.model_manager import model_manager

router = APIRouter()


@router.get("/list")
async def list_models():
    models = model_manager.list_models()
    return {"success": True, "data": models}


@router.get("/current")
async def current_model():
    info = model_manager.get_current_model_info()
    return {"success": True, "data": info}


@router.post("/select")
async def select_model(data: dict):
    name = data.get("name")
    if not name:
        return {"success": False, "error": "缺少模型名称"}
    success = model_manager.set_model(name)
    if not success:
        return {"success": False, "error": f"模型 {name} 不存在"}
    current = model_manager.get_current_model_info()
    return {"success": True, "data": current}


@router.post("/reload_yolo")
async def reload_yolo():
    success = model_manager.reload_yolo()
    if success:
        return {"success": True, "message": "YOLO11 权重重新加载成功"}
    return {"success": False, "error": "YOLO11 权重文件不存在，请先完成训练"}
