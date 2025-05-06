# Stress Level Detector

This is a Python-based stress level detector that uses computer vision to analyze facial expressions and physiological signals to estimate stress levels. The system uses:
- Face detection and facial landmark tracking
- Eye blink rate analysis
- Heart rate estimation through subtle color changes
- Stress level calculation based on these metrics

## Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository or download the files
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Download the facial landmark predictor file:
   - Download the file from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract the .dat file and place it in the same directory as the script

## Usage

1. Run the script:
```bash
python stress_detector.py
```

2. The program will open your webcam and start analyzing your stress levels
3. The following information will be displayed on screen:
   - Stress Level (0-100%)
   - Blink Rate (blinks per minute)
   - Heart Rate (beats per minute)
4. Press 'q' to quit the program

## How it Works

The stress level is calculated based on:
- Eye blink rate (normal range: 15-20 blinks per minute)
- Heart rate (normal range: 60-100 BPM)

The system uses dlib's facial landmark detector to track 68 points on your face, which helps in:
- Detecting blinks by measuring the eye aspect ratio
- Estimating heart rate by analyzing subtle color changes in the forehead region

## Notes

- The heart rate estimation is approximate and may not be as accurate as medical devices
- For best results, ensure good lighting and minimal movement
- The system works best when your face is clearly visible to the camera 