import cv2
from ultralytics import YOLO
from collections import defaultdict
import trafficlib as tl
import pandas as pd
import time
import serial
import threading



# Arduino Setup ========================================================================
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
time.sleep(2)  # wait for Arduino reset

def wait_for_ready():
    while True:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if line == "READY":
            break

def send_and_wait(command):
    """Send a command to Arduino and block until it replies DONE."""
    arduino.write(f"{command}\n".encode('utf-8'))
    print(f"Sent: {command}")
    while True:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print("Arduino:", line)
        if line == "DONE":
            break

wait_for_ready()




redlight_duration=10

#configuration =========================================================================

file_path = "src\\trafficData.xlsx" 
df = pd.read_excel(file_path)

model = YOLO('yolo11s.pt')  # this is the small version 'yolo 11 small'

class_list = model.names   

# Open the video file
capture = cv2.VideoCapture('data/videos/video5.mp4')

#waiting zone position points:
SquareX2 = 180 #left Vertical line 
SquareX1 = 450 #right Vertical line
SquareY1 = 350  #upper Horizontal line
SquareY2 = 500  #lower Horizontal line

LineY = 520  # crossing line




def greenlight(duration_seconds):
    total_crossed_count = 0
    total_crossed = defaultdict(int)
    crossed_ids = set()
    capture = cv2.VideoCapture('data/videos/video5.mp4')

    arduino_thread = threading.Thread(target=send_and_wait, args=(f"G{int(duration_seconds)}",))
    arduino_thread.start()
    start_time = time.time()

    while capture.isOpened():
        elapsed = time.time() - start_time
        if elapsed >= duration_seconds:
            print(f"Time limit of {duration_seconds}s reached.")
            break

        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
        # Run YOLO tracking on the frame
        results = model.track(frame, persist=True, classes = [1,2,3,5,6,7]) 

        # Ensure results are not empty
        if results[0].boxes.data is not None and results[0].boxes.id is not None:
            # Get the detected boxes, their class indices, and track IDs
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_indices = results[0].boxes.cls.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu()

            cv2.line(frame, (100, LineY), (500, LineY), (0, 255, 0), 3)  # crossing line

            for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
                x1, y1, x2, y2 = map(int, box)
                # Calculate the center point
                cx = (x1 + x2) // 2 
                cy = (y1 + y2) // 2 

                carPosition = (cx, cy)
                class_name = class_list[class_idx]

                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                line_crossed = tl.lineCrossedDown(carPosition, LineY)

                if line_crossed and track_id not in crossed_ids:
                    total_crossed[class_name] += 1
                    crossed_ids.add(track_id)
                    total_crossed_count = sum(total_crossed.values())
                    print(f" Total crossed: {total_crossed_count}")
        # Show the frame
        cv2.imshow("YOLO Object Tracking & Counting", frame)    
    
        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    capture.release()
    cv2.destroyAllWindows()
    arduino_thread.join()

    return total_crossed_count


def redlight(redlight_duration):
    general_count = 0
    class_counts = defaultdict(int)
    waiting_zone_ids = set()
    capture = cv2.VideoCapture('data/videos/video5.mp4')
    start_time = time.time()

    arduino_thread = threading.Thread(target=send_and_wait, args=(f"R{int(redlight_duration)}",))
    arduino_thread.start()
    

    while capture.isOpened():
        elapsed = time.time() - start_time
        if elapsed >= redlight_duration:
            print(f"Time limit of {redlight_duration}s reached.")
            break
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
        # Run YOLO tracking on the frame
        results = model.track(frame, persist=True, classes = [1,2,3,5,6,7]) 

        # Ensure results are not empty
        if results[0].boxes.data is not None and results[0].boxes.id is not None:
            # Get the detected boxes, their class indices, and track IDs
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_indices = results[0].boxes.cls.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu()

            cv2.rectangle(frame, (SquareX1, SquareY1), (SquareX2, SquareY2), (0, 0, 255), 3) #waiting zone

            for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
                x1, y1, x2, y2 = map(int, box)
                # Calculate the center point
                cx = (x1 + x2) // 2 
                cy = (y1 + y2) // 2 

                carPosition = (cx, cy)
                class_name = class_list[class_idx]

                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                check_zone = tl.check_car_zoneBox(carPosition, SquareY1, SquareY2, SquareX1, SquareX2)

                if check_zone and track_id not in waiting_zone_ids:
                    # Mark the object as crossed
                    waiting_zone_ids.add(track_id)
                    class_counts[class_name] += 1
                    general_count = sum(class_counts.values())
                    print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]} ")
                    print(f"car number {track_id} is added")

                if not check_zone and track_id in waiting_zone_ids:
                    # If the car is outside the box, remove it from count
                    print(f"car number {track_id} is removed")
                    class_counts[class_name] -= 1
                    waiting_zone_ids.remove(track_id)
                    
                    
                    if class_counts[class_name] < 0:
                        class_counts[class_name] = 0  # Ensure count doesn't go negative
                general_count = sum(class_counts.values())
                print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]} ")

                # Display the counts on the frame
                y_offset = 30
                for class_name, count in class_counts.items():
                    cv2.putText(frame, f"{class_name}: {count}", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    y_offset += 30
        # Show the frame
        cv2.imshow("YOLO Object Tracking & Counting", frame)    
    
        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    capture.release()
    cv2.destroyAllWindows()
    return general_count






queue_length = redlight(redlight_duration)  # Measure the queue length during red light
previous_green = df["Green Duration"].iloc[-1]
vehicle_crossed = df["Vehicles Crossed"].iloc[-1]
previous_estimated_discharge_rate = df["Estimated Discharge Rate"].iloc[-1]
measured_discharge_rate = vehicle_crossed / max(previous_green, 1)




green_duration, estimated_discharge_rate = tl.calculate_duration(queue_length=queue_length, previous_green=previous_green, vehicle_crossed=vehicle_crossed, previous_estimated_discharge_rate=previous_estimated_discharge_rate)

vehicles_crossed_new = greenlight(green_duration)
real_discharge_rate = vehicles_crossed_new / max(green_duration, 1)

next_number = df["number"].iloc[-1] + 1 if len(df) > 0 else 1

new_row = pd.DataFrame({
    "number": [next_number],
    "Queue": [queue_length],
    "Estimated Discharge Rate": [estimated_discharge_rate],
    "Real Discharge Rate": [real_discharge_rate],
    "Vehicles Crossed": [vehicles_crossed_new],
    "Green Duration": [green_duration],
})

df = pd.concat([df, new_row], ignore_index=True)


df.to_excel(file_path, index=False)