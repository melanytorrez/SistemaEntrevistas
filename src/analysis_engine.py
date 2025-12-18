import numpy as np
from collections import Counter

class AnalysisEngine:
    def __init__(self, emotion_map=None):
        self.emotion_map = emotion_map or {
            "joy": "happy",
            "sadness": "sad",
            "anger": "angry",
            "neutral": "neutral",
            "fear": "fear",
            "disgust": "disgust",
            "surprise": "surprise"
        }
        
        # Mapa de congruencia: {AudioEmotion: [CompatibleVisualEmotions]}
        self.compatibility_map = {
            "happy": ["happy", "surprise"],
            "sad": ["sad", "fear", "neutral"],
            "angry": ["angry", "disgust", "neutral"],
            "neutral": ["neutral", "sad", "calm"],
            "fear": ["fear", "sad", "surprise"]
        }

    def normalize_emotion(self, emotion):
        return self.emotion_map.get(emotion.lower(), emotion.lower())

    def analyze_congruence(self, audio_data, vision_data):
        """
        Analiza la congruencia segmento a segmento.
        Retorna lista de segmentos enriquecidos y métricas globales.
        """
        analyzed_segments = []
        congruence_matches = 0
        total_segments = 0
        
        # Indexar visión por timestamps para búsqueda rápida (Optimización O(n))
        # En un caso real, esto podría ser un árbol de intervalos, pero para listas ordenadas simple sirve
        # Asumimos vision_data ordenado por tiempo
        
        for audio_seg in audio_data:
            start = audio_seg.get('timestamp_start', 0)
            end = audio_seg.get('timestamp_end', 0)
            audio_emo = self.normalize_emotion(audio_seg.get('dominant_emotion', 'neutral'))
            
            # 1. Obtener frames visuales en rango
            visual_frames = [
                f for f in vision_data 
                if start <= f['timestamp'] <= end
            ]
            
            visual_emo = "unknown"
            visual_conf = 0.0
            
            if visual_frames:
                # Calcular emoción dominante visual en este segmento
                emotions = [f['dominant_emotion'] for f in visual_frames]
                if emotions:
                    visual_emo = Counter(emotions).most_common(1)[0][0]
                    # Promedio de confianza
                    confs = [f['confidence'] for f in visual_frames if f['dominant_emotion'] == visual_emo]
                    visual_conf = sum(confs) / len(confs) if confs else 0.0
            
            # 2. Verificar congruencia
            is_congruent = True
            conflict_reason = "Match"
            
            normalized_vis = self.normalize_emotion(visual_emo)
            
            if normalized_vis == "unknown":
                is_congruent = False # O Ignorar
                conflict_reason = "No visual data"
            else:
                compatible = self.compatibility_map.get(audio_emo, [])
                if normalized_vis not in compatible:
                    is_congruent = False
                    conflict_reason = f"Mismatch: Audio({audio_emo}) != Video({normalized_vis})"
                else:
                    congruence_matches += 1
            
            total_segments += 1
            
            analyzed_segments.append({
                "time_range": [start, end],
                "text": audio_seg.get('text', ''),
                "audio_emotion": audio_emo,
                "visual_emotion": visual_emo,
                "visual_confidence": visual_conf,
                "is_congruent": is_congruent,
                "reason": conflict_reason
            })
            
        congruence_score = (congruence_matches / total_segments) * 100 if total_segments > 0 else 0
        
        return {
            "segments": analyzed_segments,
            "global_metrics": {
                "congruence_score": round(congruence_score, 2),
                "total_segments": total_segments,
                "congruent_segments": congruence_matches
            }
        }

    def detect_emotional_shifts(self, vision_data, window_size=5):
        """
        Detecta cambios bruscos de emoción en el canal visual.
        """
        shifts = []
        if len(vision_data) < window_size:
            return shifts
            
        current_emo = vision_data[0]['dominant_emotion']
        start_time = vision_data[0]['timestamp']
        
        for i in range(1, len(vision_data)):
            frame_emo = vision_data[i]['dominant_emotion']
            timestamp = vision_data[i]['timestamp']
            
            if frame_emo != current_emo:
                # Registrar cambio
                shifts.append({
                    "time": timestamp,
                    "from": current_emo,
                    "to": frame_emo
                })
                current_emo = frame_emo
                
        return shifts
