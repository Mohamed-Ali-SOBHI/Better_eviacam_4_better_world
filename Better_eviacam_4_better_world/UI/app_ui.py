import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
import cv2

class UIManager:
    def __init__(self, window: tk.Tk, app_logic, click_actions):
        self.window = window
        self.app_logic = app_logic
        self.click_actions = click_actions
        self.setup_window()
        self.init_ui()

    def setup_window(self):
        self.window.title('BETTER EVIACAM 4 BETTER WORLD')
        self.canvas = Canvas(self.window, width=640, height=480)
        self.confidence_label = ttk.Label(self.window, text='Confiance: ')
        print('Window setup completed')

    def init_ui(self):
        self.toolbar = self.create_toolbar()
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.create_main_buttons()
        print('UI initialized')

    def create_toolbar(self) -> ttk.Frame:
        toolbar = ttk.Frame(self.window)
        button_texts = ["Pas de clic", "Clic gauche", "Clic milieu", "Clic droit", "Clic maintenu", "Double clic", "Ouvrir la fenêtre principale"]
        for text in button_texts:
            btn = ttk.Button(toolbar, text=text, command=self.click_actions[text])
            btn.pack(side="left", padx=2, pady=2)
        return toolbar

    def create_main_buttons(self):
        self.canvas.grid(row=1, column=0, columnspan=2)
        self.confidence_label.grid(row=2, column=0)
        self.switch_button = ttk.Button(self.window, text='Switch to Iris Detection', command=self.app_logic.switch_mode)
        self.switch_button.grid(row=3, column=0)
        self.settings_button = ttk.Button(self.window, text="Paramètres", command=self.app_logic.open_settings)
        self.settings_button.grid(row=4, column=0)

    def update_confidence(self, confidence: float):
        self.confidence_label.config(text=f"Confiance: {confidence:.2f}")

    def show_frame(self, frame):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def update_switch_button(self, text: str):
        self.switch_button.config(text=text)
