from ultralytics import YOLO

# 重头开始训练
model = YOLO("yolo11n.pt")
model.train(
    data=r"E:\VisionForge AI\model\neu_det.yaml",
    epochs=40,
    imgsz=640,
    batch=4,
    device="cpu"
)