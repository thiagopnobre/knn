#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import shuffle
from copy import deepcopy

"""
Implementa o algoritmo K-NN
"""

def construir_matriz(arquivo):
  """
  Gera uma matriz de números reais, a partir de um arquivo, onde cada linha da matriz representa uma linha do arquivo
  """
  return [map(float, linha.strip().split(',')) for linha in arquivo.readlines()]


def distancia_euclidiana(lista1, lista2):
  """
  Calcula a distancia euclidiana entre a lista 1 e a lista 2
  """

  #Intercala os elementos da lista 1 com os elementos da lista 2
  lista = zip(lista1, lista2)

  somatorio = 0.0
  for elemento in lista:
    somatorio += (elemento[0]-elemento[1])**2

  return (somatorio**0.5)


def compara_matrizes(matriz_20_porcento, matriz_80_porcento, qtdDistancias):
  """
  Calcula a distância euclidiana de cada linha da matriz de teste com os 80% restantes da matriz original e retorna as
  posições das qtdDistancias menores distâncias na ordem: linha da matriz de teste e linha da matriz original
  Obs.: A classe (ultimo elemento) de cada linha da matriz original não é utilizada no cálculo da distância euclidiana
  """

  #Gera uma lista com todas as distâncias euclidianas calculadas
  distancias = []
  for linha_m20 in matriz_20_porcento:
      distancias.append([distancia_euclidiana(linha_m20, linha_m80[:-1]) for linha_m80 in matriz_80_porcento])

  #Insere a posição das qtdDistancias menores distâncias euclidianas em uma lista
  menores_distancias = []
  for i,elemento in enumerate(distancias):
    for j in xrange(qtdDistancias):
      menores_distancias.append((i,elemento.index(min(elemento))+len(matriz_20_porcento)))
      elemento[menores_distancias[-1][1]-len(matriz_20_porcento)] = float('inf')
  
  #retorna a posição das menores distâncias euclidianas
  return menores_distancias


def main():
  #Abre o arquivo e insere seus dados em uma matriz
  with open('spambase.data', 'r') as arquivo:
    matriz = construir_matriz(arquivo)

  #Embaralha as linhas da matriz de maneira aleatória
  shuffle(matriz)

  #Gera uma matriz para testes, com 20% dos elementos da matriz original
  matriz_de_teste = deepcopy(matriz[:int(len(matriz)*0.20)])

  #Remove a classe (ultimo elemento) de cada linha da matriz de teste
  for linha in matriz_de_teste:
    linha.pop()

  #Gera um lista com as distâncias euclidianas selecionadas
  k = 9
  menores_distancias = compara_matrizes(matriz_de_teste, matriz[int(len(matriz)*0.20):], k)

  #Definindo a classe dos elementos da matriz de teste
  for i in xrange(len(menores_distancias)/k):
    cont0 = 0
    cont1 = 0
    for j in xrange(k):
      if matriz[menores_distancias[0][1]][-1] == 0:
        cont0 += 1
      else:
        cont1 += 1
      menores_distancias.pop(0)
    matriz_de_teste[i].append(0 if cont0 > cont1 else 1)

  #Contando o número de acertos
  i = 0
  tamanho = len(matriz_de_teste)
  acertos = 0
  while i < tamanho:
    if matriz_de_teste[i][-1] == matriz[i][-1]:
      acertos += 1
    i += 1

  #Imprime a porcentagem de acerto
  print ("Porcentagem de acerto: "+str((acertos*100.0)/tamanho)+"%")

  return 0

if __name__ == '__main__':
  main()
