import cv2
import sys

# 1. Robust Import Handling
try:
    from fer import FER
except (ImportError, ModuleNotFoundError):
    try:
        from fer.fer import FER
    except ImportError:
        print("Error: FER library is still not accessible. Please run: pip install fer")
        sys.exit()

# 2. Map FER's 7 basic emotions to your specific 5 categories
def map_emotion(fer_emotion):
    mapping = {
        "angry": "angry",
        "disgust": "stress",
        "fear": "stress",
        "happy": "laugh",
        "sad": "sad",
        "surprise": "smile",
        "neutral": "stress"
    }
    return mapping.get(fer_emotion, "stress")

# 3. Initialize the FER detector
# Tip: Set mtcnn=False for much faster performance (OpenCV Haar Cascade)
# Set mtcnn=True for better accuracy but slower frame rates
detector = FER(mtcnn=False)

# 4. Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

print("Starting Facial Recognition... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # 5. Detect faces and emotions
    # This returns a list of dictionaries for each face found
    results = detector.detect_emotions(frame)

    for face in results:
        # Extract bounding box coordinates
        (x, y, w, h) = face["box"]
        
        # Get the emotion with the highest confidence score
        emotions = face["emotions"]
        top_emotion = max(emotions, key=emotions.get)
        score = emotions[top_emotion]
        
        # Apply your custom mapping
        expression = map_emotion(top_emotion)

        # 6. Visual Feedback
        # Draw the rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Create the label string
        label = f"{expression} ({score:.2f})"
        
        # Draw background for text to make it readable
        cv2.rectangle(frame, (x, y - 35), (x + w, y), (0, 255, 0), -1)
        cv2.putText(frame, label, (x + 5, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # 7. Display the result
    cv2.imshow("Gesture Project: Facial Expressions", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 8. Cleanup
cap.release()
cv2.destroyAllWindows()