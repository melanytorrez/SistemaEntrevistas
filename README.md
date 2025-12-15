# Sistema de Análisis de Entrevistas Multimodal

Este proyecto implementa un sistema inteligente para analizar entrevistas utilizando visión computacional y procesamiento de lenguaje natural.

##  Tecnologías
- **Visión:** DeepFace (CNN pre-entrenada para detección de emociones).
- **Audio:** OpenAI Whisper (ASR para transcripción).
- **NLP:** Transformers (HuggingFace) para análisis de sentimiento en texto.
- **Integración:** Sincronización temporal de señales multimodales.

##  Estructura
- `/data`: Videos de validación y Ground Truth.
- `/src`: Código fuente de los módulos.
- `/models`: Pesos de modelos descargados.
- `/output`: Resultados del análisis (JSON, Gráficas).

##  Instalación
1. Crear entorno virtual.
2. `pip install -r requirements.txt`
3. Instalar FFmpeg en el sistema.

##  Equipo
- [Tu Nombre]