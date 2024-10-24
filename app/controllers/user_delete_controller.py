from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel, Field
from app.use_cases.user_delete import UserDelete
from infrastructure.db.repositories.UsersRepository import UserRepository
from app.Utils.Exceptions import IncompleteCpf, InvalidCpf, ErrorConsultNotFound, ErrorLyricsInCpf


router = APIRouter(tags=['USUARIOS'])

class Atributtes(BaseModel):
    nome: str = Field('Username')
    cpf : str = Field('000.000.000-00')
    telefone: str = Field('(99) 99999-9999')
    email: str = Field('username@gmail.com')
    
    
class SuccessResponse(BaseModel):
    Type: str = Field('Delete Users')
    Count: int = Field(1)
    User: str = Field('Deleted')
    Attributes: Atributtes
    
UserDeleteUseCase = lambda: UserDelete(repository=UserRepository())
@router.delete('/Delete', response_model=SuccessResponse, status_code=200)
def delete(CPF: str, use_case: UserDelete = Depends(UserDeleteUseCase)):
    try:
        res = use_case.delete_user(CPF)
        
        return SuccessResponse(
            Type='Delete Users',
            Count=1,
            User='Deleted',
            Attributes=Atributtes(
                nome=res['Attributes']['NOME'],
                cpf=res['Attributes']['CPF'],
                telefone=res['Attributes']['TELEFONE'],
                email=res['Attributes']['EMAIL']
            )
        )
        
    except ErrorConsultNotFound:
        res_error = {
            'Type':'Delete Users',
            'Count':0,
            'User':'Not found'
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res_error)
    
    except IncompleteCpf as incomplete_cpf:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_cpf}', 'Type': 'Delete Users', 'Count': 1, 'User': 'Not deleted'})
    
    except InvalidCpf as invalid_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_cpf}', 'Type': 'Delete Users', 'Count': 1, 'User': 'Not deleted'})
    
    except ErrorLyricsInCpf as lyrics_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{lyrics_cpf}', 'Type': 'Delete Users', 'Count': 1, 'User': 'Not deleted'})
        
