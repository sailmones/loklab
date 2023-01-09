import sys
import threading
from threading import Thread
import signal
 
import logging
import logging.config

from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.utils import iswrapper

from datetime import datetime, timedelta
from dateutil import parser

import pytz
import time

 # Define global variables
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "my_historical_data.txt",  # Enter path where the logs should be stored
            "mode": "a",
            "formatter": "detailed"
        },
    },
    "loggers": {
        "MyPythonStrategy": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        }
    }
}
logger = None  

class TradeableSecurity(Contract):
    def __init__(self,security_id: int, tradeable_hours: str = None, tradeable_hours_io: str = "in", **kwargs):
        Contract.__init__(self)
        self.security_id = security_id
        self.tradableHours = tradeable_hours
        self.tradableHoursIO = tradeable_hours_io
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        return f"{vars(self)}"

    def update_security_details(self, security_detail_objects: list):
        for obj in security_detail_objects:
            for attr in vars(obj):
                setattr(self, attr, getattr(obj, attr))
    
    def is_trading_permitted(self):
        utc_now = datetime.now().astimezone(pytz.timezone("UTC"))