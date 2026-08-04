
#librairies
import cv2
from ultralytics import YOLO
from collections import defaultdict
import trafficlib as tl

# Load the YOLO model
model = YOLO('yolo11s.pt')  # this is the small version '11small'

class_list = model.names   


# Open the video file
capture = cv2.VideoCapture('data/videos/video5.mp4')
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
# print(f"Video height: {height}")
# print(f"Video width: {width}")

#waiting zone position points:
SquareX2 = 180 #left Vertical line 
SquareX1 = 450 #right Vertical line
SquareY1 = 350  #upper Horizontal line
SquareY2 = 500  #lower Horizontal line

LineY = 520  # crossing line



# Dictionary to store object counts by class
class_counts = defaultdict(int)
total_crossed = defaultdict(int)
# Dictionary to keep track of object IDs that have crossed the line
waiting_zone_ids = set()
crossed_ids = set()

while capture.isOpened():
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
        cv2.line(frame, (100, LineY), (500, LineY), (0, 255, 0), 3)  # crossing line


        # Loop through each detected object
        for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
            x1, y1, x2, y2 = map(int, box)
            # Calculate the center point
            cx = (x1 + x2) // 2 
            cy = (y1 + y2) // 2 
                       

            class_name = class_list[class_idx]

            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            
            cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 

            carPosition = (cx, cy)
            check_zone = tl.check_car_zoneBox(carPosition, SquareY1, SquareY2, SquareX1, SquareX2)
            line_crossed = tl.lineCrossedDown(carPosition, LineY)

            if check_zone and track_id not in waiting_zone_ids:
                # Mark the object as crossed
                waiting_zone_ids.add(track_id)
                class_counts[class_name] += 1
                general_count = sum(class_counts.values())
                print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]} ")

            if not check_zone and track_id in waiting_zone_ids:
                # If the car is outside the box, remove it from count
                waiting_zone_ids.remove(track_id)
                class_counts[class_name] -= 1
                if class_counts[class_name] < 0:
                    class_counts[class_name] = 0  # Ensure count doesn't go negative
                general_count = sum(class_counts.values())
                print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]} ")
            if line_crossed and track_id not in crossed_ids:
                crossed_ids.add(track_id)
                total_crossed[class_name] += 1
                total_crossed_count = sum(total_crossed.values())
                print(f" Total crossed: {total_crossed_count}")
         

        # Display the counts on the frame
        y_offset = 30
        for class_name, count in class_counts.items():
            cv2.putText(frame, f"{class_name}: {count}", (50, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset += 30

    
    
    # Show the frame
    cv2.imshow("YOLO Object Tracking & Counting", frame)    
    
    # Exit loop if 'q' key is pressed
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# Release resources
capture.release()
cv2.destroyAllWindows()
            
print(f"Final counts: {dict(class_counts)}") 
print(f"Total count: {dict(total_crossed)}")  
print(f"Total crossed: {sum(total_crossed.values())}")          