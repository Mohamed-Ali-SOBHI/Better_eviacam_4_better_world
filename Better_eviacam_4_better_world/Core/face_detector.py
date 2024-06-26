import cv2
import mediapipe as mp
from Better_eviacam_4_better_world.Core.camera_handler import *

class FaceDetector:
    def __init__(self, camera_handler, min_detection_confidence=0.5):
        self.camera_handler = camera_handler
        self.min_detection_confidence = min_detection_confidence
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence)

    def detect_face(self):
        ret, frame = self.camera_handler.get_frame()
        if not ret:
            print("Failed to get frame from the camera")
            return 0, 0, 0, 0, 0.0  # Return zeros if no frame is captured
        
        # Convert the BGR image to RGB before processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)

        if results.detections:
            for detection in results.detections:
                # Get the bounding box and confidence of the first face detected
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape  # Image height, width
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                             int(bboxC.width * iw), int(bboxC.height * ih)
                confidence = detection.score[0]
                # Return the bounding box and confidence
                return x, y, w, h, confidence
        # If no faces are detected, return zeros
        return 0, 0, 0, 0, 0.0

    def draw_face_rectangle(self, image, x, y, w, h):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def close(self):
        self.face_detection.close()
        self.camera_handler.cap.release()
