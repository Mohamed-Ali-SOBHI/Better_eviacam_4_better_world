import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import cv2
import threading
from face_detector import FaceDetector  # Assurez-vous que face_detector.py est dans le même répertoire
from mouse_mover import MouseMover  # Uncomment this if you have the MouseMover class implemented

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

    def start_detection(self):
        self.label.config(text="Détection active")
        self.face_detector = FaceDetector()
        # self.mouse_mover = MouseMover()  # Uncomment this if you have the MouseMover class implemented

        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update_confidence(self, confidence):
        self.confidence_label.config(text=f"Confiance: {confidence:.2f}")
        
    def update(self):
        while True:
            ret, frame = self.face_detector.cap.read()
            if ret:
                x, y, w, h, confidence = self.face_detector.detect_face()
                self.face_detector.draw_face_rectangle(frame, x, y, w, h)
                # self.mouse_mover.move_mouse(x, y)  # Uncomment this if you have the MouseMover class implemented
                self.show_frame(frame)
                self.update_confidence(confidence)


    def show_frame(self, frame):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
