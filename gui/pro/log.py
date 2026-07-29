"""
ZapPhysics Professional — Logging System
Centralized logging with structured output.
"""

import logging
import sys
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
import threading


class ColoredFormatter(logging.Formatter):
    """Colorized console formatter."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    log_dir: Optional[Path] = None,
    console: bool = True,
    file_logging: bool = True,
    json_format: bool = False
) -> logging.Logger:
    """
    Configure application logging.
    
    Args:
        level: Logging level
        log_dir: Directory for log files
        console: Enable console output
        file_logging: Enable file logging
        json_format: Use JSON format for file logs
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("zapphysics")
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False
    
    # Format
    if json_format:
        fmt = '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "func": "%(funcName)s", "line": %(lineno)d}'
    else:
        fmt = "[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(ColoredFormatter(fmt, datefmt=datefmt))
        logger.addHandler(console_handler)
    
    # File handler
    if file_logging and log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Main log file
        log_file = log_dir / f"zapphysics_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(file_handler)
        
        # Error log file
        error_file = log_dir / f"zapphysics_errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        error_handler.setLevel(logging.WARNING)
        error_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(error_handler)
    
    return logger


class LoggerMixin:
    """Mixin to add logging to classes."""
    
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(f"zapphysics.{self.__class__.__module__}.{self.__class__.__name__}")
        return self._logger


# Application logger
app_logger = logging.getLogger("zapphysics.app")