import logging
import threading

class SingletonLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, level=logging.INFO, log_name="SingletonLogger"):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def get_logger(self):
        return self.logger
