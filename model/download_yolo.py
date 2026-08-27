from ultralytics import YOLO

model = YOLO(
    r"E:\VisionForge AI\model\runs\detect\output\yolo\neu_det-2\weights\best.pt"
)

results = model(
    r"E:\VisionForge AI\model\datasets_yolo\images\test\crazing_4.jpg",
    show=True,
    conf=0.001
)

print(results)