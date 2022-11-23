# flask-xgen

Go to [Google Drive](https://drive.google.com/drive/folders/1vc3ubtrhpsiRYRxEeRhr7BzEwUcXq1XI?usp=sharing) to download necessary artifacts and place them in the ***flask-xgen*** folder like the following:

## Complete API file structure

***flask-xgen***

|— app.py

|— img_url.csv

|— Dockerfile

|— knn_model.pickle

|— requirements.txt

|— resnet

|— assets

|— variables

|— saved_model.pb

**make sure the file structure is like this before running local method**

## Methods of running the flask API

1. running dev server locally:
    1. `pip install -r requirements.txt` 
    2. `python app.py`
2. creating docker image and running it locally:
    1. navigate under **********flask-xgen**********
    2. `docker build --tag flask-xgen .` 
    3. `docker run -d -p 5000:5000 flask-xgen` 
3. pulling the docker image from public docker hub:
    1.  `docker pull jimmycoding829/repo1:xgenFlask` 
    2. `docker run -d -p 5000:5000 jimmycoding829/repo1:xgenFlask`

**Running the Docker methods (2,3) require 6Gb of memory to run smoothly**

## Available End Point:

**Ping Testing purposes**

GET  [http://127.0.0.1:5000](http://127.0.0.1:5000)/

Response: `<h1>Hello from Flask & Docker</h1>`

************************************Predict Input Image************************************

POST [http://127.0.0.1:5000](http://127.0.0.1:5000)/img-upload

Params (optional):

| key | value |
| --- | --- |
| sim_count | ≤10 |

sim_count indicates the number of the most similar images user want the API to return.

(If no sim_count specify, it will default return the 10 most similar images’ URLs.)

Body (required):

| key | value |
| --- | --- |
| file | file image: target.jpg |

The key should be “file”, while the value should be the image file itself.

Example call below using Postman:

![Untitled](flask-xgen%20d7f2a330dd0b44e7846607ef1c8cdaa1/Untitled.png)

return response:

```json
{   
    "sim_count": 3, // the number of most similar images to return
    "sim_img_url": {
				 // similar image url : distance from original image (smaller the more similar)
        "https://similar_image_1.jpg": 0.6474766135215759,
        "https://similar_image_2.jpg": 0.6370326280593872,
        "https://similar_image_3.jpg": 0.5660814046859741
    },
		// time takes to do the prediction, varies based on computing resources
    "time_takes": 16.8
}
```

Example return JSON:

```json
{
    "sim_count": 5,
    "sim_img_url": {
        "https://www.valentino.com/12/12177569ps_tools_f2l.jpg": 0.6474766135215759,
        "https://www.valentino.com/12/12463694rc_tools_f2l.jpg": 0.6370326280593872,
        "https://www.valentino.com/12/12596242ok_tools_f2l.jpg": 0.5660814046859741,
        "https://www.valentino.com/variants/images/1647597278050936/F/w400.jpg": 0.6699393391609192,
        "https://www.valentino.com/variants/images/22250442025613500/F/w400.jpg": 0.6452754735946655
    },
    "time_takes": 2.78
}
```