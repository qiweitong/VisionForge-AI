import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from models.resnet import build_model
from datasets.dataset import get_val_transforms

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
) 

TEST_PATH =r"E:\VisionForge AI\model\datasets\test"
WEIGHT_PATH =r"E:\VisionForge AI\model\output\weights\best.pth"

NUM_CLASSES = 6

test_dataset = datasets.ImageFolder(
    TEST_PATH,
    transform= get_val_transforms()
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

model = build_model(
    num_classes= NUM_CLASSES
)
model.load_state_dict(
    torch.load(WEIGHT_PATH)
)
model.to(DEVICE)    
model.eval()

correct =0
total =0
all_labels = []
all_predictions = [] 

with torch.no_grad():
    for images,labels in test_loader:
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        outputs = model(images)
        _,predicted = torch.max(outputs,1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        all_labels.extend(labels.cpu().numpy())
        all_predictions.extend(predicted.cpu().numpy())
    accuracy = correct / total
    print("=" * 50)
    print(f"Test Accuracy : {accuracy:.4f}")
    print("=" * 50)


