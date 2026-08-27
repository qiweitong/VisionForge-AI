import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from services.model_manager import model_manager
from database.database import get_statistics


class DashboardService:
    @staticmethod
    def get_dashboard_data():
        model_name = model_manager.get_current_model_name()
        return get_statistics(model_name=model_name)


dashboard_service = DashboardService()
