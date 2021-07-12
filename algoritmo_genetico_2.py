import random

class Cidade:
    def __init__(self, nome_cidade, x, y):
        self.nome_cidade = nome_cidade
        self.x = x
        self.y = y

    def distancia(self, cidade):
        eixo_x = abs(self.x - cidade.x)
        eixo_y = abs(self.y - cidade.y)
        return eixo_x + eixo_y

    def __repr__(self):
        return f'({self.nome_cidade}, {self.x}, {self.y})'

    def __getitem__(self, indice):
        if indice == 0:
            return self.nome_cidade

        elif indice == 1:
            return self.x

        elif indice == 2:
            return self.y

    

class Fitness:
    def __init__(self, rota):
        self.rota = rota
        self.distância = 0
        self.fitness = 0.0

    def distancia_rota(self):
        distancia_caminho = 0
        for i in range(0, len(self.rota)):
            da_cidade = self.rota[i]
            até_cidade = None


            if i + 1 < len(self.rota):
                até_cidade = self.rota[i + 1]

            else:
                até_cidade = self.rota[0]

            
            distancia_caminho += da_cidade.distancia(até_cidade)

        self.distância = distancia_caminho

        return self.distância



   
    def fitness_rota(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.distancia_rota())
        return self.fitness
        
        


# ================ ENTRADA =====================
lista_matriz = []

#lê a entrada
with open('matriz.txt', 'r') as matriz:
    for line in matriz:
        linha = []
        for i in line:
            if i != '\n' and i != ' ':
                linha.append(i)
        lista_matriz.append(linha)


def pontos(lista_matriz):
    vertices = []

    for index, linha in enumerate(lista_matriz):
        for pos, elem in enumerate(linha):
            if elem != '0':
                ponto = (elem, index, pos)
                vertices.append(ponto)

    return vertices


vertices = pontos(lista_matriz)


lista_cidades = []
for cidade in vertices:
    if cidade[0] == 'R':
        cidade_partida = Cidade(cidade[0], cidade[1], cidade[2])

    else:
        lista_cidades.append(Cidade(cidade[0], cidade[1], cidade[2]))



def cria_rota(lista_cidades):
    rota = random.sample(lista_cidades, len(lista_cidades))

    rota.insert(0, cidade_partida)
    return rota


def população_primária(lista_cidades, tam_pop):
    população = []

    for i in range(0, tam_pop):
        população.append(cria_rota(lista_cidades))
    return população



def classificacao_rotas(população):
    resultados_fitness = {}
    for i in range(0, len(população)):
        rota = população[i]
        resultados_fitness[i] = Fitness(rota).fitness_rota()
    return sorted(resultados_fitness.items(), key=lambda x: x[1], reverse=True)



def seleção_torneio(pop_classificada, tam_elitismo):
    resultado_torneio = []
    tam_população = len(pop_classificada)

    for i in range(0, tam_elitismo):
        resultado_torneio.append(pop_classificada[i])


    for j in range(0, len(pop_classificada) - tam_elitismo):
        individuo_1 = pop_classificada[random.randint(0, tam_população-1)]
        individuo_2 = pop_classificada[random.randint(0, tam_população-1)]
        
        individuo_1_fitness = individuo_1[1]
        individuo_2_fitness = individuo_2[1]

        if individuo_1_fitness >= individuo_2_fitness:
            resultado_torneio.append(individuo_1)
        else:
            resultado_torneio.append(individuo_2)
    return resultado_torneio



def individuos_selecionados(população, resultado_torneio):
    selecionados = []
    for i in range(0, len(resultado_torneio)):
        índice = resultado_torneio[i][0]
        selecionados.append(população[índice])
    return selecionados



def cruzamento(parente_1, parente_2):
    filho = []
    filho_1 = []
    filho_2 = []

    gene_a = int(random.random() * len(parente_1))
    gene_b = int(random.random() * len(parente_2))

    gene_inicial = min(gene_a, gene_b)
    gene_final = max(gene_a, gene_b)

    filho_1.append(cidade_partida)

    for i in range(gene_inicial, gene_final):
        if cidade_partida == parente_1[i]:
            continue
        else:
            filho_1.append(parente_1[i])

    for j in range(len(parente_2)):
        if cidade_partida == parente_2[j]:
            continue
        elif parente_2[j] not in filho_1:
            filho_2.append(parente_2[j])

    filho = filho_1 + filho_2
    return filho


def cruzamento_população(selecionados, tam_elitismo):
    filhos = []
    tamanho = len(selecionados) - tam_elitismo
    porção = random.sample(selecionados, len(selecionados))

    for i in range(0, tam_elitismo):
        filhos.append(selecionados[i])

    for j in range(0, tamanho):
        filho = cruzamento(porção[j], porção[len(selecionados)-i-1])
        filhos.append(filho)
    return filhos



def mutação(individuo, taxa_mutação):
    for indice_cidade in range(1, len(individuo)):
        if random.random() < taxa_mutação:
            cidade_troca = int(random.random() * len(individuo))
            while cidade_troca == 0:
                cidade_troca = int(random.random() * len(individuo))

            cidade_1 = individuo[indice_cidade]
            cidade_2 = individuo[cidade_troca]

            individuo[indice_cidade] = cidade_2
            individuo[cidade_troca] = cidade_1

    return individuo


def mutação_população(população, taxa_mutação):
    população_mutada = []
    for indice_individuo in range(0, len(população)):
        individuo_mutado = mutação(população[indice_individuo], taxa_mutação)
        população_mutada.append(individuo_mutado)
    return população_mutada



def nova_geração(população_atual, tamanho_elistimo, taxa_mutação):
    população_classificada = classificacao_rotas(população_atual)
    resultado_do_torneio = seleção_torneio(população_classificada, tamanho_elistimo)
    individuos_selecionados_torneio = individuos_selecionados(população_atual, resultado_do_torneio)
    filhos = cruzamento_população(individuos_selecionados_torneio, tamanho_elistimo)
    nova_geração = mutação_população(filhos, taxa_mutação)
    return nova_geração    


quantidade_gerações = 300
tamanho_elitismo = 20
taxa_mutação = 0.001
tamanho_população = 200
população_atual = população_primária(lista_cidades, tamanho_população)

for i in range(0, quantidade_gerações):
    população_atual = nova_geração(população_atual, tamanho_elitismo, taxa_mutação)
    
indice = classificacao_rotas(população_atual)[0][0]
melhor_rota = população_atual[indice]
print(f'Distância: {1/ classificacao_rotas(população_atual)[0][1]}')

for i in range(len(melhor_rota)):
    print(melhor_rota[i][0], end=' ')



# print(lista_cidades)
# print(cidade_partida)
# população = população_primária(lista_cidades, 3)
# print(população)
# pop_classificada = classificacao_rotas(população)
# print(pop_classificada)
# resultado_torneio = seleção_torneio(pop_classificada, 1)
# print(resultado_torneio)
# selecionados = individuos_selecionados(população, resultado_torneio)
# print(cruzamento_população(selecionados, 1))
# print(mutação_população(população, 0.5))

