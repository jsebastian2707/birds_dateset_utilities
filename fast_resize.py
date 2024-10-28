import os
from PIL import Image
from concurrent import futures
from tqdm import tqdm
import json

# Cargar constantes desde el archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Constantes
CONST_BASE_FOLDER = config["CONST_BASE_FOLDER"]
CONST_OUTPUT_WIDTH = config["CONST_OUTPUT_WIDTH"]
#CONST_FILLBG_COLOR = tuple(config["CONST_FILLBG_COLOR"])
CONST_DATASET_NOBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_NOBG'])
CONST_DATASET_FILLBG = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_FILLBG'])
CONST_DATASET_RESIZE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_RESIZE'])
CONST_DATASET_BASE = os.path.join(CONST_BASE_FOLDER, config['CONST_DATASET_BASE'])
CONST_PROGRESS_FILE = os.path.join(CONST_BASE_FOLDER, config['CONST_PROGRESS_FILE_RESIZE'])

# Cargar progreso guardado
def load_processed_images():
    if os.path.exists(CONST_PROGRESS_FILE):
        with open(CONST_PROGRESS_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

# Guardar el nombre de un archivo procesado
def save_processed_image(filename):
    with open(CONST_PROGRESS_FILE, 'a') as f:
        f.write(f"{filename}\n")

# Función para procesar una imagen individual y guardarla en la carpeta de especie correspondiente
def process_image(file_path, species_folder, output_size=(224, 224)):
    with Image.open(file_path) as img:
        width, height = img.size

        # Recorte cuadrado
        if width > height:
            new_width = height
            left = (width - new_width) // 2
            upper = 0
            right = left + new_width
            lower = height
        else:
            new_height = width
            left = 0
            upper = (height - new_height) // 2
            right = width
            lower = upper + new_height

        # Recorte y redimensionamiento
        cropped_img = img.crop((left, upper, right, lower)).resize(output_size)

        # Guardar la imagen recortada en la subcarpeta de la especie
        output_filename = f"escale_{os.path.basename(file_path)}"
        output_path = os.path.join(species_folder, output_filename)
        cropped_img.save(output_path)

        # Guardar en el archivo de progreso
        save_processed_image(file_path)

def escale_images_in_folder(ruta_dataset, output_size=(224, 224)):
    # Crear carpeta centralizada para las imágenes redimensionadas
    os.makedirs(CONST_DATASET_RESIZE, exist_ok=True)

    # Cargar imágenes ya procesadas
    processed_images = load_processed_images()

    # Procesar imágenes de cada especie en su subcarpeta
    tasks = []
    for especie in os.listdir(ruta_dataset):
        ruta_especie = os.path.join(ruta_dataset, especie)
        if os.path.isdir(ruta_especie):
            # Crear carpeta para cada especie en la carpeta de resize
            species_folder = os.path.join(CONST_DATASET_RESIZE, especie)
            os.makedirs(species_folder, exist_ok=True)

            # Crear lista de archivos de imagen en la carpeta de la especie
            files = [
                os.path.join(ruta_especie, filename)
                for filename in os.listdir(ruta_especie)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
                and os.path.join(ruta_especie, filename) not in processed_images  # Excluir imágenes ya procesadas
            ]
            tasks.extend((file_path, species_folder) for file_path in files)

    # Procesar las imágenes en paralelo con barra de progreso
    with futures.ProcessPoolExecutor() as executor:
        # Usar tqdm para mostrar la barra de progreso
        futures_list = {
            executor.submit(process_image, file_path, species_folder, output_size): file_path
            for file_path, species_folder in tasks
        }
        for future in tqdm(futures.as_completed(futures_list), total=len(futures_list)):
            try:
                future.result()  # Manejar excepción si hay errores en el procesamiento
            except Exception as e:
                print(f"Error procesando {futures_list[future]}: {e}")

# Llamada a la función dentro de la verificación
if __name__ == '__main__':
    escale_images_in_folder(CONST_DATASET_BASE)
