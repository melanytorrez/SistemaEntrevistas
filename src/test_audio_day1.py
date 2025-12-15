import os
import whisper
from moviepy import VideoFileClip

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, 'data', 'video1.mp4')
AUDIO_OUTPUT = "temp_audio.wav"

def test_audio():
    print(f"--- INICIANDO TEST DE AUDIO ---")
    
    print(" Extrayendo audio del video...")
    try:
        video = VideoFileClip(VIDEO_PATH)
        
      
        clip_cortado = video.subclipped(0, 10)
        
        clip_cortado.audio.write_audiofile(AUDIO_OUTPUT, logger=None)
        
        video.close()
        print(" Audio extraído correctamente.")
        
    except Exception as e:
        print(f" Error extrayendo audio: {e}")
        try:
            print(" Intentando extraer audio completo sin cortar...")
            video = VideoFileClip(VIDEO_PATH)
            video.audio.write_audiofile(AUDIO_OUTPUT, logger=None)
            video.close()
            print(" Audio completo extraído (modo respaldo).")
        except:
            return

    print(" Cargando modelo Whisper (base)...")
    try:
        model = whisper.load_model("base")
        
        print(" Transcribiendo...")
        result = model.transcribe(AUDIO_OUTPUT, fp16=False)
        
        text = result["text"]
        
        print("\n" + "="*30)
        print(f" RESULTADO WHISPER:")
        print(f"Texto detectado: '{text.strip()}'")
        print("="*30)
        
        
        if os.path.exists(AUDIO_OUTPUT):
            os.remove(AUDIO_OUTPUT)
        print(" Test de Audio EXITOSO")
        
    except Exception as e:
        print(f" Error en Whisper: {e}")

if __name__ == "__main__":
    test_audio()