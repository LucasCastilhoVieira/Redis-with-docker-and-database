from app.interfaces.user_repository import UserRepositoryInterface
from infrastructure.db.settings.connection import ConnectionDB
from infrastructure.db.entities.UserEntitie import Users
from app.interfaces.models.Users import Users as Userss
from sqlalchemy.exc import IntegrityError
from typing import List
from app.Utils.Exceptions import UserAlreadyRegistered

class UserRepository(UserRepositoryInterface):
    
    def insert(self, nome: str, cpf: str, telefone: str, email: str): 
        try:
            with ConnectionDB() as db:
    
                    insert = Users(nome=nome, cpf=cpf, telefone=telefone, email=email)
                    db.session.add(insert)
                    db.session.commit()
        except IntegrityError:
            raise UserAlreadyRegistered('Usuário já Cadastrado')
 
    
    def select(self, cpf) -> List[Userss]:
        with ConnectionDB() as db:
          select =   db.session.query(Users).with_entities(\
            Users.nome, Users.cpf, Users.telefone, Users.email)\
            .filter(Users.cpf == cpf).all()
        return select
    
    def remove_user(self, cpf): 
        with ConnectionDB() as db:
            db.session.query(Users).filter(Users.cpf == cpf).delete()
            db.session.commit()
            
            
    def update_user(self, cpf: str, email = '', telefone = ''):
        with ConnectionDB() as db:
            if not email:
                db.session.query(Users).filter(Users.cpf == cpf).update({Users.telefone: telefone})
            if not telefone:
                db.session.query(Users).filter(Users.cpf == cpf).update({Users.email: email})
            if email and telefone:
                db.session.query(Users).filter(Users.cpf == cpf).update({Users.telefone: telefone})
                db.session.query(Users).filter(Users.cpf == cpf).update({Users.email: email})
            db.session.commit()