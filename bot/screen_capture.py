import mss
import numpy as np
import cv2
from .game_recognition import detectar_texto

def capture_screen():
    """ Captura la pantalla y devuelve la imagen """
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])  
        img = np.array(screenshot)
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def process_text_area(img):
    """ Recorta el área donde aparece el texto y la procesa """
    zona_texto = img[10:50, 10:200]  # Recorta parte superior izquierda
    return detectar_texto(zona_texto)
