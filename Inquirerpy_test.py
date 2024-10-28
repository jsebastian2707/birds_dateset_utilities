from InquirerPy import inquirer

# Opciones del menú
opciones = ["nobg", "resize", "fullfilled", "Salir"]

# Mostrar el menú y obtener la selección
seleccion = inquirer.select(
    message="Crear un dataset:",
    choices=opciones,
    default="resize",
).execute()

if seleccion == "Salir":
    print("Saliendo del menú.")
else:
    print(f"Has seleccionado: {seleccion}")

    # Leer un número entero después de seleccionar una opción
    numero = inquirer.number(
        message="Ingrese el minimo de imagenes:",
        validate=lambda x: x.isdigit() or "Por favor ingrese un número válido",
    ).execute()

    print(f"El número ingresado es: {numero}")
