from pymprog import *
from math import *
from random import *

# bibliotecas para desenhar
from matplotlib import pyplot as plt
import matplotlib.patches as patches

def distancia(i, j):
  return sqrt((j[0] - i[0]) ** 2 + (j[1] - i[1]) ** 2)

m = 100 # máximo das coordenadas
M = 2000
coordenadas = []

arquivo = open('./instancias/inst_15.txt', mode='r') # abre o arquivo.txt
# lê o conteudo de arquivo na variável conteudo
conteudo = arquivo.read()
# fecha o arquivo
arquivo.close()

# cria a lista 'linhas', onde cada linha é definida pela quebra de linha
linhas = conteudo.split('\n')
# remove linhas vazias
linhas.remove('')
# remove os espaços nos extremos de cada linha e define cada linha como uma lista
colunas = list(map(lambda x: x.strip().split(), linhas))
linhas.clear()

# converte os dados para inteiros e atribui para coordenadas
for c in colunas:
    coordenadas.append(list(map(lambda x: int(x), c)))

colunas.clear()

del coordenadas[0]
coordenadas[0].append(0) # adicionando 0 no final da primeira coordenada
coordenadas[0].append(0) # adicionando 0 no final da primeira coordenada
coordenadas.append(coordenadas[0]) # duplicando o primeiro valor para o final

n = len(coordenadas) # número de cidades (nós)

begin('PCV')

x = var('x', iprod(range(n), range(n)), bool)
u = var('u', n)
w = var('w', n)

# função objetivo
minimize(sum(w[i] for i in range(1,n-1)))

# primeira restrição
for i in range(n-1):
    sum(x[i,j] for j in range(1,n) if i != j) == 1

# segunda restrição
for j in range(1,n):
    sum(x[i,j] for i in range(n-1) if j != i) == 1

# eliminação de sub-rotas
for i in range(n-1):
  for j in range(1,n):
    if i!=j:
    #   M = n * (distancia(coordenadas[i], coordenadas[j]) + coordenadas[i][2]) # calculo do M
      t = distancia(coordenadas[i], coordenadas[j])
      u[j] >= u[i] - M * (1 - x[i,j]) + coordenadas[i][2] + t

# quarta restrição
for i in range(1,n-1):
    w[i] >= u[i] - coordenadas[i][3]

# parametros de resolução
solver(int, tm_lim=3600*1000)
solver(int, gmi_cuts=1)

solve()

print(f"Valor ótimo PCV = {vobj():.3f}")
print()

i = 0
j = 1
cont = 0
while cont < n-1:
    while x[i,j].primal < 0.9:
        j = j+1
    print(f"{i:2d}   -->  {j:2d}")
    i = j
    j = 0
    cont = cont + 1

# plotar rota
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)
ax1.grid(False)

for i in range(n):
    for j in range(n):
        if i != j:
            if x[i,j].primal >= 0.9:
                ax1.add_patch(patches.ConnectionPatch(xyA=(coordenadas[i][0], coordenadas[i][1]), xyB=(coordenadas[j][0], coordenadas[j][1]), coordsA="data", coordsB="data", color="black"))

for i in range(0,n):
    ax1.add_patch(patches.Circle((coordenadas[i][0], coordenadas[i][1]), radius=0.03*m, color="#F4A460"))
    plt.text(coordenadas[i][0] - len(str(i)) * 0.02 * m / 2, coordenadas[i][1] - 0.02 * m / 2, str(i), {"color": "black", "fontsize": 10})

plt.ylim(-1, m+1)
plt.xlim(-1, m+1)

fig1.show()

plt.show(block=True)
plt.interactive(False)

end()