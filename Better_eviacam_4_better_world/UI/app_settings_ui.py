from tkinter import ttk, Toplevel, Scale, Label
from Better_eviacam_4_better_world.Core.config import Config

class SettingsWindow:
    def __init__(self, master, face_detector, iris_detector, mouse_mover):
        self.top = Toplevel(master)
        self.top.title("Paramètres")

        self.confidence_scale = Scale(self.top, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", label="Confiance minimale pour la détection")
        self.confidence_scale.set(face_detector.min_detection_confidence)
        self.confidence_scale.pack()
        

        self.smoothing_factor_scale = Scale(self.top, from_=1, to=20, orient="horizontal", label="Facteur de lissage")
        self.smoothing_factor_scale.set(mouse_mover.smoothing_factor)
        self.smoothing_factor_scale.pack()
        
        self.scale_factor_scale = Scale(self.top, from_=1, to=20, orient="horizontal", label="Facteur d'échelle")
        self.scale_factor_scale.set(mouse_mover.scale_factor)
        self.scale_factor_scale.pack()
        
        # Bouton d'enregistrement
        self.save_button = ttk.Button(self.top, text="Enregistrer", command=lambda: self.save_settings(face_detector, iris_detector, mouse_mover))
        self.save_button.pack()

    def save_settings(self, face_detector, iris_detector, mouse_mover):
        # Sauvegardez les nouveaux paramètres de confiance
        new_confidence = self.confidence_scale.get()
        face_detector.min_detection_confidence = new_confidence
        Config.MIN_DETECTION_CONFIDENCE = new_confidence
        
        
        
        # Sauvegardez les nouveaux paramètres de lissage
        new_smoothing_factor = self.smoothing_factor_scale.get()
        mouse_mover.smoothing_factor = new_smoothing_factor
        Config.SMOOTHING_FACTOR = new_smoothing_factor
        
        # Sauvegardez les nouveaux paramètres d'échelle
        new_scale_factor = self.scale_factor_scale.get()
        mouse_mover.scale_factor = new_scale_factor
        Config.SCALE_FACTOR = new_scale_factor
        
        Config.save_settings()  # Enregistre tous les paramètres dans le fichier JSON
        self.top.destroy()
