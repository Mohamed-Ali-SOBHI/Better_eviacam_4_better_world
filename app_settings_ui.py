import tkinter as tk
from tkinter import Canvas, ttk, Toplevel, Scale, Label
from config import Config

class SettingsWindow:
    def __init__(self, master, face_detector, iris_detector):
        self.top = Toplevel(master)
        self.top.title("Paramètres")

        self.confidence_scale = Scale(self.top, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", label="Confiance minimale pour la détection")
        self.confidence_scale.set(face_detector.min_detection_confidence)
        self.confidence_scale.pack()

        self.save_button = ttk.Button(self.top, text="Enregistrer", command=lambda: self.save_settings(face_detector, iris_detector))
        self.save_button.pack()

    def save_settings(self, face_detector, iris_detector):
        new_confidence = self.confidence_scale.get()
        face_detector.min_detection_confidence = new_confidence
        Config.MIN_DETECTION_CONFIDENCE = new_confidence
        Config.save_settings()  # Enregistre les paramètres dans le fichier JSON
        self.top.destroy()