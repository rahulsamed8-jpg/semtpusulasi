import requests

API_KEY = "AQ.Ab8RN6JYv4NGTmFA59aHiWlY4hrAtXR0pYIUG_SJsop0977gzQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print("List Models API Testi yapılıyor...")
try:
    response = requests.get(url)
    print("Status Code:", response.status_code)
    data = response.json()
    if 'models' in data:
        print("Available Models:")
        for model in data['models']:
            print(" -", model['name'])
    else:
        print("Response JSON:", data)
except Exception as e:
    print("HATA:", e)
