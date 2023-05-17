import requests
from abc import ABC, abstractmethod


class CryptoAPI(ABC):
    """Abstract base class for a cryptocurrency API."""

    def __init__(self):
        self.base_url = ""
        self.headers = {}

    @abstractmethod
    def fetch_market_data(self, market_ids):
        pass

    @abstractmethod
    def fetch_global_data(self):
        pass
