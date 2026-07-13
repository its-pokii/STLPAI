#Libraries
import cv2
from ultralytics import YOLO

#load the camera, 0 is the default camera
# capture = cv2.VideoCapture(0)

#if i want to load a video instead of the camera, i can use the following line
capture = cv2.VideoCapture("data/videos/video3.mp4")

#=====size====
# get the width and height of the video
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

#set the width and height of the camera
# capture.set(3,640)
# capture.set(4,480)



fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(width), int(height)))


#load the model
model = YOLO("yolo11s.pt")


#render the camera and detect objects in real time until the user presses 'q' to quit
while True :
    ret,frame = capture.read()
    if not ret:
        print("End of video or Error.")
        break
    results = model.track(frame, persist = True)
    for r in results:
        frame = r.plot()
        # out.write(frame)
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

#At the end of the loop, we release the camera and destroy all windows    
capture.release()
out.release()
cv2.destroyAllWindows()


