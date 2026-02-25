"""
Firebase Admin SDK integration for state persistence and real-time data streaming
"""
import json
import threading
import time
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from contextlib import contextmanager

import firebase_admin
from firebase_admin import credentials, firestore, db as realtime_db
from google.cloud.firestore_v1.base_query import FieldFilter

from .config import config
from .logger import logger

class FirebaseClient:
    """Firebase client for state management and real-time updates"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return