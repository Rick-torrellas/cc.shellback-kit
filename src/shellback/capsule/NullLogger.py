from ..core import Logger

class NullLogger(Logger):
    """
    Implementación 'Null Object'. 
    No realiza ninguna acción, permitiendo que la Shell funcione 
    sin comprobaciones de nulidad constantes.
    """
    def info(self, message: str):
        pass

    def debug(self, message: str):
        pass

    def warning(self, message: str):
        pass

    def error(self, message: str):
        pass