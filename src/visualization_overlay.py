import cv2
import json
import os
import numpy as np

# Configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, 'data', 'video1.mp4')
REPORT_JSON = os.path.join(BASE_DIR, 'results', 'integrated_report_video1.json')
OUTPUT_VIDEO = os.path.join(BASE_DIR, 'results', 'video1_analysis_overlay.mp4')

# Colores (BGR)
COLOR_TEXT = (255, 255, 255)       # Blanco
COLOR_BG = (0, 0, 0)               # Negro (Fondo texto)
COLOR_ALERT = (0, 0, 255)          # Rojo (Incongruencia)
COLOR_OK = (0, 255, 0)             # Verde (Coherente)

def load_data():
    if not os.path.exists(REPORT_JSON):
        print("❌ No se encontró el reporte integrado.")
        return []
    with open(REPORT_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_data_for_timestamp(report_data, current_time):
    """
    Busca qué segmento de datos corresponde al tiempo actual.
    """
    for item in report_data:
        start, end = item['time_range']
        if start <= current_time <= end:
            return item
    return None

def draw_text_with_bg(img, text, pos, font_scale=0.6, color=COLOR_TEXT, thickness=2, bg_color=COLOR_BG):
    """
    Dibuja texto con un fondo rectangular para mejor legibilidad.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    
    # Dibujar rectángulo de fondo
    cv2.rectangle(img, (x - 5, y - text_h - 5), (x + text_w + 5, y + 5), bg_color, -1)
    # Dibujar texto
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness)

def create_overlay():
    print("--- GENERANDO VIDEO CON OVERLAY ---")
    
    data_points = load_data()
    if not data_points:
        return

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("❌ Error abriendo video original.")
        return

    # Propiedades del video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Configurar Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))
    
    print(f"🎬 Video: {width}x{height} @ {fps}fps")
    print("🚀 Renderizando... (esto puede tardar)")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        current_time = frame_count / fps
        
        # Buscar datos para este momento
        info = get_data_for_timestamp(data_points, current_time)
        
        if info:
            # 1. Datos de AUDIO (Arriba)
            audio_emo = info['audio_analysis']['emotion'].upper()
            audio_conf = info['audio_analysis']['confidence']
            text_content = info['text_content']
            
            # Header Audio
            header_text = f"AUDIO: {audio_emo} ({audio_conf:.2f})"
            draw_text_with_bg(frame, header_text, (20, 30), font_scale=0.7, thickness=2, color=(0, 255, 255)) # Cyan
            
            # Subtítulos (Multi-linea)
            max_chars = 60
            words = text_content.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                if len(" ".join(current_line + [word])) <= max_chars:
                    current_line.append(word)
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            
            # Dibujar líneas
            y_pos = 60
            for line in lines:
                draw_text_with_bg(frame, f"'{line}'", (20, y_pos), font_scale=0.6, thickness=2)
                y_pos += 25
            
            # 2. Datos de VISIÓN (Abajo)
            vis_emo = info['visual_analysis']['dominant_emotion'].upper()
            vis_conf = info['visual_analysis']['avg_confidence']
            
            bottom_text = f"VISION: {vis_emo} ({vis_conf:.2f})"
            draw_text_with_bg(frame, bottom_text, (20, height - 30), font_scale=0.7, thickness=2)
            
            # 3. ALERTA DE INCONGRUENCIA (Centro)
            if info['integration']['is_incongruent']:
                alert_text = "⚠️ INCONGRUENCIA DETECTADA ⚠️"
                
                # Efecto parpadeo (cada 10 frames)
                if (frame_count // 10) % 2 == 0:
                     # Texto rojo grande en el centro
                    text_size = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
                    text_x = (width - text_size[0]) // 2
                    text_y = (height + text_size[1]) // 2
                    
                    draw_text_with_bg(frame, alert_text, (text_x, text_y), font_scale=1.2, color=COLOR_TEXT, bg_color=COLOR_ALERT, thickness=3)
                    
                    # Borde rojo a todo el video
                    cv2.rectangle(frame, (0, 0), (width, height), COLOR_ALERT, 10)

        # Barra de progreso en consola
        if frame_count % 50 == 0:
            prog = (frame_count / total_frames) * 100
            print(f"   Procesando: {prog:.1f}%", end='\r')

        out.write(frame)
        frame_count += 1
        
    cap.release()
    out.release()
    print(f"\n✅ Video mudo guardado en: {OUTPUT_VIDEO}")
    
    # --- PASO EXTRA: AGREGAR AUDIO CON MOVIEPY ---
    try:
        from moviepy import VideoFileClip, AudioFileClip
        print("🔊 Agregando audio original...")
        
        # Cargar videos
        original_clip = VideoFileClip(VIDEO_PATH)
        processed_clip = VideoFileClip(OUTPUT_VIDEO)
        
        # Asignar audio
        final_clip = processed_clip.with_audio(original_clip.audio)
        
        # Guardar final
        FINAL_OUTPUT = OUTPUT_VIDEO.replace(".mp4", "_audio.mp4")
        final_clip.write_videofile(FINAL_OUTPUT, codec='libx264', audio_codec='aac', logger=None)
        
        # Limpiar
        original_clip.close()
        processed_clip.close()
        final_clip.close()
        
        # Opcional: Reemplazar el mudo con el final
        if os.path.exists(OUTPUT_VIDEO):
            os.remove(OUTPUT_VIDEO)
        os.rename(FINAL_OUTPUT, OUTPUT_VIDEO)
        
        print(f"✅ Video CON AUDIO listo en: {OUTPUT_VIDEO}")
        
    except Exception as e:
        print(f"⚠️ No se pudo agregar audio (Error MoviePy): {e}")
        print("El video generado está correcto pero sin sonido.")

if __name__ == "__main__":
    create_overlay()
