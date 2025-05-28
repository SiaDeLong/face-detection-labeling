import cv2

# Open the webcam
video_capture = cv2.VideoCapture(0)

# Optional: Set to HD resolution for better quality (if supported by your camera)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Show the live camera feed
    cv2.imshow('Smooth Camera Feed', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and close
video_capture.release()
cv2.destroyAllWindows()
