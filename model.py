import io
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# Load YOUR custom trained YOLO11 model brain!
model = YOLO("best.pt")

def detect_sign(image_bytes: bytes) -> dict:
    try:
        # Load image from the webcam bytes
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)
        
        # 🔥 BACKEND SPEED HACK: imgsz=320 makes the CPU process the image 2x faster!
        results = model(image_np, conf=0.5, imgsz=320, verbose=False)[0]
        
        # If no hand/sign is found
        if len(results.boxes) == 0:
            return {"sign": None, "message": "No hand detected"}
            
        # Get the highest confidence detection
        best_box = results.boxes[0]
        
        # Extract the Sign Name
        class_id = int(best_box.cls[0])
        sign_name = results.names[class_id]
        
        # Extract the bounding box coordinates
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])
        
        # Extract Confidence
        confidence_value = float(best_box.conf[0])
        conf_level = "High" if confidence_value > 0.8 else "Medium"
        
        return {
            "sign": sign_name.upper(),
            "confidence": conf_level,
            "box": [x1, y1, x2, y2],
            "message": f"Detected: {sign_name.upper()}"
        }
        
    except Exception as e:
        return {"sign": None, "message": f"Error: {str(e)}"}