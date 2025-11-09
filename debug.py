# ========================================================================
# FACIAL DETECTION PROGRAM - DEBUGGING VERSION
# ========================================================================

import cv2
import mediapipe as mp
import numpy as np
import traceback

try:
    print("Step 1: Importing libraries...")
    
    # Initialize MediaPipe Face Mesh
    print("Step 2: Initializing MediaPipe...")
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    # Open webcam
    print("Step 3: Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Webcam not found!")
        exit()
    
    print("Step 4: Webcam opened successfully!")
    
    # Set window properties
    print("Step 5: Creating window...")
    cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Detection", 800, 600)
    
    print("Step 6: Starting main loop...")
    print("Program started! Press 'q' to exit.")
    print("=" * 50)
    
    frame_count = 0
    
    while True:
        print(f"\nFrame {frame_count}...", end=" ")
        
        ret, frame = cap.read()
        
        if not ret:
            print("ERROR: Cannot read frame!")
            break
        
        print("Read OK...", end=" ")
        
        # Flip frame
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        print("Processing...", end=" ")
        
        # Detect face
        results = face_mesh.process(rgb_frame)
        
        status_text = "No face detected"
        status_color = (0, 0, 255)
        
        if results.multi_face_landmarks:
            print("Face found...", end=" ")
            face_landmarks = results.multi_face_landmarks[0]
            
            # Get iris positions
            left_iris = face_landmarks.landmark[473]
            right_iris = face_landmarks.landmark[468]
            
            # Get eye corners
            left_eye_inner = face_landmarks.landmark[133]
            left_eye_outer = face_landmarks.landmark[263]
            right_eye_inner = face_landmarks.landmark[362]
            right_eye_outer = face_landmarks.landmark[33]
            
            # Calculate iris ratios
            left_iris_x_ratio = (left_iris.x - left_eye_outer.x) / (left_eye_inner.x - left_eye_outer.x)
            right_iris_x_ratio = (right_iris.x - right_eye_outer.x) / (right_eye_inner.x - right_eye_outer.x)
            iris_x_ratio = (left_iris_x_ratio + right_iris_x_ratio) / 2
            
            # Determine gaze
            tolerance = 0.15
            looking_center = 0.5
            
            if (looking_center - tolerance) <= iris_x_ratio <= (looking_center + tolerance):
                status_text = "LOOKING AT SCREEN"
                status_color = (0, 255, 0)
            elif iris_x_ratio < 0.3:
                status_text = "Looking LEFT"
                status_color = (255, 100, 0)
            elif iris_x_ratio > 0.7:
                status_text = "Looking RIGHT"
                status_color = (255, 100, 0)
            else:
                status_text = "Looking AWAY"
                status_color = (0, 165, 255)
            
            # Draw face mesh
            try:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )
                print("Drawing OK...", end=" ")
            except Exception as e:
                print(f"Drawing error: {e}")
        
        # Add text
        cv2.rectangle(frame, (30, 30), (500, 80), (0, 0, 0), -1)
        cv2.putText(frame, status_text, (50, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, status_color, 3)
        
        # Show instruction
        cv2.putText(frame, "Press 'q' to quit", (30, h - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display
        print("Displaying...", end=" ")
        cv2.imshow("Face Detection", frame)
        print("OK")
        
        # Check for 'q' key
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("\nProgram closed by user!")
            break
        
        frame_count += 1
        
except Exception as e:
    print("\n" + "=" * 50)
    print("ERROR OCCURRED!")
    print("=" * 50)
    print(f"Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    print("=" * 50)

finally:
    print("\nCleaning up...")
    cap.release()
    cv2.destroyAllWindows()
    print("Done!")
