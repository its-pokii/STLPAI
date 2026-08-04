# STLPAI

A vehicle detection, tracking, and counting tool built with [YOLO11](https://github.com/ultralytics/ultralytics) and OpenCV. It processes video input, detects and tracks vehicles across frames, counts how many cross a defined zone, and calculates metrics like duration — useful for traffic monitoring, road usage analysis, or similar computer vision tasks.

## How It Works

The core application logic lives in `src/trafficLogic.py`, backed by `src/trafficlib.py`, a small library of supporting functions (including duration calculation). Together they handle vehicle detection and tracking with the YOLO11-small model (`yolo11s.pt`), and derive metrics such as how many vehicles are in the waiting zone , the count is saved in a exel file `trafficData.xlsx` to be used in the decision later a long side the estimated discharge rate and other parameters, then the duration is send to the arduino prototype .

The root-level `count.py` and `detect.py` scripts are standalone test/prototyping scripts, used to validate the counting logic and detection pipeline in isolation before they were integrated into `src/`. They're useful references for understanding the core approach, but are not the entry point for actual use.

## Prototype

The repo also includes Arduino code for a physical prototype; where the duration is sent from the python code to the prototype and updated in the 7 segments 4 digits diplay. See `final_prototype/` for the sketch.

## Features

- Real-time vehicle detection and tracking with YOLO11
- Per-class and total vehicle counts based on zone/line crossing
- Duration calculation for tracked vehicles
- Live annotated video display with bounding boxes, track IDs, and running counts
- Console logging of counts and metrics as they update

## Project Structure

## Requirements

- Python 3.8+
- Key dependencies (see `requirements.txt` for the full pinned list): `ultralytics`, `opencv-python`, `torch`/`torchvision`, `numpy`, `pandas`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your input video in the `data/` directory (or update the path used in `src/trafficLogic.py`).
2. Run the main application:

   ```bash
   python src/trafficLogic.py
   ```
3. A window will open showing the video with live detections, tracking IDs, and counts overlaid. Press `q` to quit.
4. Final per-class and total counts (and any duration metrics) are printed to the console when the video ends or the window is closed.

To experiment with the underlying detection or counting logic in isolation, you can also run the standalone test scripts:

```bash
python detect.py   # test detection only
python count.py    # test counting logic only
```

## Notes

- Vehicle classes are filtered using COCO class IDs (e.g. car, motorcycle, bus, truck), configurable wherever `model.track()` is called.
- Zone/line positions used for counting are tuned to the sample footage and will likely need adjusting for other videos or camera angles.
