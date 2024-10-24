from app.use_cases.user_select import UserInfo
from infrastructure.db.repositories.UsersRepository import UserRepository
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from app.Utils.Exceptions import ErrorConsultNotFound, InvalidCpf, IncompleteCpf, ErrorLyricsInCpf
from fastapi.responses import JSONResponse


class Info(BaseModel):
    Nome: str = Field('Username')
    CPF: str = Field('000.000.000-00')
    Telefone: str = Field('(99) 99999-9999')
    Email: str = Field('username@gmail.com')


class UserFound(BaseModel):
    Type: str = Field('Consult Users')
    Count: int = Field(1)
    User: str = Field('Found')
    Info: Info


router = APIRouter(tags=['USUARIOS'])




UserInfoUseCase = lambda: UserInfo(repository=UserRepository())
@router.get('/Consult', response_model=UserFound, status_code=200)
def consult(CPF: str, use_case: UserInfo = Depends(UserInfoUseCase)):
    try:
        res = use_case.select_user(CPF)
        
        return JSONResponse(status_code=200,content=UserFound(
            Type='Consult Users',
            Count=1,
            User='Found',
            Info=Info(
                Nome=res['Info']['nome'],
                CPF=res['Info']['cpf'],
                Telefone=res['Info']['telefone'],
                Email=res['Info']['email']
            )
        ).dict()
        )
        
    except ErrorConsultNotFound:
        res_error = {
            'Type':'Consult Users',
            'Count':0,
            'User':'Not found'
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res_error)
    
    except IncompleteCpf as incomplete_cpf:
        raise HTTPException(status_code=411, detail={"Error": f'{incomplete_cpf}', 'Type': 'Consult Users', 'Count': 1, 'User': 'Not found'})
    
    except InvalidCpf as invalid_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{invalid_cpf}', 'Type': 'Consult Users', 'Count': 1, 'User': 'Not found'})
    
    except ErrorLyricsInCpf as lyrics_cpf:
        raise HTTPException(status_code=400, detail={"Error": f'{lyrics_cpf}', 'Type': 'Consult Users', 'Count': 1, 'User': 'Not found'})
    