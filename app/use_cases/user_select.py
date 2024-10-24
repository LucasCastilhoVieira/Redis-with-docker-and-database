from app.interfaces.use_cases.user_select import UserSelectInfoInterface
from app.interfaces.user_repository import UserRepositoryInterface
import re
from typing import Dict
from app.Utils.Exceptions import ErrorConsultNotFound, IncompleteCpf, InvalidCpf, ErrorLyricsInCpf





class UserInfo(UserSelectInfoInterface):
    
    def __init__(self, repository: UserRepositoryInterface):
        self.user_repo = repository
        
    def select_user(self, cpf: str) -> Dict:
        cpf_user = self.cpf_format(cpf)
        
        
        users = self.user_repo
        select = users.select(cpf_user)
        self.verification_select(select)
        response = self.format_response(select)
        return response
    
    
    @classmethod
    def cpf_format(self, cpf):
            format = re.compile('[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}')
            finder = format.match(cpf)
            abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ç']
            for letra in abc:
                if letra in cpf or letra.upper() in cpf:
                    raise ErrorLyricsInCpf('O CPF NÃO DEVE CONTER LETRAS! PARA CONSULTA, DIGITE APENAS NÚMEROS.')
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
    def format_response(self, select):
        for name, cpf, telefone, email in select:
            
            response = {
                "Type": "Consult Users",
                "Count": 1,
                "User": "Found",
                "Info": {
                    "nome": name,
                    "cpf": cpf,
                    "telefone": telefone,
                    "email": email
                }
                
            }

            return response
            
        
        
