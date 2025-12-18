import json
import os
import datetime

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTEGRATED_JSON = os.path.join(BASE_DIR, 'results', 'integrated_report_video1.json')
FINAL_REPORT_MD = os.path.join(BASE_DIR, 'results', 'final_report_day4.md')

class InterviewAnalyzer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            print(f"❌ Error: No se encontró {self.data_path}")
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def detect_emotional_shifts(self):
        """Identifica cambios bruscos en la emoción dominante entre segmentos."""
        shifts = []
        for i in range(1, len(self.data)):
            prev_audio = self.data[i-1]['audio_analysis']['emotion']
            curr_audio = self.data[i]['audio_analysis']['emotion']
            
            if prev_audio != curr_audio:
                shifts.append({
                    "time": self.data[i]['time_range'][0],
                    "from": prev_audio,
                    "to": curr_audio,
                    "type": "Audio/Texto"
                })
        return shifts

    def calculate_congruence_metrics(self):
        """Calcula el porcentaje de congruencia multimodal."""
        total_segments = len(self.data)
        if total_segments == 0: return 0, 0
        
        congruent_count = sum(1 for item in self.data if not item['integration']['is_incongruent'])
        score = (congruent_count / total_segments) * 100
        return score, total_segments

    def generate_insights(self, score, shifts):
        """Genera conclusiones automáticas basadas en los datos."""
        insights = []
        
        # Insight de Congruencia
        if score >= 80:
            insights.append("✅ **Alta Coherencia:** El entrevistado muestra una alineación excepcional entre su lenguaje verbal y sus expresiones faciales.")
        elif score >= 50:
            insights.append("⚠️ **Coherencia Moderada:** Existen algunas discrepancias menores entre el discurso y la expresión facial.")
        else:
            insights.append("🚩 **Baja Coherencia:** Se detectaron múltiples contradicciones entre lo que se dice y lo que se muestra físicamente.")

        # Insight de Estabilidad
        if len(shifts) > 3:
            insights.append("🔄 **Alta Volatilidad Emocional:** Se detectaron cambios frecuentes en el estado anímico durante la sesión.")
        elif len(shifts) == 0:
            insights.append("⚖️ **Estabilidad Emocional:** El entrevistado mantuvo una línea emocional constante.")

        return insights

    def create_markdown_report(self):
        """Genera el reporte final de análisis en formato Markdown."""
        if not self.data:
            print("⚠️ No hay datos para generar el reporte.")
            return

        score, total = self.calculate_congruence_metrics()
        shifts = self.detect_emotional_shifts()
        insights = self.generate_insights(score, shifts)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        report = f"""# 📝 Reporte Avanzado de Análisis de Entrevista
**Fecha de Generación:** {now}
**Video Analizado:** video1.mp4

## 📊 Resumen Ejecutivo
- **Puntaje de Congruencia Multimodal:** `{score:.2f}%`
- **Total de segmentos analizados:** {total}
- **Cambios emocionales detectados:** {len(shifts)}

## 💡 Insights y Hallazgos Principales
{chr(10).join(['- ' + i for i in insights])}

## 🔄 Cronología de Cambios Emocionales
{"| Tiempo | De | A | Tipo |" if shifts else "*No se detectaron cambios bruscos.*"}
{"| :--- | :--- | :--- | :--- |" if shifts else ""}
{chr(10).join([f"| {s['time']}s | {s['from']} | {s['to']} | {s['type']} |" for s in shifts])}

## 🕵️ Detalle por Segmento
| Tiempo (s) | Texto Transcrito | Emoción Audio | Emoción Rostro | Estado |
| :--- | :--- | :--- | :--- | :--- |
"""
        for item in self.data:
            t = f"{item['time_range'][0]}-{item['time_range'][1]}"
            text = item['text_content'][:50] + "..." if len(item['text_content']) > 50 else item['text_content']
            e_a = item['audio_analysis']['emotion']
            e_v = item['visual_analysis']['dominant_emotion']
            status = "✅ OK" if not item['integration']['is_incongruent'] else "🚩 Conflicto"
            report += f"| {t} | {text} | {e_a} | {e_v} | {status} |\n"

        report += "\n\n--- \n*Este reporte es generado automáticamente por el Sistema Integrado de Análisis de Entrevistas (Día 4).* "

        with open(FINAL_REPORT_MD, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return FINAL_REPORT_MD

if __name__ == "__main__":
    print("--- INICIANDO ANÁLISIS AVANZADO (Día 4) ---")
    analyzer = InterviewAnalyzer(INTEGRATED_JSON)
    report_path = analyzer.create_markdown_report()
    
    if report_path:
        print(f"✅ Reporte generado exitosamente en: {report_path}")
        print("-" * 40)
        # Mostrar resumen rápido
        score, _ = analyzer.calculate_congruence_metrics()
        print(f"📈 Congruencia Final: {score:.2f}%")
