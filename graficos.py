import numpy as np 
import gudhi as gd 
import pandas as pd
import matplotlib.pyplot as plt 
import os.path
import pickle as pickle
from gudhi.wasserstein import wasserstein_distance

# Leitura dos dados categorizados
dados = pd.read_csv('csv/dados_cat.csv',on_bad_lines='skip',
                    sep=';',header=0, decimal='.',index_col=0)
'''
vetor_atributos = []
for i in dados.columns:
    if len(dados[i].value_counts()) == 2:
        vetor_atributos.append(i)
'''

vetor_atributos = dados.columns

# Função para abrir arquivos pickle
def openPickle(nome,atributo,dim):
    nome = 'diagramas/'+nome+'/'+atributo+'/'+atributo+'_dim'+str(dim)    
    file = open(nome, 'rb')
    arquivo = pickle.load(file)
    file.close()
    return arquivo

def dicioPercentual(dicionario,percentual):
    dicionario_red = {}
    for ind,diagram in dicionario.items():
        diagram = dicionario[ind]
        
        #Constroi um dicionario com os varores ordenados do tempo de vida para cada respectivo índice
        dists = {i:diagram[i,1]-diagram[i,0] for i in range(len(diagram))}
        ordenado = {k: v for k, v in sorted(dists.items(), key=lambda item: item[1])}
        
        #Define o número de pontos remanescentes de acordo com o percentual
        num_pt = int(len(diagram)*percentual)
        
        #Define uma lista com os indices dos pontos escolhidos
        lista = list(ordenado.keys())
        lista = lista[-num_pt:]
        
        #Constroi uma lista como o diagrama apenas dos pontos selecionados
        diagrama_aux = [diagram[i] for i in lista]
        diagrama_aux = np.array(diagrama_aux)
        
        #Insere o diagrama em sua respectiva posição no dicionário de acordo com seu grupo
        dicionario_red[ind] = diagrama_aux
    
    return dicionario_red

def uniao(diag0,diag1):
    diagrama0 = [(0,i) for i in diag0]
    diagrama1 = [(1,i) for i in diag1]
    return diagrama0+diagrama1


def plotDiag(dicio0,dicio1,diretorio,atributo):

    dicio_leg = {
    'LYMPH_NODES_EXAMINED_POSITIVE':['Number of lymph nodes examined positive','Zero', 'Two or More','One'],
    'CELLULARITY':['Tumor cellularity','High','Moderate','Low'],
    'CHEMOTHERAPY':['Chemotherapy','No','Yes'],
    'COHORT':['Cohort','3','1','2','5'],
    'ER_IHC':['Estrogen Receptor Status by IHC','Positive','Negative'],
    'HER2_SNP6':['Human Epidermal growth factor Receptor-type 2 by SNP6','Neutral','Gain','Loss'],
    'HORMONE_THERAPY':['Hormone Therapy','Yes','No'],
    'INFERRED_MENOPAUSAL_STATE':['Inferred Menopausal State','Post','Pre'],
    'OS_STATUS':['Overall Survival Status','Deceased','Living'],
    'CLAUDIN_SUBTYPE':['Claudin Subtype','LumA','LumB','claudin-low','Her2','Basal','Normal'],
    'THREEGENE':['3-Gene classifier subtype','ER+,HER2- Low Prolif','ER+,HER2- High Prolif','ER-,HER2-','HER2+'],
    'VITAL_STATUS':['Patient\'s Vital Status','Living','Died of Disease','Died of Other Causes'],
    'LATERALITY':['Laterality','Left','Right'],
    'RADIO_THERAPY':['Radio Therapy','Yes','No'],
    'HISTOLOGICAL_SUBTYPE':['Tumor\'s Histologic Subtype','Ductal,NST','Mixed','Lobular','Tubular,cribriform','Mucinous','Medullary','Other'],
    'BREAST_SURGERY':['Type of Breast Surgery','Mastectomy','Breast Conserving'],
    'RFS_STATUS':['Relapse Free Status','Not Recurred','Recurred'],
    'INTCLUST':['Integrative Cluster','3','8','4ER+','10','7','5','1','9','6','2','4ER-'],
    'CANCER_TYPE_DETAILED':['Cancer Type Detailed','Breast Invasive Ductal Carcinoma','Breast Mixed Ductal and Lobular Carcinoma','Other'],
    'ER_STATUS':['Estrogen Receptor Status','Positive','Negative'],
    'HER2_STATUS':['Human Epidermal growth factor Receptor-type 2','Negative','Positive'],
    'GRADE':['Grade','3','2','1'],
    'PR_STATUS':['Progesterone Receptor','Positive','Negative'],
    'TUMOR_STAGE':['Tumor Stage','2','1','3','4'],
    'NPI':['Nottingham Prognostic Index','0->3','3->4','4->5','5 or High'],
    'AGE_AT_DIAGNOSIS':['Age at Diagnosis','Up to 50 years old','50 to 61 years old','61 to 70 years old','Over 70 years old'],
    'OS_MONTHS':['Overall Survival in Months Since Initial Diagonosis','Up to 60.5','60.5 to 116','116 to 187.1','187.1 or High'],
    'RFS_MONTHS':['Time Until Last Follow-up or Relapse (in months)','Up to 40.9','40.9 to 98.7','98.7 to 172.4','172.4 or High'],
    'TUMOR_SIZE':['Tumor Size','Up tp 17','17 to 22','22 to 30', '30 or Larger'],
    'TMB_NONSYNONYMOUS':['Tumor Mutational Burden','Up to 3.9','3.9 to 6.5','6.5 to 9.1', '9.1 or High']
    }

    vec = dicio_leg[atributo]
    numero = len(vec)-1

    dicio0_red = dicioPercentual(dicio0,percentual)
    dicio1_red = dicioPercentual(dicio1,percentual)

    for i in range(numero):
        gd.plot_persistence_diagram(uniao(dicio0[i],dicio1[i]),legend=True)
        plt.title(vec[i+1])
        plt.savefig(diretorio + '/' + vec[i+1] + '.pdf')  
        plt.close()

        gd.plot_persistence_diagram(uniao(dicio0_red[i],dicio1_red[i]),legend=True)
        plt.title(vec[i+1])
        plt.savefig(diretorio + '/' + vec[i+1] + 'red.pdf')  
        plt.close()
        #plt.xlabel("")
        #plt.ylabel("")
        

if not os.path.exists('graficos'):
	os.mkdir('graficos')

percentual = 0.1


nome = 'dist_indireta_com_norm_l1'


if not os.path.exists('graficos/'+nome):
    os.mkdir('graficos/'+nome)

#vetor_atributos2 = ['CHEMOTHERAPY']

#vetor_atributos = list(vetor_atributos)

for atributo in vetor_atributos:

    diretorio = 'graficos/' + nome +'/'+ atributo

    if not os.path.exists(diretorio):
        os.mkdir(diretorio)


    dicio0 = openPickle(nome,atributo,0)
    dicio1 = openPickle(nome,atributo,1)

    #print(diretorio)

    plotDiag(dicio0,dicio1,diretorio,atributo)

