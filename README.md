# FACE COUNT AND VALIDATION API


### Step 1: Get all the requirements

Run the following command to install all the requirements

    pip install -r requirements.txt

---

### Step 2: Get the yolo weights (Necessary step for face count)

- Option 1: From bash script

    Run the `get_models.sh` script in the _**main**_ folder


- Option 2: Download files from GDrive, extract and save them to _**model-weights**_ folder.
    
    - yolov3-wider_16000.weights : [Download](https://drive.google.com/file/d/1xo_G2GK8Y7DuriRT8RYk9FzxCVjS3ZkO/view?usp=sharing)

    - YOLO_Face.h5 : [Download](https://docs.google.com/uc?export=download&id=1a_pbXPYNj7_Gi6OxUqNo_T23Dt_9CzOV)

---



### Step 3: Start the server

>Note: Check the ending of server.py file before running and set your config by uncommenting the lines.

Run:

    python server.py 



---
---
# USAGE 

## 1. Face Count API
This API can be used in 2 ways:
-   Using Image URL
-   Using Image Absoloute Path
---
### A) USING URL

Call the api with:

    /api/face_count_url

Send 2 parameters in json format.

    {
        "id":"<refrence id for image>",
        "image": "<img_url>"
    }
---
### B) USING PATH

Call the api with:

    /api/face_count_path

Send 2 parameters in json format.

    {
        "id":"<refrence id for image>",
        "image": "path//to//image"
    }

>Note: Remember to use double forward slashes in path.
---
---
## 2. Face Validation API
This API can be used in 2 ways:
-   Using Image URLs
-   Using Image Absoloute Paths
---
### A) USING URL
Call the api with:

    /api/face_validate_url

**Send 3 parameters** in json format.

    {
        "id":"<refrence id for image>",
        "image": "<known_img_url>",
        "test_image": "<test_img_url>"
    }
---
### B) USING PATH
Call the api with:

    /api/face_validate_path

**Send 3 parameters** in json format.

    {
        "id":"<refrence id for image>",
        "image": "path//to//known_image",
        "test_image": "path//to//test_image"
    }

>Note: Remember to use double forward slashes in path.


---
# 2 NEW FUNCTIONALITY ADDED


### 1) __Images as URL, test_image as file__


    /api/face_validate_url_file

*Send 3 parameters* in form data.

    id: <refrence id for image>
    image: <known_img_url>
    test_image: image as file

---

### 2) __Both image and test_image as file__
    
        /api/face_validate_file


*Send 3 parameters* in form data.
        
            id: <refrence id for image>
            image: image as file
            test_image: image as file