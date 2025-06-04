import requests

url = "http://127.0.0.1:8000/modelo_ML/clustering"  # Ajusta se precisar
payload = {"categorias": 2}

response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Resposta da API:", response.text)
