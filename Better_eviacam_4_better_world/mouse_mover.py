import pyautogui
import numpy as np
from pynput.mouse import Controller, Listener

class MouseMover:
    def __init__(self, smoothing_factor=5, scale_factor=10):
        # Initialiser le contrôleur de la souris
        self.mouse_controller = pyautogui
        self.smoothing_factor = smoothing_factor
        self.scale_factor = scale_factor
        self.previous_positions = np.zeros((smoothing_factor, 2))
        self.reference_position = None  # Position de référence pour calculer le vecteur de mouvement

    def update_reference_position(self, x, y):
        self.reference_position = (x, y)

    def move_mouse(self, x, y):
        if self.reference_position is None:
            self.update_reference_position(x, y)

        # Calcul du vecteur de mouvement
        vx = x - self.reference_position[0]
        vy = y - self.reference_position[1]

        # Mise à jour de la position de référence
        self.update_reference_position(x, y)

        # Lissage des mouvements
        self.previous_positions = np.roll(self.previous_positions, -1, axis=0)
        self.previous_positions[-1, :] = [vx, vy]
        smooth_vx, smooth_vy = np.mean(self.previous_positions, axis=0)

        # Application du facteur d'échelle
        smooth_vx *= self.scale_factor
        smooth_vy *= self.scale_factor

        # Traduction en mouvements de souris
        current_mouse_x, current_mouse_y = self.mouse_controller.position()
        new_mouse_x = current_mouse_x + smooth_vx
        new_mouse_y = current_mouse_y + smooth_vy

        self.mouse_controller.moveTo(new_mouse_x, new_mouse_y)
