import torch
import os

# ======================
# 数据集
# ======================

DATASET_ROOT = r"E:\VisionForge AI\model\datasets"

NUM_CLASSES = 6

CLASS_NAMES = [
    "Cr",
    "In",
    "Pa",
    "PS",
    "RS",
    "Sc"
]

# ======================
# 训练
# ======================

BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 0.001

NUM_WORKERS = 6

# ======================
# 模型
# ======================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ======================
# 输出目录
# ======================

OUTPUT_DIR = r"E:\VisionForge AI\model\output"

WEIGHT_DIR = os.path.join(
    OUTPUT_DIR,
    "weights"
)

BEST_MODEL = os.path.join(
    WEIGHT_DIR,
    "best.pth"
)

LAST_MODEL = os.path.join(
    WEIGHT_DIR,
    "last.pth"
)

LOG_DIR = os.path.join(
    OUTPUT_DIR,
    "logs"
)

CLASS_INFO ={
    "Cr":"Crack（裂纹）",
    "In":"Inclusion（夹杂）",
    "Pa":"Patch（斑块）",
    "PS":"Pitted Surface（麻点）",
    "RS":"Rolled Scale（氧化皮）",
    "Sc":"Scratches（划痕）"
}