# Mood Tracker

A Python-based mood tracking system that uses facial emotion recognition to track your mood throughout the day. The system categorizes your mood into three categories: happy, neutral, and sad.

## Features

- Real-time facial emotion detection using your webcam
- Automatic mood logging with timestamps
- Mood history saved to CSV file
- Mood distribution visualization
- Simple and intuitive interface

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

## Usage

1. Run the mood tracker:
```bash
python mood_tracker.py
```

2. The program will open your webcam and start detecting your mood
3. Your current mood will be displayed on the screen
4. Press 'q' to quit the program
5. When you quit, the program will:
   - Save your mood history to 'mood_history.csv'
   - Generate a mood distribution plot as 'mood_distribution.png'

## Output Files

- `mood_history.csv`: Contains timestamped records of your detected moods
- `mood_distribution.png`: A bar chart showing the distribution of your moods

## Note

The system uses the FER (Facial Emotion Recognition) library which is built on top of OpenCV. It maps the detected emotions to three mood categories:
- Happy: happy, surprise
- Neutral: neutral
- Sad: sad, angry, disgust, fear 