from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel, Field
from app.use_cases.user_register import UserRegister
from infrastructure.db.repositories.UsersRepository import UserRepository
from app.Utils.Exceptions import IncompleteCpf, InvalidCpf, ErrorNumberInName, UserAlreadyRegistered, ErrorLyricsInCpf, ErrorEmail, IncompleteTel, InvalidTel




router = APIRouter(tags=['USUARIOS'])

class UsersRegister(BaseModel):
    nome: str  = Field('username')
    cpf : str = Field('000.000.000-00')
    telefone: int = Field('99999999999')
    email: str = Field('username@gmail.com')
    
    
class Atributtes(BaseModel):
    nome: str = Field('Username')
    cpf : str = Field('000.000.000-00')
    telefone: str = Field('(99) 99999-9999')
    email: str = Field('username@gmail.com')


    
class SuccessResponse(BaseModel):
    Type: str = Field('Users')
    Count: int = Field(1)
    User: str = Field('Registered')
    Attributes: Atributtes
        
        

    
UsersRegisterUseCase = lambda: UserRegister(repository=UserRepository())

@router.post('/Register', status_code= 201,response_model=SuccessResponse)
def register(users: UsersRegister, use_cases: UserRegister = Depends(UsersRegisterUseCase)):

        
    try:
        res = use_cases.user_register_db(\
            users.nome.rstrip().lstrip(),
            users.cpf,
            users.telefone,
            users.email
        )
           
        return SuccessResponse(
            
            Type=res['Type'],
            Count=res['Count'],
            User=res['User'],
            Attributes=Atributtes(
                nome=res['Attributes']['NOME'],
                cpf=res['Attributes']['CPF'],
                telefone=res['Attributes']['TELEFONE'],
                email=res['Attributes']['EMAIL']
            )
        )
    
    except IncompleteCpf as incomplete_cpf:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_cpf}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
    
    except InvalidCpf as invalid_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_cpf}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
    
    except ErrorNumberInName as numbers:
        raise HTTPException(status_code=400, detail={"Error": f'{numbers}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
    
    except ErrorLyricsInCpf as lyrics:
        raise HTTPException(status_code=400, detail={"Error": f'{lyrics}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
    
    except UserAlreadyRegistered as user:
        raise HTTPException(status_code=208, detail={"Error": f'{user}', 'Type': 'Users', 'Count': 1, 'User': 'Already registered'})
    
    except ErrorEmail as error_email:
       raise HTTPException(status_code=411, detail={"Error": f'{error_email}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
   
    except IncompleteTel as incomplete_tel:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_tel}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})
    
    except InvalidTel as invalid_tel:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_tel}', 'Type': 'Users', 'Count': 1, 'User': 'Not registered'})