import sounddevice as sd
from scipy.io.wavfile import write

print("Sprich jetzt 5 Sekunden...")

aufnahme = sd.rec(
    int(5 * 44100),
    samplerate=44100,
    channels=1,
    dtype="int16"
)

sd.wait()

write("aufnahme.wav", 44100, aufnahme)

print("aufnahme.wav gespeichert")