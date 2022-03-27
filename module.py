import math
import cv2
import mediapipe as mp
import time
from time import strftime
import json

dictionary = {
    "head": {
        "total duration": {
            "Front": 0,
            "Right": 0,
            "Left": 0
        },
        "max uninterrupted sleep": {
            "Front": 0,
            "Right": 0,
            "Left": 0
        },
        "timestamp": {
            "Front": [],
            "Right": [],
            "Left": []
        }
    },
    "pose": {
        "timestamp": [],
        "id": [],
        "max uninterrupted duration": 0,
        "total uninterrupted duration": 0
    }
}


cap = cv2.VideoCapture(0)

cnt = 0
previous_list = []

side = "Front"
previous_time1 = previous_time= time.time()
count = 0


def core(index):
    x_pre, y_pre = previous_list[index]
    x_cur, y_cur = position_list[index]
    if abs(x_cur - x_pre) > 10:
        return 1
    return 0


def movement():
    global previous_time1
    for i in range(11, 33):
        if core(i):
            idle_time = (time.time() - previous_time1)
            if idle_time > 2.5:
                dictionary["pose"]["timestamp"].append(strftime("%H:%M:%S"))
                dictionary["pose"]["id"].append(i)
                print(strftime("%H:%M:%S"))
                print(f"{i} : {idle_time}")
                dictionary["pose"]["total uninterrupted duration"] += math.floor(idle_time)

                if idle_time > dictionary["pose"]["max uninterrupted duration"]:
                    dictionary["pose"]["max uninterrupted duration"] = math.floor(idle_time)

                previous_time1 = time.time()
                break


def face_position(set_):
    global side, previous_time, previous_time1
    idle_time = time.time() - previous_time

    dictionary["head"]["timestamp"][set_].append(strftime("%H:%M:%S"))
    dictionary["head"]["total duration"][set_] += math.floor(idle_time)
    if idle_time > dictionary["head"]["max uninterrupted sleep"][set_]:
        dictionary["head"]["max uninterrupted sleep"][set_] = math.floor(idle_time)

    print(strftime("%H:%M:%S"))
    print(f"{side} : {idle_time}")

    side = set_
    previous_time = previous_time1 = time.time()


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.2)

while cap.isOpened():

    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(image).pose_landmarks

    if results:
        position_list = []
        mpDraw.draw_landmarks(image, results, mpPose.POSE_CONNECTIONS)

        for id_, lm in enumerate(results.landmark):
            h, w, c = image.shape
            position_list.append((int(lm.x*w), int(lm.y*h)))

        if len(previous_list) > 0:
            movement()

        if position_list[0] < position_list[8] and side != "Left":
            face_position("Left")

        elif position_list[0] > position_list[7] and side != "Right":
            face_position("Right")

        elif position_list[7] > position_list[0] > position_list[8] and side != "Front":
            face_position("Front")

        previous_list = position_list

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    cv2.imshow("Frame", image)

    # time.sleep(3)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

print(dictionary)
cap.release()
cv2.destroyAllWindows()

