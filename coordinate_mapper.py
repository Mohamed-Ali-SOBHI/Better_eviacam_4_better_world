import pyautogui

class CoordinateMapper:
    def __init__(self, frame_width, frame_height, movement_range_x, movement_range_y):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.movement_range_x = movement_range_x
        self.movement_range_y = movement_range_y
        self.screen_width, self.screen_height = pyautogui.size()

    def convert_to_screen_coordinates(self, x, y, w, h):
        """
        Convertit les coordonnées de détection de la caméra en coordonnées de l'écran.
        """
        # Calculer le centre de la détection de la tête
        center_x = x + w / 2
        center_y = y + h / 2

        # Calculer les coordonnées relatives centrées
        relative_x = (center_x - self.frame_width / 2) / (self.frame_width / 2)
        relative_y = (center_y - self.frame_height / 2) / (self.frame_height / 2)

        # Appliquer la sensibilité et la plage de mouvement
        screen_x = int((relative_x * self.movement_range_x / 2 + 0.5) * self.screen_width)
        screen_y = int((relative_y * self.movement_range_y / 2 + 0.5) * self.screen_height)

        # Assurez-vous que les coordonnées de l'écran ne dépassent pas les dimensions de l'écran
        screen_x = min(max(screen_x, 0), self.screen_width)
        screen_y = min(max(screen_y, 0), self.screen_height)

        return screen_x, screen_y
