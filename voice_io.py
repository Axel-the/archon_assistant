import speech_recognition as sr
import pyttsx3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceIO:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure voice (try to find a Spanish voice)
        voices = self.engine.getProperty('voices')
        spanish_voice_found = False
        for voice in voices:
            if "spanish" in voice.name.lower() or "es-" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                spanish_voice_found = True
                break
        
        if not spanish_voice_found:
            logger.warning("No Spanish voice found. Using default voice.")
        else:
            logger.info(f"Voz configurada: {self.engine.getProperty('voice')}")

        self.engine.setProperty('rate', 145) # Slower speed for better clarity

    def listen(self):
        """Listens to the microphone and returns text."""
        with sr.Microphone() as source:
            logger.info("Calibrando ruido de fondo... (silencio por favor)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.pause_threshold = 1.0  # Allow longer pauses
            self.recognizer.energy_threshold += 50 # Slightly increase sensitivity buffer
            
            logger.info("Escuchando... ¡Habla ahora!")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                logger.info("Procesando audio...")
                text = self.recognizer.recognize_google(audio, language="es-ES")
                logger.info(f"Usuario dijo: {text}")
                return text
            except sr.WaitTimeoutError:
                logger.info("Tiempo de espera agotado.")
                return None
            except sr.UnknownValueError:
                logger.info("No se entendió el audio.")
                return None
            except sr.RequestError as e:
                logger.error(f"Error en el servicio de reconocimiento: {e}")
                return None
            except Exception as e:
                logger.error(f"Error inesperado al escuchar: {e}")
                return None

    def clean_text(self, text):
        """Removes markdown and special characters for better TTS."""
        import re
        # Remove bold/italic markers
        text = text.replace("**", "").replace("*", "")
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove headers
        text = text.replace("###", "").replace("##", "").replace("#", "")
        return text.strip()

    def speak_powershell(self, text):
        """Uses PowerShell to speak text (Fallback)."""
        import subprocess
        try:
            # PowerShell command to speak
            cmd = f"Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Rate = 0; $speak.Speak('{text}')"
            subprocess.run(["powershell", "-Command", cmd], check=True)
        except Exception as e:
            logger.error(f"Error en PowerShell TTS: {e}")

    def speak(self, text):
        """Converts text to speech."""
        if not text:
            return
        
        clean_text = self.clean_text(text)
        logger.info(f"ARCHON (Voz): {clean_text}")
        
        # Try PowerShell first as it seems more robust for this user
        # If it fails or is too slow, we can revert, but let's try this to fix the "no sound" issue.
        # We escape single quotes for PowerShell
        safe_text = clean_text.replace("'", "''")
        self.speak_powershell(safe_text)
        
        # Fallback/Original (Commented out to force test of PowerShell)
        # self.engine.say(clean_text)
        # self.engine.runAndWait()
