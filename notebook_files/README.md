### Image Classification notebook file

This notebook file consists the required code for Biologial Image Analysis.
Since the data is huge I couldn't able to download it or when i download it I am getting as differnet partitions. So I decided to run the notebook file in the google colab so that I can read the data from the drive itself.

### Data Preprocessing 

Since the data is in google drive I have given some permission so that data can be read directly from the drive using google colab. 

Image Classification data consists of the train and test folders each containing the images of the differnet human organs. There are 12 sub folders namely skin, lungs, tissue etc which are the labels for our data.
So we got the images inside each sub folder. When I saw the images all the images are in "tif" format which is not compatible with the tensorflow. So I decided to convert each and every image to jpg format. I used open-cv library to read "tif" image and convert to "jpg" image and finally saved to my drive with new data directory.

Once I have the new data directories for both train and test, I used the keras image from the directory method to read the dataset. I have used 2 percent of records for the validation split.

### Model Training

Once data is ready, I created a Keras Sequential Model with first layer as Normalization layer(since image is RGB image each pixel will have values in range or 0-255, we need to rescale it to 0-1 so that features can be extracted properly), next 3 layers as Convolution layers with Max pooling and finally 2 Dense layers with last Dense layer having 12 nodes since it has to give those many outputs to classify 12 images.

After Model is built, we need to compile model. During Model compilation we need to provide loss function, optimizer and what metrics need to be calculated.
I have used sparseCategoricalCrossEntrophy which applies the softmax function on the input so that it calculates the probabilities of those 12 classes and apply cross entrophy function. 
For optimizer function I have used "adam" optimizer function which is combination of the Adagrad and Momentum optimizer.
As for metrics calculation I have just used "accuracy"

Once model is compiled, we need to fit the model using train data, valid data. Here we can also provide other hyper parameters like epochs, callbacks etc. I have also provided tensorboard callback to view the metrics and projections. Once the model training is done I have plotted the accuracy and loss results using the matplotlib and the Tensorboard.


### Model Evaluation

We can evaluate the model using model.evaluate() method by passing the test data and logging the results.

### Model Prediction

We can predict the results by passing the new dataset(dataset which is new and dont have labels). Since we don't new data I have predicted on the test data itself.

### Model Training using the pre-defined models.

We can train any model using the pre-defined models. This can be done by using the 
1) TF Hub models
2) Keras applications Networks

I have used the Keras applications for the pre-defined models like VGG and Inception models. I have repeated the same process Model Training, plotting metrics  using matplotlib and the Tensorboard, Model Evaluation and Model Prediction.


### Visualize the Predictions

We can visualize the prediction results using scatter plot between the predicted output and the actual output. Predicted output will be list of 12 probability values belong to each class, so we can take a argmax of each output which gives the classification of that input and also we have test labels output in test data. We can plot scatter plot between those two results for entire data. If there are more points at the diagonal that means it is predicting properly otherwise prediction is wrong.
So I have used scatter plot and swarmplot to check the results of the predicted results and actual labels. I found that there are lot of results outside the diagonal which says prediction is not proper.

### Visualize Datasets and Predictions

I couldn't able to visualize properly the dataset properly. I have used different techniques like Tensorflow Projectors. I understood the process to visualize like we need to generate the metadata.tsv file and save it in the checkpoint so that when we run the tensorboard we can visualize the TSNE, UMAP, PCA of the data.
I have tried few methods to produce the projector but not successful. I am working on the same as of now.

 








