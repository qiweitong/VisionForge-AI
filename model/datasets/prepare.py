import os
import random
import shutil

RAW_DIR = r"E:\VisionForge AI\model\raw"

OUTPUT_DIR = r"E:\VisionForge AI\model\datasets"

TRAIN_RATIO = 0.8
VAL_PATIO = 0.1
TEST_RATIO = 0.1
RANDOM_SEED = 42

def create_dir(classes):
    """
    创建训练集、验证集和测试集的目录结构
    """
    for split in ['train', 'val', 'test']:
        split_dir = os.path.join(OUTPUT_DIR, split)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)
        for cls in classes:
            cls_dir = os.path.join(split_dir, cls)
            if not os.path.exists(cls_dir):
                os.makedirs(cls_dir,exist_ok=True)


def split_dataset():
    random.seed(RANDOM_SEED)

    classes = sorted(os.listdir(RAW_DIR))
    create_dir(classes)
    print("="*50)

    for cls in classes:

        class_path = os.path.join(RAW_DIR, cls)

        images = os.listdir(class_path)

        random.shuffle(images)

        total =len(images)
        train_num = int(total * TRAIN_RATIO)
        val_num = int(total * VAL_PATIO)

        train_images = images[:train_num]
        val_images = images[train_num:train_num + val_num]  
        test_images = images[train_num + val_num:]

        print(f"{cls}")
        print(f"总数: {total}")
        print(f"Train: {len(train_images)}")
        print(f"Val: {len(val_images)}")
        print(f"Test: {len(test_images)}")
        print("-" * 30)

        copy_images(train_images, cls, "train")
        copy_images(val_images, cls, "val")
        copy_images(test_images, cls, "test")

def copy_images(images_list, cls, split):
   save_dir = os.path.join(OUTPUT_DIR, split, cls)
   source_dir = os.path.join(RAW_DIR, cls)

   for image_name in images_list:

       shutil.copy2(
           os.path.join(source_dir, image_name),
           os.path.join(save_dir, image_name)
       )


if __name__ == "__main__":
    split_dataset()
    print("数据集划分完成！")