from fastapi import FastAPI,Request
import uvicorn
from utils import count_faces
import cv2
import os
from helper import *


net = cv2.dnn.readNetFromDarknet('./cfg/yolov3-face.cfg', './model-weights/yolov3-wider_16000.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

app = FastAPI()

@app.post('/api/face_count_url')
async def face_count_url(info: Request):
    data=await info.json()
    id=data['id']
    image_path=data['image']
    image=get_image_from_url(image_path)
    return {'id':id,'count':count_faces(image,net)}

@app.post('/api/face_count_path')
async def face_count_path(info: Request):
    data=await info.json()
    id=data['id']
    image_path=data['image']
    image=get_image_from_path(image_path)
    return {'id':id,'count':count_faces(image,net)}

@app.post('/api/face_validate_url')
async def face_validate_url(info: Request):
    data= await info.json()
    id=data['id']
    image=data['image']
    test_image=data['test_image']
    result,distance=predict(get_image_from_url(image),get_image_from_url(test_image))
    result=str(result[0])
    distance=str(distance[0])
    return {'id':id,'result':result,'distance':distance}


@app.post('/api/face_validate_path')
async def face_validate_path(info: Request):
    data= await info.json()
    id=data['id']
    image=data['image']
    test_image=data['test_image']
    result,distance=predict(get_image_from_path(image),get_image_from_path(test_image))
    result=str(result[0])
    distance=str(distance[0])
    return {'id':id,'result':result,'distance':distance}

if __name__ == '__main__':
    ## uncomment to run locally
    uvicorn.run(app)

    ## uncomment to run on heroku
    #uvicorn.run("server:app", host='0.0.0.0', port=(int)(os.environ.get('PORT', 5001)))