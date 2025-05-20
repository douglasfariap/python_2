from funcionario import Funcionario

class Gerente(Funcionario):
    def __init__(self,nome,email,salario,departamento):
        super().__init__(nome,email,salario)
        self.departamento=departamento
    
    def definir_metas(self):
        return 0