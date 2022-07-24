import os
from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import cv2
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from utils import count_faces
from helper import *

#Configure the model
net = cv2.dnn.readNetFromDarknet('/var/www/html/face-count/cfg/yolov3-face.cfg', '/var/www/html/face-count/model-weights/yolov3-wider_16000.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Create an API 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)

@app.get('/')
async def readRoot():
    return { 'message': 'Server up and running.' }

# Will be used by current system
@app.post('/api/face-validation')
async def face_validation(test_image: UploadFile, id: str = Form(default="Null"), image: str = Form(default="Null")):
    test_image = await test_image.read()
    test_image = byteImg_to_cvImg(test_image)
    result,distance = predict(get_image_from_url(image), test_image)
    result = bool(result[0])
    distance = str(distance[0])
    return {'id': id, 'count': count_faces(test_image, net), 'result': result, 'distance': distance}

if __name__ == '__main__':
    # uvicorn.run(app)
    uvicorn.run("server:app", host='0.0.0.0', port=(int)(os.environ.get('PORT', 5000)), ssl_keyfile='/etc/letsencrypt/live/nayara.like2gift.com/privkey.pem', ssl_certfile='/etc/letsencrypt/live/nayara.like2gift.com/fullchain.pem', log_level='error')