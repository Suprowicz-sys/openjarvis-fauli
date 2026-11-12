datei = r"F:\Jarvis\voices\de_DE-thorsten-medium.onnx.json"

with open(datei, "rb") as f:
    daten = f.read(200)

print(daten)