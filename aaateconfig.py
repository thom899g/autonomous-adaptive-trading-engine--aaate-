"""
AAATE Configuration Management
Centralized configuration with environment variables and Firebase integration.
"""
import os
import json
import logging
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DataConfig:
    """Data ingestion and preprocessing configuration"""
    DATA_SOURCES = {
        'crypto': ['binance', 'kraken', 'coinbase'],
        'forex': ['oanda', 'fxcm'],
        'stocks': ['alpaca', 'yfinance']
    }
    TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h', '1d']
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0
    DATA_CACHE_SECONDS = 30

@dataclass
class ModelConfig:
    """ML model and algorithm configuration"""
    RL_AGENT_MEMORY_SIZE = 10000
    RL_BATCH_SIZE = 64
    RL_LEARNING_RATE = 0.001
    RL_GAMMA = 0.99
    RL_TAU = 0.005
    MARKET_REGIME_CLUSTERS = 5
    MIN_SAMPLES_FOR_TRAINING = 1000

@dataclass
class TradingConfig:
    """Trading execution parameters"""
    MAX_POSITION_SIZE = 0.1  # 10% of portfolio per trade
    MAX_LEVERAGE = 3.0
    STOP_LOSS_PCT = 0.02  # 2%
    TAKE_PROFIT_PCT = 0.05  # 5%
    MIN_TRADE_SIZE_USD = 10.0
    COOLDOWN_PERIOD_SECONDS = 60

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase_credentials.json')
    COLLECTION_PREFIX = os.getenv('FIREBASE_COLLECTION_PREFIX', 'aaate_')
    STATE_COLLECTION = 'trading_states'
    PERFORMANCE_COLLECTION = 'performance_metrics'
    MODEL_COLLECTION = 'model_parameters'

class Config:
    """Main configuration class"""
    def __init__(self):
        self.data = DataConfig()
        self.model = ModelConfig()
        self.trading = TradingConfig()
        self.firebase = FirebaseConfig()
        self.environment = os.getenv('AAATE_ENV', 'development')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def validate(self) -> bool:
        """Validate critical configuration"""
        if not os.path.exists(self.firebase.CREDENTIALS_PATH):
            logging.error(f"Firebase credentials not found at {self.firebase.CREDENTIALS_PATH}")
            return False
        if not self.telegram_bot_token or not self.telegram_chat_id:
            logging.warning("Telegram credentials not set - notifications disabled")
        return True

config = Config()