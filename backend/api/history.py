import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import APIRouter
from services.history_service import history_service
from services.model_manager import model_manager

router = APIRouter()


@router.get("/")
async def get_history(limit: int = 20, offset: int = 0):
    history = history_service.get_history(limit=limit, offset=offset)
    return {"success": True, "data": history}


@router.delete("/{record_id}")
async def delete_history(record_id: int):
    history_service.delete_history(record_id)
    return {"success": True}


@router.delete("/")
async def clear_history():
    model_name = model_manager.get_current_model_name()
    history_service.clear_history(model_name=model_name)
    return {"success": True}
