import numpy as np
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
import matplotlib.pyplot as plt
import json

app = Flask(__name__)


@app.route('/')
def home():
    f = open('log.json')

    data = json.load(f)
    f.close()

    f = len(data["head"]["timestamp"]["Front"])
    r = len(data["head"]["timestamp"]["Right"])
    l = len(data["head"]["timestamp"]["Left"])

    f_ = data["head"]["total duration"]["Front"]
    r_ = data["head"]["total duration"]["Right"]
    l_ = data["head"]["total duration"]["Left"]

    if f_ > r_ and l_:
        side = "Front"
    elif l_ > r_ and f_:
        side = "Left"
    else:
        side = "Right"

    return render_template("index.html", moves=f+r+l+len(data["pose"]["timestamp"]),
                           sleep=round(data["head"]["total duration"][side] / 60, 2),
                           un=round((data["pose"]["max uninterrupted duration"])/60, 2),
                           side=side)


@app.route('/graph1')
def graph1():
    f = open('log.json')

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
    f = open('log.json')

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


@app.route('/monitor')
def monitor():
    # start_time=request.form["start_time"]
    Data = [[5, 6, 8], [10, 11, 14], [12, 10, 15]]

    X = np.arange(3)
    plt.plot(X, Data[0], color='b', label='Toy 1')
    plt.plot(X, Data[1], color='g', label='Toy 2')
    plt.plot(X, Data[2], color='r', label='Toy 3')
    plt.legend(loc='upper left')
    plt.title("Previous Data")
    plt.xlabel("Movement")
    plt.ylabel("Time")
    plt.show()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
