from fastapi import FastAPI, Request, Form, UploadFile, File
import uvicorn
from utils import count_faces
import cv2
import os
from helper import *
from pydantic import BaseModel


class Data(BaseModel):
    id: str
    image: str
    test_image: str


net = cv2.dnn.readNetFromDarknet(
    "./cfg/yolov3-face.cfg", "./model-weights/yolov3-wider_16000.weights"
)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )
# app.add_middleware(HTTPSRedirectMiddleware)



@app.get('/')
async def readRoot():
    return { 'message': 'Server up and running.' }

@app.post("/api/face_count_url")
async def face_count_url(info: Request):
    data = await info.json()
    id = data["id"]
    image_path = data["image"]
    image = get_image_from_url(image_path)
    return {"id": id, "count": count_faces(image, net)}


@app.post("/api/face_count_path")
async def face_count_path(info: Request):
    data = await info.json()
    id = data["id"]
    image_path = data["image"]
    image = get_image_from_path(image_path)
    return {"id": id, "count": count_faces(image, net)}


@app.post("/api/face_validate_url")
async def face_validate_url(data: Data):
    id, image, test_image = data.id, data.image, data.test_image
    result, distance = predict(
        get_image_from_url(image), get_image_from_url(test_image)
    )
    result = str(result[0])
    distance = str(distance[0])
    return {"id": id, "result": result, "distance": distance}


@app.post("/api/face_validate_path")
async def face_validate_path(data: Data):
    id, image, test_image = data.id, data.image, data.test_image
    result, distance = predict(
        get_image_from_path(image), get_image_from_path(test_image)
    )
    result = str(result[0])
    distance = str(distance[0])
    return {"id": id, "result": result, "distance": distance}



#  First image will be as URL, 2nd will be as File

@app.post("/api/face_validate_url_file")
async def create_file(test_image: UploadFile, id: str = Form(), image: str=Form()):
    # image=image.file.read()
    test_image = await test_image.read()
    result, distance = predict(get_image_from_url (image), byteImg_to_cvImg( test_image))
    result = str(result[0])
    distance = str(distance[0])
    return {"id": id, "result": result, "distance": distance}


# First both images will be as File
@app.post("/api/face_validate_file")
async def create_file(image: UploadFile,test_image: UploadFile, id: str = Form()):
    image=await image.read()
    test_image = await test_image.read()
    result, distance = predict(byteImg_to_cvImg(image), byteImg_to_cvImg( test_image))
    result = str(result[0])
    distance = str(distance[0])
    return {"id": id, "result": result, "distance": distance}

@app.post('/api/face-validation')
async def face_validation(test_image: UploadFile, id: str = Form(default="Null"), image: str = Form(default="Null")):
    test_image = await test_image.read()
    test_image = byteImg_to_cvImg(test_image)
    result,distance = predict(get_image_from_url(image), test_image)
    result = bool(result[0])
    distance = str(distance[0])
    return {'id': id, 'count': count_faces(test_image, net), 'result': result, 'distance': distance}



if __name__ == "__main__":
    ## uncomment to run locally
    uvicorn.run(app)

    ## uncomment to run on heroku
    # uvicorn.run("server:app", host='0.0.0.0', port=(int)(os.environ.get('PORT', 5001)))
