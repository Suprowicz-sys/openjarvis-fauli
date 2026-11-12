import requests

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "qwen3-4b-thinking-2507.Q4_K_M.gguf",
        "messages": [
            {
                "role": "user",
                "content": "Sage nur Hallo Michael"
            }
        ]
    }
)

print("Status:", response.status_code)
print()
print(response.text)