import os
from pynput.keyboard import Controller, Key
import time
import pytesseract
import cv2
import numpy as np


keyboard = Controller()

temp_folder = "temp_images"
os.makedirs(temp_folder, exist_ok=True)


def save_image(img, name):
    route = os.path.join(temp_folder, name)
    cv2.imwrite(route, img)
    print(f"Imagen guardada: {route}")


def on_combat(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    text = pytesseract.image_to_string(thresh, lang="spa")

    print(f"Texto detectado: {text}")

    if "lucha" in text.lower():
        print("✅ Combate detectado.")
        return True
    else:
        print("❌ Combate no detectado.")
        return False


def execute_movement():
    print("✅ moviendo")
    keyboard.press(Key.right)
    time.sleep(1)
    keyboard.release(Key.right)

    time.sleep(1)
    keyboard.press(Key.left)
    time.sleep(1)
    keyboard.release(Key.left)
