import requests
import json

API_KEY = "AIzaSyBmMCmbSftjsXKBOIUpdsNfvuuNDzb-JFo"

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": "Give me 3 key facts about Tesla in 3 bullet points. Keep it short."
        }
    ]
}

print("⏳ Contacting AI... Please wait...")

try:
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    print(result)  # ← Add this line to see full response

    ai_reply = result["choices"][0]["message"]["content"]
    print("\n✅ AI Says:")
    print(ai_reply)

except Exception as e:
    print(f"❌ Something went wrong: {e}")