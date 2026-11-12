from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import numpy as np

DATEI = "aufnahme.wav"

gespraechsverlauf = []
MAX_VERLAUF = 10

print("Lade Fauli...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Fauli bereit.")

while True:

    print("\nENTER = Aufnahme starten")
    print("ENTER erneut = Aufnahme beenden")
    print("STRG + C = Fauli beenden")

    input()

    print("\nAufnahme läuft...")

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

    print("Aufnahme gespeichert.")

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

    text_klein = text.lower()

    wakeword_erkannt = False

    wakeword_varianten = [
        "fauli",
        "fawli",
        "fauley",
        "fraule",
        "fauly",
        "faulye",
        "folly",
        "foli",
        "frauli"
    ]

    for wort in wakeword_varianten:
        if wort in text_klein:
            wakeword_erkannt = True
            break

    if not wakeword_erkannt:
        print("Wakeword nicht erkannt.")
        print("Fauli bleibt ruhig.")
        continue

    gespraechsverlauf.append({
        "role": "user",
        "content": text
    })

    if len(gespraechsverlauf) > MAX_VERLAUF:
        gespraechsverlauf = gespraechsverlauf[-MAX_VERLAUF:]

    nachrichten = [
        {
            "role": "system",
            "content": """
Du bist Fauli.

Du bist mein persönlicher Assistent.

Du sprichst mit Michael.

Merke dir Informationen aus dem laufenden Gespräch.

Wenn Michael etwas über sich erzählt,
darfst du dir das merken.

Antworte freundlich.

Antworte kurz.

Verwende keine Emojis.
"""
        }
    ]

    nachrichten.extend(gespraechsverlauf)

    print("Fauli denkt nach...")

    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
            "messages": nachrichten,
            "max_tokens": 100
        }
    )

    result = response.json()

    print("\nDEBUG:")
    print(result)

    message = result["choices"][0]["message"]

    antwort = message.get("content", "")

    if not antwort:
        antwort = "Ich habe momentan keine Antwort erhalten."

    gespraechsverlauf.append({
        "role": "assistant",
        "content": antwort
    })

    if len(gespraechsverlauf) > MAX_VERLAUF:
        gespraechsverlauf = gespraechsverlauf[-MAX_VERLAUF:]

    print("\nFauli:")
    print(antwort)