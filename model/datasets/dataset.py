from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
def get_train_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    ])

def get_val_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def get_dataloaders(
        dataset_root,
        batch_size=32,
        num_workers=0
):
    train_dir =os.path.join(dataset_root, 'train')
    val_dir = os.path.join(dataset_root, 'val')
    #转为数字编号id
    train_dataset = datasets.ImageFolder(
        root=train_dir,
        transform=get_train_transforms()
    )

    val_dataset = datasets.ImageFolder(
        root=val_dir,
        transform=get_val_transforms()
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )

    return (
        train_loader,
        val_loader,
        train_dataset.classes
    )



if __name__ == '__main__':

    train_loader, val_loader, classes = get_dataloaders(
        dataset_root=r"E:\VisionForge AI\model\datasets",
        batch_size=32,
    )

    print("=" * 50)
    print("类别名称：", classes)

    print("训练集数量：", len(train_loader.dataset))
    print("验证集数量：", len(val_loader.dataset))

    images, labels = next(iter(train_loader))

    print("=" * 50)
    print("图片 Shape：", images.shape)
    print("标签 Shape：", labels.shape)

    print("前10个标签：")
    print(labels[:10])

    print("=" * 50)
    print("类别映射：")
    print(train_loader.dataset.class_to_idx)

    print("=" * 50)

    image =images[0]

    image =image.permute(1, 2, 0).numpy()  # 将通道维度移到最后，并转换为 NumPy 数组
    image = image * [0.229, 0.224, 0.225] + [0.485, 0.456, 0.406]  # 反归一化
    plt.imshow(image)
    plt.title(classes[labels[0]])
    plt.axis("off")
    plt.show()
