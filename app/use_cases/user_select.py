from app.interfaces.use_cases.user_select import UserSelectInfoInterface
from app.interfaces.user_repository import UserRepositoryInterface
import re
from typing import Dict
from app.Utils.Exceptions import ErrorConsultNotFound, IncompleteCpf, InvalidCpf, ErrorLyricsInCpf
from app.interfaces.redis_repository import RedisUserInterface





class UserInfo(UserSelectInfoInterface):
    
    def __init__(self, repository: UserRepositoryInterface, redis_repository: RedisUserInterface):
        self.user_repo = repository
        self.user_redis_repo = redis_repository
        
        
        
        
    def select_user(self, cpf: str) -> Dict:
        cpf_user = self.cpf_format(cpf)
        select_redis = self.user_redis_repo.search_user_on_redis(cpf_user)
        info = self.verification_select_redis(select_redis, cpf_user)
       
        return info

        
    
    
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
        



    def verification_select_redis(self, select_redis, cpf):
            if select_redis == None:
                select_database = self.user_repo.select(cpf)
                self.verification_select_database(select_database)
                for name, cpf, telefone, email in select_database:
                    self.user_redis_repo.insert_redis(name, cpf, telefone, email)
                response = self.format_response_database(select_database)
                return response
            else:
                res = self.format_response_redis(select_redis)
                return res
        
    @classmethod
    def verification_select_database(self, select):
        if select == []:
            raise ErrorConsultNotFound('USUÁRIO NÃO ENCONTRADO')
    
    
    
    @classmethod
    def format_response_redis(self, select):
            
            response = {
                "Where": "Redis",
                "Type": "Consult Users",
                "Count": 1,
                "User": "Found",
                "Info": {
                    "nome": select['nome'],
                    "cpf": select['cpf'],
                    "telefone": select['telefone'],
                    "email": select['email']
                }
                
            }

            return response
            
            
    @classmethod
    def format_response_database(self, select):
        for name, cpf, telefone, email in select:
            
            response = {
                "Where": "Database",
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
            
        
        
        
