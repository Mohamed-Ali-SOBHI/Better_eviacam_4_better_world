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
    # Ajoutez les paramètres de vitesse et d'accélération
    HORIZONTAL_SPEED = 1.0  # Vitesse horizontale initiale pour le déplacement de la souris
    VERTICAL_SPEED = 1.0    # Vitesse verticale initiale pour le déplacement de la souris
    ACCELERATION = 1.1      # Facteur d'accélération pour le déplacement de la souris
    MOUVEMENT_RANGE_X = 1.0 # Plage de mouvement horizontale
    MOUVEMENT_RANGE_Y = 1.0 # Plage de mouvement verticale
    SETTINGS_FILE = "settings.json"

    @staticmethod
    def load_settings():
        try:
            with open(Config.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                Config.MIN_DETECTION_CONFIDENCE = settings.get('min_detection_confidence', 0.7)
                Config.HORIZONTAL_SPEED = settings.get('horizontal_speed', 1.0)
                Config.VERTICAL_SPEED = settings.get('vertical_speed', 1.0)
                Config.ACCELERATION = settings.get('acceleration', 1.1)
        except FileNotFoundError:
            Config.save_settings()  # Créer le fichier de paramètres s'il n'existe pas

    @staticmethod
    def save_settings():
        settings = {
            'min_detection_confidence': Config.MIN_DETECTION_CONFIDENCE,
            'horizontal_speed': Config.HORIZONTAL_SPEED,
            'vertical_speed': Config.VERTICAL_SPEED,
            'acceleration': Config.ACCELERATION
        }
        with open(Config.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)
