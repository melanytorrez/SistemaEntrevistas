import os
import whisper
import torch
from moviepy import VideoFileClip
from transformers import pipeline
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioAnalyzer:
    def __init__(self):
        """
        Inicializa los modelos una sola vez para ahorrar memoria.
        """
        logging.info("⏳ Cargando modelo Whisper (ASR)...")
        # Usamos 'base' para CPU.
        self.asr_model = whisper.load_model("base")
        
        logging.info("⏳ Cargando modelo de Emociones (NLP Multilingüe)...")
        # Usamos 'pysentimiento/robertuito-emotion-analysis' que es específico para español/tweets
        self.nlp_classifier = pipeline(
            "text-classification", 
            model="pysentimiento/robertuito-emotion-analysis", 
            return_all_scores=True
        )

    def extract_audio(self, video_path, output_audio_path="temp_audio.wav"):
        """
        Paso 1: Extraer el audio del video usando MoviePy.
        """
        try:
            if os.path.exists(output_audio_path):
                os.remove(output_audio_path)
                
            video = VideoFileClip(video_path)
            
            # CORRECCIÓN MOVIEPY 2.0: Eliminado 'verbose=False'
            video.audio.write_audiofile(output_audio_path, logger=None)
            
            video.close()
            logging.info(f"✅ Audio extraído en: {output_audio_path}")
            return output_audio_path
        except Exception as e:
            logging.error(f"❌ Error extrayendo audio: {e}")
            return None

    def analyze_sentiment(self, text):
        """
        Paso 3: Analizar la emoción de un texto específico.
        Retorna: (emoción_dominante, score_dominante, dict_todas_las_emociones)
        """
        try:
            # El modelo puede truncar textos muy largos
            preds = self.nlp_classifier(text[:512])[0]
            
            # Ordenar de mayor a menor probabilidad
            preds_sorted = sorted(preds, key=lambda x: x['score'], reverse=True)
            
            dom_label = preds_sorted[0]['label']
            if dom_label == 'others':
                dom_label = 'neutral'
            
            dom_score = preds_sorted[0]['score']
            
            # Crear diccionario simple {emocion: score}
            # Renombrar 'others' a 'neutral' también aquí
            all_emotions = {}
            for item in preds:
                lbl = item['label']
                if lbl == 'others':
                    lbl = 'neutral'
                all_emotions[lbl] = float(item['score'])
            
            return dom_label, dom_score, all_emotions
        except Exception as e:
            logging.error(f"Error en NLP: {e}")
            return "neutral", 0.0, {}

    def process_video(self, video_path):
        """
        PIPELINE COMPLETO: Video -> Audio -> Texto -> Emociones (JSON)
        """
        logging.info(f"🚀 Iniciando análisis de audio para: {video_path}")
        
        # 1. Extraer Audio
        audio_path = self.extract_audio(video_path)
        if not audio_path:
            return []

        # 2. Transcribir (Whisper)
        logging.info("🗣️ Transcribiendo audio con timestamps...")
        # fp16=False es vital para que no falle en CPU
        transcription = self.asr_model.transcribe(audio_path, fp16=False)
        segments = transcription['segments']

        results = []
        
        # 3. Analizar cada segmento
        logging.info(f"🧠 Analizando emociones de {len(segments)} segmentos de texto...")
        for segment in segments:
            text = segment['text'].strip()
            start = segment['start']
            end = segment['end']
            
            if len(text) < 2:  # Ignorar ruidos o balbuceos cortos
                continue

            # Obtener emoción del texto
            dom_label, dom_score, all_emotions = self.analyze_sentiment(text)

            # Estructura JSON final (Alineada con Vision Module)
            entry = {
                "timestamp_start": start,
                "timestamp_end": end,
                "text": text,
                "dominant_emotion": dom_label,
                "confidence": float(dom_score),
                "all_emotions": all_emotions
            }
            results.append(entry)

        # Limpieza
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        logging.info("✅ Procesamiento de Audio/Texto finalizado.")
        return results