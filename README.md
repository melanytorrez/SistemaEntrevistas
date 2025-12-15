# Sistema de Analisis de Entrevistas Multimodal

Este proyecto implementa un sistema inteligente para analizar entrevistas utilizando vision computacional y procesamiento de lenguaje natural (NLP). El objetivo es detectar congruencias e incongruencias emocionales combinando el analisis facial con el analisis semantico del discurso.

## Tecnologias Utilizadas
- Vision: DeepFace (Wrapper para modelos CNN pre-entrenados como VGG-Face).
- Audio: OpenAI Whisper (Sistema ASR para transcripcion robusta).
- NLP: Transformers (HuggingFace) para analisis de sentimiento en texto (Modelo RoBERTa).
- Integracion: Sincronizacion temporal de señales multimodales.

## Estructura del Proyecto
- /data: Contiene los videos de validacion y el archivo Excel de Ground Truth.
- /src: Codigo fuente de los modulos de procesamiento (Python).
- /models: Almacenamiento local de pesos de modelos descargados.
- /output: Resultados del analisis (Archivos JSON y Graficas generadas).

## Instalacion y Requisitos
1. Crear un entorno virtual en Python 3.x.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Instalar FFmpeg en el sistema operativo y agregarlo al PATH.