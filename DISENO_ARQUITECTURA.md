# DISEÑO DE ARQUITECTURA E INTERFAZ DE DATOS

Para asegurar la integracion entre los modulos de Vision Computacional y Procesamiento de Lenguaje Natural, se ha definido el siguiente esquema estandarizado.

## 1. Flujo de Datos
Video de Entrada -> [Modulo Vision] -> JSON Emociones Faciales (Time-series)
Video de Entrada -> [Modulo Audio] -> Texto -> [Modulo NLP] -> JSON Emociones Texto (Segmentos)

## 2. Interfaz de Salida: Modulo de Vision
El script procesador de video generara una lista de objetos, donde cada objeto representa un muestreo del video (ej. cada 5 frames).

Formato JSON:
[
  {
    "frame_id": 15,
    "timestamp": 0.5,
    "emotions": {
      "angry": 0.02,
      "disgust": 0.00,
      "fear": 0.01,
      "happy": 0.10,
      "sad": 0.05,
      "surprise": 0.00,
      "neutral": 0.82
    },
    "dominant_emotion": "neutral"
  },
  ...
]

## 3. Interfaz de Salida: Modulo de Audio/NLP
El script procesador de audio utilizara Whisper para segmentar por frases y RoBERTa para clasificar la emocion de cada frase.

Formato JSON:
[
  {
    "start_time": 0.0,
    "end_time": 4.5,
    "text_content": "La verdad es que estoy muy contento con el proyecto.",
    "emotion_prediction": {
      "label": "happy",
      "score": 0.98
    }
  },
  ...
]

## 4. Estrategia de Fusion (Dia 3)
La integracion se realizara mediante alineacion temporal:
1. Se tomara el intervalo de tiempo [start_time, end_time] de cada frase de texto.
2. Se buscaran todos los frames de video cuyo "timestamp" caiga dentro de ese intervalo.
3. Se calculara el promedio de los vectores de emocion facial en ese lapso.
4. Se comparara el vector promedio facial contra el vector de emocion del texto para calcular la "Distancia de Congruencia".