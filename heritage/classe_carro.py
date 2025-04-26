class Carro (object):
    def __init__(self,modelo,cor,ano):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano

    def ligar(self):
        print('O Carro está ligado.')
    
    def acelerar(self, velocidade):
        print('O carro está acelerando a {velocidade} km/h.')

# Criando objtos a partir dos objetos

carro1 = Carro('Vermelho', 'Sedan', 2020)
carro2 = Carro('Marrom', 'Palio', 2015)


# Acessando atributos dos objetos

print(carro1.cor) # Saida: Vermelho
print(carro2.modelo) # Saida: Palio


# Chamando métodos dos objetos

carro1.ligar() # saida: o carro está ligado
carro2.acelerar(80) # saida: o carro está acelerando a 80 km/h

