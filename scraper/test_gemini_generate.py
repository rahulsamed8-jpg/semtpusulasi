import requests

API_KEY = "AIzaSyAFx28L5Vf6lRS9NyTm3a9yJbh6bfcvU08"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

payload = {
    "contents": [{"parts": [{"text": "Bana sadece 'Merhaba, fatura sorunu çözülmüş!' yaz."}]}]
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("BAŞARILI:", response.json()['candidates'][0]['content']['parts'][0]['text'])
    else:
        print("HATA:", response.status_code, response.json())
except Exception as e:
    print("İSTİSNA:", e)
