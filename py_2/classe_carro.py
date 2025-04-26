class Carro:
    def __init__(self, modelo, cor, ano):
        self.modelo=modelo
        self.cor=cor
        self.ano=ano
    
    def ligar(self):
        print(f"o carro de modelo {self.modelo} está ligando. ")    
        #utiliza-se self.marca pois a variavel está definida apenas no __init__ (método construtor)

    def acelerar(self, velocidade):
        print(f"O carro está aelerando a {velocidade} km/h.")
    
carro1= Carro("sedan","vermelho",2020)
carro2= Carro("Palio","Marrom",2015)

print(carro1.cor)
print(carro2.modelo)

carro1.ligar()
carro2.acelerar(80)