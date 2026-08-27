import sys
import time
import threading
import cv2
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from camera.config import CAMERA_ID, FRAME_SKIP
from camera.draw import draw_info
from camera.fps import FPSCounter
from services.model_manager import model_manager


class Camera:
    def __init__(self):
        self.cap = None
        self.fps_counter = FPSCounter()
        self.frame_count = 0
        self.running = False
        self.result = None
        self._frame_lock = threading.Lock()
        self._latest_frame = None
        self._frame_ready = threading.Event()

        self.current_cls = "None"
        self.current_conf = 0.0
        self.real_fps = 0.0

    def start(self):
        if self.running:
            return True, "camera already running"

        new_cap = cv2.VideoCapture(CAMERA_ID)
        new_cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not new_cap.isOpened():
            new_cap.release()
            return False, "无法打开摄像头，请检查摄像头ID/设备占用"

        self.cap = new_cap
        self.running = True
        self._frame_ready.clear()

        t = threading.Thread(target=self._read_loop, daemon=True)
        t.start()

        ready = self._frame_ready.wait(timeout=2.0)
        if not ready:
            self.stop()
            return False, "摄像头启动超时，未读取到图像"

        return True, "camera started"

    def _read_loop(self):
        while self.running and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            self.frame_count += 1
            if self.frame_count % FRAME_SKIP == 0:
                predictor = model_manager.get_predictor()
                if predictor is not None:
                    self.result = predictor.predict_frame(frame)
                    if self.result["task_type"] == "classification":
                        self.current_cls = self.result["class_name"]
                        self.current_conf = round(float(self.result["confidence"]), 4)
                    elif self.result["task_type"] == "detection":
                        if self.result["detections"]:
                            best = max(self.result["detections"], key=lambda d: d["confidence"])
                            self.current_cls = best["class_name"]
                            self.current_conf = round(best["confidence"], 4)
                        else:
                            self.current_cls = "NoDetection"
                            self.current_conf = 0.0

            self.real_fps = self.fps_counter.update()
            draw_info(frame, self.result, self.real_fps)

            with self._frame_lock:
                self._latest_frame = frame.copy()

            self._frame_ready.set()

    def stop(self):
        self.running = False
        self._frame_ready.clear()
        if self.cap:
            self.cap.release()
            self.cap = None
        with self._frame_lock:
            self._latest_frame = None
        self.result = None
        self.current_cls = "None"
        self.current_conf = 0.0
        self.real_fps = 0.0
        return "camera stopped"

    def get_frame(self):
        with self._frame_lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()

    def get_status(self):
        return {
            "running": self.running,
            "class": self.current_cls,
            "confidence": self.current_conf,
            "fps": round(self.real_fps, 1)
        }

    def release(self):
        self.stop()


camera_instance = Camera()
