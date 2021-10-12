import cv2

def open_webcam(video_path: str):
    """Simple webcam program with opencv"""

    cap = cv2.VideoCapture(video_path)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            cv2.destroyAllWindows()
            break
