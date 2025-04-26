from funcionario import Funcionario

class Dev(Funcionario):
    def __init__(self,nome,email,salario,linguagem):
        super().__init__(nome,email,salario)
        self.linguagem = linguagem
    
    def projeto_momento(self):
        return f'Odesenvolvedor {self.nome} está em um projeto usando a linguagem {self.linguagem}'