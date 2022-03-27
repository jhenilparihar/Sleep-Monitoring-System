import numpy as np
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
import matplotlib.pyplot as plt
import math
import cv2
import mediapipe as mp
import time
from time import strftime
import json

app = Flask(__name__)


@app.route('/')
def home():
    f = open('sample.json')

    data = json.load(f)
    f.close()

    f = len(data["head"]["timestamp"]["Front"])
    r = len(data["head"]["timestamp"]["Right"])
    l = len(data["head"]["timestamp"]["Left"])

    if f > r and l:
        side = "Front"
    elif l > r and f:
        side = "Left"
    else:
        side = "Right"

    return render_template("index.html",moves=f+r+l+len(data["pose"]["timestamp"]),
                           sleep=80,un=(data["pose"]["max uninterrupted duration"])/60,
                           side=side)


@app.route('/graph1')
def graph1():
    f = open('sample.json')

    data = json.load(f)
    f.close()
    hr = int(data["pose"]["timestamp"][0][0:2])
    dic = {
        hr: 0
    }

    for i in data["pose"]["timestamp"]:
        hour = int(i[0:2])
        if hr == hour:
            dic[hr] += 1
        else:
            hr = hour
            dic[hr] = 1

    k = dic.keys()
    v = dic.values()

    plt.plot(k, v)
    plt.xlabel("Time (Hours)")
    plt.ylabel("No. of Movements")
    plt.title("Disturbance Tracking")
    plt.show()

    return redirect("/")

@app.route('/graph2')
def graph2():
    f = open('sample.json')

    data = json.load(f)
    f.close()
    dic = {}

    for side in ["Front", "Left", "Right"]:
        dic[side] = len(data["head"]["timestamp"][side])

    print(dic)
    side = list(dic.keys())
    values = list(dic.values())

    # fig = plt.figure(figsize=(10, 5))

    plt.bar(side, values, color='maroon', width=0.4)

    plt.xlabel("Movements")
    plt.ylabel("Face Side")
    plt.title("Side Detection")
    plt.show()
    return redirect("/")



@app.route('/login')
def login():



    return redirect("/")


@app.route('/monitor')
def monitor():
    # start_time=request.form["start_time"]
    file = open(r'module.py', 'r').read()
    return exec(file)


if __name__ == "__main__":
    app.run(debug=True)
