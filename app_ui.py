import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import threading
import cv2
from config import Config
from face_detector import FaceDetector
from iris_detector import IrisDetector
from camera_handler import CameraHandler
from app_settings_ui import SettingsWindow
from mouse_mover import MouseMover
from coordinate_mapper import CoordinateMapper

class App:
    def __init__(self, window):
        Config.load_settings()
        self.window = window
        self.window.title(Config.WINDOW_TITLE)
        self.init_ui()
        self.init_detectors()
        self.detection_mode = Config.INITIAL_DETECTION_MODE
        self.mapper = CoordinateMapper(Config.CANVAS_WIDTH, Config.CANVAS_HEIGHT,
                                       Config.MOUVEMENT_RANGE_X, Config.MOUVEMENT_RANGE_Y)
        self.start_detection()
        self.mouse_mover = MouseMover()

    def init_ui(self):

        self.canvas = Canvas(self.window, width=Config.CANVAS_WIDTH, height=Config.CANVAS_HEIGHT)
        self.canvas.grid(row=1, column=0)

        self.confidence_label = ttk.Label(self.window, text=Config.CONFIDENCE_LABEL_TEXT)
        self.confidence_label.grid(row=2, column=0)

        self.switch_button = ttk.Button(self.window, text=Config.SWITCH_BUTTON_TEXT, command=self.switch_mode)
        self.switch_button.grid(row=3, column=0)

        self.settings_button = ttk.Button(self.window, text="Paramètres", command=self.open_settings)
        self.settings_button.grid(row=4, column=0)

    def open_settings(self):
        SettingsWindow(self.window, self.face_detector, self.iris_detector)
        
    def init_detectors(self):
        self.camera_handler = CameraHandler()
        self.face_detector = FaceDetector(self.camera_handler, min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE)
        self.iris_detector = IrisDetector(self.camera_handler)

    def start_detection(self):
        self.thread = threading.Thread(target=self.update, args=(), daemon=True)
        self.thread.start()

    def update_confidence(self, confidence):
        self.confidence_label.config(text=f"Confiance: {confidence:.2f}")

    def update(self):
        while True:
            ret, frame = self.camera_handler.get_frame()
            if ret:
                self.process_frame(frame)

    def process_frame(self, frame):
        if self.detection_mode == 'face':
            self.process_face_detection(frame)
        elif self.detection_mode == 'iris':
            self.process_iris_detection(frame)
        self.show_frame(frame)

    def process_face_detection(self, frame):
        """
        Process face detection and move the mouse accordingly.
        """
        detection_result = self.face_detector.detect_face()
        if detection_result:
            x, y, w, h, confidence = detection_result
            if confidence > Config.MIN_DETECTION_CONFIDENCE:
                self.face_detector.draw_face_rectangle(frame, x, y, w, h)
                self.update_confidence(confidence)
                # Convert detected face position to screen coordinates
                screen_x, screen_y = self.mapper.convert_to_screen_coordinates(x, y, w, h)
                # Move the mouse to the converted screen coordinates
                self.mouse_mover.move_mouse(screen_x, screen_y)
            
    def process_iris_detection(self, frame):
        l_cx, l_cy, l_radius, r_cx, r_cy, r_radius = self.iris_detector.detect_iris()
        if l_radius > 0 and r_radius > 0:
            self.iris_detector._draw_iris(frame, l_cx, l_cy, l_radius)
            self.iris_detector._draw_iris(frame, r_cx, r_cy, r_radius)
            avg_x = (l_cx + r_cx) // 2
            avg_y = (l_cy + r_cy) // 2
            #self.mouse_mover.move_mouse(avg_x, avg_y)

    def show_frame(self, frame):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def switch_mode(self):
        self.detection_mode = 'iris' if self.detection_mode == 'face' else 'face'
        buttonText = "Switch to Face Detection" if self.detection_mode == 'iris' else "Switch to Iris Detection"
        self.switch_button.config(text=buttonText)



