import logging

def setup_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("SystemMonitorPro")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
