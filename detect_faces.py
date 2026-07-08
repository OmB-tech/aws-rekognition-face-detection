import boto3
import json
import os

# -----------------------------
# Configuration
# -----------------------------
BUCKET_NAME = os.environ["S3_BUCKET"]
IMAGE_FILE = "employee.jpg"
print("Bucket:", BUCKET_NAME)
print("Region:", os.environ.get("AWS_DEFAULT_REGION"))
# -----------------------------
# AWS Clients
# -----------------------------
s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")

# -----------------------------
# Upload Image to S3
# -----------------------------
print(f"Uploading {IMAGE_FILE} to S3...")

s3.upload_file(
    Filename=IMAGE_FILE,
    Bucket=BUCKET_NAME,
    Key=IMAGE_FILE
)

print("Image uploaded successfully.\n")

# -----------------------------
# Detect Faces
# -----------------------------
print("Detecting faces...\n")

response = rekognition.detect_faces(
    Image={
        "S3Object": {
            "Bucket": BUCKET_NAME,
            "Name": IMAGE_FILE
        }
    },
    Attributes=["ALL"]
)

faces = response["FaceDetails"]

print("=" * 40)
print(f"Total Faces Detected: {len(faces)}")
print("=" * 40)

results = []

for i, face in enumerate(faces, start=1):
    confidence = face["Confidence"]

    print(f"\nFace {i}")
    print(f"Confidence: {confidence:.2f}%")

    results.append({
        "Face": i,
        "Confidence": round(confidence, 2)
    })

# -----------------------------
# Save JSON Result
# -----------------------------
output = {
    "TotalFaces": len(faces),
    "Faces": results
}

with open("result.json", "w") as f:
    json.dump(output, f, indent=4)

print("\nresult.json created successfully.")
print("\nDone!")