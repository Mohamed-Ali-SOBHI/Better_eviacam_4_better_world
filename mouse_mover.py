import pyautogui

class MouseMover:
    def move_mouse(self, x, y):
        screen_width, screen_height = pyautogui.size() # Récupère la taille de l'écran
        #print(screen_width, screen_height)
        edge_threshold = 10  # Distance en pixels du bord où le curseur sera bloqué

        # Assurez-vous que x et y ne sont pas None
        if x is None or y is None:
            return

        if x > screen_width - edge_threshold or x < edge_threshold or y > screen_height - edge_threshold or y < edge_threshold: # Si x ou y sont supérieurs à la taille de l'écran ou inférieurs à 0
            # Ne déplacez pas le curseur si x ou y sont en dehors de l'écran
            print("x ou y sont en dehors de l'écran")
            return      

        # Vérifiez si le curseur est déjà à la position désirée pour éviter des mouvements inutiles
        current_x, current_y = pyautogui.position()
        if (current_x, current_y) == (x, y):
            return

        pyautogui.moveTo(x, y, duration=0.1)  # Déplacez le curseur vers la position désirée en 0,1 seconde 
