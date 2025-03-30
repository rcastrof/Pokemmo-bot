import os
from pynput.keyboard import Controller, Key
import time
import pytesseract
import cv2
import numpy as np
from datetime import datetime

# Configurar el controlador de teclado
keyboard = Controller()

# Crear una carpeta temporal para almacenar las imágenes
temp_folder = "temp_images"
os.makedirs(temp_folder, exist_ok=True)

def guardar_imagen(img, nombre):
    """Guardar la imagen en la carpeta temporal con el nombre dado"""
    ruta = os.path.join(temp_folder, nombre)
    cv2.imwrite(ruta, img)
    print(f"Imagen guardada: {ruta}")

def detectar_texto(img):
    """ Extrae texto de la imagen """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)
    texto = pytesseract.image_to_string(binaria, lang="eng")
    return texto

def es_plea(img):
    """Detecta si la imagen muestra una pelea."""
    texto = detectar_texto(img)
    if "lucha" in texto.lower() or "fight" in texto.lower():
        return True
    return False

def mover_dentro_del_pasto():
    """Mover al personaje dentro del pasto de forma continua."""
    keyboard.press(Key.right)
    time.sleep(1)
    keyboard.release(Key.right)
    
    keyboard.press(Key.left)
    time.sleep(1)
    keyboard.release(Key.left)

def detectar_pasto(img):
    """Detectar si estamos dentro del pasto."""
    zona_pasto = img[200:400, 300:500]  # Ajusta a la zona donde está el pasto en tu pantalla
    promedio_color = np.mean(zona_pasto, axis=(0, 1))  # Promedio de colores en el área
    if promedio_color[1] > promedio_color[0] and promedio_color[1] > promedio_color[2]:
        return True
    return False

def obtener_nombre_pokemon(img):
    """Extrae el nombre del Pokémon en la parte superior de la pantalla."""
    zona_nombre = img[50:100, 200:500]  # Ajusta las coordenadas
    nombre_pokemon = detectar_texto(zona_nombre)
    guardar_imagen(zona_nombre, f"nombre_pokemon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    return nombre_pokemon.strip()

def comparar_imagenes(img1, img2):
    """Compara dos imágenes y retorna True si hay una diferencia significativa."""
    # Convertir imágenes a escala de grises
    gris1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gris2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Calcular la diferencia absoluta entre las dos imágenes
    diferencia = cv2.absdiff(gris1, gris2)
    _, binaria = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)
    numero_pixels_diferentes = np.sum(binaria)  # Cuenta los píxeles diferentes
    
    # Si la diferencia supera un umbral, hay un cambio significativo
    if numero_pixels_diferentes > 50000:  # Ajusta este valor según sea necesario
        return True
    return False

def ejecutar_movimientos(img):
    """Ejecutar los movimientos y la lógica del bot."""
    # Detectar si estamos dentro del pasto
    if detectar_pasto(img):
        print("✅ Estás dentro del pasto")
        mover_dentro_del_pasto()

    # Tomar una captura antes de mover
    print('tomando foto inicial')
    img_anterior = img.copy()
    guardar_imagen(img_anterior, f"anterior_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    # Moverse de forma continua a la derecha e izquierda
    keyboard.press(Key.right)
    time.sleep(1)
    keyboard.release(Key.right)
    
    time.sleep(1)  # Espera entre movimientos
    keyboard.press(Key.left)
    time.sleep(1)
    keyboard.release(Key.left)

    # Tomar una nueva captura después de mover
    print('tomando foto después de mover')
    img_nueva = img.copy()
    guardar_imagen(img_nueva, f"actual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    # Comparar las imágenes para detectar cualquier cambio (como una pelea)
    if comparar_imagenes(img_anterior, img_nueva):
        print("✅ La imagen ha cambiado, verificando si hay pelea...")

        if es_plea(img_nueva):
            print("✅ ¡Ha comenzado la pelea!")

            # Obtener el nombre del Pokémon
            nombre_pokemon = obtener_nombre_pokemon(img_nueva)
            print("Nombre del Pokémon:", nombre_pokemon)

            # Comprobar si es un Pokémon shiny
            if "shiny" in nombre_pokemon.lower():
                print("✨ Shiny detectado. Deteniendo movimientos para acción manual.")
                return True  # Detenemos el bot si es shiny
            else:
                print("❌ No es shiny. Continuando con el bot.")

    return False  # Continuamos moviéndonos si no es shiny
