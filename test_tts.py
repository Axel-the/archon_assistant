import pyttsx3

def test_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"Found {len(voices)} voices.")
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name} - ID: {voice.id}")
        
    print("\nTesting default voice...")
    engine.say("Prueba de audio. Hola usuario.")
    engine.runAndWait()

    # Try to find a Spanish voice specifically
    print("\nTesting Spanish voice search...")
    spanish_voice = None
    for voice in voices:
        if "spanish" in voice.name.lower() or "es-" in voice.id.lower():
            spanish_voice = voice.id
            print(f"Found Spanish voice: {voice.name}")
            break
    
    if spanish_voice:
        engine.setProperty('voice', spanish_voice)
        engine.say("Esta es una prueba en español.")
        engine.runAndWait()
    else:
        print("No Spanish voice found.")

if __name__ == "__main__":
    test_tts()
