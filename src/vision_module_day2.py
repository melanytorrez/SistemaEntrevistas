import cv2
import os
import json
import time
from deepface import DeepFace

# Configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, 'data', 'video1.mp4')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'vision_analysis.json')
SAMPLE_RATE = 1  # Analizar un frame cada 1 segundo

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_video():
    print(f"--- INICIANDO MÓDULO DE VISIÓN (Día 2) ---")
    print(f"📁 Video: {VIDEO_PATH}")
    
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: No se encuentra el archivo {VIDEO_PATH}")
        return

    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"ℹ️ Info: {fps:.2f} FPS | Duración: {duration:.2f}s | Total Frames: {total_frames}")
    
    # Calcular cada cuántos frames capturamos
    frame_interval = int(fps * SAMPLE_RATE)
    
    results = []
    frame_count = 0
    analyzed_count = 0
    
    start_time = time.time()
    
    print("🚀 Procesando video... (esto tomará tiempo)")
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Solo analizamos si toca según el intervalo
            if frame_count % frame_interval == 0:
                current_time = frame_count / fps
                print(f"   Frame {frame_count}/{total_frames} ({current_time:.1f}s)... ", end="", flush=True)
                
                # Guardar frame temporalmente para DeepFace
                temp_img = "temp_vision_frame.jpg"
                cv2.imwrite(temp_img, frame)
                
                try:
                    # DeepFace analyze
                    analysis = DeepFace.analyze(img_path=temp_img, 
                                              actions=['emotion'], 
                                              detector_backend='opencv',
                                              enforce_detection=False,
                                              silent=True)
                    
                    # Extraer datos (DeepFace devuelve una lista o dict según versión/caras)
                    if isinstance(analysis, list):
                        item = analysis[0]
                    else:
                        item = analysis
                        
                    dom_emotion = item['dominant_emotion']
                    confidence = float(item['emotion'][dom_emotion]) # Force float
                    
                    # Convertir todo el diccionario de emociones a float nativo
                    all_emotions = {k: float(v) for k, v in item['emotion'].items()}

                    results.append({
                        "timestamp": round(current_time, 2),
                        "frame": frame_count,
                        "dominant_emotion": dom_emotion,
                        "confidence": round(confidence, 2),
                        "all_emotions": all_emotions
                    })
                    print(f"✅ {dom_emotion} ({confidence:.1f}%)")
                    analyzed_count += 1
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Limpiar
                if os.path.exists(temp_img):
                    os.remove(temp_img)
            
            frame_count += 1

    except KeyboardInterrupt:
        print("\n🛑 Interrumpido por usuario. Guardando progreso...")
        
    finally:
        cap.release()
        if os.path.exists("temp_vision_frame.jpg"):
            os.remove("temp_vision_frame.jpg")

    # Guardar resultados
    print(f"💾 Guardando {len(results)} registros en {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=4)
        
    elapsed = time.time() - start_time
    print(f"\n✨ Proceso completado en {elapsed:.1f} segundos.")

if __name__ == "__main__":
    process_video()
