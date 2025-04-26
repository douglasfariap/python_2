class Pessoa:
    def __init__(self, nome, idade):
        self.nome=nome
        self.__idade=idade
    
    def __repr__(self):
        return f"Nome: {self.nome}, idade: {self.idade}"

    def get_idade(self):
        return self.__idade

    def set_idade(self, nova_idade):
        if nova_idade > 0:
            self.__idade = nova_idade
        else:
            print("idade invalida")

pessoa= Pessoa("Douglas",32)
print(pessoa.nome)
print(pessoa.get_idade())
pessoa.set_idade(30)
print(pessoa.get_idade())
pessoa.set_idade(-5)