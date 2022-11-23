# Dev

## General Idea:

Convert image to CNN features and utilize KNN model to search top K similar images in the features space.

Pros: easy to implement

Cons: computationally costly (requires large amount of memory (at least 5 Gb)) and scalability would be a great issues if the number of images increase.

### Alternative approach:

- **Offline generating precomputed mapping**: Given the constraint that the input images would be from the given dataset, precomputed the mapping of each image url and its top 10 most similar images in URL forms, store them in JSON or pickle, and able to quickly look up the images as well as saving deployment computing resources. However **********************************************************************input will be limited to image URL and offline generating the mapping would takes more time compared to the other two alternative appraoches.**********************************************************************
- **Dimension reduction**: PCA + TSNE to decrease the dimension of the features and reduce the search space so that it can improve the run time. This also reduces the memory cost. However, **approximate nearest neighbor might not be as accurate as the current appraoch.**
- **Label filtering to reduce the search space:** categorize each image to a certain label such as woman shoes, white dress, black hoodie, black shorts etc. After label annotation, train a multi-class classification model to reduce the search space, then search similar images inside that class. However, ************************************************************************************************this would take more time, as it needs to annotate and train another model to have this cascade structure work.************************************************************************************************ The scalability as well as accuracy is most promising in this case.

## Folder structure:

|— data_extract.ipynb

|— valentino

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|— 0.jpg

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|— 1.jpg …

|— img_similarity.ipynb

|— resnet

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|— assets

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|— variables

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|— saved_model.pb

1. Run the first part of data_extract.ipynb to create folder of images
2. Run img_similarity.ipynb to 
    1. export `resnet` folder for Resnet50 models to transform features
    2. export `features-valentino-resnet-448-224.pickle` that contain all of the embedded features of processed images from valentino folder
    3. export `knn_model.pickle` that contain the NN model that find the most similar images given an input image via euclidean distance in the embedded features space
    4. export `filenames-valentino-448-224.pickle` that contain the mapping between filename (valentino/[original index].jpg) and processed index (which are exported from the NN model)
3. Run the second part of the data_extract.ipynb to create the mapping between the original image url and the NN predicted index and export it to `img_url.csv`

**********Move********** `knn_model.pickle` and folder `resnet` into the *flask-xgen* folder to run the API
