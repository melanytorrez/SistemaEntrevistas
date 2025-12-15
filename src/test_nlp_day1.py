from transformers import pipeline

def test_nlp_model():
    print("--- INVESTIGACIÓN MODELO NLP (TEXTO) ---")
    # Elegimos este modelo porque sus emociones coinciden con las de DeepFace
    model_name = "j-hartmann/emotion-english-distilroberta-base"
    
    print(f"⏳ Descargando modelo: {model_name}...")
    try:
        # Pipeline hace todo el trabajo sucio
        classifier = pipeline("text-classification", model=model_name, return_all_scores=True)
        
        frase_prueba = "I am so angry about the delay but happy to see you."
        print(f"📝 Frase: '{frase_prueba}'")
        
        resultados = classifier(frase_prueba)
        
        # Mostramos resultados
        print("\n📊 Predicciones:")
        # resultados es una lista de listas, accedemos a la primera
        scores = resultados[0] 
        # Ordenamos por puntaje
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        for emotion in scores:
            print(f"   - {emotion['label']}: {emotion['score']:.4f}")
            
        print("\n✅ Modelo NLP validado y descargado.")
        
    except Exception as e:
        print(f"❌ Error en NLP: {e}")

if __name__ == "__main__":
    test_nlp_model()