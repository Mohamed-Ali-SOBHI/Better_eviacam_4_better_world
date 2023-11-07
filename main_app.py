import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import threading
from face_detector import FaceDetector  # Make sure face_detector.py is in the same directory
from camera_handler import CameraHandler
import cv2

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
        
        self.confidence_label = ttk.Label(self.window, text="Confidence: ")
        self.confidence_label.grid(row=3, column=0)
        
        self.camera_handler = CameraHandler()
        self.face_detector = FaceDetector(self.camera_handler, min_detection_confidence=0.5)


    def start_detection(self):
        self.label.config(text="Détection active")
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update_confidence(self, confidence):
        self.confidence_label.config(text=f"Confiance: {confidence:.2f}")

    def update(self):
        while True:
            ret, frame = self.camera_handler.get_frame()  # Use the CameraHandler's method here
            if ret:
                x, y, w, h, confidence = self.face_detector.detect_face()
                self.face_detector.draw_face_rectangle(frame, x, y, w, h)
                self.show_frame(frame)
                self.update_confidence(confidence)


    def show_frame(self, frame):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
