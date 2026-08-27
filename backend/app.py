import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
backend_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.predict import router as predict_router
from api.history import router as history_router
from api.statistics import router as statistics_router
from api.video import router as video_router, camera_router as video_camera_router
from api.model import router as model_router
from database.database import init_db
from services.model_manager import model_manager

app = FastAPI(
    title="VisionForge AI",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(history_router, prefix="/history")
app.include_router(statistics_router, prefix="/statistics")
app.include_router(video_router)
app.include_router(video_camera_router)
app.include_router(model_router, prefix="/model")

init_db()
model_manager.initialize()


@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("VisionForge AI Backend Starting...")
    print(f"Models loaded: {model_manager.list_models()}")
    info = model_manager.get_current_model_info()
    print(f"Current model: {info.get('display_name', 'None')}")
    print("=" * 50)


@app.get("/")
def root():
    return {
        "message": "VisionForge AI Backend Running!",
        "version": "2.0.0",
        "models": model_manager.list_models(),
        "current_model": model_manager.get_current_model_info()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
