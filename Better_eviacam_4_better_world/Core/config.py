import json

class Config:
    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    
    INITIAL_DETECTION_MODE = 'face'
    
    MIN_DETECTION_CONFIDENCE = 0.5
    
    SMOOTHING_FACTOR = 5
    SCALE_FACTOR = 10
    
    
    SETTINGS_FILE = "settings.json"

    @staticmethod
    def load_settings():
        try:
            with open(Config.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                Config.MIN_DETECTION_CONFIDENCE = settings.get('min_detection_confidence', 0.5) 
                Config.INITIAL_DETECTION_MODE = settings.get('initial_detection_mode', 'face')
                Config.SMOOTHING_FACTOR = settings.get('smoothing_factor', 5)
                Config.SCALE_FACTOR = settings.get('scale_factor', 10)
        except FileNotFoundError:
            Config.save_settings()  # Créer le fichier de paramètres s'il n'existe pas

    @staticmethod
    def save_settings():
        settings = {
            'min_detection_confidence': Config.MIN_DETECTION_CONFIDENCE,
            'initial_detection_mode': Config.INITIAL_DETECTION_MODE,  # 'face' ou 'iris
            'smoothing_factor': Config.SMOOTHING_FACTOR,
            'scale_factor': Config.SCALE_FACTOR
        }
        with open(Config.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)
