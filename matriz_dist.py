import numpy as np 
import gudhi as gd 
from gudhi.wasserstein import wasserstein_distance
import pandas as pd
import matplotlib.pyplot as plt 
import os.path
import pickle as pickle


tipo = 'dist_indireta_sem_norm_l1'

ordem = 1
p = 1

dados = pd.read_csv('csv/dados_norm_pos.csv',on_bad_lines='skip',
                    sep=';',header=0, decimal='.',index_col=0)



file = open('diagramas_individuais/'+tipo, 'rb')
diagramas = pickle.load(file)
file.close()


# Variáveis auxiliares
n = len(dados)
matriz_dist = np.zeros((n,n))
i=0
j=0
total = len(dados)*len(dados)/2
contador = 1 # Variável para acompanhar o prgresso

for id1 in dados.index:
    for id2 in dados.index:
        if i<j:
            #matriz_dist[i,j] = gd.bottleneck_distance(diagramas[id1],diagramas[id2])
            matriz_dist[i,j] = wasserstein_distance(diagramas[id1],diagramas[id2], order=ordem, internal_p=p)
            matriz_dist[j,i] = matriz_dist[i,j]			
            contador+=1
        j +=1    
    
    # Procedimento para acompanhar o progresso
    print('\r',end="")
    print(round((contador/total)*100),'%',end="")
    contador += 1
    
    j=0
    i +=1


distancias = pd.DataFrame(matriz_dist,dados.index,dados.index)
if not os.path.exists('dist'):
    os.mkdir('dist')
distancias.to_csv("dist/"+tipo+".csv",header=True,index=True)
