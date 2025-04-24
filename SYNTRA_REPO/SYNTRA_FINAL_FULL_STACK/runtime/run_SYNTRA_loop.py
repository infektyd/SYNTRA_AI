# run_SYNTRA_loop.py
from utils.language_engine.language_core import run_language_loop
from utils.language_engine.voice_bridge import speak_text

if __name__ == "__main__":
    while True:
        user_input = input("\n🗣️ Input text to SYNTRA: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        output = run_language_loop(user_input)
        print("\n🌀 Final Drift Output:")
        print(output)
        speak_text(output)  # <- This line speaks the final result aloud

