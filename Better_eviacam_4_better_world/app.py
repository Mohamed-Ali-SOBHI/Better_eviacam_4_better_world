import os
import sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Better_eviacam_4_better_world.Core.config import Config
from Better_eviacam_4_better_world.Core.mouse_mover import MouseMover
from Better_eviacam_4_better_world.Core.camera_handler import CameraHandler
from Better_eviacam_4_better_world.Core.face_detector import FaceDetector
from Better_eviacam_4_better_world.Core.iris_detector import IrisDetector
from Better_eviacam_4_better_world.UI.app_ui import UIManager

class App:
    def __init__(self, window):
        self.window = window
        self.detection_mode = Config.INITIAL_DETECTION_MODE
        self.mouse_mover = MouseMover(smoothing_factor=Config.SMOOTHING_FACTOR, scale_factor=Config.SCALE_FACTOR)
        self.init_detectors()
        self.ui_manager = UIManager(window, self, self.get_click_actions())
        print('App logic initialized')

    def init_detectors(self):
        self.camera_handler = CameraHandler()
        self.face_detector = FaceDetector(self.camera_handler, min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE)
        self.iris_detector = IrisDetector(self.camera_handler)

    def switch_mode(self):
        self.detection_mode = 'iris' if self.detection_mode == 'face' else 'face'
        buttonText = "Switch to Face Detection" if self.detection_mode == 'iris' else "Switch to Iris Detection"
        self.ui_manager.update_switch_button(buttonText)

    def open_settings(self):
        from Better_eviacam_4_better_world.UI.app_settings_ui import SettingsWindow
        SettingsWindow(self.ui_manager.window, self.face_detector, self.iris_detector, self.mouse_mover)

    def get_click_actions(self):
        return {
            "Pas de clic": lambda: self.mouse_mover.set_click_mode('no_click'),
            "Clic gauche": lambda: self.mouse_mover.set_click_mode('left_click'),
            "Clic milieu": lambda: self.mouse_mover.set_click_mode('middle_click'),
            "Clic droit": lambda: self.mouse_mover.set_click_mode('right_click'),
            "Clic maintenu": lambda: self.mouse_mover.set_click_mode('click_and_hold'),
            "Double clic": lambda: self.mouse_mover.set_click_mode('double_click'),
            "Ouvrir la fenêtre principale": lambda: self.open_settings()
        }

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
