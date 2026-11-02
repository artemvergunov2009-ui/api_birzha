from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_rates():
    response = requests.get(CBR_URL)
    if response.status_code != 200:
        return None
    return response.json()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/api/rates")
def all_rates():
    data = get_rates()
    if data is None:
        raise HTTPException(status_code=502, detail="Не удалось получить данные с ЦБ")

    result = []
    for code in data["Valute"]:
        v = data["Valute"][code]
        result.append({
            "code": v["CharCode"],
            "name": v["Name"],
            "nominal": v["Nominal"],
            "value": v["Value"],
            "previous": v["Previous"],
            "change": round(v["Value"] - v["Previous"], 4)
        })
    return {"date": data["Date"], "rates": result}


@app.get("/api/rates/{code}")
def one_rate(code: str):
    code = code.upper()
    data = get_rates()
    if data is None:
        raise HTTPException(status_code=502, detail="Не удалось получить данные с ЦБ")

    if code not in data["Valute"]:
        raise HTTPException(status_code=404, detail="Такой валюты нет")

    v = data["Valute"][code]
    return {
        "code": v["CharCode"],
        "name": v["Name"],
        "nominal": v["Nominal"],
        "value": v["Value"],
        "previous": v["Previous"]
    }
