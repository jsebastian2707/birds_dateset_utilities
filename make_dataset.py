import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import json

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_DATASET_NOBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_NOBG'])
CONST_DATASET_FILLBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_FILLBG'])
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])
PRODUCTION_DATASET_FOLDER = os.path.join(CONST_BASE_FOLDER, "production_dataset_52_resize/transformed_dataset")

# Crear la carpeta principal de producción y subcarpetas si no existen
os.makedirs(PRODUCTION_DATASET_FOLDER, exist_ok=True)

# Leer archivo CSV
csv_file = 'resultados.csv'
if not os.path.exists(csv_file):
    print(f"Archivo CSV no encontrado en {csv_file}")
    exit()

data = pd.read_csv(csv_file)

# Filtrar solo las especies habilitadas
selected_species = data[data['Enabled'] == "True"]['Especie'].unique()
print(f"Especies habilitadas: {len(selected_species)}")

if len(selected_species) == 0:
    print("No se encontraron especies habilitadas en el CSV.")
    exit()

# Limites de imágenes para entrenamiento y validación
train_limit = 160
valid_limit = 40
total_images_limit = train_limit + valid_limit

# Calcular el total de imágenes a procesar para la barra de progreso general
total_images = len(selected_species) * total_images_limit

# Crear barra de progreso general
with tqdm(total=total_images, desc="Procesando todas las especies") as pbar:
    for species in selected_species:
        
        # Crear rutas de carpetas de destino para entrenamiento y validación
        train_dir = os.path.join(PRODUCTION_DATASET_FOLDER, "train", species)
        valid_dir = os.path.join(PRODUCTION_DATASET_FOLDER, "valid", species)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(valid_dir, exist_ok=True)

        # Listar todas las imágenes de la especie en la carpeta fuente
        species_folder = os.path.join(CONST_DATASET_RESIZE, species)
        
        # Verificar que la carpeta de la especie existe
        if not os.path.exists(species_folder):
            print(f"No se encontró la carpeta para la especie {species} en {species_folder}")
            continue

        all_images = [img for img in os.listdir(species_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
        if len(all_images) == 0:
            print(f"No se encontraron imágenes para la especie {species}.")
            continue
        
        # Limitar a 200 imágenes por especie
        selected_images = all_images[:total_images_limit]
        train_images, valid_images = train_test_split(selected_images, train_size=train_limit)

        # Copiar imágenes de entrenamiento y validación con barra de progreso general
        for img in train_images:
            shutil.copy(os.path.join(species_folder, img), os.path.join(train_dir, img))
            pbar.update(1)  # Actualizar barra de progreso general
        
        for img in valid_images:
            shutil.copy(os.path.join(species_folder, img), os.path.join(valid_dir, img))
            pbar.update(1)  # Actualizar barra de progreso general

print("Imágenes copiadas en la estructura de 'transformed_dataset'")
