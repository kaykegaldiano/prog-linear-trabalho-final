from pymprog import*
from math import*
from random import*

# bibliotecas para desenhar
# from matplotlib import pyplot as plt
# import matplotlib.patches as patches

distancias = []

def distancia(i, j):
    aux = sqrt((j[0] - i[0]) ** 2 + (j[1] - i [1]) ** 2)
    distancias.append(aux)
    return aux

m = 100 # máximo das coordenadas
M = 100000
coordenadas = []

f = open('./instancias/inst_10.txt') # lendo o arquivo com as instâncias

lines = f.read()
splited_lines = lines.splitlines()
for row in splited_lines:
    aux = []
    for i in row.split(' '):
        if (i != ''):
            aux.append(int(i))
    coordenadas.append(aux)

del coordenadas[0]

coordenadas.append(coordenadas[0]) # duplicando o primeiro valor para o final
coordenadas[0].append(0) # adicionando 0 no final da primeira coordenada

dis = distancia(coordenadas[0], coordenadas[1])

n = len(coordenadas) # número de cidades (nós)

begin('PCV')

x = var('x', iprod(range(n), range(n)), bool)
u = var('u', n)
w = var('w', n)

# função objetivo
minimize(sum(w[i] for i in range(1,n-1)))

# restrições

# primeira restrição
for i in range(n-1):
    sum(x[i,j] for j in range(1,n) if i != j) == 1

# segunda restrição
for j in range(1,n):
    sum(x[i,j] for i in range(n -1) if i != j) == 1

# eliminação de sub-rotas
for i in range(n-1):
  for j in range(1,n):
    if i!=j:
      u[j] >= u[i] - M * (1 - x[i,j]) + coordenadas[i][2] + distancia(coordenadas[i], coordenadas[j])

for i in range(1,n-1):
    w[i] >= u[i] - coordenadas[i][3]

# parametros de resolução
solver(int, tm_lim=3600*1000)
solver(int, gmi_cuts=1)

solve()