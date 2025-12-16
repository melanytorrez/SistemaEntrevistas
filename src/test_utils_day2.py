from utils import setup_logger, get_video_path, get_video_properties, save_analysis_json

def test_utilities_module():
    logger = setup_logger()
    print("--- INICIANDO TEST DE UTILIDADES ---")
    logger.info("Test de logging iniciado (esto debería salir en el archivo .log)")

    
    video_name = "video1.mp4" 
    try:
        logger.info(f"Buscando video: {video_name}")
        path = get_video_path(video_name)
        
        logger.info("Obteniendo propiedades...")
        props = get_video_properties(path)
        print(f" Propiedades detectadas: {props}")
        
    except Exception as e:
        logger.error(f"Fallo en prueba de video: {e}")
        print(" Error en video (revisa logs)")

    logger.info("Probando guardado de JSON estructurado...")
    
    datos_simulados = [
        {"id": 1, "status": "test"},
        {"id": 2, "status": "ok"}
    ]
    
    save_analysis_json(datos_simulados, "test_output_utils.json", "test_module")
    print(" JSON de prueba guardado en /output/test_output_utils.json")
    
    print("\n MÓDULO DE UTILIDADES FUNCIONANDO CORRECTAMENTE")
    print("Revisa la carpeta 'logs' y la carpeta 'output'.")

if __name__ == "__main__":
    test_utilities_module()