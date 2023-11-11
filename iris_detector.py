import cv2 as cv
import numpy as np
import mediapipe as mp
from camera_handler import CameraHandler

class IrisDetector:
    def __init__(self, camera_handler):
        self.camera_handler = camera_handler

    def detect_iris(self):
        ret, frame = self.camera_handler.get_frame()
        if not ret:
            print("Failed to get frame from the camera")
        
        # Indices pour les iris gauche et droit
        LEFT_IRIS_INDICES = [474, 475, 476, 477]
        RIGHT_IRIS_INDICES = [469, 470, 471, 472]

        # Inversion et conversion de la frame pour le traitement
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]

        # Traitement avec FaceMesh
        with mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                    for p in results.multi_face_landmarks[0].landmark])

                l_cx, l_cy, l_radius = self._calculate_iris(mesh_points, LEFT_IRIS_INDICES)
                r_cx, r_cy, r_radius = self._calculate_iris(mesh_points, RIGHT_IRIS_INDICES)

                self._draw_iris(frame, l_cx, l_cy, l_radius)
                self._draw_iris(frame, r_cx, r_cy, r_radius)

                # Renvoyer les informations des iris
                return l_cx, l_cy, l_radius, r_cx, r_cy, r_radius

            # Si aucun iris n'est détecté, renvoyer des zéros
            return 0, 0, 0, 0, 0, 0


    def _calculate_iris(self, mesh_points, iris_indices):
        iris_points = mesh_points[iris_indices]
        center, radius = cv.minEnclosingCircle(iris_points)
        return int(center[0]), int(center[1]), int(radius)

    def _draw_iris(self, frame, cx, cy, radius):
        cv.circle(frame, (cx, cy), radius, (0, 255, 0), 2, cv.LINE_AA)

    def close(self):
        self.camera_handler.cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    camera_handler = CameraHandler()
    iris_detector = IrisDetector(camera_handler)
    iris_detector.detect_iris()
    iris_detector.close()