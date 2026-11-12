from faster_whisper import WhisperModel
import requests

print("Lade Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Transkribiere Aufnahme...")

segments, info = model.transcribe(
    "aufnahme.wav",
    language="de"
)

text = ""

for segment in segments:
    text += segment.text + " "

text = text.strip()

print("\nDu hast gesagt:")
print(text)

print("\nFrage Qwen3...")

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
        "messages": [
            {
                "role": "system",
                "content": "Du bist Jarvis. Antworte kurz und direkt auf Deutsch. Gib keine Gedankengänge aus."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
)

result = response.json()

print("\nDEBUG:")
print(result)

print("\nJarvis:")

message = result["choices"][0]["message"]

if message.get("content"):
    print(message["content"])
else:
    print("Keine Antwort erhalten.")

if message.get("reasoning_content"):
    print("\n--- Thinking wurde trotzdem ausgegeben ---")
    print(message["reasoning_content"])