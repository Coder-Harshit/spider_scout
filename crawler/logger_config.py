import logging
import os
from datetime import datetime
import sys
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv(dotenv_path='.env.local')


def setup_logger():
    """Configure logging with file and console handlers, adapted for environments"""

    # Determine environment
    environment = os.getenv("ENV", "development")  # Default to 'development'
    is_debug = environment == "development"
    # print(is_debug, flush=True)
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate timestamp for log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/spiderscout_{timestamp}.log'
    
    # Configure root logger
    logger = logging.getLogger('SpiderScout')
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)
    
    # File handler - detailed logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Always log debug info to the file
    file_format = logging.Formatter(
        '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Console handler - simplified logging for production
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.DEBUG if is_debug else logging.INFO)
    console_format = logging.Formatter(
        '[%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger initialized. Environment: {environment}")
    return logger
