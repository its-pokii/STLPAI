
#librairies
import cv2
from ultralytics import YOLO
from collections import defaultdict

# Load the YOLO model
model = YOLO('yolo11s.pt')  # this is the small version

class_list = model.names 


# Open the video file
capture = cv2.VideoCapture('data/videos/video3.mp4')

height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
# print(f"Video height: {height}")
# print(f"Video width: {width}")

line_y_red_1 = 400  # upper Red line position
line_y_red_2 = 470  # lower Red line position

# Dictionary to store object counts by class
class_counts = defaultdict(int)
# Dictionary to keep track of object IDs that have crossed the line
crossed_ids = set()

while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    # Run YOLO tracking on the frame
    results = model.track(frame, persist=True, classes = [1,2,3,5,6,7]) 
    

    # Ensure results are not empty
    if results[0].boxes.data is not None:
        # Get the detected boxes, their class indices, and track IDs
        boxes = results[0].boxes.xyxy.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        class_indices = results[0].boxes.cls.int().cpu().tolist()
        confidences = results[0].boxes.conf.cpu()

        #line drawing
        cv2.line(frame, (0, line_y_red_1), (int(width), line_y_red_1), (0, 0, 255), 3)
        cv2.line(frame, (0, line_y_red_2), (int(width), line_y_red_2), (0, 0, 255), 3)


        # Loop through each detected object
        for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
            x1, y1, x2, y2 = map(int, box)
            # Calculate the center point
            cx = (x1 + x2) // 2 
            cy = (y1 + y2) // 2            

            class_name = class_list[class_idx]

            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            
            cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 


            # Check if the car is between the lines
            #those conditions are related to the video i'm using, they may need to adjust them for your other captures
            if cy > line_y_red_1 and cy < line_y_red_2 and track_id not in crossed_ids:
                # Mark the object as crossed
                crossed_ids.add(track_id)
                class_counts[class_name] += 1
                general_count = sum(class_counts.values())
                print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]}")

            if (cy < line_y_red_1 or cy > line_y_red_2) and track_id in crossed_ids:
                # If the car is outside the lines, remove it from count
                crossed_ids.remove(track_id)
                class_counts[class_name] -= 1
                general_count = sum(class_counts.values())
                print(f" general count: {general_count} | {class_name} count: {class_counts[class_name]}")

        # Display the counts on the frame
        y_offset = 30
        for class_name, count in class_counts.items():
            cv2.putText(frame, f"{class_name}: {count}", (50, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset += 30

    
    
    # Show the frame
    cv2.imshow("YOLO Object Tracking & Counting", frame)    
    
    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
capture.release()
cv2.destroyAllWindows()
            
print(f"Final counts: {dict(class_counts)}") 
print(f"Total count: {general_count}")          