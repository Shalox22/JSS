from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io

app = FastAPI(title="Poultry Disease Detection API")

# Load your trained CNN model
model = None
model_load_error = None
tf = None
try:
    import tensorflow as tf  # type: ignore[reportMissingModuleSource]
    from tensorflow.keras.models import load_model  # type: ignore[reportMissingModuleSource]

    # load without compiling to avoid issues with optimizer/function signatures
    model = load_model("poultry_disease_cnn.h5", compile=False)
except Exception as e:
    model_load_error = str(e)
class_names = ["Healthy", "Coccidiosis", "Newcastle Disease", "Salmonella"]

# Automatically get input shape from the model
if model is not None:
    _, model_height, model_width, model_channels = model.input_shape
else:
    model_height = model_width = model_channels = None

@app.get("/")
def home():
    return {"message": "Welcome to Poultry Disease Detection API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is unavailable. {model_load_error}",
        )
    try:
        if tf is None:
            raise HTTPException(
                status_code=503,
                detail="TensorFlow is not installed in this container image.",
            )

        # Read image
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Resize to model input size
        img = img.resize((model_width, model_height))

        pixels = list(img.getdata())
        width, height = img.size

        # Ensure correct channels
        if model_channels != 3:
            raise HTTPException(status_code=400, detail=f"Expected RGB (3 channels), got model_channels={model_channels}")

        # Flatten HWC row-major pixels into a normalized tensor without NumPy
        flat = []
        for y in range(height):
            row_off = y * width
            for x in range(width):
                r, g, b = pixels[row_off + x]
                flat.extend((r / 255.0, g / 255.0, b / 255.0))

        img_tensor = tf.constant(flat, dtype=tf.float32)
        img_tensor = tf.reshape(img_tensor, (height, width, 3))
        img_tensor = tf.expand_dims(img_tensor, axis=0)

        # Predict
        prediction = model.predict(img_tensor)
        pred_tensor = tf.constant(prediction, dtype=tf.float32)
        pred_idx = int(tf.argmax(pred_tensor, axis=-1)[0].numpy())
        confidence = float(tf.reduce_max(pred_tensor, axis=-1)[0].numpy())
        predicted_class = class_names[pred_idx]

        return {"class": predicted_class, "confidence": round(confidence, 4)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image or format. {str(e)}")
