import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class MoodTracker:
    def __init__(self):
        # Load face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.mood_history = []
        self.cap = None
        
    def start_camera(self):
        """Initialize the camera"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
            
    def stop_camera(self):
        """Release the camera"""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        
    def detect_face_features(self, face_roi):
        """Detect basic facial features to estimate mood"""
        # Convert to grayscale
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        # Simple feature detection
        # Smile detection (using edge detection)
        edges = cv2.Canny(gray, 100, 200)
        smile_ratio = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        
        # Eye detection (using brightness)
        eye_region = gray[gray.shape[0]//4:gray.shape[0]//2, :]
        eye_brightness = np.mean(eye_region)
        
        # Determine mood based on features
        if smile_ratio > 0.1 and eye_brightness > 100:
            return 'happy'
        elif smile_ratio < 0.05 and eye_brightness < 80:
            return 'sad'
        else:
            return 'neutral'
        
    def log_mood(self, mood):
        """Log the detected mood with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mood_history.append({
            'timestamp': timestamp,
            'mood': mood
        })
        
    def save_mood_history(self):
        """Save mood history to CSV file"""
        df = pd.DataFrame(self.mood_history)
        df.to_csv('mood_history.csv', index=False)
        
    def plot_mood_history(self):
        """Plot mood history"""
        if not self.mood_history:
            print("No mood history to plot")
            return
            
        df = pd.DataFrame(self.mood_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        plt.figure(figsize=(12, 6))
        mood_counts = df['mood'].value_counts()
        plt.bar(mood_counts.index, mood_counts.values)
        plt.title('Mood Distribution')
        plt.xlabel('Mood')
        plt.ylabel('Count')
        plt.savefig('mood_distribution.png')
        plt.close()
        
    def run(self):
        """Main loop for mood tracking"""
        try:
            self.start_camera()
            print("Press 'q' to quit")
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    # Draw rectangle around face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Get face region
                    face_roi = frame[y:y+h, x:x+w]
                    
                    # Detect mood
                    mood = self.detect_face_features(face_roi)
                    self.log_mood(mood)
                    
                    # Display mood on frame
                    cv2.putText(frame, f"Mood: {mood}", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Display the frame
                cv2.imshow('Mood Tracker', frame)
                
                # Break loop on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            self.stop_camera()
            self.save_mood_history()
            self.plot_mood_history()
            print("Mood history saved to 'mood_history.csv'")
            print("Mood distribution plot saved to 'mood_distribution.png'")

if __name__ == "__main__":
    tracker = MoodTracker()
    tracker.run() 