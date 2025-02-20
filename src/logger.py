import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class LoggerSetup:
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Create formatter
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup different log files
        self.setup_loggers()

    def setup_loggers(self):
        # Setup main application logger
        self.setup_logger('app_logger', 'app.log')
        
        # Setup database logger
        self.setup_logger('db_logger', 'database.log')
        
        # Setup query logger
        self.setup_logger('query_logger', 'queries.log')
        
        # Setup error logger
        self.setup_logger('error_logger', 'errors.log')

    def setup_logger(self, logger_name, log_file):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Create handlers
        file_handler = RotatingFileHandler(
            os.path.join(self.logs_dir, log_file),
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(self.formatter)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger