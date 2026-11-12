from faster_whisper import WhisperModel

print("Lade Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe("aufnahme.wav")

print("\nErkannt:")

for segment in segments:
    print(segment.text)