from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

MODEL = tf.keras.models.load_model("C:/Code/Deep Learning/potato-disease/models/1.keras")
CLASS_NAMES = ["Early Blight","Late Blight","Healthy"]



@app.get('/ping')
async def ping():
    return "Hello I am alive!"

def read_file_as_image(data)->np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)

    predictions =  MODEL.predict(img_batch)

    predicted_class =  CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {
        'class' : predicted_class,
        'confidence' : float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, port = 8000, host = "localhost")