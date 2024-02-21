import pandas as pd
import numpy as np
import os.path




# Função para leitura dos dados
def leitura(nome: object) -> object:
    data = pd.read_csv(nome, on_bad_lines='skip', sep=';', decimal='.')
    return data

dados = leitura("csv/dados_norm_pos.csv")
dados.set_index('PATIENT_ID', inplace=True)

i=0
j=0

n = len(dados)
matriz_dist = np.zeros((n,n))

for id1 in dados.index:
    for id2 in dados.index:
        if i<j:
            v1 = dados.loc[id1]
            v2 = dados.loc[id2]
            matriz_dist[i,j] = np.sum([ abs(a-b) for a,b in zip(v1,v2)])
            matriz_dist[j,i] = matriz_dist[i,j]         
        j +=1    
    j=0
    i +=1

distancias = pd.DataFrame(matriz_dist,dados.index,dados.index)
if not os.path.exists('dist'):
    os.mkdir('dist')
distancias.to_csv("dist/dist_direta_com_norm_l1.csv",header=True,index=True, decimal='.')











