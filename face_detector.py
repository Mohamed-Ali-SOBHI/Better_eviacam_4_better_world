import cv2

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = self.get_first_available_camera()

    def get_first_available_camera(self):
        for i in range(10):  # Essayez les indices de 0 à 9
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:  # Vérifie si la caméra est en mesure de capturer une image
                    print(f"Caméra trouvée à l'indice {i}")
                    return cap
                else:
                    cap.release()  # Libère la ressource si elle ne peut pas capturer d'image
        raise Exception("Aucune caméra disponible")

    def detect_face(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            confidence = 0
            for (x, y, w, h) in faces:
                return x, y, w, h, confidence
        return 0, 0, 0, 0, 0  # retourne des valeurs par défaut si aucune détection

    def draw_face_rectangle(self, frame, x, y, w, h):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

