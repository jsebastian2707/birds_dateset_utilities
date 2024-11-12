---

# Clasificación de Especies de Aves con Redes Neuronales Convolucionales

Este proyecto utiliza una red neuronal convolucional basada en VGG16 para clasificar diferentes especies de aves. La aplicación entrena un modelo de aprendizaje profundo para identificar las especies en imágenes, permitiendo así una clasificación precisa.

## Descripción del Proyecto

El objetivo de este proyecto es construir un modelo de clasificación de imágenes capaz de identificar una variedad de especies de aves con precisión. Utilizando una arquitectura basada en VGG16, el modelo ha sido entrenado con un conjunto de datos de imágenes etiquetadas de varias especies, incluyendo transformaciones en los datos para mejorar su precisión y robustez.

## Tabla de Contenidos
- [Características](#características)
- [Configuración del Proyecto](#configuración-del-proyecto)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Evaluación del Modelo](#evaluación-del-modelo)
- [Ejemplo de Resultados](#ejemplo-de-resultados)
- [Requisitos](#requisitos)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Características
- Clasificación de imágenes en múltiples especies de aves.
- Uso de una red VGG16 preentrenada con capas adicionales para mejorar la precisión.
- Preprocesamiento de datos, incluyendo redimensionamiento y eliminación de fondos.
- Visualización de las métricas del modelo y generación de informes detallados (matriz de confusión y reporte de clasificación).

## Configuración del Proyecto

1. **Clonar el repositorio**:
    ```bash
    git clone <URL del repositorio>
    cd bird-classification
    ```

2. **Instalar dependencias**:
    Se requiere Python 3.8 o superior y las siguientes librerías.
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar las constantes**:
   Modificar el archivo `config.json` con las rutas correctas para los conjuntos de datos y carpetas de salida. Ejemplo de configuración:

   ```json
   {
       "CONST_BASE_FOLDER": "/ruta/del/proyecto",
       "CONST_DATASET_NOBG": "datasets/nobg",
       "CONST_DATASET_FILLBG": "datasets/fillbg",
       "CONST_DATASET_RESIZE": "datasets/resize",
       "MODEL_SAVE_PATH": "modelos/keras_models"
   }
   ```

## Entrenamiento del Modelo

Ejecutar el script `train_model.py` para entrenar el modelo VGG16:
```bash
python train_model.py
```
Durante el entrenamiento, el modelo guardará checkpoints en la carpeta especificada y se guardará un archivo `.keras` al finalizar cada época.

## Evaluación del Modelo

El modelo entrenado puede ser evaluado en el conjunto de datos de prueba, generando una matriz de confusión y un reporte de clasificación detallado.

1. Cargar el modelo guardado.
2. Ejecutar el script `evaluate_model.py` para generar la evaluación:
   ```bash
   python evaluate_model.py
   ```

## Ejemplo de Resultados

Se incluyen funciones para la visualización de la precisión y pérdida durante el entrenamiento, así como la matriz de confusión y reporte de clasificación tras la evaluación. 

Ejemplo de visualización:
```python
from utilities import plotTraining

# Visualización del entrenamiento
plotTraining(hist, epochs, "accuracy")
plotTraining(hist, epochs, "loss")
```

## Requisitos

### Librerías de Python
- TensorFlow y Keras (para construir y entrenar el modelo)
- Scikit-Learn (para métricas de evaluación)
- Matplotlib (para visualización)
- TQDM (barra de progreso en la terminal)
- Json (para configuraciones)

### Hardware
Es recomendable ejecutar el entrenamiento en una GPU para un rendimiento óptimo, especialmente si se utilizan grandes volúmenes de datos de imagen.

## Uso

1. **Preprocesamiento de Imágenes**: Si tus datos no están preprocesados, utiliza el script `preprocess_images.py` para redimensionar y limpiar las imágenes.
2. **Entrenamiento**: Ejecuta el script de entrenamiento (`train_model.py`) y verifica el rendimiento del modelo guardado en cada época.
3. **Evaluación**: Utiliza `evaluate_model.py` para probar el modelo final y generar las métricas.

## Estructura del Proyecto

```plaintext
├── dataset
│   ├── base                  # Dataset original sin modificaciones
│   ├── resize                # Dataset redimensionado a 224x224
│   ├── fillbg                # Dataset con fondo rellenado
│   ├── nobg                  # Dataset sin fondo
├── models
│   └── keras_models          # Archivos .keras del modelo entrenado
├── scripts
│   ├── train_model.py        # Entrenamiento del modelo
│   ├── evaluate_model.py     # Evaluación y generación de reportes
│   └── preprocess_images.py  # Procesamiento de imágenes
├── config.json               # Archivo de configuración del proyecto
└── README.md
```

---
