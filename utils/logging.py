import logging

logging.basicConfig(
    filename='talon.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def log_error(msg):
    logging.error(msg)

def log_info(msg):
    logging.info(msg)
