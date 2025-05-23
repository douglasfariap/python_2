from functools import reduce

def uso_reduce(lista:list) -> int: #
    '''
    Recebe uma lista de inteiros e retorna a soma de todols os elementos da lista.
    args: a soma de todos os elementos da lista
    '''
    return reduce(lambda x,y: x+y, lista)

def uso_map(lista:list) -> list:
    '''
    Recebe uma lista de inteiros e retorna uma nova lista com os quadrados dos elementos da lista

    '''
    return list(map(lambda x:x**2, lista))

def uso_filter(lista:list) -> list:
    '''
    recebe uma lista de inteiros e retorna uma nova lista aplicando o filtro da funcao lambda
    que no caso é avaliar se o item da lista/2 resta zero, caso verdadeiro, guarda o elemento, caso não, ignora
    '''
    return list(filter(lambda x: x%2 ==0, lista))

if __name__ == '__main__':
    lista = [1,2,3,4]
    soma = uso_reduce(lista)
    print(soma)

    mapa= uso_map(lista)
    print(mapa)