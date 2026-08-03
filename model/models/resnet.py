from torchvision import models
import torch.nn as nn

def build_model(num_classes=6):

    # 旧版torchvision专用写法
    model = models.resnet18(pretrained=True)
    in_features = model.fc.in_features

    model.fc = nn.Linear(in_features, num_classes)
    return model
