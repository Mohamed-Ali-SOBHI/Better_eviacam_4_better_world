import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import threading
import cv2
from face_detector import FaceDetector
from iris_detector import IrisDetector
from camera_handler import CameraHandler

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("MVP eViacam")
        
        self.label = ttk.Label(self.window, text="Cliquez pour activer")
        self.label.grid(row=0, column=0)
        
        self.button = ttk.Button(self.window, text="Activer", command=self.start_detection)
        self.button.grid(row=1, column=0)
        
        self.canvas = Canvas(self.window, width=640, height=480)
        self.canvas.grid(row=2, column=0)
        
        self.confidence_label = ttk.Label(self.window, text="Confiance: ")
        self.confidence_label.grid(row=3, column=0)

        # Initialisation des détecteurs
        self.camera_handler = CameraHandler()
        self.face_detector = FaceDetector(self.camera_handler, min_detection_confidence=0.5)
        self.iris_detector = IrisDetector(self.camera_handler)  # Assurez-vous que ce fichier est dans le même répertoire

        # Mode de détection initial
        self.detection_mode = 'face' 

        # Bouton pour changer le mode de détection
        self.switch_button = ttk.Button(self.window, text="Switch to Iris Detection", command=self.switch_mode)
        self.switch_button.grid(row=4, column=0)

    def start_detection(self):
        self.label.config(text="Détection active")
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update_confidence(self, confidence):
        self.confidence_label.config(text=f"Confiance: {confidence:.2f}")

    def update(self):
        while True:
            ret, frame = self.camera_handler.get_frame()
            if ret:
                if self.detection_mode == 'face':
                    x, y, w, h, confidence = self.face_detector.detect_face()
                    self.face_detector.draw_face_rectangle(frame, x, y, w, h)
                    self.update_confidence(confidence)
                elif self.detection_mode == 'iris':
                    # Récupération des informations des iris
                    l_cx, l_cy, l_radius, r_cx, r_cy, r_radius = self.iris_detector.detect_iris()

                    # Si des iris sont détectés (vérifier avec le rayon par exemple)
                    if l_radius > 0 and r_radius > 0:
                        self.iris_detector._draw_iris(frame, l_cx, l_cy, l_radius)
                        self.iris_detector._draw_iris(frame, r_cx, r_cy, r_radius)

                self.show_frame(frame)

    def show_frame(self, frame):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def switch_mode(self):
        if self.detection_mode == 'face':
            self.detection_mode = 'iris'
            self.switch_button.config(text="Switch to Face Detection")
        else:
            self.detection_mode = 'face'
            self.switch_button.config(text="Switch to Iris Detection")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
