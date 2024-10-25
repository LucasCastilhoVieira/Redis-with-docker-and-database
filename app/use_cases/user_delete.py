from typing import Dict
from app.interfaces.use_cases.user_delete import UserDeleteInterface
from app.Utils.Exceptions import ErrorLyricsInCpf, IncompleteCpf, InvalidCpf, ErrorConsultNotFound
import re
from app.interfaces.user_repository import UserRepositoryInterface
from app.interfaces.redis_repository import RedisUserInterface



class UserDelete(UserDeleteInterface):
    def __init__(self, repository: UserRepositoryInterface, redis_repository: RedisUserInterface):
        self.user_repo = repository
        self.user_redis_repo = redis_repository
        
    def info_user(self, cpf: str):
        select = self.user_repo.select(cpf)
        return select
    
    
    def delete_user(self, cpf: str) -> Dict:
    
        cpf_format = self.cpf_format(cpf)
        select = self.info_user(cpf_format)
        self.verification_select(select)
        self.user_redis_repo.delete_user_redis(cpf_format)
        self.user_repo.remove_user(cpf_format)
        response = self.response(select)
        return response
        
    @classmethod
    def cpf_format(self, cpf):
            format = re.compile('[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}')
            finder = format.match(cpf)
            abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ç']
            for letra in abc:
                if letra in cpf or letra.upper() in cpf:
                    raise ErrorLyricsInCpf('O CPF NÃO DEVE CONTER LETRAS! DIGITE APENAS NÚMEROS.')
                else:
                    pass
            if finder == None:
                if len(cpf) == 11:
                    cpf_format = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
                    return cpf_format
                if len(cpf) < 11:
                    raise IncompleteCpf("CPF INCOMPLETO")
                else:
                    raise InvalidCpf("CPF MUITO GRANDE") 
            
            else:
                return cpf
    @classmethod
    def verification_select(self, select):
        if select == []:
            raise ErrorConsultNotFound('USUÁRIO NÃO ENCONTRADO')
        
    @classmethod
    def response(self, select):
        res = {}
        for name, cpf, tel, email in select:   
            res = {
                "Type": "Delete Users",
                "Count": 1,
                "User": "Deleted",
                "Attributes": {
                    "NOME": name,
                    "CPF": cpf,
                    "TELEFONE": tel,
                    "EMAIL": email
                    
                }
            }
            return res
        
    