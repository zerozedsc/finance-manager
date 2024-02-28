from datetime import datetime
from pprint import pprint
from flask import current_app
import time, logging, json, os, sys, uuid

# Global Constants
MAIN_TITLE = "Finance Planner"
CURRENCY = "JPY"
DATETIME_FT = '%d-%m-%Y %H:%M:%S'


# logs function

def create_logs(log_name, filename, log_message, status='info'):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    foldername = "logs"
    full_filename = os.path.join(foldername, filename + ".log")

    # Ensure the logs directory exists
    os.makedirs(foldername, exist_ok=True)

    # Create a logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)  # Set logger to debug level to catch all messages

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Check if logger already has handlers to prevent duplicate messages
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(full_filename)
        file_handler.setFormatter(formatter)

        # Create stream handler for terminal output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Set the level for handlers based on the status
        if status == 'info':
            file_handler.setLevel(logging.INFO)
            stream_handler.setLevel(logging.INFO)
        elif status == 'error':
            file_handler.setLevel(logging.ERROR)
            stream_handler.setLevel(logging.ERROR)
        elif status == 'warning':
            file_handler.setLevel(logging.WARNING)
            stream_handler.setLevel(logging.WARNING)
        elif status == 'debug':
            file_handler.setLevel(logging.DEBUG)
            stream_handler.setLevel(logging.DEBUG)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    # Log the message
    if status == 'info':
        logger.info(log_message)
    elif status == 'error':
        logger.error(log_message)
    elif status == 'warning':
        logger.warning(log_message)
    elif status == 'debug':
        logger.debug(log_message)


def generate_id(i, n, id_type="uuid") -> str:
    if id_type == "numeric":
        # Generate n digits number ID with leading zeros
        return str(i).zfill(n)
    elif id_type == "uuid":
        # Generate random UUID
        return str(uuid.uuid4())
    elif id_type == "alphanumeric":
        # Generate number and letter as ID
        prefix = chr(65 + (i // (10**n)))  # 65 is ASCII for 'A'
        number = i % (10**n)
        return f"{prefix}{str(number).zfill(n)}"
    else:
        return None


# global functions

def datetime_now() -> str:
    return datetime.now().strftime(DATETIME_FT)


def to_datetime_ft(str) -> datetime:
    return datetime.strptime(str, DATETIME_FT)


def timestampID() -> int:
    time_now = datetime.now().strftime(DATETIME_FT)
    dt_object = datetime.strptime(time_now, DATETIME_FT)
    timestamp = datetime.timestamp(dt_object)
    return int(timestamp)


def timestampIDtoDT(timestamp) -> str:
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime(DATETIME_FT)


def numeric(value) -> any:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
