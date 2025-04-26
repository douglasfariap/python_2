class Pessoa:
    def __init__ (self, nome, idade,time):
        self.nome = nome
        self.__idade = idade
        self._time = time

    def exibir_informacoes(self):
        return f"Nome: {self.nome},Time: {self._time}, Idade: {self.__idade}"
    
