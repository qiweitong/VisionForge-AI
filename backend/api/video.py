import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
import cv2
import numpy as np
from camera.camera import camera_instance
from services.model_manager import model_manager

router = APIRouter()
camera_router = APIRouter(prefix="/camera")


def _generate_frames():
    while True:
        frame = camera_instance.get_frame()
        if frame is None:
            import time
            time.sleep(0.03)
            continue

        encode_ok, buffer = cv2.imencode(".jpg", frame)
        if not encode_ok:
            continue
        frame_bytes = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        _generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@camera_router.post("/start")
async def start_camera():
    success, msg = camera_instance.start()
    if not success:
        return JSONResponse({"success": False, "message": msg}, status_code=400)
    current = model_manager.get_current_model_info()
    return {"success": True, "message": msg, "model": current}


@camera_router.post("/stop")
async def stop_camera():
    msg = camera_instance.stop()
    return {"success": True, "message": msg}


@camera_router.get("/status")
async def camera_status():
    status = camera_instance.get_status()
    current = model_manager.get_current_model_info()
    status["model"] = current
    return {"success": True, "data": status}
