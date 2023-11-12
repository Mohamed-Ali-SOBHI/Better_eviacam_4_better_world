import json

class Config:
    WINDOW_TITLE = "MVP eViacam"
    LABEL_TEXT = "Détection active"
    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    CONFIDENCE_LABEL_TEXT = "Confiance: "
    INITIAL_DETECTION_MODE = 'face'
    SWITCH_BUTTON_TEXT = "Switch to Iris Detection"
    MIN_DETECTION_CONFIDENCE = 0.5
    SETTINGS_FILE = "settings.json"

    @staticmethod
    def load_settings():
        try:
            with open(Config.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                Config.MIN_DETECTION_CONFIDENCE = settings.get('min_detection_confidence', 0.5)
        except FileNotFoundError:
            Config.save_settings()  # Créer le fichier de paramètres s'il n'existe pas

    @staticmethod
    def save_settings():
        settings = {
            'min_detection_confidence': Config.MIN_DETECTION_CONFIDENCE
        }
        with open(Config.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)
