import json
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VISION_JSON = os.path.join(BASE_DIR, 'results', 'vision_analysis.json')
AUDIO_JSON = os.path.join(BASE_DIR, 'results', 'audio_analysis_video1.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'results', 'integrated_report_video1.json')


EMOTION_MAP = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "others": "neutral" 
}

def load_json(path):
    if not os.path.exists(path):
        print(f" Error: No se encuentra {path}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_visual_emotions_in_range(vision_data, start_time, end_time):
    """
    Busca los frames visuales que caen dentro del rango de tiempo del audio.
    Retorna la emoción más frecuente (moda) o promedio de scores.
    """
    frames_in_range = []
    for frame in vision_data:
        t = frame['timestamp']
        if start_time <= t <= end_time:
            frames_in_range.append(frame)
            
    if not frames_in_range:
        return None

    
    agg_scores = {}
    for frame in frames_in_range:
        emotions = frame['all_emotions']
        for emo, score in emotions.items():
            if emo not in agg_scores:
                agg_scores[emo] = 0.0
            agg_scores[emo] += score
            
    count = len(frames_in_range)
    avg_scores = {k: v / count for k, v in agg_scores.items()}
    
    dominant_visual = max(avg_scores, key=avg_scores.get)
    
    return {
        "dominant_emotion": dominant_visual,
        "avg_scores": avg_scores,
        "frame_count": count
    }

def check_incongruence(audio_emo, visual_emo):
    """
    Verifica si las emociones chocan.
    """
    normalized_audio = EMOTION_MAP.get(audio_emo, audio_emo)
    
    
    if normalized_audio == visual_emo:
        return False, "Coherent"
    
    if normalized_audio == "neutral" or visual_emo == "neutral":
        return False, "Neutral Match"
        
    opposites = {
        "happy": ["sad", "angry", "fear", "disgust"],
        "sad": ["happy", "surprise"],
        "angry": ["happy"],
        "fear": ["happy"]
    }
    
    if normalized_audio in opposites and visual_emo in opposites[normalized_audio]:
        return True, f"Conflict: Audio({normalized_audio}) vs Face({visual_emo})"
        
    return False, "Different but compatible"

def integrate_data():
    print("--- INICIANDO INTEGRACIÓN MULTIMODAL (Día 3) ---")
    
    vision_data = load_json(VISION_JSON)
    audio_data = load_json(AUDIO_JSON)
    
    print(f" Datos cargados: {len(vision_data)} frames de visión, {len(audio_data)} segmentos de audio.")
    
    integrated_results = []
    
    for segment in audio_data:
        t_start = segment['timestamp_start']
        t_end = segment['timestamp_end']
        text = segment['text']
        audio_dom = segment['dominant_emotion']
        audio_conf = segment['confidence']
        
        print(f"\n🔹 Analizando segmento: [{t_start}s - {t_end}s]")
        print(f"   🗣️ Audio: {audio_dom} ({audio_conf:.2f}) -> '{text}'")
        
        visual_stats = get_visual_emotions_in_range(vision_data, t_start, t_end)
        
        if visual_stats:
            vis_dom = visual_stats['dominant_emotion']
            vis_conf = visual_stats['avg_scores'][vis_dom]
            frames_n = visual_stats['frame_count']
            
            print(f"   Visión ({frames_n} frames): Promedio={vis_dom} ({vis_conf:.2f})")
            
            is_incongruent, reason = check_incongruence(audio_dom, vis_dom)
            
            status_icon = "🚩" if is_incongruent else "✅"
            print(f"   {status_icon} Estado: {reason}")
            
            integrated_results.append({
                "time_range": [t_start, t_end],
                "text_content": text,
                "audio_analysis": {
                    "emotion": audio_dom,
                    "confidence": audio_conf
                },
                "visual_analysis": {
                    "dominant_emotion": vis_dom,
                    "avg_confidence": vis_conf,
                    "frames_analyzed": frames_n
                },
                "integration": {
                    "is_incongruent": is_incongruent,
                    "status_message": reason
                }
            })
        else:
            print(" No hay datos visuales suficientes para este rango.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(integrated_results, f, indent=4, ensure_ascii=False)
        
    print(f"\n💾 Reporte integrado guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    integrate_data()
