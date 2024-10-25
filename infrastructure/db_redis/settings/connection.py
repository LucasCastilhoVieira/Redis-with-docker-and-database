from .redis_config_connection.config import redis_config
from redis import Redis
import json
class RedisConnectionHandler:
    def __init__(self):
        self.host = redis_config['host']
        self.port = redis_config['port']
        self.db = redis_config['db']
        
    def connect(self):
        Connection = Redis(host=self.host, port=self.port, db=self.db)
        return Connection
    
    
        
