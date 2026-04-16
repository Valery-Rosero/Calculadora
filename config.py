"""
Configuración central de la aplicación.
Los valores se leen desde variables de entorno con fallbacks seguros.
"""

import os


class Config:
    """Configuración base."""
    DEBUG = False
    TESTING = False
    PORT = int(os.getenv("PORT", 5000))
    MAX_EXPRESSION_LENGTH = int(os.getenv("MAX_EXPRESSION_LENGTH", 200))
    MAX_FACTORIAL_INPUT = int(os.getenv("MAX_FACTORIAL_INPUT", 170))
    RESULT_PRECISION = int(os.getenv("RESULT_PRECISION", 10))


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False


class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    DEBUG = True


# Mapa de entornos disponibles
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> Config:
    """Retorna la configuración según la variable de entorno FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)()
