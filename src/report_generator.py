import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def generate_markdown_report(self, analysis_results, video_name="Video Unknown"):
        metrics = analysis_results['global_metrics']
        segments = analysis_results['segments']
        shifts = analysis_results.get('emotional_shifts', [])
        
        score = metrics['congruence_score']
        status_icon = "🟢" if score > 70 else "🟡" if score > 40 else "🔴"
        
        report = f"""# 📊 Reporte de Análisis Multimodal: {video_name}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Resumen Ejecutivo
- **Puntaje de Congruencia**: {status_icon} **{score}%**
- **Total Segmentos Analizados**: {metrics['total_segments']}
- **Segmentos Congruentes**: {metrics['congruent_segments']}

### Interpretación
El sujeto muestra un nivel de coherencia **{'ALTO' if score > 70 else 'MEDIO' if score > 40 else 'BAJO'}** entre su expresión verbal y no verbal.
{self._generate_insight_text(score)}

## 2. Análisis Temporal y Anomalías
"""
        if shifts:
            report += "### 🔄 Cambios Emocionales Detectados (Visual)\n"
            for shift in shifts[:10]: # Top 10
                report += f"- `T={shift['time']}s`: Cambio de **{shift['from']}** a **{shift['to']}**\n"
        else:
            report += "No se detectaron cambios emocionales bruscos significativos.\n"

        report += "\n## 3. Desglose por Segmentos (Muestreo)\n"
        report += "| Tiempo | Audio (Texto) | Emoción Audio | Emoción Video | Congruencia |\n"
        report += "|--------|---------------|---------------|---------------|-------------|\n"
        
        for seg in segments:
            # Shorten text
            text = (seg['text'][:30] + '...') if len(seg['text']) > 30 else seg['text']
            cong_icon = "✅" if seg['is_congruent'] else "❌"
            
            report += f"| {seg['time_range'][0]}-{seg['time_range'][1]}s | {text} | {seg['audio_emotion']} | {seg['visual_emotion']} | {cong_icon} |\n"
            
        output_path = os.path.join(self.output_dir, f"final_report_{video_name.replace(' ', '_').lower()}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        return output_path

    def _generate_insight_text(self, score):
        if score < 40:
            return "⚠️ **ALERTA**: Se detectan múltiples inconsistencias. El sujeto podría estar ocultando información, sintiéndose incómodo o mintiendo (microexpresiones no coinciden con el discurso)."
        elif score < 70:
            return "ℹ️ **NOTA**: Existen algunas divergencias puntuales que podrían indicar nerviosismo o duda en temas específicos."
        else:
            return "✅ **OK**: El comportamiento es consistente y genuino."
