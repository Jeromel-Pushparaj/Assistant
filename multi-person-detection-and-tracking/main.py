import cv2
import numpy as np
import time
import math

# Video source (0 for webcam, or replace with video file path)
videoSource = r"F:\Project LIGHT Your  Desktop assistant\multi-person-detection-and-tracking\maingate.mp4"  # Set to 0 for webcam
cap = cv2.VideoCapture(videoSource)

# Load YOLO model (update paths as needed)
net = cv2.dnn.readNet(r'F:\Project LIGHT Your  Desktop assistant\multi-person-detection-and-tracking\yolov3.cfg', r'F:\Project LIGHT Your  Desktop assistant\multi-person-detection-and-tracking\yolov3.weights.1')

# GPU/CUDA (uncomment if available)
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Globals
people = []
personId = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
enteredPeople = 0
exitedPeople = 0
doorThresh = 50
doorCoord = (670, 400)
appendThresh = 80

# Load class names
with open(r"F:\Project LIGHT Your  Desktop assistant\multi-person-detection-and-tracking\coco.names", "r") as f:
    classes = f.read().strip().split('\n')

# Person Class
class Person:
    def __init__(self, personId, location):
        self.id = personId
        self.curLocation = location
        self.trajectory = []
        self.flag = 0
        self.color = colors[personId % len(colors)]

    def addPointToTrajectory(self, location):
        self.trajectory.append(location)

# Calculate Distance
def calcDist(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# Plot Trajectories
def plotTrajectories(frame):
    for person in people:
        prev_point = None
        traj = person.trajectory[-5:] if len(person.trajectory) >= 5 else person.trajectory
        for i in traj:
            x, y = i
            frame = cv2.circle(frame, (x, y), 3, person.color, cv2.FILLED)
            if prev_point:
                frame = cv2.line(frame, prev_point, (x, y), person.color, 1)
            prev_point = (x, y)
    return frame

# Track and Update Persons
def trackerHandle(curCoords, frame):
    global enteredPeople, exitedPeople
    for person in people:
        if person.flag == 0:
            initialCoord, finalCoord = person.trajectory[0], person.trajectory[-1]
            if (calcDist(doorCoord, initialCoord) < 50 and calcDist(doorCoord, finalCoord) < 80):
                enteredPeople += 1
                person.flag = 1
            elif (calcDist(doorCoord, initialCoord) < 20 and calcDist(doorCoord, finalCoord) > 50):
                exitedPeople += 1
                person.flag = 1
    frame = plotTrajectories(frame)
    return frame

def createPerson(currentCoord):
    global personId
    person = Person(personId, currentCoord)
    people.append(person)
    personId += 1

# Main Loop
font = cv2.FONT_HERSHEY_PLAIN
cv2.namedWindow("Person Tracking", cv2.WINDOW_NORMAL)

while True:
    startTime = time.time()
    ret, frame = cap.read()
    frame = cv2.resize(frame, (800, 600))
    frame = cv2.circle(frame, doorCoord, 5, (255, 0, 0), -1)

    # Object Detection
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    class_ids, confidences, boxes = [], [], []
    curCoords = []

    # Process each detection
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only consider persons
            if confidence > 0.5 and classes[class_id] == 'person':
                center_x, center_y, w, h = (detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])).astype(int)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                curCoords.append([center_x, center_y])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
    for i in indices:
        x, y, w, h = boxes[i[0]]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, 'Person', (x, y - 10), font, 1, (0, 255, 0), 1)

    # Track and Update People
    frame = trackerHandle(curCoords, frame)

    # Display info
    fps = 1 / (time.time() - startTime)
    cv2.putText(frame, f"People Count: {len(people)}", (550, 30), font, 1.5, (0, 0, 255), 2)
    cv2.putText(frame, f"Entered Count: {enteredPeople}", (550, 60), font, 1.5, (0, 0, 255), 2)
    cv2.putText(frame, f"Exited Count: {exitedPeople}", (550, 90), font, 1.5, (0, 0, 255), 2)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), font, 1.5, (0, 0, 255), 2)

    cv2.imshow("Person Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
