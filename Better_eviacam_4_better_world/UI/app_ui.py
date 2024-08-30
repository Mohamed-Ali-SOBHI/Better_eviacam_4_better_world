import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import cv2

class UIManager:
    def __init__(self, window: tk.Tk, app_logic, click_actions):
        self.window = window
        self.app_logic = app_logic
        self.click_actions = click_actions
        self.full_window = None  # This will hold the reference to the new window if opened

        self.setup_small_window()

    def setup_small_window(self):
        self.window.title('BETTER EVIACAM 4 BETTER WORLD - Small Window')

        # Set the initial size of the small window based on percentage of screen size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        small_window_width = int(screen_width * 1)  # 100% of screen width
        small_window_height = int(screen_height * 0.03)  # 3% of screen height
        self.window.geometry(f"{small_window_width}x{small_window_height}")

        self.toolbar = ttk.Frame(self.window)
        self.toolbar.pack(side="top", fill="x")

        self.main_button = ttk.Button(self.toolbar, text="Ouvrir la fenêtre principale", command=self.open_main_window)
        self.main_button.pack(side="left", padx=2, pady=2)

        # Add buttons for click actions, initially disabled
        self.buttons = []
        for text in ["Pas de clic", "Clic gauche", "Clic milieu", "Clic droit", "Clic maintenu", "Double clic"]:
            btn = ttk.Button(self.toolbar, text=text, command=self.click_actions[text], state=tk.DISABLED)
            btn.pack(side="left", padx=2, pady=2)
            self.buttons.append(btn)

        print('Small window setup completed')

    def open_main_window(self):
        if self.full_window is None or not tk.Toplevel.winfo_exists(self.full_window):
            self.full_window = tk.Toplevel(self.window)
            self.setup_full_window(self.full_window)
        else:
            self.full_window.lift()

    def setup_full_window(self, full_window):
        full_window.title('BETTER EVIACAM 4 BETTER WORLD - Full Window')

        # Enable the buttons in the original window
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

        # Create the canvas and other main window elements in the new window
        self.canvas = Canvas(full_window, width=640, height=480)
        self.canvas.pack(pady=10)

        self.confidence_label = ttk.Label(full_window, text='Confiance: ')
        self.confidence_label.pack()

        self.switch_button = ttk.Button(full_window, text='Switch to Iris Detection', command=self.app_logic.switch_mode)
        self.switch_button.pack(pady=5)

        self.settings_button = ttk.Button(full_window, text="Paramètres", command=self.app_logic.open_settings)
        self.settings_button.pack(pady=5)

        # Set the full window size
        full_window.geometry("700x600")

        full_window.protocol("WM_DELETE_WINDOW", self.close_main_window)
        print('Full window setup completed')

    def close_main_window(self):
        if self.full_window is not None:
            self.full_window.destroy()
            self.full_window = None
        print('Full window closed')

    def update_confidence(self, confidence: float):
        if hasattr(self, 'confidence_label'):
            self.confidence_label.config(text=f"Confiance: {confidence:.2f}")

    def show_frame(self, frame):
        if hasattr(self, 'canvas'):
            self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def update_switch_button(self, text: str):
        if hasattr(self, 'switch_button'):
            self.switch_button.config(text=text)
