def pontos(lista_matriz):
    vertices = []

    for index, linha in enumerate(lista_matriz):
        for pos, elem in enumerate(linha):
            if elem != '0':
                ponto = (elem, index, pos)
                vertices.append(ponto)

    return calcula_distancia(vertices)


def calcula_distancia(vertices):
    cities = {}
    city = {}
    for elem in vertices:
        key = elem[0]
        x = elem[1]
        y = elem[2]

        for elem_next in vertices:
            if elem_next[0] == key:
                continue
            else:
                other_key = elem_next[0]
                other_x = elem_next[1]
                other_y = elem_next[2]
                soma = abs(x - other_x) + abs(y - other_y)
                city[other_key] = soma
        cities[key] = city
        city = {}
    return cities
