import os
import sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Better_eviacam_4_better_world.Core.config import Config
from Better_eviacam_4_better_world.Core.mouse_mover import MouseMover
from Better_eviacam_4_better_world.Core.camera_handler import CameraHandler
from Better_eviacam_4_better_world.Core.face_detector import FaceDetector
from Better_eviacam_4_better_world.Core.iris_detector import IrisDetector
from Better_eviacam_4_better_world.UI.app_settings_ui import SettingsWindow
from Better_eviacam_4_better_world.UI.app_ui import UIManager

class App:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.detection_mode = Config.INITIAL_DETECTION_MODE
        self.mouse_mover = MouseMover(smoothing_factor=Config.SMOOTHING_FACTOR, scale_factor=Config.SCALE_FACTOR)
        self.init_detectors()
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
        SettingsWindow(self.ui_manager.window, self.face_detector, self.iris_detector, self.mouse_mover)

    # Define real click actions
    def no_click(self):
        self.mouse_mover.set_click_mode('no_click')
        
    def left_click(self):        
        self.mouse_mover.set_click_mode('left_click')               
        
    def middle_click(self):       
        self.mouse_mover.set_click_mode('middle_click')
        
    def right_click(self):
        self.mouse_mover.set_click_mode('right_click')
        
    def click_and_hold(self):
        self.mouse_mover.set_click_mode('click_and_hold')
        
    def double_click(self):
        self.mouse_mover.set_click_mode('double_click')

if __name__ == "__main__":
    root = tk.Tk()
    app_logic = App(None)  # Temporary None, will be set after UIManager initialization
    click_actions = {
        "Pas de clic": app_logic.no_click,
        "Clic gauche": app_logic.left_click,
        "Clic milieu": app_logic.middle_click,
        "Clic droit": app_logic.right_click,
        "Clic maintenu": app_logic.click_and_hold,
        "Double clic": app_logic.double_click,
        "Ouvrir la fenêtre principale": lambda: print('Main window opened')
    }
    ui_manager = UIManager(root, app_logic, click_actions)
    app_logic.ui_manager = ui_manager  # Set the UIManager reference in AppLogic
    root.mainloop()
