import numpy as np 
import gudhi as gd 
import pandas as pd
import math
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


def curvaBetti(diagram,I):
    
    step_x = I[1]-I[0]
    bc =  np.zeros(len(I))
    diagram_int = np.clip(np.ceil((diagram[:,:2] - I[0]) / step_x), 0, len(I)).astype(int)
    
    for interval in diagram_int:
        bc[interval[0]:interval[1]] += 1
        
    curve = np.reshape(bc,[1,-1])
    
    return curve[0]

def plotBetti(dicio0,dicio1,num,diretorio,atributo):
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
    'THREEGENE':['3-Gene classifier subtype','ER+/HER2- Low Prolif','ER+/HER2- High Prolif','ER-/HER2-','HER2+'],
    'VITAL_STATUS':['Patient\'s Vital Status','Living','Died of Disease','Died of Other Causes'],
    'LATERALITY':['Laterality','Left','Right'],
    'RADIO_THERAPY':['Radio Therapy','Yes','No'],
    'HISTOLOGICAL_SUBTYPE':['Tumor\'s Histologic Subtype','Ductal/NST','Mixed','Lobular','Tubular/ cribriform','Mucinous','Medullary','Other'],
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
    'TUMOR_SIZE':['Tumor Size','Up tp 1','1 to 17','17 to 22','22 to 30', '30 or Larger'],
    'TMB_NONSYNONYMOUS':['Tumor Mutational Burden','Up to 3.9','3.9 to 6.5','6.5 to 9.1', '9.1 or High']
    }


    vec = dicio_leg[atributo]

    titulo = vec[0]
    del(vec[0])

    dicio = [dicio0,dicio1]
    m = 0
    for n in range(2):
        m=0
        for diagram in dicio[n].values():
            a = diagram[:-1]
            if not a.any() :
                dicio[n].popitem()
                break
            if max(a[:,1])>m:
                m = max(a[:,1])
        I = np.linspace(0,math.ceil(m),num) #Define o eixo x

        aux=0
        for ind,diagram in dicio[n].items():
            curva = curvaBetti(diagram,I)
            legg = vec[aux]
            plt.step(I, curva,label=legg)
            aux = aux+1

        plt.title(titulo)
        if n==0:
            plt.ylabel("Connected components $H_0$")
        else:
            plt.ylabel("Cycles $H_1$")
        plt.xlabel("Survival time")

        plt.legend()

        plt.savefig(diretorio + '/' + '-Dim'+str(n)+'.pdf')  
 
        plt.close()

if not os.path.exists('betti'):
    os.mkdir('betti')

num = 100

nome = 'dist_direta_com_norm_l1'

if not os.path.exists('betti/'+nome):
    os.mkdir('betti/'+nome)



for atributo in vetor_atributos:

    diretorio = 'betti/' + nome +'/'+ atributo


    if not os.path.exists(diretorio):
        os.mkdir(diretorio)


    dicio0 = openPickle(nome,atributo,0)
    dicio1 = openPickle(nome,atributo,1)

    #dicio0.popitem()
    #dicio1.popitem()


    plotBetti(dicio0,dicio1,num,diretorio,atributo)

