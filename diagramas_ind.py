import numpy as np 
import gudhi as gd 
import pandas as pd
import pickle as pickle
import os.path

tipo1 = 'com_norm'
tipo2 = 'dist_indireta_'+tipo1+'_l1'

dados = pd.read_csv('csv/dados_norm_pos.csv',on_bad_lines='skip',
                    sep=';',header=0, decimal='.',index_col=0)



# Variáveis auxiliares
prefixo = 'pointclouds/'+tipo1+'/'
diagramas = {}
ids = dados.index
contador = 1 # Variável para acompanhar o progresso

for i in ids:
    # Leitura da nuvem de pontos do paciente
    nome = prefixo+i+'.csv'
    pontos = pd.read_csv(nome,on_bad_lines='skip',sep=',',header=None)
    
    # Transforma o dataframe em matriz
    matriz = np.array(pontos)
    
    # Cria o driagrama de Rips
    rips_complex = gd.RipsComplex(points=matriz, max_edge_length=1000.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=(1))
    simplex_tree.persistence()
    
    #Retorna o diagrama apenas na dimensão 0
    diag = simplex_tree.persistence_intervals_in_dimension(0)
 
	# Insere o resultado no dicionario diagramas
    diagramas[i] = diag
    
    # Procedimento para acompanhar o progresso
    print('\r',end="")
    print(round((contador/len(ids))*100),'%',end="")
    contador += 1

if not os.path.exists('diagramas_individuais'):
	os.mkdir('diagramas_individuais')
file = open('diagramas_individuais/'+tipo2, 'wb')
pickle.dump(diagramas, file)
file.close()