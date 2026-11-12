from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import numpy as np
import json
import os

DATEI = "aufnahme.wav"
GEDAECHTNIS_DATEI = "gedaechtnis.json"

gespraechsverlauf = []
MAX_VERLAUF = 10

# =====================
# Gedächtnis laden
# =====================

if os.path.exists(GEDAECHTNIS_DATEI):
    with open(GEDAECHTNIS_DATEI, "r", encoding="utf-8") as f:
        gedaechtnis = json.load(f)
else:
    gedaechtnis = {
        "name": "",
        "freundin": "",
        "interessen": [],
        "erinnerungen": []
    }

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

    # =====================
    # Name merken
    # =====================

    if "ich bin michael" in text_klein:
        gedaechtnis["name"] = "Michael"

    if "mein name ist michael" in text_klein:
        geda