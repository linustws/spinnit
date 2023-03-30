import logging
import logging.handlers


class Logger:
    def __init__(self, log_name, log_file_path):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add a file handler to write logs to a file
        file_handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=5242880, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Add a console handler to write logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, message, exc_info=None):
        getattr(self.logger, level)(message, exc_info=exc_info)
