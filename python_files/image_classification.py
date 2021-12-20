# -*- coding: utf-8 -*-
"""image_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OfAf-Zy8EYN5wovMXMiPU96naJQz8on8

All the necessary imports for the module
"""

from google.colab import drive
import cv2, os
import pathlib
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

"""Mounting the Drive folder to read dataset from drive"""

drive.mount('/content/drive', force_remount=False)

"""Point the data directory frmo where data has to read."""

train_data_dir = "/content/drive/MyDrive/ML Hiring Test Materials/Data/Image Classification Data/data/train/"
test_data_dir = "/content/drive/MyDrive/ML Hiring Test Materials/Data/Image Classification Data/data/test/"

"""Point the data directory path to where data has to be saved"""

train_data_new_path = "/content/drive/MyDrive/CNS_Image_Classification/data/train/"
test_data_new_path = "/content/drive/MyDrive/CNS_Image_Classification/data/test/"

"""Now move the data from train_data_dir to new_path. We are doing this because the actual data images are given in "tif" format which is hard to read in tensorflow. So we are converting the "tif" images to "jpg" images using open cv library. """

import cv2, os
for infile in os.listdir(train_data_dir):
  os.makedirs(train_data_new_path+infile, exist_ok = True)
  for file in os.listdir(train_data_dir + infile):
    read = cv2.imread(train_data_dir +infile+"/"+ file)
    outfile = file.split('.')[0] + '.jpg'
    cv2.imwrite(train_data_new_path+infile+"/"+outfile,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])

import cv2, os
for infile in os.listdir(test_data_dir):
  os.makedirs(test_data_new_path+infile, exist_ok = True)
  for file in os.listdir(test_data_dir + infile):
    read = cv2.imread(test_data_dir +infile+"/"+ file)
    outfile = file.split('.')[0] + '.jpg'
    cv2.imwrite(test_data_new_path+infile+"/"+outfile,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])

"""Now read the train data from the directory usig the Keras image dataset from directory module. Also we are doing validation on the data.

Also we need to define the batch size, image height and image width.
"""

batch_size = 32
img_height = 180
img_width = 180

train_data = tf.keras.utils.image_dataset_from_directory(
  train_data_new_path,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

valid_data = tf.keras.utils.image_dataset_from_directory(
  train_data_new_path,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

test_data = tf.keras.utils.image_dataset_from_directory(
  test_data_new_path,
  image_size=(img_height, img_width),
  batch_size=batch_size)

"""Lets check the labels of the data"""

class_names = train_data.class_names
class_names

"""As we can see there are 12 labels. so we can define a no_of_classes as 12 """

num_classes = 12

train_data

"""Lets check the shape of each batch data input and label"""

for input_batch_data, labels_batch_data in train_data:
  print(input_batch_data.shape)
  print(labels_batch_data.shape)
  break

"""We can do prefetch so that input can be stored in buffer memory to read instead of reading from main memory everytime. Also it helps in fast execution since prefetch can happen during the model execution which saves some time"""

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.cache().prefetch(buffer_size=AUTOTUNE)
valid_data = valid_data.cache().prefetch(buffer_size=AUTOTUNE)

"""Now we have come to modelling part. We can use two differnet type of models. One is Keras sequential model and other is functional model. In sequential model we the output will be forwarded to next layer in sequential form. Lets build the CNN image classification model with 3 CNN layers and Max pooling and some Dense layers.

Important Note : We are using the Normalization layer as the first layer since input images shoule be in the range of 0-1 but the image pixel values will have from 0-255. So by applying Normalization layer we can scale the values to 0-1
"""

model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

"""Once model is build we need to compile the model with proper optimizer function, loss function and the metrics.

We use adam optimizer which is the common optimizer function and sparse categorical cross entrophy which is the softmax loss function which can be used for categorical data and we are calculating the accuracy metrics
"""

model.compile(optimizer='adam', loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

"""Now Fit the model using the train data and the valid data.

Specify the no of epochs to be run.

Important Note: We are also using the tensorbaord callbacks to check the metrics, graphs in the tensorboard
"""

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='logs/')

model_output = model.fit(train_data, validation_data=valid_data, epochs=30, callbacks= [tensorboard_callback])

"""Lets see the history of the model_output"""

model_output.history

"""Lets plot the Train and Valid metrics using the matplotlib"""

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.plot(model_output.history['accuracy'])
ax1.plot(model_output.history['val_accuracy'])
ax1.set_title('model accuracy')
ax1.set_ylabel('accuracy')
ax1.set_xlabel('epoch')
ax1.legend(['train', 'val'], loc='upper left')
# 
ax2.plot(model_output.history['loss'])
ax2.plot(model_output.history['val_loss'])
ax2.set_title('model loss')
ax2.set_ylabel('loss')
ax2.set_xlabel('epoch')
ax2.legend(['train', 'val'], loc='upper left')
plt.tight_layout()
plt.show()

"""Lets see the same metrics plots in tesorboard by loading the tensorboard."""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs/

"""### Model Evaluation using the test data"""

test_output = model.evaluate(test_data, batch_size=64)

"""Lets check the training output, validation output and test output"""

print("Training accuracy", model_output.history['accuracy'][-1])
print("Training Loss", model_output.history['loss'][-1])
print("Validation accuracy", model_output.history['val_accuracy'][-1])
print("Validation Loss", model_output.history['val_loss'][-1])
print("Testing accuracy", test_output[1])
print("Testing Loss", test_output[0])

"""### Model Prediction"""

prediction_output = model.predict(test_data, batch_size=64)

prediction_output

"""### Visualize the Prediction results.

We can visualize the prediction results using scatter plot between the predicted output and the actual output. Predicted output will be list of 12 probability values belong to each class, so we can take a argmax of each output which gives the classification of that input and also we have test labels output in test data. We can plot scatter plot between those two results for entire data. If there are more points at the diagonal that means it is predicting properly otherwise prediction is wrong.
"""

prediction_results = []
actual_labels = []
for input_batch_data, labels_batch_data in test_data:
  prediction_output = model.predict(input_batch_data, batch_size=64)
  for pred, label in zip(prediction_output,labels_batch_data ):
    prediction_results.append(pred.argmax())
    actual_labels.append(label.numpy())
print(len(prediction_results))
print(len(actual_labels))

plt.scatter(actual_labels, prediction_results, alpha=0.6, 
          color='#FF0000', lw=1, ec='black')
      
classes = [0, 12]

plt.plot(classes, classes, lw=1, color='#0000FF')
plt.ticklabel_format(useOffset=False, style='plain')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(classes)
plt.ylim(classes)

plt.tight_layout()
plt.show()

"""From above plot we can see that there are lot values outside the diagonal which says all the images are not predicted properly. But since it is scatter plot there can be data overlap. Lets try with some other plot to check the results again."""

import seaborn as sns
sns.swarmplot(x=actual_labels, y=prediction_results)

"""From above swarmplot we can clearly see that there are lot of values outside the diagonal.

Now let train the model using the Tensorflow Pre defined models like VGG, Inception, Resnet etc. We can do this by two ways. 
1) By using the TF Hub Models
2) By using the Keras applications models

Lets use the keras applications for above model and check the results.

### VGG Network
"""

from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
model = VGG16(include_top=False, input_shape=(180, 180, 3))
flat1 = Flatten()(model.layers[-1].output)
class1 = Dense(128, activation='relu')(flat1)
output = Dense(num_classes)(class1)
model = Model(inputs=model.inputs, outputs=output)

"""Compile the model and fit the model using train data and the valid data"""

model.compile(optimizer='adam',loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

model_output = model.fit(train_data,validation_data=valid_data, epochs=10)

"""As we can see the results are not that good using the vgg network. Lets try the same model using the inception network.

### Inception Network
"""

from tensorflow.keras.applications import InceptionV3
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
model = InceptionV3(include_top=False, input_shape=(180, 180, 3))
flat1 = Flatten()(model.layers[-1].output)
class1 = Dense(128, activation='relu')(flat1)
output = Dense(num_classes)(class1)
model = Model(inputs=model.inputs, outputs=output)

model.compile( optimizer='adam', loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='inception_logs/')

model_output = model.fit(train_data, validation_data=valid_data, epochs=30, callbacks=[tensorboard_callback])

"""Plot the metrics of the inception model """

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.plot(model_output.history['accuracy'])
ax1.plot(model_output.history['val_accuracy'])
ax1.set_title('model accuracy')
ax1.set_ylabel('accuracy')
ax1.set_xlabel('epoch')
ax1.legend(['train', 'val'], loc='upper left')
# 
ax2.plot(model_output.history['loss'])
ax2.plot(model_output.history['val_loss'])
ax2.set_title('model loss')
ax2.set_ylabel('loss')
ax2.set_xlabel('epoch')
ax2.legend(['train', 'val'], loc='upper left')
plt.tight_layout()
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir inception_logs/

"""### Model Evaluation"""

test_output = model.evaluate(test_data, batch_size=64)

print("Training accuracy", model_output.history['accuracy'][-1])
print("Training Loss", model_output.history['loss'][-1])
print("Validation accuracy", model_output.history['val_accuracy'][-1])
print("Validation Loss", model_output.history['val_loss'][-1])
print("Testing accuracy", test_output[1])
print("Testing Loss", test_output[0])

"""Model Prediction"""

predict_output = model.predict(test_data, batch_size=64)

predict_output

"""### Comparing the results

As we can see that training results are good compared to validation and the testing. There are lot of reasons for that. One such reason is images look similar for different categories or data is over fitting. We can solve this by trying out different hyper parameters and shuffle the data in between the batches etc.

### Dimensonality Reduction

We can visualize the Data in 2D or 3D using the Tensorflow Projector. We need to build the ".tsv" file and save to folder and launch the tensorflow using the same folder directory. Once tensorboard opens you can change the visualization to PCA, UMAP or even you can change the dimensions to 2D or 3D. We can also upload our own metadata.tsv file such that it visualize the data.

Few methods to visualize the training data in 2D using Tensorboard
"""

# import csv
# import numpy as np
# import tensorflow as tf
# from PIL import Image

# def get_img(img_path):
#     print(img_path)
#     img = tf.io.read_file(img_path)
#     # convert the compressed string to a 3D uint8 tensor
#     img = tf.image.decode_jpeg(img, channels=3)
#     # resize the image to the desired size for your model
#     img = tf.image.resize_with_pad(img, 100, 100)
#     return img
# # Generate embeddings
# images_pil = []
# images_embeddings = []
# labels = []
# for x in train_data.take(1500): 
#     img_path = x[0]
#     # img_tf = get_img(img_path)
#     # Save both tf image for prediction and PIL image for sprite
#     img_pil = Image.open(img_path.numpy()).resize((100, 100))
#     img_embedding = embeddings(tf.expand_dims(img_tf, axis=0))
#     images_embeddings.append(img_embedding.numpy()[0])
#     images_pil.append(img_pil)
#     # Assuming your output data is directly the label
#     label = x[1] 
#     labels.append(label)

from tensorboard.plugins import projector
images_embeddings = []
images_pil = []
for images, labels in train_data.take(100):
    img_embedding = tf.expand_dims(images, axis=0)
    images_embeddings.append(img_embedding.numpy()[0])
    images_pil.append(images)

log_dir = "logs/"
os.makedirs("logs/embeddings", exist_ok = True)
with open("logs/embeddings/metadata.tsv", "w") as fw:
    csv_writer = csv.writer(fw, delimiter="\t")
    csv_writer.writerows(images_embeddings)
 
checkpoint = tf.train.Checkpoint()
checkpoint.save(os.path.join(log_dir, "embedding.ckpt"))

config = projector.ProjectorConfig()
embedding = config.embeddings.add()

embedding.tensor_name = "embedding/.ATTRIBUTES/VARIABLE_VALUE"
embedding.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(log_dir, config)

# one_square_size = int(np.ceil(np.sqrt(len(images_embeddings))))
# master_width = 100 * one_square_size
# master_height = 100 * one_square_size
# spriteimage = Image.new(
#     mode="RGBA",
#     size=(master_width, master_height),
#     color=(0,0,0,0) # fully transparent
#   )
# for count, image in enumerate(images_pil):
#     div, mod = divmod(count, one_square_size)
#     h_loc = 100 * div
#     w_loc = 100 * mod
#     spriteimage.paste(image, (w_loc, h_loc))
# spriteimage.convert("RGB").save("logs/embeddings/sprite.jpg", transparency=0)

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs/

