# Importaciones necesarias
import time
import psutil
import numpy as np
import json
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]

# Definir el número de muestras de entrenamiento y validación
nb_train_samples = 8320
nb_validation_samples = 2080

PRODUCTION_DATASET_FOLDER = os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/transformed_dataset")

# Crear directorio para guardar modelos si no existe
models_dir = os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/keras_models")
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# Definir el número de épocas
epochs = 50

# Definir el tamaño de las imágenes
width_shape = 224
height_shape = 224

# Definir el número de clases
num_classes = 52  # Ajustar según el número de clases en tu dataset

# Directorios de datos de entrenamiento y validación
train_data_dir = os.path.join(PRODUCTION_DATASET_FOLDER, 'train')
validation_data_dir = os.path.join(PRODUCTION_DATASET_FOLDER, 'valid')

# Función para crear y entrenar el modelo
def create_and_train_vgg16_model(learning_rate, l2_regularization, batch_size):
    # Crear generadores de datos con el batch_size proporcionado
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        vertical_flip=False,
        preprocessing_function=preprocess_input
    )

    valid_datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        vertical_flip=False,
        preprocessing_function=preprocess_input
    )

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(width_shape, height_shape),
        batch_size=batch_size,
        class_mode='categorical'
    )

    validation_generator = valid_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(width_shape, height_shape),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # Definir la entrada de la red neuronal con el tamaño de las imágenes
    image_input = Input(shape=(width_shape, height_shape, 3))

    # Cargar el modelo VGG16 preentrenado con pesos ajustados desde ImageNet
    model = VGG16(input_tensor=image_input, include_top=False, weights='imagenet')

    # Aplanar la salida del VGG16
    x = Flatten()(model.output)

    # Añadir una nueva capa densa al final del modelo para la clasificación multiclase con regularización L2
    out = Dense(num_classes, activation='softmax', kernel_regularizer='l2')(x)

    # Crear un nuevo modelo personalizado que toma la entrada de la imagen y produce la salida clasificada
    custom_vgg_model = Model(inputs=model.input, outputs=out)

    # Congelar todas las capas del modelo base VGG16
    for layer in model.layers:
        layer.trainable = False

    # Compilar el modelo con una función de pérdida, optimizador y métricas especificadas
    custom_vgg_model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=learning_rate), metrics=['accuracy'])

    # Mostrar un resumen del modelo que incluye la arquitectura y el número de parámetros
    custom_vgg_model.summary()

    # Medir el tiempo y el uso de CPU/memoria antes de entrenar
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)
    start_memory = psutil.virtual_memory().used

    # Crear los callbacks para Early Stopping y guardar el mejor modelo
    checkpoint = ModelCheckpoint('best_model.keras', monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, verbose=1, restore_best_weights=True)

    # Entrenar el modelo utilizando generadores de datos para el conjunto de entrenamiento y validación
#  ████████ ██████   █████  ██ ███    ██ ██ ███    ██  ██████  
#     ██    ██   ██ ██   ██ ██ ████   ██ ██ ████   ██ ██       
#     ██    ██████  ███████ ██ ██ ██  ██ ██ ██ ██  ██ ██   ███ 
#     ██    ██   ██ ██   ██ ██ ██  ██ ██ ██ ██  ██ ██ ██    ██ 
#     ██    ██   ██ ██   ██ ██ ██   ████ ██ ██   ████  ██████  
#                                                              
    model_history = custom_vgg_model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        validation_steps=nb_validation_samples // batch_size,
        callbacks=[checkpoint, early_stopping]
    )

    # Medir el tiempo y el uso de CPU/memoria después de entrenar
    end_time = time.time()
    end_cpu = psutil.cpu_percent(interval=None)
    end_memory = psutil.virtual_memory().used

    # Calcular métricas de tiempo y uso de recursos
    elapsed_time = end_time - start_time
    cpu_usage = end_cpu - start_cpu
    memory_usage = end_memory - start_memory

    print(f"Tiempo transcurrido para el entrenamiento: {elapsed_time} segundos")
    print(f"Uso de CPU durante el entrenamiento: {cpu_usage}%")
    print(f"Aumento en uso de memoria: {memory_usage / (1024 ** 3)} GB")

    return model_history, elapsed_time, cpu_usage, memory_usage

# Definir rangos de búsqueda para hiperparámetros
learning_rates = [0.0001, 0.0005, 0.001]
l2_regularizations = [0.01, 0.05, 0.1]
batch_sizes = [16, 32, 64]

# Variables para almacenar los mejores hiperparámetros y su rendimiento
best_val_accuracy = 0
best_hyperparams = {}

# Realizar la búsqueda de cuadrícula
for learning_rate in learning_rates:
    for l2_regularization in l2_regularizations:
        for batch_size in batch_sizes:
            # Crear y entrenar el modelo con los hiperparámetros actuales
            model_history, elapsed_time, cpu_usage, memory_usage = create_and_train_vgg16_model(learning_rate, l2_regularization, batch_size)

            # Obtener la mejor precisión de validación de esta combinación de hiperparámetros
            val_accuracy = np.max(model_history.history['val_accuracy'])

            # Imprimir los resultados
            print(f"Resultados para lr={learning_rate}, l2={l2_regularization}, batch_size={batch_size}:")
            print(f"Tiempo: {elapsed_time} segundos, CPU: {cpu_usage}%, Memoria: {memory_usage / (1024 ** 3)} GB")
            print(f"Precisión de validación: {val_accuracy}")

            # Actualizar los mejores hiperparámetros si la precisión de validación mejora
            if val_accuracy > best_val_accuracy:
                best_val_accuracy = val_accuracy
                best_hyperparams = {
                    'learning_rate': learning_rate,
                    'l2_regularization': l2_regularization,
                    'batch_size': batch_size,
                    'val_accuracy': val_accuracy,
                    'elapsed_time': elapsed_time,
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory_usage
                }

# Imprimir los mejores hiperparámetros y su rendimiento
print("Mejores hiperparámetros encontrados:")
print(best_hyperparams)