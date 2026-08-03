import os
import torch
import torch.nn as nn
import torch.optim as optim

from datasets.dataset import get_dataloaders
from models.resnet import build_model

# 配置参数
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001
NUM_WORKERS = 0  # Windows必须改为0，否则终端卡死无输出
NUM_CLASSES = 6

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATASET_ROOT = r"E:\VisionForge AI\model\datasets"

def main():
    print("===== 脚本开始执行 =====")  # 新增调试打印
    # 权重保存路径，只初始化一次
    save_dir = r"E:\VisionForge AI\model\output\weights"
    os.makedirs(save_dir, exist_ok=True)
    best_acc = 0.0  # 最优准确率初始化，放在epoch循环外面

    # 加载数据集
    train_loader, val_loader, classes = get_dataloaders(
        dataset_root=DATASET_ROOT,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS
    )

    print("=" * 50)
    print("类别名称：", classes)
    print("训练集数量：", len(train_loader.dataset))
    print("验证集数量：", len(val_loader.dataset))

    # 初始化模型、损失、优化器
    model = build_model(num_classes=NUM_CLASSES)
    model = model.to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 训练循环
    for epoch in range(EPOCHS):
        train_loss = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            DEVICE
        )

        val_loss, val_acc = validate(
            model,
            val_loader,
            criterion,
            DEVICE
        )

        print(
            f"Epoch [{epoch+1}/{EPOCHS}] "
            f"Train Loss: {train_loss:.4f} "
            f"Val Loss: {val_loss:.4f} "
            f"Val Acc: {val_acc:.4f}"
        )

        # 仅当当前准确率超过历史最优时保存
        if val_acc > best_acc:
            best_acc = val_acc
            save_path = os.path.join(save_dir, "best.pth")
            # 删除旧权重，规避Windows占用报错123
            if os.path.exists(save_path):
                os.remove(save_path)
            torch.save(model.state_dict(), save_path)
            print(f"✅ 保存最佳模型，Val Acc: {best_acc:.4f}，路径：{save_path}\n")


def train_one_epoch(
        model,
        train_loader,
        criterion,
        optimizer,
        device
):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    epoch_loss = running_loss / len(train_loader)
    return epoch_loss


def validate(
        
        model,
        val_loader,
        criterion,
        device
):
    model.eval()
    with torch.no_grad():
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / len(val_loader)
    accuracy = 100 * correct / total
    return epoch_loss, accuracy


if __name__ == '__main__':
    main()