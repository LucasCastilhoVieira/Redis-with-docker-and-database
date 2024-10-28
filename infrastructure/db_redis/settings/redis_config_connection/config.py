import os 
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379)) 
redis_config ={
    "host": redis_host,
    "port": redis_port,
    "db": 0
}