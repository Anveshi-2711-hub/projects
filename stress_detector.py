import cv2
import numpy as np
from scipy.signal import find_peaks
import time

class StressDetector:
    def __init__(self):
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Initialize variables for stress detection
        self.blink_count = 0
        self.last_blink_time = time.time()
        self.blink_rate = 0
        self.heart_rate = 0
        self.stress_level = 0
        
        # Buffer for heart rate calculation
        self.heart_rate_buffer = []
        self.last_heart_rate_time = time.time()
        
        # Previous eye state
        self.prev_eyes_count = 2
        
    def detect_blinks(self, frame, face):
        x, y, w, h = face
        roi_gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(roi_gray)
        
        # Count visible eyes
        current_eyes_count = len(eyes)
        
        # Detect blink when eyes disappear and reappear
        if current_eyes_count < self.prev_eyes_count:
            current_time = time.time()
            if current_time - self.last_blink_time > 0.3:  # Minimum time between blinks
                self.blink_count += 1
                self.last_blink_time = current_time
        
        self.prev_eyes_count = current_eyes_count
        
        # Calculate blink rate (blinks per minute)
        if time.time() - self.last_blink_time > 10:  # Update every 10 seconds
            self.blink_rate = self.blink_count * 6  # Convert to blinks per minute
            self.blink_count = 0
            self.last_blink_time = time.time()
        
        # Draw rectangles around eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame[y:y+h, x:x+w], (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    def estimate_heart_rate(self, frame, face):
        x, y, w, h = face
        forehead_roi = frame[y:y+h//3, x:x+w]
        
        if forehead_roi.size > 0:
            # Convert to grayscale
            gray = cv2.cvtColor(forehead_roi, cv2.COLOR_BGR2GRAY)
            
            # Calculate average intensity
            avg_intensity = np.mean(gray)
            self.heart_rate_buffer.append(avg_intensity)
            
            # Keep buffer size manageable
            if len(self.heart_rate_buffer) > 100:
                self.heart_rate_buffer.pop(0)
            
            # Calculate heart rate every 10 seconds
            if time.time() - self.last_heart_rate_time > 10:
                if len(self.heart_rate_buffer) > 30:
                    # Find peaks in the signal
                    peaks, _ = find_peaks(self.heart_rate_buffer, distance=10)
                    if len(peaks) > 0:
                        # Calculate heart rate (beats per minute)
                        self.heart_rate = len(peaks) * 6  # Convert to BPM
                self.last_heart_rate_time = time.time()
                self.heart_rate_buffer = []

    def calculate_stress_level(self):
        # Simple stress level calculation based on blink rate and heart rate
        # Normal ranges: Blink rate: 15-20 per minute, Heart rate: 60-100 BPM
        blink_factor = max(0, min(1, (self.blink_rate - 15) / 5))
        heart_factor = max(0, min(1, (self.heart_rate - 60) / 40))
        
        self.stress_level = int((blink_factor + heart_factor) * 50)  # Scale to 0-100
        return self.stress_level

    def process_frame(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for face in faces:
            # Get face coordinates
            (x, y, w, h) = face
            
            # Detect blinks
            self.detect_blinks(frame, face)
            
            # Estimate heart rate
            self.estimate_heart_rate(frame, face)
            
            # Calculate stress level
            stress_level = self.calculate_stress_level()
            
            # Draw stress level on frame
            cv2.putText(frame, f"Stress Level: {stress_level}%", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Blink Rate: {self.blink_rate}/min", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Heart Rate: {self.heart_rate} BPM", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Draw face rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        return frame

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    stress_detector = StressDetector()
    
    print("Starting stress level detection...")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        processed_frame = stress_detector.process_frame(frame)
        
        # Display frame
        cv2.imshow('Stress Level Detector', processed_frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 