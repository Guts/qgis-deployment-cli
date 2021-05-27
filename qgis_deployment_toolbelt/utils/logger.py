import logging
from logging.handlers import RotatingFileHandler

logger = None


def init_Logger(console=True, file=False, loggerName="", logLevel=logging.DEBUG):
    """
    Création d'un nouveau logger, ou bien retour le logger existant si la fonction
    a déja été appelée.
    """
    # création de l'objet logger qui va nous servir à écrire dans les logs
    global logger
    if logger is None:
        logger = logging.getLogger(loggerName)
        logger.setLevel(logLevel)
        if file:
            # création d'un handler qui va rediriger une écriture du log vers
            # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
            file_handler = RotatingFileHandler(file, "a", 1000000, 1)
            file_handler.setLevel(logLevel)
            formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        if console:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logLevel)
            formatter = logging.Formatter("%(levelname)s :: %(message)s")
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
    return logger


def get_logger():
    return logger


class Logger:
    def __init__(self, folder_path, file_name, log_level="DEBUG"):
        # création de l'objet logger qui va nous servir à écrire dans les logs
        self.logger = logging.getLogger()

        # création d'un formateur qui va ajouter le temps, le niveau
        # de chaque message quand on écrira un message dans le log
        formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
        # création d'un handler qui va rediriger une écriture du log vers
        # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        file_handler = RotatingFileHandler(
            folder_path + "\\" + file_name, "a", 1000000, 1
        )
        # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
        # créé précédement et on ajoute ce handler au logger
        if log_level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
        elif log_level == "INFO":
            self.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
        elif log_level == "WARNING":
            self.logger.setLevel(logging.WARNING)
            file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, msg, log_level="INFO"):
        switcher = {
            "INFO": self.logger.info,
            "WARNING": self.logger.warning,
            "DEBUG": self.logger.debug,
        }
        switcher[log_level](msg)
