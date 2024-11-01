from app.interfaces.use_cases.user_register import UserRegisterInterface
from app.interfaces.user_repository import UserRepositoryInterface
from app.interfaces.redis_repository import RedisUserInterface
from typing import Dict
from app.Utils.Exceptions import IncompleteCpf, ErrorNumberInName,\
InvalidCpf, ErrorLyricsInCpf, ErrorEmail, IncompleteTel, ErrorLyricsInTel
import re


class UserRegister(UserRegisterInterface):
    def __init__(self, repository: UserRepositoryInterface, redis_repository: RedisUserInterface):
        self.user_repo = repository
        self.user_redis_repo = redis_repository
        
    def user_register(self, nome: str, cpf: str, telefone: int, email: str) -> Dict: 

            cpf_str = str(cpf)
            tele = str(telefone)
            
            self.verification_name(nome.title())
            format_cpf = self.formatation_cpf(cpf_str)
            tel = self.format_tel(tele)
            self.verification_email(email)

            self.user_redis_repo.insert_redis(nome.title(), format_cpf, tel, email)
            self.user_repo.insert(nome.title(), format_cpf, tel, email)
            response = self.response(nome.title(), format_cpf, tel, email)
            return response
        
    @classmethod
    def verification_name(self, nome: str):
        
            if len(nome) > 50:
                raise ValueError('NOME MUITO GRANDE')
            
            numbers = ['0','1','2','3','4','5','6','7','8','9']
            for number in numbers:
                if number in nome:
                    raise ErrorNumberInName("ONOME NÃO DEVE CONTER NÚMEROS") 

    @classmethod
    def formatation_cpf(self, cpf: str):
                if cpf == '000.000.000-00':
                    raise InvalidCpf("CPF INVÁLIDO")
                
                else:
                        abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ç']
                        for letra in abc:
                            if letra in cpf or letra.upper() in cpf:
                                raise ErrorLyricsInCpf('O CPF NÃO DEVE CONTER LETRAS')
                            else:
                                pass
                        format = re.compile('[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}')
                        finder = format.match(cpf)
                        
                        if finder == None:
                                if len(cpf) == 11:
                                    try:
                                        cpf_format = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
                                        return cpf_format
                                    except:
                                        InvalidCpf('CPF INVÁLIDO')
                                elif len(cpf) > 11:
                                    raise IncompleteCpf("CPF MUITO GRANDE")
                                    
                                elif len(cpf) < 11:
                                    raise IncompleteCpf("CPF INCOMPLETO")
                        else:
                            return cpf


        
    @classmethod
    def verification_email(self, email):

            g = '@'
            outlook = 'outlook.com'
            gmail = 'gmail.com'
            if g in email:
                if gmail in email or outlook in email:
                    return email
            raise ErrorEmail('O CAMPO DEVE CONTER O ENDEREÇO DE EMAIL')
    
    def format_tel(self, telefone: str):
            abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ç']
            for letra in abc:
                if letra in telefone or letra.upper() in telefone:
                    raise ErrorLyricsInTel('O TELEFONE NÃO DEVE CONTER LETRAS')
                
            if len(telefone) == 11:
                format = '({}) {}-{}'.format(telefone[:2], telefone[2:7], telefone[7:])
                return format
            elif len(telefone) < 11:
                raise IncompleteTel('TELEFONE INCOMPLETO')
            else:
                raise IncompleteTel('TELEFONE MUITO GRANDE')

    @classmethod
    def response(self, nome, cpf, telefone, email):
        
        response = {
            "Type": 'Users',
            'Count': 1,
            'User': 'Registered',
            'Attributes':{
                "NOME": nome,
                "CPF": cpf,
                "TELEFONE": telefone,
                "EMAIL": email
            }
            }
        
        return response
    
    