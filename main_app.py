import tkinter as tk
from tkinter import ttk
import threading
from face_detector import FaceDetector
from mouse_mover import MouseMover

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MVP eViacam")
        self.label = ttk.Label(self.root, text="Cliquez pour activer")
        self.label.grid(row=0, column=0)
        self.button = ttk.Button(self.root, text="Activer", command=self.start_detection)
        self.button.grid(row=1, column=0)

    def start_detection(self):
        self.label.config(text="Détection active")
        self.face_detector = FaceDetector()
        self.mouse_mover = MouseMover()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            x, y = self.face_detector.detect_face()
            self.mouse_mover.move_mouse(x, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
