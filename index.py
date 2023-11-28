from flask import Flask, render_template
from ru_cptdb_scraper import scrapeByNum
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/bus/<int:bus_num>")
def bus_page(bus_num):
    bus_data = scrapeByNum(bus_num)
    return render_template("bus.html", **bus_data)

@app.route("/api/bus/<int:bus_num>")
def api_bus_page(bus_num):
    try:
        return {"type": "success", "data": scrapeByNum(bus_num)}
    except Exception as e:
        return {"type": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(debug=True)