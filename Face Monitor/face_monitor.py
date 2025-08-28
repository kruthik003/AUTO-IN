import cv2
import dlib
import math

# Load face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to calculate angle between three points
def calculate_angle(pointA, pointB, pointC):
    # Calculate vectors
    vector1 = [pointA[0] - pointB[0], pointA[1] - pointB[1]]
    vector2 = [pointC[0] - pointB[0], pointC[1] - pointB[1]]

    # Calculate dot product and magnitude of vectors
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    # Check if magnitude is not zero to avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Default angle is 0 if magnitude is zero

    # Calculate angle in radians
    angle_radians = math.acos(min(max(dot_product / (magnitude1 * magnitude2), -1.0), 1.0))

    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees

# Function to check if face is looking at the monitor
def is_face_looking_at_monitor(face_landmarks, monitor_angle_threshold):
    # Define landmarks for left eye, right eye, and center of face
    left_eye = (face_landmarks.part(36).x, face_landmarks.part(36).y)
    right_eye = (face_landmarks.part(45).x, face_landmarks.part(45).y)
    face_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)

    # Calculate angle between line connecting eyes and line perpendicular to monitor
    eye_angle = calculate_angle(left_eye, right_eye, face_center)

    # Adjust angle based on monitor placement
    if eye_angle > 90:
        eye_angle = 180 - eye_angle

    # Check if angle is within threshold
    return eye_angle <= monitor_angle_threshold

# Capture video from webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 5)
# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = detector(gray)

    # Iterate over detected faces
    for face in faces:
        # Predict facial landmarks
        landmarks = predictor(gray, face)

        # Check if face is looking at monitor
        if is_face_looking_at_monitor(landmarks, monitor_angle_threshold=30):
            cv2.putText(frame, "Looking at Monitor", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Looking at Monitor", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Face Monitor", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
