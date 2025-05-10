from functools import reduce

def uso_reduce(lista:list) -> int:

    return reduce(lambda x,y:x+y,lista)

def uso_map(lista:list) -> list:
    return list(map(lambda x:x**2,lista))

def uso_filter(lista:list) ->list:

    return list(filter(lambda x:x%2==0,lista))

if __name__ =='__main__':
    lista=[1,2,3,4,5]
    soma= uso_reduce(lista)
    lista_quadrados = uso_map(lista)
    pares= uso_filter(lista)

    print(f'Resultado do uso_reduce: {soma} \nResultadodo uso_map: {lista_quadrados} \nResultado do uso_filter: {pares}')