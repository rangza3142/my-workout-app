from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data/records.json"

# 파일이 없다면 빈 데이터 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# 오늘 날짜
def today_str():
    return datetime.now().strftime("%Y-%m-%d")

# 기록 불러오기
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# 기록 저장하기
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    data = load_data()
    today = today_str()
    today_data = data.get(today, {})
    return render_template("index.html", data=today_data)

@app.route("/add", methods=["POST"])
def add():
    exercise = request.form["exercise"]
    data = load_data()
    today = today_str()

    if today not in data:
        data[today] = {}
    if exercise not in data[today]:
        data[today][exercise] = 0
    data[today][exercise] += 1

    save_data(data)
    return redirect("/")

@app.route("/reset", methods=["POST"])
def reset():
    data = load_data()
    today = today_str()
    data[today] = {}
    save_data(data)
    return redirect("/")

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    new_ex = request.form["new_exercise"].strip()
    if new_ex:
        data = load_data()
        today = today_str()
        if today not in data:
            data[today] = {}
        if new_ex not in data[today]:
            data[today][new_ex] = 0
        save_data(data)
    return redirect("/")

@app.route("/calendar")
def calendar():
    data = load_data()
    return render_template("calendar.html", records=data)

if __name__ == "__main__":
    app.run(debug=True)