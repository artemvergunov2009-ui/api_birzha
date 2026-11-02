import requests

url = "http://127.0.0.1:8000/api/rates"

response = requests.get(url)
data = response.json()

print("Курсы валют на", data["date"])
for item in data["rates"]:
    print(item["code"], "-", item["value"], "руб. за", item["nominal"])

usd = requests.get("http://127.0.0.1:8000/api/rates/USD").json()
print()
print('Доллар', usd["value"])