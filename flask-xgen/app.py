from flask import Flask,request,jsonify
import os
import sklearn
import pandas as pd
import tensorflow
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import  preprocess_input
from werkzeug.utils import secure_filename
import pickle
#ResNet50,
app = Flask(__name__)

resmodel = tensorflow.keras.models.load_model('resnet')
neighbors = pickle.load(open('knn_model.pickle','rb'))
img_url_df = pd.read_csv('img_url.csv')

def extract_features(img_path, model):
    input_shape = (448, 224, 3)
    img = image.load_img(img_path, target_size=(
        input_shape[0], input_shape[1]))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(flattened_features)
    return normalized_features

def findNN(neighbors,features,img_url_df,sim_count):
    distances,indices = neighbors.kneighbors([features])
    # print(indices)
    # print("=>",img_url_df.head(3))
    ret_dict = {}
    for i in range(1,sim_count+1):
        idx = int(indices[0][i])
        # print("=>",img_url_df[img_url_df['feature_idx']==str(idx)])
        url = img_url_df[img_url_df['feature_idx']==str(idx)].values[0][0]
        ret_dict[url] = float(distances[0][i])
    return ret_dict


@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'


# technically, we only need a knn model
# a feature extraction model to read the input image
# return a list of links of those images for embedding purposes


@app.route('/img-upload', methods=['POST'])
def predict_img():
    # check if the post request has the file part
    import time
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file :
        sim_count = request.args.get('sim_count')
        try:
            sim_count = int(sim_count)
        except:
            # default return top 10 similar images
            sim_count = 10
        filename = secure_filename(file.filename)
        filename_path = os.path.join('.', filename)
        file.save(filename_path)
        features = extract_features(filename_path,resmodel)
        # print(f"\n{sim_count},{type(sim_count)}\n")
        start = time.time()
        ret_dict = findNN(neighbors,features,img_url_df,sim_count)
        end = time.time()
        resp = jsonify({'time_takes':round(end-start,2),
        'sim_count':sim_count,'sim_img_url' : ret_dict})
        
        # print("\n",end-start,"<<<<<< need this amount of time\n")
        resp.status_code = 201
        os.remove(filename_path)
        return resp


if __name__ == "__main__":
    app.run(debug=True)