from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import pyttsx3
import numpy as np

# =====================
# Einstellungen
# =====================

DATEI = "aufnahme.wav"

# =====================
# Sprachausgabe
# =====================

tts = pyttsx3.init()
tts.setProperty("rate", 170)

# =====================
# Whisper laden
# =====================

print("Lade Fauli...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("✅ Fauli bereit.")

# =====================
# Hauptschleife
# =====================

while True:

    print("\nENTER = Aufnahme starten")
    print("ENTER erneut = Aufnahme beenden")
    print("STRG+C = Fauli beenden")

    input()

    print("\n🎤 Aufnahme läuft...")

    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    stream = sd.InputStream(
        samplerate=44100,
        channels=1,
        dtype="int16",
        callback=callback
    )

    stream.start()

    input()

    stream.stop()
    stream.close()

    audio = np.concatenate(recording, axis=0)

    write(DATEI, 44100, audio)

    print("✅ Aufnahme gespeichert.")

    # =====================
    # Whisper
    # =====================

    segments, info = model.transcribe(
        DATEI,
        language="de"
    )

    text = ""

    for segment in segments:
        text += segment.text + " "

    text = text.strip()

    print("\nDu hast gesagt:")
    print(text)

    # =====================
    # Wakewords
    # =====================

    wakewords = [
        "hey fauli",
        "hallo fauli",
        "fauli",
        "was geht ab fauli"
    ]

    wakeword_erkannt = False

    for wort in wakewords:
        if wort in text.lower():
            wakeword_erkannt = True

    if not wakeword_erkannt:
        print("❌ Wakeword nicht erkannt.")
        continue

    # =====================
    # Qwen
    # =====================

    print("🧠 Fauli denkt nach...")

    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
            "messages": [
                {
                    "role": "system",
                    "content": """
Du bist Fauli.

Du bist mein persönlicher lokaler KI-Assistent.

Du sprichst mit Michael.

Dein Name ist Fauli.

Wenn jemand nach deinem Namen fragt,
antwortest du:

Ich bin Fauli.

Antworte freundlich, kurz und natürlich.

Verwende keine Emojis.
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "max_tokens": 100
        }
    )

    result = response.json()

    antwort = result["choices"][0]["message"]["content"]

    print("\n🤖 Fauli:")
    print(antwort)

    tts.say(antwort)
    tts.runAndWait()