import pyautogui

class MouseMover:
    def move_mouse(self, x, y):
        screen_width, screen_height = pyautogui.size()
        edge_threshold = 10  # Distance en pixels du bord où le curseur sera bloqué

        # Assurez-vous que x et y ne sont pas None
        if x is None or y is None:
            return

        # Si x ou y est trop près du bord, ajustez les coordonnées pour les empêcher d'atteindre le bord
        x = max(edge_threshold, min(x, screen_width - edge_threshold))
        y = max(edge_threshold, min(y, screen_height - edge_threshold))

        # Vérifiez si le curseur est déjà à la position désirée pour éviter des mouvements inutiles
        current_x, current_y = pyautogui.position()
        if (current_x, current_y) == (x, y):
            return

        pyautogui.moveTo(x, y, duration=0.1)
