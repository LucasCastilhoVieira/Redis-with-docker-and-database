from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


db_port = os.getenv('DB_PORT', '3306')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'root')
class ConnectionDB:
    def __init__(self):
        self.url = f"mysql+pymysql://{db_user}:{db_password}@db:{db_port}/Users"
        self.engine = self.create_engine()
        self.session = None
        
        
    def create_engine(self):
        engine = create_engine(self.url)
        return engine
    
    def get_engine(self):
        return self.engine
    
    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self
    
    def __exit__(self, exc_val, exc_type, exc_tb):
        self.session.close()
