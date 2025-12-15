import os
import sys

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def log_success(msg):
    print(f"{GREEN}[OK] {msg}{RESET}")

def log_error(msg):
    print(f"{RED}[ERROR] {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}[INFO] {msg}{RESET}")

def check_libraries():
    print("--- 1. Verificando Librerías Críticas ---")
    errors = False
    
    try:
        import cv2
        log_success(f"OpenCV versión: {cv2.__version__}")
    except ImportError:
        log_error("OpenCV no instalado (pip install opencv-python)")
        errors = True

    try:
        from deepface import DeepFace
        log_success("DeepFace importado correctamente")
    except ImportError:
        log_error("DeepFace no instalado (pip install deepface tf-keras)")
        errors = True

    try:
        import whisper
        log_success("OpenAI Whisper importado correctamente")
    except ImportError:
        log_error("Whisper no instalado (pip install openai-whisper)")
        errors = True

    try:
        import transformers
        log_success(f"Transformers versión: {transformers.__version__}")
    except ImportError:
        log_error("Transformers no instalado (pip install transformers)")
        errors = True

    try:
        import torch
        gpu_status = "Disponible (CUDA)" if torch.cuda.is_available() else "No detectada (Usando CPU)"
        log_success(f"PyTorch instalado. Aceleración GPU: {gpu_status}")
    except ImportError:
        log_error("PyTorch no instalado (pip install torch)")
        errors = True

    try:
        import moviepy
        log_success("MoviePy importado correctamente")
    except ImportError:
        log_error("MoviePy no instalado (pip install moviepy)")
        errors = True

    try:
        import pandas as pd
        log_success("Pandas importado correctamente")
    except ImportError:
        log_error("Pandas no instalado (pip install pandas)")
        errors = True

    return not errors

def check_data_folder():
    print("\n--- 2. Verificando Datos (Dataset Propio) ---")
    data_path = os.path.join(os.getcwd(), 'data')
    
    if not os.path.exists(data_path):
        log_error(f"La carpeta '{data_path}' no existe.")
        return False
    
    files = os.listdir(data_path)
    videos = [f for f in files if f.endswith(('.mp4', '.mov', '.avi'))]
    excel = [f for f in files if f.endswith(('.xlsx', '.csv'))]
    
    if not videos:
        log_error("No se encontraron videos (.mp4, .mov, .avi) en /data")
    else:
        log_success(f"Videos encontrados: {len(videos)} ({', '.join(videos)})")
        
    if not excel:
        log_warning("No se encontró el Excel de Ground Truth (.xlsx/.csv). ¡Recuerda crearlo antes de validar!")
    else:
        log_success(f"Ground Truth encontrado: {excel[0]}")
        
    return len(videos) > 0

def main():
    print(f"{YELLOW}INICIANDO VERIFICACIÓN DEL ENTORNO - SISTEMA DE ENTREVISTAS{RESET}\n")
    
    libs_ok = check_libraries()
    data_ok = check_data_folder()
    
    print("\n" + "="*40)
    if libs_ok and data_ok:
        print(f"{GREEN} SISTEMA LISTO PARA EL DÍA 1{RESET}")
        print(f"{GREEN}Todo está configurado correctamente. ¡A programar!{RESET}")
    else:
        print(f"{RED} REVISIÓN FALLIDA{RESET}")
        print(f"{RED}Por favor corrige los errores listados arriba antes de continuar.{RESET}")
    print("="*40)

if __name__ == "__main__":
    main()