import os
import random
import shutil

PROJECT = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project"
CANCEROUS_DIR = os.path.join(PROJECT, "cancerous")
NON_CANCEROUS_DIR = os.path.join(PROJECT, "non_cancerous")

TRAIN_DIR = os.path.join(PROJECT, "train")
TEST_DIR = os.path.join(PROJECT, "test")

SPLIT = 0.7
SEED = 42

random.seed(SEED)

def split_class(src_dir, class_name):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    random.shuffle(files)

    n_train = int(len(files) * SPLIT)
    train_files = files[:n_train]
    test_files = files[n_train:]

    train_dest = os.path.join(TRAIN_DIR, class_name)
    test_dest = os.path.join(TEST_DIR, class_name)
    os.makedirs(train_dest, exist_ok=True)
    os.makedirs(test_dest, exist_ok=True)

    for f in train_files:
        shutil.copy2(os.path.join(src_dir, f), os.path.join(train_dest, f))
    for f in test_files:
        shutil.copy2(os.path.join(src_dir, f), os.path.join(test_dest, f))

    print(f"  {class_name}: {len(train_files)} train / {len(test_files)} test  (total {len(files)})")
    return len(train_files), len(test_files)

print("Splitting dataset 70/30...")
c_train, c_test = split_class(CANCEROUS_DIR, "cancerous")
n_train, n_test = split_class(NON_CANCEROUS_DIR, "non_cancerous")

print(f"\nDone!")
print(f"  train/  -> {c_train + n_train} images  ({TRAIN_DIR})")
print(f"  test/   -> {c_test  + n_test}  images  ({TEST_DIR})")
