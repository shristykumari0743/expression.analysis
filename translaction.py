import requests
import os
import wave

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("[INFO] Install pyaudio: pip install pyaudio")


class SarvamSpeechTranslator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai"

    # -------- SPEECH TO TEXT --------
    def transcribe(self, audio_path, language_code="unknown"):
        url = f"{self.base_url}/speech-to-text"
        headers = {"api-subscription-key": self.api_key}

        try:
            with open(audio_path, "rb") as audio_file:
                files = {
                    "file": (os.path.basename(audio_path), audio_file, "audio/wav")
                }

                data = {
                    "language_code": language_code
                }

                response = requests.post(url, headers=headers, files=files, data=data)

            print("STT Status Code:", response.status_code)

            if response.status_code == 200:
                result = response.json()
                return result.get("transcript", "")
            else:
                print("[ERROR STT]:", response.text)
                return None

        except Exception as e:
            print("STT Exception:", e)
            return None

    # -------- TRANSLATE --------
    def translate(self, text, target_language="en-IN", source_language="unknown"):
        url = f"{self.base_url}/translate"
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "input": text,
            "source_language_code": source_language,
            "target_language_code": target_language
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            print("Translate Status Code:", response.status_code)

            if response.status_code == 200:
                result = response.json()
                return result.get("translated_text", "")
            else:
                print("[ERROR TRANSLATE]:", response.text)
                return None

        except Exception as e:
            print("Translate Exception:", e)
            return None

    # -------- RECORD AUDIO --------
    def record_audio(self, duration=5):
        if not PYAUDIO_AVAILABLE:
            print("[ERROR] pyaudio not installed.")
            return None

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        filename = "temp.wav"

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        print(f"\n🎤 Speak now ({duration} seconds)...")
        frames = []

        for _ in range(int(RATE / CHUNK * duration)):
            frames.append(stream.read(CHUNK, exception_on_overflow=False))

        print("✅ Recording finished.")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

        return filename


def main():
    # ⚠️ Replace with NEW regenerated key
    api_key = "sk_km7at76s_mGW53BBV78WZCkvvprNKzOLk"

    app = SarvamSpeechTranslator(api_key)

    try:
        duration = int(input("Enter recording duration (seconds): ") or 5)
    except:
        duration = 5

    target_lang = input("Translate to (default: en-IN): ").strip() or "en-IN"

    audio_file = app.record_audio(duration)

    if not audio_file:
        return

    print("\n📝 Transcribing...")
    transcript = app.transcribe(audio_file, language_code="unknown")

    if not transcript:
        print("Transcription failed.")
        return

    print("\nOriginal Speech:")
    print(transcript)

    print("\n🌍 Translating...")
    translated = app.translate(transcript, target_lang, source_language="auto")

    if translated:
        print("\nTranslated Text:")
        print(translated)
    else:
        print("Translation failed.")

    if os.path.exists(audio_file):
        os.remove(audio_file)


if __name__ == "__main__":
    main()
