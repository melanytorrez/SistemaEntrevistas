import cv2
import os
from deepface import DeepFace
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, 'data', 'video1.mp4')

def test_vision():
    print(f"--- INICIANDO TEST DE VISIÓN ---")
    print(f"Leyendo: {VIDEO_PATH}")

    cap = cv2.VideoCapture(VIDEO_PATH)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 50) 
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(" Error: No se pudo leer el video.")
        return

    temp_img = "temp_frame.jpg"
    cv2.imwrite(temp_img, frame)
    print(" Frame capturado correctamente.")

    print(" Analizando emoción con DeepFace (esto puede tardar la primera vez)...")
    try:
        analysis = DeepFace.analyze(img_path=temp_img, 
                                  actions=['emotion'], 
                                  detector_backend='opencv',
                                  enforce_detection=False)
        
        result = analysis[0]
        dominant = result['dominant_emotion']
        confianza = result['emotion'][dominant]
        
        print("\n" + "="*30)
        print(f" RESULTADO DEEPFACE:")
        print(f"Emoción Dominante: {dominant.upper()}")
        print(f"Confianza: {confianza:.2f}%")
        print("="*30)
        
        os.remove(temp_img)
        print(" Test de Visión EXITOSO")
        
    except Exception as e:
        print(f" Error en DeepFace: {e}")

if __name__ == "__main__":
    test_vision()