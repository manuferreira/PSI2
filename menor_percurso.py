from distancia_pontos import pontos


def permutations(cidades):
    result = []

    if len(cidades) == 1:
        result.append(cidades)
        return result

    else:
        perms = permutations(cidades[1:])
        caractere = cidades[0:1]

        for perm in perms:
            for i in range(len(cidades)):
                result.append(perm[:i] + caractere + perm[i:])
    return result


def distancia_minima(result, origem='R'):
    min_dist = None
    min_percurso = None

    for percurso in result:
        k = origem

        distancia_atual = 0

        for i in percurso:
            distancia_atual += dicionario[k][i]
            k = i

        distancia_atual += dicionario[k][origem]

        if min_dist is None or min_dist >= distancia_atual:
            min_dist = distancia_atual
            min_percurso = percurso

    return min_percurso


lista_matriz = []

with open('matriz.txt', 'r') as matriz:
    for line in matriz:
        linha = []
        for i in line:
            if i != '\n' and i != ' ':
                linha.append(i)
        lista_matriz.append(linha)


dicionario = pontos(lista_matriz)

cidades = []
for i in dicionario.keys():
    if i == 'R':
        continue
    cidades.append(i)


resultado = permutations(cidades)
menor_percurso = distancia_minima(resultado)
res = ' '.join(menor_percurso)
print(res)
