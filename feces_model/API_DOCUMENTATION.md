# Poultry Disease Detection API - Developer Documentation

## Overview

This is a FastAPI-based REST API that uses a trained Convolutional Neural Network (CNN) to detect and classify poultry diseases from image inputs. The API analyzes chicken images and identifies whether the bird is healthy or suffering from one of three diseases: Coccidiosis, Newcastle Disease, or Salmonella.

**Framework:** FastAPI  
**Model:** TensorFlow/Keras CNN (`poultry_disease_cnn.h5`)  
**Port:** 8000 (default)

---
docker build -t poultry-disease-api .
docker run -p 8000:8000 poultry-disease-api
## API Endpoints

### 1. Home Endpoint

**Endpoint:** `GET /`

**Description:** Returns a welcome message and verifies the API is running.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Welcome to Poultry Disease Detection API"
}
```

**Status Code:** `200 OK`

---

### 2. Disease Prediction Endpoint

**Endpoint:** `POST /predict`

**Description:** Accepts an image file and returns the predicted disease classification and confidence score.

#### Request

**Method:** `POST`  
**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (Required): Image file in `multipart/form-data` format
  - **Supported Formats:** JPEG, PNG, or any format supported by PIL
  - **Required Channels:** RGB (automatically converted if needed)
  - **Model Input Size:** Automatically resized to match model requirements

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/poultry_image.jpg"
```

**Example with Python:**
```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("poultry_image.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()
print(result)
```

#### Response

**Success Response (Status: 200 OK):**
```json
{
  "class": "Healthy",
  "confidence": 0.9876
}
```

**Response Fields:**
- `class` (string): Predicted disease classification. Possible values:
  - `"Healthy"` - No disease detected
  - `"Coccidiosis"` - Parasitic disease
  - `"Newcastle Disease"` - Viral infection
  - `"Salmonella"` - Bacterial infection

- `confidence` (float): Confidence score of the prediction (0.0 to 1.0)
  - `1.0` = 100% confidence
  - `0.5` = 50% confidence
  - Lower values indicate uncertain predictions

#### Error Responses

**Invalid Image Format (Status: 400 Bad Request):**
```json
{
  "detail": "Invalid image or format. Cannot identify image file"
}
```

**Unsupported Channel Count (Status: 400 Bad Request):**
```json
{
  "detail": "Invalid image or format. Expected 3 channels, got 1"
}
```

**No File Provided (Status: 422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

**Common Error Scenarios:**
| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid image or format" | Corrupted file or unsupported format | Provide a valid JPEG, PNG, or image file |
| "Expected 3 channels, got X" | Image is not in RGB format (e.g., grayscale) | Convert image to RGB before sending |
| 422 Unprocessable Entity | No file included in request | Include `file` parameter in multipart form |

---

## Image Processing Pipeline

The API processes images through the following steps:

1. **Read Image:** Image file is read from the request
2. **Convert to RGB:** Ensures the image has 3 color channels (if needed)
3. **Resize:** Image is resized to model input dimensions
4. **Normalize:** Pixel values are normalized to 0-1 range (divided by 255)
5. **Add Batch Dimension:** Adds batch dimension required by the model
6. **Predict:** CNN model generates predictions
7. **Return Results:** Returns predicted class and confidence score

**Model Input Shape:** Retrieved dynamically from `poultry_disease_cnn.h5`

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- TensorFlow/Keras
- FastAPI
- Uvicorn

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the model file exists:
```bash
# The file should be in the same directory as api.py
ls poultry_disease_cnn.h5
```

### Running the API

**Development Mode:**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Production Mode:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker Deployment:**
```bash
docker-compose up --build
```

The API will be available at: `http://localhost:8000`

---

## Testing

### Using FastAPI Interactive Docs

Once the API is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Example Test Cases

**Test 1: Healthy Bird Image**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@healthy_bird.jpg"
```

Expected output:
```json
{
  "class": "Healthy",
  "confidence": 0.98
}
```

**Test 2: Coccidiosis Detection**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sick_bird.jpg"
```

**Test 3: Error Handling (Invalid Format)**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@text_file.txt"
```

---

## Integration Guide

### Python Integration
```python
import requests

def detect_disease(image_path):
    url = "http://localhost:8000/predict"
    with open(image_path, "rb") as img:
        response = requests.post(url, files={"file": img})
    
    if response.status_code == 200:
        result = response.json()
        print(f"Disease: {result['class']}")
        print(f"Confidence: {result['confidence']}")
    else:
        print(f"Error: {response.json()}")

# Usage
detect_disease("poultry_image.jpg")
```

### JavaScript/Node.js Integration
```javascript
async function detectDisease(imagePath) {
  const formData = new FormData();
  formData.append('file', await fs.readFile(imagePath));

  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  console.log(`Disease: ${result.class}`);
  console.log(`Confidence: ${result.confidence}`);
}
```

---

## Performance Considerations

- **Inference Time:** Depends on image size and server hardware
- **Supported Batch Size:** Currently processes one image per request
- **Model Size:** `poultry_disease_cnn.h5` should be optimized for production use
- **Concurrency:** FastAPI handles multiple concurrent requests efficiently

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Ensure `poultry_disease_cnn.h5` is in the same directory as `api.py` |
| Port 8000 already in use | Use `--port 8001` or kill the process using port 8000 |
| Out of memory errors | Reduce concurrent requests or use smaller model |
| Slow predictions | Check server resources and optimize model if needed |

---

## Additional Notes

- The model dynamically reads its input shape from the saved model file
- Images are automatically converted to RGB format
- Confidence scores are rounded to 4 decimal places
- All predictions are deterministic (same input = same output)

For questions or issues, contact the development team.
