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

dis = distancia(coordenadas[0], coordenadas[1])

n = len(coordenadas) # número de cidades (nós)