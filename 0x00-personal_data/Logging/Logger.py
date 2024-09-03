#!/usr/bin/python3
import logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

logger.info("This is my info message")
logger.debug("This is my debug message")
