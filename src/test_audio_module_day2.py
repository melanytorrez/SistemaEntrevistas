import json
import os
from audio_module import AudioAnalyzer

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, 'data', 'video1.mp4') # Usamos tu video 1
OUTPUT_DIR = os.path.join(BASE_DIR, 'results') # Carpeta results (ya la tienes creada)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'audio_analysis_video1.json')

def main():
    print("--- INICIANDO TEST DEL MÓDULO DE AUDIO (DÍA 2) ---")
    
    # 1. Instanciar la clase (cargará los modelos)
    analyzer = AudioAnalyzer()
    
    # 2. Procesar el video
    print(f"📂 Procesando: {VIDEO_PATH}")
    results = analyzer.process_video(VIDEO_PATH)
    
    # 3. Guardar resultados
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    # 4. Mostrar resumen en consola
    print("\n" + "="*40)
    print("RESULTADOS OBTENIDOS:")
    for item in results:
        print(f"[{item['start']:.1f}s - {item['end']:.1f}s] {item['emotion']['label'].upper()} ({item['emotion']['score']:.2f})")
        print(f"   --> \"{item['text']}\"")
        print("-" * 20)
    print("="*40)
    print(f"✅ JSON guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()