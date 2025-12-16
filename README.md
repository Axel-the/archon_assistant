# 🤖 ARCHON Assistant

ARCHON es un asistente virtual inteligente, amigable y con personalidad, diseñado para ayudarte en tus tareas diarias mediante comandos de voz. Utiliza la tecnología de Google Gemini para entender y procesar tus peticiones de manera natural.

## 📋 Requisitos

- **Python 3.8** o superior.
- Una **API Key de Google Gemini** (gratuita).
- Micrófono y altavoces funcionales.

## 🚀 Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local:

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Axel-the/archon_assistant.git
    cd archon_assistant
    ```

2.  **Crear un entorno virtual (Recomendado):**

    ```bash
    python -m venv venv
    ```

    - En Windows: `.\venv\Scripts\activate`
    - En macOS/Linux: `source venv/bin/activate`

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

    > **Nota:** Si tienes problemas instalando `pyaudio` en Windows, intenta descargar el archivo `.whl` correspondiente a tu versión de Python desde [aquí](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) e instálalo con `pip install archivo.whl`.

## ⚙️ Configuración

### ⚠️ IMPORTANTE: Seguridad de la API Key

Este proyecto utiliza variables de entorno para proteger tu API Key.

**NUNCA subas tu API Key real a GitHub.**

1.  Crea un archivo llamado `.env` en la raíz del proyecto (junto a `main.py`).
2.  Abre el archivo `.env` y añade tu clave de la siguiente manera:

```env
GOOGLE_API_KEY=(Pon tu clave aquí)
```

**Nota:** El archivo `.env` ya está añadido al `.gitignore`, por lo que git lo ignorará automáticamente.


## 🎮 Uso

Para iniciar el asistente, simplemente ejecuta:

```bash
python main.py
```

ARCHON te saludará y podrás empezar a interactuar con él usando tu voz.

### Comandos de Ejemplo:
- "Hola Archon, ¿cómo estás?"
- "Busca información sobre el clima en Peru."
- "Abre el Bloc de notas." (Requiere configurar nombres de apps en `skills.py` o `AppOpener`)
- "Adiós."

## 🛠️ Tecnologías Usadas

- **Google Generative AI (Gemini):** Cerebro del asistente.
- **SpeechRecognition:** Conversión de voz a texto.
- **pyttsx3:** Síntesis de voz (Texto a voz).
- **AppOpener:** Control de aplicaciones.

---
Hecho con ❤️ por Axel
