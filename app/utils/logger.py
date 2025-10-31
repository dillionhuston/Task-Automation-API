"""
Singleton logger implementation to provide a consistent logging instance across the app.
"""

import logging
import threading


class SingletonLogger:
    """
    Thread-safe singleton logger class.

    Ensures only one logger instance is created and configured.
    """

    _instance = None
    _lock = threading.Lock()
    _logger: logging.Logger | None = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        # pylint: disable=unused-argument
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, level=logging.INFO, log_name="SingletonLogger"):
        """
        Initialize the logger instance if not already initialized.

        Args:
            level (int): Logging level (default: logging.INFO)
            log_name (str): Logger name (default: 'SingletonLogger')
        """
        if self._initialized:
            return
        self._logger = logging.getLogger(log_name)
        self._logger.setLevel(level)

        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        self._initialized = True

    def set_level(self, level: int):
        """Set logging level."""
        if self._logger:
            self._logger.setLevel(level)

    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        if not self._initialized:
            self.initialize()
        assert self._logger is not None
        return self._logger
