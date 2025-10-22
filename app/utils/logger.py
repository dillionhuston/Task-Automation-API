"""
Singleton logger implementation to provide a consistent logging instance across the app.
"""

import logging
import threading

logger = logging.getLogger(__name__)

class SingletonLogger:
    """
    Thread-safe singleton logger class.

    Ensures only one logger instance is created and configured.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Override object creation to ensure singleton behavior.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def initialize(self, level=logging.INFO, log_name="SingletonLogger"):
        """
        Initialize the logger instance if not already initialized.

        Args:
            level (int): Logging level (default: logging.INFO).
            log_name (str): Logger name (default: 'SingletonLogger').
        """
        if getattr(self, "_initialized", False):
            return
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self._initialized = True

    def set_level(self, level):
        """
        Set logging level.

        Args:
            level (int): New logging level.
        """
        self.logger.setLevel(level)

    def get_logger(self):
        """
        Get the logger instance.

        Returns:
            logging.Logger: The singleton logger.
        """
        if not getattr(self, "_initalized", False):
            self.initialize()
        return self.logger
