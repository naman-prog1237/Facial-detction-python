
# ========================================================================
# FACIAL DETECTION PROGRAM - SIMPLER VERSION (Haar Cascade)
# ========================================================================
# This is a simpler version using OpenCV Haar Cascade
# Less accurate but faster and easier to understand
# ========================================================================

import cv2
import numpy as np

# Step 1: Load the pre-trained Haar Cascade classifiers
# These are trained models for detecting faces and eyes
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

# Step 2: Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam!")
    exit()

print("Simpler Face Detection Program Started!")
print("Press 'q' to exit.")
print("=" * 50)

# Step 3: Main loop
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame!")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to grayscale (face detection works better on grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 4: Detect faces in the frame
    # scaleFactor: Image size reduction at each scale (1.1 = 10% reduction)
    # minNeighbors: How many neighbors each rectangle should have (higher = stricter)
    # minSize: Minimum face size to detect
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )

    # Step 5: For each detected face
    for (x, y, w, h) in faces:
        # Draw a green rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Region of Interest (ROI) - the area inside the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Step 6: Check if person is looking at screen
        # If eyes are detected and looking forward = looking at screen
        if len(eyes) >= 2:  # Both eyes detected = looking at screen
            status = "LOOKING AT SCREEN"
            color = (0, 255, 0)  # Green
            cv2.putText(frame, status, (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        else:
            status = "NOT LOOKING AT SCREEN"
            color = (0, 0, 255)  # Red
            cv2.putText(frame, status, (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

        # Draw blue rectangles around detected eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    # If no face detected
    if len(faces) == 0:
        cv2.putText(frame, "No face detected", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

    # Add instruction
    cv2.putText(frame, "Press 'q' to quit", (50, frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Step 7: Display the frame
    cv2.imshow("Simple Face Detection - Haar Cascade", frame)

    # Step 8: Wait for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Step 9: Clean up
cap.release()
cv2.destroyAllWindows()
print("Program closed!")
