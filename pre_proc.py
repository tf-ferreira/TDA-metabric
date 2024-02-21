import pandas as pd
import numpy as np
import os.path
from sklearn.preprocessing import StandardScaler


# Função para leitura dos dados
def leitura(nome: object) -> object:
    data = pd.read_csv(nome, on_bad_lines='skip', sep='\t', decimal='.')
    return data


# Importa os dados dos arquivos txt
dados1 = leitura('paciente.txt')
dados2 = leitura('amostra.txt')

# O arquivo amostra pode apresentar índices de pacientes duplicados
dados2.drop_duplicates(subset='PATIENT_ID', keep='first', inplace=True)

# Une os dois arquivos em um conjunto de dados
dados = dados1.merge(dados2, how='inner', on='PATIENT_ID')
dados.set_index('PATIENT_ID', inplace=True)

dados.dropna(inplace=True)

## REMOVER SAMPLE_ID
dados.drop(labels=["SAMPLE_ID"], axis=1, inplace=True)

# REMOVER SEX -> todos Female
dados.drop(labels=["SEX"], axis=1, inplace=True)

## REMOVER 'CANCER_TYPE -> SOMENTE 1
dados.drop(labels=["CANCER_TYPE"], axis=1, inplace=True)

## REMOVER 'SAMPLE_TYPE -> SOMENTE 1
dados.drop(labels=["SAMPLE_TYPE"], axis=1, inplace=True)

## REMOVER 'ONCOTREE_CODE == CANCER_TYPE_DETAILED
dados.drop(labels=["ONCOTREE_CODE"], axis=1, inplace=True)

## LINFONODOS -> 0, 1, 2 OU MAIS 
dados.loc[dados["LYMPH_NODES_EXAMINED_POSITIVE"] >= 2, ["LYMPH_NODES_EXAMINED_POSITIVE"]] = 2

# REMOVER HER2_SNP6 UNDEF, apenas 5 resultados
dados.drop(dados.loc[dados["HER2_SNP6"] == 'UNDEF'].index, inplace=True)

# REMOVER CLAUDIN_SUBTYPE NC, apenas 6 resultados
dados.drop(dados.loc[dados["CLAUDIN_SUBTYPE"] == 'NC'].index, inplace=True)


# FUNÇÃO PARA AGRUPAR DIFERENTES VALOREM EM UM SÓ
def agrupa(data, categoria, valores):
    for valor in valores:
        data.loc[data[categoria] == valor, [categoria]] = 'x'
    return data


## AGRUPA 2 SUBTIPOS COM POUCOS RESULTADOS COM APENAS "BREAST"
valores = ['Breast', 'Breast Invasive Mixed Mucinous Carcinoma', 'Breast Invasive Lobular Carcinoma']
dados = agrupa(dados, "CANCER_TYPE_DETAILED", valores)


if not os.path.exists('csv'):
    os.mkdir('csv')

## EXPORTA PRIMEIRA VERSÃO DOS DADOS
dados.to_csv(os.path.join('csv', 'data.csv'), sep=';', header=True, index=True, decimal='.')


## CONTINUOS       (Categoriza dados contínuos pelos quartis)
continuos = ["NPI", "AGE_AT_DIAGNOSIS", 'OS_MONTHS', 'RFS_MONTHS', 'TUMOR_SIZE', 'TMB_NONSYNONYMOUS']
for categoria in continuos:
    dados[categoria] = pd.qcut(dados[categoria],q=4).astype('category')

### CATEGORIZAÇÃO     (Categorização de todos os dados)
cols = dados.columns
##
for d in cols:
    dados[d] = dados[d].astype("category")
    dados[d] = dados[d].cat.codes
dados.to_csv(os.path.join('csv', 'dados_cat.csv'), sep=';', header=True, index=True, decimal='.')


## BINARIZAÇÃO       (Cria categorias binárias)
bins = dados
for i in cols:
    bins[i] = pd.to_numeric(bins[i], downcast='integer')
    bins = pd.concat([bins, pd.get_dummies(bins[i], prefix=i)], axis=1)
    bins = bins.drop(columns=i)
dados = bins
dados.to_csv(os.path.join('csv', 'dados_bin.csv'), sep=';', header=True, index=True, decimal='.')

## NORMALIZAÇÃO UTILIZANDO fit_transform()
colunas = dados.columns.tolist()
data_norm = dados
data_norm[colunas] =  StandardScaler().fit_transform(data_norm[colunas])
dados = data_norm
dados.to_csv(os.path.join('csv', 'dados_norm.csv'), sep=';', header=True, index=True, decimal='.')

## POSITIVA      (Soma o menor valor para todos resultados serem positivos)
menor = dados
menor = menor.min()
menor = menor.values
menor = menor.min()
menor = abs(menor)

for j in colunas:
    dados[j] += menor

## EXPORTA NORMALIZADOS POSITIVOS    
dados.to_csv(os.path.join('csv', 'dados_norm_pos.csv'), sep=';', header=True, index=True, decimal='.')


## EXPORTA VERSÃO FINAL DOS DADOS    
dados.to_csv(os.path.join('csv', 'dados_pp.csv'), sep=';', header=True, index=True, decimal='.')

