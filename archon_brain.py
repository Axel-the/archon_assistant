import google.generativeai as genai
import json
import logging
from config import GOOGLE_API_KEY, ARCHON_SYSTEM_PROMPT, ARCHON_GENERATION_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

class ArchonBrain:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest', system_instruction=ARCHON_SYSTEM_PROMPT)
        self.chat = self.model.start_chat(history=[])

    def analyze_input(self, text):
        """
        Phase 1: Analysis of Input.
        Sends the user text to the LLM to get the JSON analysis.
        """
        try:
            # We force the model to return JSON by prompting it or using generation config if supported efficiently.
            # For now, we rely on the system prompt instructions.
            response = self.chat.send_message(f"TRANSCRIPCIÓN_DE_VOZ: {text}\nINSTRUCCIÓN: Genera SOLO el JSON de la FASE 1. No generes nada más.")
            
            # Clean up response to ensure it's valid JSON
            content = response.text.strip()
            
            # Extract the first JSON object found
            start_idx = content.find('{')
            if start_idx != -1:
                brace_count = 0
                for i, char in enumerate(content[start_idx:], start=start_idx):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            content = content[start_idx:i+1]
                            break
            
            data = json.loads(content)
            logger.info(f"Fase 1 Análisis: {data}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {e} - Contenido: {response.text}")
            # Fallback: try to guess intent from text if JSON fails
            return {"intencion_detectada": "Desconocida", "entidades_extraidas": {}}
        except Exception as e:
            logger.error(f"Error en Fase 1: {e}")
            return {"intencion_detectada": "Desconocida", "entidades_extraidas": {}}

    def generate_response(self, analysis_data, search_results=None):
        """
        Phase 3: Response Generation.
        Generates the final text response based on analysis and optional search results.
        """
        try:
            # Create a fresh prompt for generation to avoid context pollution
            prompt = "Eres ARCHON. Genera la respuesta verbal final para el usuario.\n"
            prompt += "IMPORTANTE: NO generes JSON. NO menciones 'Fase'. Solo el texto que dirás.\n\n"
            prompt += f"INTENCIÓN DETECTADA: {analysis_data.get('intencion_detectada')}\n"
            prompt += f"ENTIDADES: {analysis_data.get('entidades_extraidas')}\n"
            prompt += f"TRANSCRIPCIÓN ORIGINAL: {analysis_data.get('transcripcion_original', '')}\n"
            
            if search_results:
                prompt += f"INFORMACIÓN DE BÚSQUEDA: {search_results}\n"
            
            prompt += "\nRESPUESTA (Texto plano, breve y servicial):"
            
            response = self.chat.send_message(prompt)
            
            # Clean up any potential markdown or headers from the response
            text_response = response.text.strip()
            text_response = text_response.replace("```", "").replace("json", "")
            
            logger.info(f"Fase 3 Respuesta: {text_response}")
            return text_response
        except Exception as e:
            logger.error(f"Error en Fase 3: {e}")
            return "Lo siento, hubo un error al generar mi respuesta."
