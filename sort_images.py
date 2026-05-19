import csv
import os
import zipfile

PROJECT = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project"
METADATA = os.path.join(PROJECT, "HAM10000_metadata")
ZIP1 = os.path.join(PROJECT, "HAM10000_images_part_1.zip")
ZIP2 = os.path.join(PROJECT, "HAM10000_images_part_2.zip")

CANCEROUS_DIR = os.path.join(PROJECT, "cancerous")
NON_CANCEROUS_DIR = os.path.join(PROJECT, "non_cancerous")

# Diagnoses considered malignant/cancerous
CANCEROUS_DX = {"mel", "bcc", "akiec"}

os.makedirs(CANCEROUS_DIR, exist_ok=True)
os.makedirs(NON_CANCEROUS_DIR, exist_ok=True)

# Build image_id -> label mapping from metadata
label_map = {}
with open(METADATA, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        image_id = row["image_id"].strip()
        dx = row["dx"].strip()
        label_map[image_id] = dx in CANCEROUS_DX

print(f"Loaded {len(label_map)} entries from metadata")

def extract_zip(zip_path):
    counts = {"cancerous": 0, "non_cancerous": 0, "skipped": 0}
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        total = len(names)
        for i, name in enumerate(names, 1):
            if i % 500 == 0:
                print(f"  [{i}/{total}] {os.path.basename(zip_path)}")
            basename = os.path.basename(name)
            if not basename:
                continue
            image_id = os.path.splitext(basename)[0]
            if image_id not in label_map:
                counts["skipped"] += 1
                continue
            dest_dir = CANCEROUS_DIR if label_map[image_id] else NON_CANCEROUS_DIR
            dest_path = os.path.join(dest_dir, basename)
            if not os.path.exists(dest_path):
                data = zf.read(name)
                with open(dest_path, "wb") as out:
                    out.write(data)
            if label_map[image_id]:
                counts["cancerous"] += 1
            else:
                counts["non_cancerous"] += 1
    return counts

print("Processing part 1...")
c1 = extract_zip(ZIP1)
print("Processing part 2...")
c2 = extract_zip(ZIP2)

total_cancerous = c1["cancerous"] + c2["cancerous"]
total_non_cancerous = c1["non_cancerous"] + c2["non_cancerous"]
total_skipped = c1["skipped"] + c2["skipped"]

print("\nDone!")
print(f"  Cancerous images   : {total_cancerous}  -> {CANCEROUS_DIR}")
print(f"  Non-cancerous images: {total_non_cancerous}  -> {NON_CANCEROUS_DIR}")
print(f"  Skipped (not in metadata): {total_skipped}")
