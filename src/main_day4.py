import sys
import os
import json
import argparse
from analysis_engine import AnalysisEngine
from report_generator import ReportGenerator
from utils import setup_logger

logger = setup_logger("MainDay4")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

def load_json(path):
    if not os.path.exists(path):
        logger.error(f"Archivo no encontrado: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Sistema de Analisis de Entrevistas - Dia 4")
    parser.add_argument('--video', type=str, default='video1', help='Identificador del video (ej: video1, video2)')
    args = parser.parse_args()
    
    video_id = args.video
    logger.info(f"🚀 Iniciando Análisis Avanzado para: {video_id}")
    
    # Rutas de archivos esperados (Optimización: Usar pre-calculados)
    # Nota: Si no existen, en un sistema real se llamaría al pipeline de inferencia.
    # Aquí asumimos que existen para demostrar la optimización de velocidad.
    
    audio_path = os.path.join(RESULTS_DIR, f'audio_analysis_{video_id}.json')
    vision_path = os.path.join(RESULTS_DIR, f'vision_analysis_{video_id}.json') # Estandarizar nombre
    if not os.path.exists(vision_path):
        # Fallback a nombre antiguo si es video1
        if video_id == 'video1':
             vision_path = os.path.join(RESULTS_DIR, 'vision_analysis.json')

    logger.info(f"Cargando datos de: {audio_path}")
    logger.info(f"Cargando datos de: {vision_path}")
    
    audio_data = load_json(audio_path)
    vision_data = load_json(vision_path)
    
    if not audio_data or not vision_data:
        logger.error("❌ Faltan datos de entrada. Ejecuta Dia 1, 2 y 3 primero o verifica los archivos.")
        sys.exit(1)
        
    # Normalizar estructuras si es necesario (el json de audio a veces es lista directa, a veces dict)
    if isinstance(audio_data, dict) and 'segments' in audio_data:
        audio_data = audio_data['segments']
    elif isinstance(audio_data, dict) and 'data' in audio_data: 
         audio_data = audio_data['data']
         
    if isinstance(vision_data, dict) and 'data' in vision_data:
        vision_data = vision_data['data']

    # --- ANÁLISIS ---
    engine = AnalysisEngine()
    
    # 1. Análisis de Congruencia
    results = engine.analyze_congruence(audio_data, vision_data)
    
    # 2. Detección de Cambios Emocionales
    shifts = engine.detect_emotional_shifts(vision_data)
    results['emotional_shifts'] = shifts
    
    logger.info(f"✅ Análisis completado. Score: {results['global_metrics']['congruence_score']}%")
    
    # --- REPORTE ---
    reporter = ReportGenerator(RESULTS_DIR)
    report_path = reporter.generate_markdown_report(results, video_name=f"Day4_{video_id}")
    
    logger.info(f"📄 Reporte generado en: {report_path}")
    print(f"DONE_REPORT: {report_path}")

if __name__ == "__main__":
    main()
