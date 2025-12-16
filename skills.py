from AppOpener import open as app_opener
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Skills:
    def open_app(self, app_name):
        """Opens an application using AppOpener."""
        try:
            logger.info(f"Intentando abrir: {app_name}")
            app_opener(app_name, match_closest=True, throw_error=True)
            return True
        except Exception as e:
            logger.error(f"Error al abrir la app {app_name}: {e}")
            return False

    def search_web(self, query):
        """
        Simulates a web search. 
        In a real scenario with a Google Search API Key, this would make an HTTP request.
        """
        logger.info(f"Buscando en web: {query}")
        # Placeholder simulation
        return f"Resultados simulados para '{query}'. (Nota: API de búsqueda no configurada)"
