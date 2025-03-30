import pytesseract
import cv2

def detectar_texto(img):
    """ Extrae texto de la imagen """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    _, binaria = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)  
    texto = pytesseract.image_to_string(binaria, lang="eng")
    return texto

def is_in_game(texto):
    """ Verifica si el texto contiene 'PUEBLO PALETA' o algo similar """
    if "PUEBLO" in texto.upper() or "PALETA" in texto.upper():
        return True
    return False
