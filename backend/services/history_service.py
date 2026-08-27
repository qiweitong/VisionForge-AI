import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from services.model_manager import model_manager
from database.database import get_history as db_get_history, delete_history as db_delete_history, clear_history as db_clear_history


class HistoryService:
    @staticmethod
    def get_history(limit=100, offset=0, model_name=None):
        model = model_name or model_manager.get_current_model_name()
        return db_get_history(limit=limit, offset=offset, model_name=model)

    @staticmethod
    def delete_history(record_id: int):
        return db_delete_history(record_id)

    @staticmethod
    def clear_history(model_name=None):
        model = model_name or model_manager.get_current_model_name()
        return db_clear_history(model_name=model)


history_service = HistoryService()
