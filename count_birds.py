import os
import json
import csv

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file) 

# Acceder a las constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_DATASET_NOBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_NOBG'])
CONST_DATASET_FILLBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_FILLBG'])
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])
CONST_DATASET_BASE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_BASE'])

CONST_MIN_IMAGES_TO_ENABLE = 200

min_archivos_principal = float('inf')
carpeta_min_archivos_principal = ""
enabled_count = 0  # Contador de clases con "Enabled" en True

def contar_archivos_por_especie(ruta_dataset):
    global min_archivos_principal, carpeta_min_archivos_principal, enabled_count
    resultados = []

    for idx, especie in enumerate(os.listdir(ruta_dataset), start=1):
        ruta_especie = os.path.join(ruta_dataset, especie)
        
        # Número de archivos en la carpeta principal de la especie
        num_archivos_principal = len(os.listdir(ruta_especie)) if os.path.isdir(ruta_especie) else 0
            
        # Número de archivos en el dataset de resize
        ruta_dataset_resize = os.path.join(CONST_DATASET_RESIZE, especie)
        num_archivos_dataset_resize = len(os.listdir(ruta_dataset_resize)) if os.path.isdir(ruta_dataset_resize) else 0

        # Número de archivos en el dataset de nobg
        ruta_dataset_nobg = os.path.join(CONST_DATASET_NOBG, especie)
        num_archivos_dataset_nobg = len(os.listdir(ruta_dataset_nobg)) if os.path.isdir(ruta_dataset_nobg) else 0
        
        # Actualizar la especie con menos archivos en la carpeta principal
        if num_archivos_principal < min_archivos_principal:
            min_archivos_principal = num_archivos_principal
            carpeta_min_archivos_principal = especie
        
        # Determinar si habilitar (Enabled)
        enabled = num_archivos_principal >= CONST_MIN_IMAGES_TO_ENABLE
        if enabled:
            enabled_count += 1

        # Agregar los resultados al CSV
        resultados.append([idx, especie, enabled, num_archivos_principal, num_archivos_dataset_resize, num_archivos_dataset_nobg])

    # Guardar en archivo CSV
    with open('resultados.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Especie", "Enabled", "Main", "dataset_resize", "dataset_nobg"])  # Encabezados
        writer.writerows(resultados)
        
        # Agregar fila con la especie con menos imágenes en la carpeta principal
        writer.writerow(["##", carpeta_min_archivos_principal, min_archivos_principal, "", ""])
        
        # Agregar fila con el número de clases con "Enabled" en True
        writer.writerow(["##", "Clases con Enabled en True", enabled_count, "", ""])

contar_archivos_por_especie(CONST_DATASET_BASE)
