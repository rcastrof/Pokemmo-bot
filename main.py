# main.py

import time
import mss
import numpy as np
import cv2
from bot.actions import execute_movement, on_combat

print("Cambiando a la ventana del juego... Capturando en 5 segundos.")
time.sleep(5)

with mss.mss() as sct:
    screenshot = sct.grab(sct.monitors[1])
    img = np.array(screenshot)

cv2.imshow("Screen", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

attempts = 0
detected_combat = False

while not detected_combat:
    attempts += 1
    print(f"Intento número: {attempts}")

    execute_movement()

    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = np.array(screenshot)
    detected_combat = on_combat(img)
    time.sleep(1)
