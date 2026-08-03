import torch
import time
from PIL import Image
import sys
from pathlib import Path
current_folder = Path(__file__).parent
# 把 model 文件夹加入检索路径，才能识别 models / datasets
sys.path.append(str(current_folder))

from models.resnet import build_model
from datasets.dataset import get_val_transforms

class Predictor:
    def __init__(
            self,
            weight_path,
            device,
            num_classes =6,
            


    ):
        self.class_name =[
             "Cr",
             "In",
             "Pa",
             "PS",
             "RS",
             "Sc"
                         ]
        
        self.device =device
        self.transform = get_val_transforms()
        self.model = build_model(
            num_classes=num_classes
        )
        self.model.load_state_dict(
            torch.load(
                weight_path,
                map_location=device
            )
        )
        self.model.to(device)
        self.model.eval()

    def preprocess(
            self,
            image
    ):
        if isinstance(image,str):
            image = Image.open(image)
        image = image.convert("RGB")
        image = self.transform(image)
        image = image.unsqueeze(0)
        return image.to(self.device)
    
    def predict(
            self,
            image
    ):
        start = time.time()
        image = self.preprocess(image)
        with torch.no_grad():
            outputs = self.model(image)

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            confidence,predicted = torch.max(
                probabilities,
                dim=1
            )

            end = time.time()
            inference_time = round((end-start)*1000,2)
            return {
                "class_id": predicted.item(),
                "class_name":self.class_name[predicted.item()],
                "confidence": confidence.item(),
                "inference": inference_time
            }