import pandas as pd
import numpy as np
import os.path

tipo = 'sem_norm'


dados = pd.read_csv('csv/dados_norm_pos.csv',
                    on_bad_lines='skip',sep=';',header=0, decimal='.',index_col=0)
data = dados.reset_index()

if not os.path.exists('pointclouds'):
    os.mkdir('pointclouds')

if not os.path.exists('pointclouds/'+tipo):
    os.mkdir('pointclouds/'+tipo)



# variáveis auxiliares no processo
n_lines = dados.shape[0]
n_cols = dados.shape[1]
nome = ''
contador = 0 # Variável para acompanhar o progresso


for i in range(0,n_lines):
    irow = data.iloc[[i]]

    # Copia os dados de um paciente para a linha inicial da nuvem de pontos
    pointcloud = irow.copy() 

    # O nome do arquivo será o código do paciente
    nome = pointcloud.iat[0,0]
    pointcloud.drop(['PATIENT_ID'],axis=1,inplace=True)

    # Para cada linha da nuvem de pontos uma das colunas é zerada
    for j in range(0,n_cols):
        newrow = irow.copy()
        newrow.drop(['PATIENT_ID'],axis=1,inplace=True)
        newrow.iat[0,j] = 0
        pointcloud = pd.concat([pointcloud,newrow])

    # Exporta a nuvem de pontos como csv     
    pointcloud.to_csv(os.path.join('pointclouds/'+tipo,
                	nome+'.csv'),header=False,index=False, decimal='.')

    # Procedimento para acompanhar o progresso
    print('\r',end="")
    print(round((contador/n_lines)*100),'%',end="")
    contador += 1
