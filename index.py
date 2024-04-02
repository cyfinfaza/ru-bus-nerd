from flask import Flask, render_template
from ru_cptdb_scraper import scrapeByNum
from ru_transitstat_api import getLiveData
import json

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html", code=e.code, message=str(e)), e.code

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/bus/<int:bus_num>")
def bus_page(bus_num):
    try:
        bus_data = scrapeByNum(bus_num)
        bus_data['live'] = getLiveData(str(bus_num))
        bus_data['live_available'] = bus_data['live'] is not None
        return render_template("bus.html", **bus_data)
    except Exception as e:
        return render_template("error.html", code=404, message=str(e)), 404

@app.route("/api/bus/<int:bus_num>")
def api_bus_page(bus_num):
    try:
        return {"type": "success", "data": scrapeByNum(bus_num)}
    except Exception as e:
        return {"type": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(debug=True)