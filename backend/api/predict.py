import sys
from pathlib import Path
# 定位到 VisionForge AI 项目根目录
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


from fastapi import APIRouter, UploadFile, File
from PIL import Image
import torch

from model.predict import Predictor
from model.config import *
from fastapi import HTTPException
router = APIRouter()


predictor = Predictor(
    weight_path=r"E:\VisionForge AI\model\output\weights\best.pth",
    device=DEVICE,
    num_classes=NUM_CLASSES
)
@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...)
):
 try:
    #FastAPI,自动把：jpg,png,bmp 变成：文件对象。
    image =Image.open(file.file)
    result = predictor.predict(image)
    return {
      "success": True,
      "data": result
    }
 except Exception as e:
   raise HTTPException(
     status_code=500,
     detail=str(e)
   )
