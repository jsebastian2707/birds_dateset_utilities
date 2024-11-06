import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])
PRODUCTION_DATASET_FOLDER = os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/transformed_dataset")

# Define test data directory and generator

width_shape, height_shape, batch_size = 224, 224, 32
test_datagen = ImageDataGenerator()

# Load the test data
test_generator = test_datagen.flow_from_directory(
    CONST_DATASET_RESIZE,
    target_size=(width_shape, height_shape),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False)

# Load model and make predictions
custom_Model = load_model(os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/keras_models/epoch_50.keras"))
predictions = custom_Model.predict(test_generator)

# Process predictions
y_pred = np.argmax(predictions, axis=1)
y_real = test_generator.classes

# Confusion matrix and classification report
conf_matrix = confusion_matrix(y_real, y_pred)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", classification_report(y_real, y_pred))
