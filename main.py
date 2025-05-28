import cv2
import face_recognition
import threading
import time

AUTO_LABELLING = True

# Globals for sharing data between threads
frame = None
lock = threading.Lock()
running = True
tracker = None
tracking_name = None
last_success_time = None

# Load known faces (can be empty initially)
known_face_encodings = []
known_face_names = []

def face_detection_loop():
    global frame, running
    global tracker, tracking_name
    
    while running:
        if frame is not None and tracker is None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

            # Detect faces in the background
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            detected_faces = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                
                if known_face_encodings:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = face_distances.argmin()
                    if face_distances[best_match_index] < 0.45:  # Try tightening this from 0.6 to 0.45
                        name = known_face_names[best_match_index]

                # Scale back the coordinates
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Expand the rectangle slightly (e.g., by 10 pixels on each side)
                padding = 10
                top = max(0, top - padding)
                right += padding
                bottom += padding
                left = max(0, left - padding)

                detected_faces.append(((top, right, bottom, left, name)))
                
            if detected_faces:
                (top, right, bottom, left, name) = detected_faces[0]

                with lock:
                    bbox = (left, top, right - left, bottom - top)
                    tracker = cv2.TrackerKCF.create()
                    tracker.init(frame, bbox)
                    
                    if AUTO_LABELLING and name == "Unknown":
                        name = "Person " + str(len(known_face_encodings)+1)
                        known_face_encodings.append(face_encodings[0])
                        known_face_names.append(name)
                    
                    tracking_name = name

# Start webcam
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Start the background thread
thread = threading.Thread(target=face_detection_loop, daemon=True)
thread.start()

while True:
    ret, frame_raw = video_capture.read()
    if not ret:
        break

    frame = frame_raw.copy()
    
    with lock:
        frame_for_tracking = frame.copy() if frame is not None else None
    
    # Update tracker if active
    if tracker is not None and frame_for_tracking is not None:
        success, box = tracker.update(frame_for_tracking)

        if success:
            last_success_time = time.time() 
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y + h - 20), (x + w, y + h), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, tracking_name, (x + 2, y + h - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        else:
            if last_success_time and time.time() - last_success_time > 1:
                tracker = None
                tracking_name = None
                last_success_time = None 

    cv2.imshow('Async Face Detection', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False
        break
    elif key == ord('n') and tracker is not None:
        # Get the tracked box
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            face_image = frame[y:y+h, x:x+w]
            rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_face)

            if encodings:
                name = input("Enter name for the new face: ")
                known_face_encodings.append(encodings[0])
                known_face_names.append(name)
                tracking_name = name
                print(f"Added {name} to known faces.")
            else:
                print("Face encoding failed. Try again.")

video_capture.release()
cv2.destroyAllWindows()
