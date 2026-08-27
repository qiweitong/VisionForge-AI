import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ultralytics import YOLO

model = YOLO(str(project_root / "yolo11n.pt"))

results = model.train(
    data=str(Path(__file__).parent / "neu_det.yaml"),
    epochs=40,
    imgsz=640,
    batch=4,
    device="cpu",
    project=str(project_root / "model" / "runs"),
    name="yolo11n_steel",
    exist_ok=True,
    patience=10,
    save=True,
    save_period=5,
    workers=0,
)

print(f"\nTraining complete!")
print(f"Best model saved at: {project_root}/model/runs/yolo11n_steel/weights/best.pt")
