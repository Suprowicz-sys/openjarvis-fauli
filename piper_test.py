datei = r"F:\Jarvis\voices\de_DE-thorsten-medium.onnx.json"

with open(datei, encoding="utf-8") as f:
    text = f.read()

print("UTF8 OK")
print("Zeichen:", len(text))