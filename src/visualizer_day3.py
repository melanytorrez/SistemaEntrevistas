import matplotlib.pyplot as plt
import json
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'results', 'integrated_report_video1.json')
OUTPUT_IMG = os.path.join(BASE_DIR, 'results', 'final_integration_chart.png')

EMOTION_SCORES = {
    "happy": 1, "joy": 1, "surprise": 1,

    "neutral": 0, "others": 0,

    "sad": -1, "sadness": -1, "anger": -1, "angry": -1, 
    "fear": -1, "disgust": -1
}

def generate_visualization():
    print("--- GENERANDO VISUALIZACIÓN INTEGRADA (Pareja 3) ---")
    
    if not os.path.exists(JSON_PATH):
        print(f" Error: No existe el reporte integrado en {JSON_PATH}")
        return

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print(" El JSON está vacío.")
        return

    times = []
    audio_vals = []
    visual_vals = []
    labels_audio = []
    labels_visual = []
    
    zones = []

    for item in data:
        t_start = item['time_range'][0]
        t_end = item['time_range'][1]
        mid_time = (t_start + t_end) / 2
        times.append(mid_time)

        emo_audio = item['audio_analysis']['emotion']
        emo_visual = item['visual_analysis']['dominant_emotion']

        val_a = EMOTION_SCORES.get(emo_audio, 0)
        val_v = EMOTION_SCORES.get(emo_visual, 0)

        audio_vals.append(val_a)
        visual_vals.append(val_v)
        
        labels_audio.append(emo_audio)
        labels_visual.append(emo_visual)

        is_incongruent = item['integration']['is_incongruent']
        color = 'red' if is_incongruent else 'green'
        zones.append((t_start, t_end, color))

    plt.figure(figsize=(14, 7))
    
    for start, end, color in zones:
        plt.axvspan(start, end, color=color, alpha=0.15)

    plt.plot(times, audio_vals, marker='o', linestyle='-', color='blue', label='Audio/Texto (NLP)', linewidth=2, markersize=8)
    plt.plot(times, visual_vals, marker='s', linestyle='--', color='orange', label='Visión (CNN)', linewidth=2, markersize=8)

    for i, txt in enumerate(labels_audio):
        plt.annotate(txt, (times[i], audio_vals[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='blue')
        
    for i, txt in enumerate(labels_visual):
        plt.annotate(txt, (times[i], visual_vals[i]), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color='darkorange')

    plt.title("Análisis de Congruencia Multimodal: Entrevista", fontsize=16)
    plt.xlabel("Tiempo (segundos)", fontsize=12)
    plt.ylabel("Polaridad Emocional", fontsize=12)
    plt.yticks([-1, 0, 1], ["Negativo\n(Triste/Enojo)", "Neutral", "Positivo\n(Feliz/Sorpresa)"])
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='upper right')
    
    plt.figtext(0.5, 0.01, "Fondo Verde: Congruente | Fondo Rojo: Incongruente", ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG)
    print(f" Gráfico generado exitosamente en: {OUTPUT_IMG}")

if __name__ == "__main__":
    generate_visualization()