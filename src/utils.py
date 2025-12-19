import json
import os
import logging
import cv2
from datetime import datetime

def setup_logger(name="SistemaEntrevistas"):
    """
    Configura un logger que escribe en consola y en un archivo .log
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"execution_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CONFIGURACIÓN CENTRALIZADA (DÍA 5) ---
VIDEO_NAME = "videoFinal.mp4" # <--- CAMBIAR AQUÍ PARA PROBAR OTROS VIDEOS
SAFE_NAME = VIDEO_NAME.split('.')[0]

CONFIG = {
    "VIDEO_PATH": os.path.join(DATA_DIR, VIDEO_NAME),
    "AUDIO_OUTPUT": os.path.join(OUTPUT_DIR, "temp_audio.wav"),
    
    # Archivos Intermedios
    "VISION_JSON": os.path.join(RESULTS_DIR, f"vision_{SAFE_NAME}.json"),
    "AUDIO_JSON": os.path.join(RESULTS_DIR, f"audio_{SAFE_NAME}.json"),
    "INTEGRATED_JSON": os.path.join(RESULTS_DIR, f"integrated_{SAFE_NAME}.json"),
    
    # Reportes Finales
    "FINAL_REPORT": os.path.join(RESULTS_DIR, f"report_{SAFE_NAME}.md"),
    "FINAL_CHART": os.path.join(RESULTS_DIR, f"chart_{SAFE_NAME}.png"),
    "OVERLAY_VIDEO": os.path.join(RESULTS_DIR, f"overlay_{SAFE_NAME}.mp4")
}

logger = setup_logger()

def get_video_path(filename):
    """Devuelve la ruta absoluta de un video en la carpeta data"""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        logger.error(f"Video no encontrado: {path}")
        raise FileNotFoundError(f"El video {filename} no existe en /data")
    return path

def get_video_properties(video_path):
    """
    Helper para que el equipo de video obtenga FPS y duración fácil.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"No se pudo abrir el video para leer propiedades: {video_path}")
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count / fps if fps > 0 else 0
    
    cap.release()
    
    props = {
        "fps": round(fps, 2),
        "total_frames": frame_count,
        "duration_seconds": round(duration_sec, 2)
    }
    logger.info(f"Propiedades del video obtenidas: {props}")
    return props

def ms_to_timestamp(milliseconds):
    """Convierte milisegundos a formato MM:SS:mmm"""
    seconds = int(milliseconds / 1000)
    m, s = divmod(seconds, 60)
    remain_ms = int(milliseconds % 1000)
    return f"{m:02d}:{s:02d}:{remain_ms:03d}"


def save_analysis_json(data, filename, module_type):
    """
    Guarda los datos en JSON asegurando una estructura estándar.
    
    Args:
        data (list): Lista de diccionarios con los datos.
        filename (str): Nombre del archivo (ej: 'video1_vision.json').
        module_type (str): 'vision' o 'audio' para validar estructura.
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    final_structure = {
        "meta": {
            "module": module_type,
            "timestamp": datetime.now().isoformat(),
            "count": len(data)
        },
        "data": data 
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(final_structure, f, indent=4, ensure_ascii=False)
        logger.info(f"Archivo guardado exitosamente: {filepath}")
    except Exception as e:
        logger.error(f"Error guardando JSON {filename}: {e}")