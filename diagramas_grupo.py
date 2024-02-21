import numpy as np 
import gudhi as gd 
import pandas as pd
import matplotlib.pyplot as plt 
import os.path
import pickle as pickle

nome = 'dist_indireta_sem_norm_l1'

# Leitura dos dados categorizados
dados = pd.read_csv('csv/dados_cat.csv',on_bad_lines='skip',
                    sep=';',header=0, decimal='.',index_col=0)

'''
binarios = []
for i in dados.columns:
	if len(dados[i].value_counts()) == 2:
		binarios.append(i)
'''

binarios = dados.columns


if not os.path.exists('diagramas'):
	os.mkdir('diagramas')

diretorio = 'diagramas/'+ nome

# Leitura dos dados categorizados
dados = pd.read_csv('csv/dados_cat.csv',on_bad_lines='skip',
                    sep=';',header=0, decimal='.',index_col=0)

# Leitura da matriz de distâncias
matriz_df = pd.read_csv('dist/'+nome+'.csv',
 decimal='.',on_bad_lines='skip',sep=',',header=0,index_col=0)


# Variáveis auxiliares
prefixo = ''
contador = 0


if not os.path.exists(diretorio):
	os.mkdir(diretorio)

############################################################################# 
##                               CICLO ATRIBUTOS                           ##
#############################################################################
# Aqui será criado um diag de persistência e um Barcode para cada grupo de cada atributo
for atributo in binarios:
	contador = 0

	prefixo=diretorio+'/'+atributo+'/'

	if not os.path.exists(prefixo):
		os.mkdir(prefixo)

	# Variável contendo os índices dos grupos de cada atributo
	grupos = dados[atributo].value_counts().index
	diagramas = {}
	diagramas0 = {}
	diagramas1 = {}
	######################################################################### 
	##                          CICLO GUPOS                                ##
	#########################################################################
	for gp in grupos:
		contador += 1

		grupo = dados.loc[dados[atributo]==gp]
	
		# Monta a matriz de distâncias de um grupo em específico
		matriz = np.array(matriz_df.loc[grupo.index])

		# Cria o driagrama de Rips com dimensão máxima dada por 'dim'
		rips_complex = gd.RipsComplex(distance_matrix=matriz ,max_edge_length=100)
		simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
		diag = simplex_tree.persistence()
		
		diag0 = simplex_tree.persistence_intervals_in_dimension(0) 
		diag1 = simplex_tree.persistence_intervals_in_dimension(1) 

		diagramas[gp] = diag
		diagramas0[gp] = diag0
		diagramas1[gp] = diag1

		# Impressão para acompanhar o progresso
		print(atributo,":",str(contador),"/",str(len(grupos)))

	## DOC TODAS DIM
	# open a file, where you ant to store the data
	nome = prefixo+str(atributo)
	file = open(nome, 'wb')
	# dump information to that file
	pickle.dump(diagramas, file)
	# close the file
	file.close()

	## DOC DIM 0
	# open a file, where you ant to store the data
	nome0 = nome+'_dim0'
	file = open(nome0, 'wb')
	# dump information to that file
	pickle.dump(diagramas0, file)
	# close the file
	file.close()	

	## DOC DIM 1
	# open a file, where you ant to store the data
	nome1 = nome+'_dim1'
	file = open(nome1, 'wb')
	# dump information to that file
	pickle.dump(diagramas1, file)
	# close the file
	file.close()

