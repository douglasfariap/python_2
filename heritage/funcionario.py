class Funcionario():
    def __init__(self, nome,email,salario):
        self.nome=nome
        self.email=email
        self.salario=salario
    
    def calcula_salario(self):
        return self.salario

