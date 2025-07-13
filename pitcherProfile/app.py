from flask import Flask, render_template, request, send_from_directory
from pitcher import Pitcher
import os

app = Flask(__name__)
CHART_DIR = "static/images"

@app.route("/", methods=["GET", "POST"])
def index():
    pitcher = Pitcher("Shohei", "Ohtani", '2025-03-20', '2025-09-30')
    pitcher.pitch_dist()
    chart_path = pitcher.chart_path["pitch_dist"]
    selected_count = None

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        count_filter = request.form.get("count_filter")

        pitcher = Pitcher(first_name, last_name, '2025-03-20', '2025-09-30')

        if count_filter != "All":
            pitcher.count_filter(count_filter)


        pitcher.pitch_dist(use_filter=True)
        chart_path = pitcher.chart_path["pitch_dist"]
        selected_count = pitcher.active_filter

    return render_template("index.html", chart_path=f"/{chart_path}", selected_count=selected_count)