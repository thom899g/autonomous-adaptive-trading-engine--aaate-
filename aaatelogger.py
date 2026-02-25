"""
Advanced logging system with Firebase integration and real-time monitoring
"""
import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any
import traceback
from firebase_admin import firestore
from .config import config

class FirebaseHandler(logging.Handler):
    """Firestore log handler for persistent storage"""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.batch_size = 10
        self.buffer = []
        
    def emit(self, record):
        try:
            log_entry = {
                'timestamp': datetime.utcnow(),
                'level': record.levelname,
                'module': record.module,
                'function': record.funcName,
                'message': record.getMessage(),
                'environment': config.environment
            }
            
            if record.exc_info:
                log_entry['exception'] = traceback.format_exception(*record.exc_info)
                
            # Add to buffer
            self.buffer.append(log_entry)
            
            # Flush if buffer is full
            if len(self.buffer) >= self.batch_size:
                self.flush()
                
        except Exception as e:
            # Fallback to console if Firebase fails
            print(f"Logging error: {e}", file=sys.stderr)
            
    def flush(self):
        """Flush buffer to Firestore"""
        try:
            batch = self.db.batch()
            for log_entry in self.buffer:
                doc_ref = self.db.collection(
                    f"{config.firebase.COLLECTION_PREFIX}logs"
                ).document()
                batch.set(doc_ref, log_entry)
            batch.commit()
            self.buffer.clear()
        except Exception as e:
            print(f"Firebase flush error: {e}", file=sys.stderr)

def setup_logger(name: str, level: str = None) -> logging.Logger:
    """Configure and return a logger instance"""
    logger = logging.getLogger(name)
    
    if level is None:
        level = config.log_level
        
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
        
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler for critical errors
    file_handler = logging.FileHandler('aaate_errors.log')
    file_handler.setLevel(logging.ERROR)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger('aaate')