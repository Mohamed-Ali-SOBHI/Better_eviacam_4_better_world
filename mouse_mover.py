import pyautogui

class MouseMover:
    def move_mouse(self, x, y):
        if x is not None and y is not None:
            pyautogui.moveTo(x, y, duration=0.1)
