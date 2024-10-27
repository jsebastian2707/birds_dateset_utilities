import os
import unicodedata
from tqdm import tqdm
import json

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_DATASET_NOBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_NOBG'])
CONST_DATASET_FILLBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_FILLBG'])
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])
CONST_DATASET_BASE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_BASE'])

# Función para normalizar los nombres de archivos y carpetas
def normalize_name(name):
    normalized = unicodedata.normalize('NFD', name)
    normalized = ''.join(
        char for char in normalized if unicodedata.category(char) != 'Mn'
    )  # Elimina marcas de tilde
    normalized = normalized.replace('ñ', 'n').replace('Ñ', 'N')
    return normalized

# Función para renombrar archivos y carpetas en un directorio
def rename_files_and_folders(root_dir):
    # Obtener la lista completa de archivos y carpetas
    all_items = []
    for root, dirs, files in os.walk(root_dir, topdown=False):
        all_items.extend([(root, item, 'dir') for item in dirs])  # Agregar carpetas primero
        all_items.extend([(root, item, 'file') for item in files])  # Luego, agregar archivos

    # Barra de progreso para el renombrado
    for root, name, item_type in tqdm(all_items, desc="Renombrando archivos y carpetas"):
        old_path = os.path.join(root, name)
        new_name = normalize_name(name)
        new_path = os.path.join(root, new_name)
        
        # Renombrar solo si el nombre ha cambiado y no genera conflicto
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
            except FileExistsError:
                print(f"El archivo o carpeta '{new_path}' ya existe. Saltando renombrado.")

# Ejecutar la función de renombrado
rename_files_and_folders(CONST_DATASET_NOBG)