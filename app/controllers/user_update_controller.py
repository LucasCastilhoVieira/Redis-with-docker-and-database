from fastapi import APIRouter, Depends, HTTPException
from app.use_cases.user_update import UserUpdate
from infrastructure.db.repositories.UsersRepository import UserRepository
from app.Utils.Exceptions import NotUpdated, ErrorConsultNotFound,ErrorEmail, ErrorLyricsInCpf, InvalidCpf, InvalidTel, IncompleteCpf, IncompleteTel
from pydantic import Field, BaseModel


router = APIRouter(tags=['USUARIOS'])


class InfoUpdate(BaseModel):
    Cpf: str = Field('000.000.000-00')
    Telefone: str = Field('')
    Email: str = Field('')



class InfoUser(BaseModel):
    Nome: str = Field('Username')
    CPF: str = Field('000.000.000-00')
    Telefone: str = Field('(99) 99999-9999 -> (88) 88888-8888')
    Email: str = Field('username@gmail.com -> username123@gmail.com')


class UserUpdated(BaseModel):
    Type: str = Field('Update Users')
    Count: int = Field(2)
    User: str = Field('Updated')
    Attributes: InfoUser




Update = lambda: UserUpdate(repository=UserRepository())
@router.put('/Update', response_model=UserUpdated)
def update_user_info(Info: InfoUpdate, use_cases: UserUpdate = Depends(Update)):
    try:
        res = use_cases.update_user(Info.Cpf, Info.Telefone, Info.Email)
        return UserUpdated(
            Type='Update Users',
            Count=res['Count'],
            User='Updated',
            Attributes=InfoUser(
                Nome=res['Attributes']['NOME'],
                CPF=res['Attributes']['CPF'],
                Telefone=res['Attributes']['TELEFONE'],
                Email=res['Attributes']['EMAIL']
                
            )
            )
        
    except NotUpdated as not_updated:
        raise HTTPException(status_code=411, detail={"Error": f'{not_updated}', 'Type': 'Update Users', 'Count': 0, 'User': 'Not updated'})
            
    except ErrorConsultNotFound as cpf_not_found:
        raise HTTPException(status_code=411, detail={"Error": f'{cpf_not_found}', 'Type': 'Update Users', 'Count': 0, 'User': 'Not updated'})
        
    except IncompleteCpf as incomplete_cpf:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_cpf}', 'Type': 'Update Users', 'Count': 1, 'User': 'Not updated'})
    
    except InvalidCpf as invalid_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_cpf}', 'Type': 'Update Users', 'Count': 1, 'User': 'Not updated'})
    
    except ErrorLyricsInCpf as lyrics:
        raise HTTPException(status_code=400, detail={"Error": f'{lyrics}', 'Type': 'Update Users', 'Count': 1, 'User': 'Not updated'})
    
    except ErrorEmail as error_email:
       raise HTTPException(status_code=411, detail={"Error": f'{error_email}', 'Type': 'UpdateUsers', 'Count': 1, 'User': 'Not updated'})
   
    except IncompleteTel as incomplete_tel:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_tel}', 'Type': 'Update Users', 'Count': 1, 'User': 'Not updated'})
    
    except InvalidTel as invalid_tel:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_tel}', 'Type': 'Update Users', 'Count': 1, 'User': 'Not updated'})