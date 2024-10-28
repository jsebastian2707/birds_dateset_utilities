import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm  # Importar tqdm para la barra de progreso
import json

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_DATASET_NOBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_NOBG'])
CONST_DATASET_FILLBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_FILLBG'])
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])

# Rutas de carpetas
CONST_DATASET_SELECTED_FOLDER = CONST_DATASET_RESIZE
PRODUCTION_DATASET_FOLDER = os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/transformed_dataset")

# Crear la carpeta principal de producción y subcarpetas si no existen
os.makedirs(PRODUCTION_DATASET_FOLDER, exist_ok=True)

# Leer archivo CSV
data = pd.read_csv("resultados.csv")

# Filtrar solo las especies habilitadas
selected_species = data[data['Enabled'] == 1]['Especie'].unique()

# Proporción de entrenamiento y validación
train_ratio = 0.8  # 80% para entrenamiento, 20% para validación

for species in selected_species:
    # Crear rutas de carpetas de destino para entrenamiento y validación
    train_dir = os.path.join(PRODUCTION_DATASET_FOLDER, "train", species)
    valid_dir = os.path.join(PRODUCTION_DATASET_FOLDER, "valid", species)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)

    # Listar todas las imágenes de la especie en la carpeta fuente
    species_folder = os.path.join(CONST_DATASET_SELECTED_FOLDER, species)
    all_images = [img for img in os.listdir(species_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Dividir imágenes en entrenamiento y validación
    train_images, valid_images = train_test_split(all_images, train_size=train_ratio)

    # Copiar imágenes de entrenamiento con barra de progreso
    print(f"Copiando imágenes de entrenamiento para la especie {species}...")
    for img in tqdm(train_images, desc=f"Entrenamiento - {species}", leave=False):
        shutil.copy(os.path.join(species_folder, img), os.path.join(train_dir, img))
    
    # Copiar imágenes de validación con barra de progreso
    print(f"Copiando imágenes de validación para la especie {species}...")
    for img in tqdm(valid_images, desc=f"Validación - {species}", leave=False):
        shutil.copy(os.path.join(species_folder, img), os.path.join(valid_dir, img))

print("Imágenes copiadas en la estructura de 'transformed_dataset'")
