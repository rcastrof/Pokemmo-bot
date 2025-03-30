# main.py

import time
import mss
import numpy as np
import cv2
from bot.actions import ejecutar_movimientos

print("Cambiando a la ventana del juego... Capturando en 5 segundos.")
time.sleep(5)

# Captura de pantalla
with mss.mss() as sct:
    screenshot = sct.grab(sct.monitors[1])
    img = np.array(screenshot)

# Si se desea ver la imagen antes de comenzar a procesar
cv2.imshow("Screen", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Empezamos el loop de captura de pantalla
while True:
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = np.array(screenshot)

    # Ejecutar movimientos y lógica del bot
    if ejecutar_movimientos(img):
        break  # Detener si encontramos un Pokémon shiny
