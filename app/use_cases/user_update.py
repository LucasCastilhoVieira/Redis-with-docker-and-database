from app.interfaces.use_cases.user_update import UserUpdateInterface
from app.interfaces.user_repository import UserRepositoryInterface
from typing import Dict
from app.Utils.Exceptions import ErrorLyricsInCpf, InvalidCpf, IncompleteCpf, IncompleteTel, InvalidTel, ErrorEmail, NotUpdated, ErrorConsultNotFound
import re


class UserUpdate(UserUpdateInterface):
    def __init__(self, repository: UserRepositoryInterface):
        self.user_repository = repository
        
    def info_before(self, cpf: str):
        select = self.user_repository.select(cpf)
        return select
        
    def update_user(self, cpf: str, telefone: str, email: str) -> Dict:
        cpf_format = self.formatation_cpf(cpf)
        select_before = self.info_before(cpf_format)
        
        self.verification_select(select_before)
        tel = self.format_tel(telefone)
        self.verification_email(email)
        
        response = self.response(select_before, tel, email)
        self.user_repository.update_user(cpf_format, email, tel)       
        return response
    
    
    @classmethod
    def verification_select(self, select):
        if select == []:
            raise ErrorConsultNotFound('USUÁRIO NÃO ENCONTRADO')
    
    
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
                            raise IncompleteCpf('CPF MUITO GRANDE')
                            
                        elif len(cpf) < 11:
                            raise IncompleteCpf('CPF INCOMPLETO')
                else:
                    return cpf
                
    @classmethod
    def format_tel(self, telefone: str):
        if telefone == '':
            return telefone
        else:
                if len(telefone) == 11:
                    try:
                        format = '({}) {}-{}'.format(telefone[:2], telefone[2:7], telefone[7:])
                        return format
                    except:
                        raise InvalidTel('TELEFONE INVÁLIDO')
                elif len(telefone) < 11:
                    raise IncompleteTel('TELEFONE INCOMPLETO')
                elif len(telefone) > 11:
                    raise IncompleteTel('TELEFONE MUITO GRANDE')
    
    @classmethod
    def verification_email(self, email):
            if email == '':
                return email
            else:
                g = '@'
                outlook = 'outlook.com'
                gmail = 'gmail.com'
                if g in email:
                    if gmail in email or outlook in email:
                        return email
                raise ErrorEmail('O CAMPO DEVE CONTER O ENDEREÇO DE EMAIL')
            
            
    @classmethod
    def response(self, select_before, tel, email):
        res = {}
        count = 2
        for name, cpf, tel_before, email_before in select_before:
            while not tel and not email:
                tel = tel_before
                email = email_before
                count = 0
            else:
                if not tel:
                    tel = tel_before
                    count = count - 1
                else:
                    pass
            
                if not email:
                    email = email_before
                    count = count - 1
                else: 
                    pass

            if count == 0:
                raise NotUpdated("SEM ATUALIZAÇÕES DO USUÁRIO")
                
            res = {
                "Type": "Update Users",
                "Count": count,
                "User": "Updated",
                "Attributes": {
                    "NOME": name,
                    "CPF": cpf,
                    "TELEFONE": f"{tel_before} -> {tel}",
                    "EMAIL": f"{email_before} -> {email}"
                    
                }
            }
            return res
        