from tkinter import ttk, Toplevel, Scale, Label
from config import Config

class SettingsWindow:
    def __init__(self, master, face_detector, iris_detector):
        self.top = Toplevel(master)
        self.top.title("Paramètres")

        self.confidence_scale = Scale(self.top, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", label="Confiance minimale pour la détection")
        self.confidence_scale.set(face_detector.min_detection_confidence)
        self.confidence_scale.pack()

        # Ajoutez des contrôles pour la vitesse horizontale et verticale
        self.horizontal_speed_scale = Scale(self.top, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", label="Vitesse horizontale de la souris")
        self.horizontal_speed_scale.set(Config.HORIZONTAL_SPEED)
        self.horizontal_speed_scale.pack()

        self.vertical_speed_scale = Scale(self.top, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", label="Vitesse verticale de la souris")
        self.vertical_speed_scale.set(Config.VERTICAL_SPEED)
        self.vertical_speed_scale.pack()

        # Ajoutez un contrôle pour l'accélération
        self.acceleration_scale = Scale(self.top, from_=1.0, to=2.0, resolution=0.1, orient="horizontal", label="Accélération de la souris")
        self.acceleration_scale.set(Config.ACCELERATION)
        self.acceleration_scale.pack()

        self.save_button = ttk.Button(self.top, text="Enregistrer", command=lambda: self.save_settings(face_detector, iris_detector))
        self.save_button.pack()

    def save_settings(self, face_detector, iris_detector):
        # Sauvegardez les nouveaux paramètres de confiance
        new_confidence = self.confidence_scale.get()
        face_detector.min_detection_confidence = new_confidence
        Config.MIN_DETECTION_CONFIDENCE = new_confidence

        # Sauvegardez les nouveaux paramètres de vitesse et d'accélération
        Config.HORIZONTAL_SPEED = self.horizontal_speed_scale.get()
        Config.VERTICAL_SPEED = self.vertical_speed_scale.get()
        Config.ACCELERATION = self.acceleration_scale.get()

        Config.save_settings()  # Enregistre tous les paramètres dans le fichier JSON
        self.top.destroy()
