
class ErrorConsultNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg
    
    
class IncompleteCpf(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg
    
    
class ErrorRequest(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg
    
    
class InvalidCpf(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg   
    
    
class ErrorNumberInName(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg   
    
    
class UserAlreadyRegistered(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg   
    
    
    
class ErrorLyricsInCpf(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg      


class ErrorEmail(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg     
    
    
class InvalidTel(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg     
    
    
class IncompleteTel(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg     
    
    
class NotUpdated(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.show()
        
    def show(self):
        return self.msg     