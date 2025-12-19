import json
import os
from audio_module import AudioAnalyzer

# Rutas
from audio_module import AudioAnalyzer
from utils import CONFIG

# Rutas
VIDEO_PATH = CONFIG["VIDEO_PATH"]
OUTPUT_FILE = CONFIG["AUDIO_JSON"]
TEMP_AUDIO = CONFIG["AUDIO_OUTPUT"]

def main():
    print("--- INICIANDO TEST DEL MÓDULO DE AUDIO (DÍA 2) ---")
    
    # 1. Instanciar la clase (cargará los modelos)
    analyzer = AudioAnalyzer()
    
    # 2. Procesar el video
    print(f"📂 Procesando: {VIDEO_PATH}")
    # Nota: process_video usa internamente su propia lógica de temp audio, 
    # pero le pasamos el path del video centralizado.
    results = analyzer.process_video(VIDEO_PATH)
    
    # 3. Guardar resultados
    # Directory exist check moved to utils
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    # 4. Mostrar resumen en consola
    print("\n" + "="*40)
    print("RESULTADOS OBTENIDOS:")
    for item in results:
        t_start = item['timestamp_start']
        t_end = item['timestamp_end']
        label = item['dominant_emotion'].upper()
        score = item['confidence']
        print(f"[{t_start:.1f}s - {t_end:.1f}s] {label} ({score:.2f})")
        print(f"   --> \"{item['text']}\"")
        print("-" * 20)
    print("="*40)
    print(f"✅ JSON guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()