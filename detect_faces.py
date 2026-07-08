import boto3
import json
import os
from PIL import Image

# -----------------------------
# Configuration
# -----------------------------
BUCKET_NAME = os.environ["S3_BUCKET"]
REGION = os.environ["AWS_DEFAULT_REGION"]
IMAGE_FILE = "employee.jpg"

print("=" * 50)
print("Bucket :", BUCKET_NAME)
print("Region :", REGION)
print("Image  :", IMAGE_FILE)
print("=" * 50)

# -----------------------------
# Check Local Image
# -----------------------------
if not os.path.exists(IMAGE_FILE):
    raise FileNotFoundError(f"{IMAGE_FILE} not found!")

print("File Size:", os.path.getsize(IMAGE_FILE), "bytes")

img = Image.open(IMAGE_FILE)
print("Image Format :", img.format)
print("Image Mode   :", img.mode)
print("Image Size   :", img.size)

# -----------------------------
# AWS Clients
# -----------------------------
s3 = boto3.client("s3", region_name=REGION)
rekognition = boto3.client("rekognition", region_name=REGION)

# -----------------------------
# Upload Image
# -----------------------------
print("\nUploading image to S3...")

s3.upload_file(
    IMAGE_FILE,
    BUCKET_NAME,
    IMAGE_FILE,
    ExtraArgs={
        "ContentType": "image/jpeg"
    }
)

print("Upload Successful!")

# -----------------------------
# Verify Upload
# -----------------------------
head = s3.head_object(
    Bucket=BUCKET_NAME,
    Key=IMAGE_FILE
)

print("S3 Object Size :", head["ContentLength"])
print("S3 ContentType :", head.get("ContentType"))

# -----------------------------
# Detect Faces (Using Image Bytes)
# -----------------------------
print("\nRunning Rekognition...")

with open(IMAGE_FILE, "rb") as image:
    response = rekognition.detect_faces(
        Image={
            "Bytes": image.read()
        },
        Attributes=["DEFAULT"]
    )

faces = response["FaceDetails"]

print("\n==============================")
print("Faces Detected :", len(faces))
print("==============================")

results = []

for i, face in enumerate(faces, start=1):
    confidence = face["Confidence"]

    print(f"\nFace {i}")
    print(f"Confidence : {confidence:.2f}%")

    results.append({
        "Face": i,
        "Confidence": round(confidence, 2)
    })

output = {
    "TotalFaces": len(faces),
    "Faces": results
}

with open("result.json", "w") as f:
    json.dump(output, f, indent=4)

print("\nresult.json created successfully.")
print("Done!")