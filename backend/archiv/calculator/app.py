#!/usr/bin/python
from flask import request, jsonify
from apiflask import APIFlask, Schema
from apiflask.fields import Float, String, Dict
from apiflask.validators import OneOf
from apiflask.schemas import EmptySchema
from requests import get as request_get
from json import loads as json_loads

class CalculatorIn(Schema):
    a = Float(required=True)
    b = Float(required=True)
    op = String(required=True, validate=OneOf(["add", "sub", "mul", "div"]))

class CalculatorOut(Schema):
    result = Float()

class BitcoinConverterIn(Schema):
    currency = String(required=True, validate=OneOf(["EUR", "GBP", "USD"]))
    amount = Float(required=True)

class BitcoinConverterOut(Schema):
    result = String()

# start the webserver
app = APIFlask(__name__)

# default route, return simple hello world
@app.route('/')
@app.input(EmptySchema)
def hello_world():
    return 'Hello ITCNE! Gruss von Marco'

# calculator route
@app.get('/calculator')
@app.input(CalculatorIn, location="query")
@app.output(CalculatorOut)
def calc(query_data):
    # Hole die Parameter a und b aus der Anfrage
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    op = request.args.get("op", type=str)
    # Prüfe, ob die Parameter gültig sind
    if a is None or b is None or op is None:
        return {"error": "Invalid parameters"}
    # Führe die Rechenoperation aus
    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        result = a / b
    else:
        return {"error": "Invalid operation"}
    # Gib das Ergebnis als JSON zurück
    return {"result": result}

# bitcoin converter
@app.get('/bitcoin-converter')
@app.input(BitcoinConverterIn, location="query")
@app.output(BitcoinConverterOut)
def bitcoin_converter(query_data):
    # get query params
    currency = str(query_data["currency"])
    amount = float(query_data["amount"])

    # get current conversion rate
    response = request_get("https://api.coindesk.com/v1/bpi/currentprice.json")
    if response.status_code == 200:
        response_as_json = response.json()
        conversion_rate = response_as_json["bpi"][currency]["rate_float"]
    
        # convert currency to bitcoin
        bitcoin_amount = amount / conversion_rate
        
        # return the amount in bitcoin
        return {"result": f"{bitcoin_amount} BTC"}

    else:
        return {"error": "Conversion Rate Lookup failed!"}
