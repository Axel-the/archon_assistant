import time
import logging
from voice_io import VoiceIO
from archon_brain import ArchonBrain
from skills import Skills

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Iniciando ARCHON...")
    
    voice = VoiceIO()
    brain = ArchonBrain()
    skills = Skills()
    
    voice.speak("Sistemas en línea. Soy Archon. ¿En qué puedo ayudarte?")
    
    while True:
        try:
            # 1. Listen
            text = voice.listen()
            if not text:
                continue
            
            # 2. Analyze
            analysis = brain.analyze_input(text)
            intent = analysis.get("intencion_detectada")
            entities = analysis.get("entidades_extraidas", {})
            
            logger.info(f"Intención: {intent}")
            
            response_text = ""
            
            # 3. Decision Logic & Execution
            if intent == "AbrirAplicacion":
                app_name = entities.get("nombre_app")
                if app_name:
                    voice.speak(f"Abriendo {app_name}...")
                    success = skills.open_app(app_name)
                    if success:
                        response_text = f"He abierto {app_name}."
                    else:
                        response_text = f"No pude encontrar la aplicación {app_name}."
                else:
                    response_text = "No entendí qué aplicación abrir."

            elif intent == "BuscarInformacion":
                query = entities.get("query_busqueda")
                if query:
                    voice.speak(f"Buscando información sobre {query}...")
                    search_results = skills.search_web(query)
                    response_text = brain.generate_response(analysis, search_results)
                else:
                    response_text = "No entendí qué buscar."

            elif intent == "ResponderPregunta":
                response_text = brain.generate_response(analysis)

            elif intent == "SaludoDespedida":
                 response_text = brain.generate_response(analysis)
                 # Optional: Exit loop if goodbye
                 if "adiós" in text.lower() or "hasta luego" in text.lower():
                     voice.speak(response_text)
                     break

            elif intent == "ComandoSistema":
                # Placeholder for system commands
                response_text = "Comando de sistema reconocido, pero no tengo permisos para ejecutarlo aún."

            else:
                # Unknown or other intents
                response_text = brain.generate_response(analysis)
            
            # 4. Speak Response
            if response_text:
                voice.speak(response_text)
                
        except KeyboardInterrupt:
            logger.info("Deteniendo ARCHON...")
            break
        except Exception as e:
            logger.error(f"Error crítico en el bucle principal: {e}")
            voice.speak("Ocurrió un error interno.")

if __name__ == "__main__":
    main()
