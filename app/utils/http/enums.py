import random
from enum import Enum
from typing import List

class BrowserTypeEnum(str, Enum):
    CHROME116 = 'chrome116'
    CHROME119 = 'chrome119'
    CHROME120 = 'chrome120'
    CHROME123 = 'chrome123'
    EDGE101 = 'edge101'
    SAFARI17_0 = 'safari17_0'
    @classmethod
    def get_browser_type(cls, browser_type: str) -> 'BrowserTypeEnum':
        return cls(browser_type)
    
    @classmethod
    def get_browser_type_by_name(cls, name: str) -> 'BrowserTypeEnum':
        return cls(name)
    
    @classmethod
    def get_all_browser_types(cls) -> List['BrowserTypeEnum']:
        return list(cls)
    
    @classmethod
    def get_random_browser_type(cls) -> 'BrowserTypeEnum':
        return random.choice(list(cls))
    
class LocationEnum(str, Enum):
    EUROPE = 'EUROPE'
    UNITED_STATES = 'UNITED_STATES'
    UNITED_KINGDOM = 'UNITED_KINGDOM'
    IRELAND = 'IRELAND'
    
class RequestTypeEnum(str, Enum):
    GET = 'GET'
    POST = 'POST'