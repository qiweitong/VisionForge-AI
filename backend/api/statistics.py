import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import APIRouter
from services.dashboard_service import dashboard_service

router = APIRouter()


@router.get("/")
async def get_statistics():
    data = dashboard_service.get_dashboard_data()
    return {"success": True, "data": data}
