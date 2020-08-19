# Código para TD do Ipea
# Organizar e calcular produtividade setorial e agregada do Brasil usando dados do IBGE/Ipea

from glob2 import glob
import numpy as np
import pandas as pd

### Importar matrizes de insumo-produto nominais

filenamesn = glob('D:\OneDrive\Documentos OK\Python Scripts\MIP_*.xlsx')

dataframesn = [pd.read_excel(f) for f in filenamesn]

# Juntar tabelas em uma

dadosn = pd.concat(dataframesn, ignore_index=True)

# Filtrar e organizar matriz insumo produto 2000-2017 para obter apenas variáveis essenciais

var = ['CI', 'Remunerações', 'Valor adicionado bruto ( PIB )','Valor da produção', 'Fator trabalho (ocupações)']

dadosn = (dadosn[dadosn.Variáveis.isin(var)]
               .iloc[:, 0:53]
               .melt(id_vars=["Ano", "Variáveis"], var_name='Setores')
               .pivot_table(index=["Ano", "Setores"], columns="Variáveis", values="value")
               .reset_index()
               .rename(columns = {'CI' : 'vQji', 'Fator trabalho (ocupações)' : 'rLi',
                      'Remunerações' : 'vLi', 'Valor adicionado bruto ( PIB )' : 'vVA',
                      'Valor da produção' : 'vQi'})
               .assign(vKi = lambda x: x.vVA - x.vLi)
               .assign(nKi = lambda x: x.vVA - x.vKi +x.vLi)) # estoque de capital (fictício) ver como fazer


### Importar matrizes de insumo-produto valores constantes

filenamesr = glob('D:\OneDrive\Documentos OK\Python Scripts\MIPdeflacionados\deflac_*.xlsx')

dataframesr = [pd.read_excel(f) for f in filenamesr]

# Juntar tabelas em uma

dadosr = pd.concat(dataframesr, ignore_index=True)

# Filtrar e organizar matriz insumo produto 2000-2017 para obter apenas variáveis essenciais

var = ['CI', 'Valor da produção']

dadosr = (dadosr[dadosr.Variáveis.isin(var)]
               .iloc[:, 0:53]
               .melt(id_vars=["Ano", "Variáveis"], var_name='Setores')
               .pivot_table(index=["Ano", "Setores"], columns="Variáveis", values="value")
               .reset_index()
               .rename(columns = {'CI' : 'rQji',
                      'Valor da produção' : 'rQi'}))

### Juntar dadosn e dadosr no mesmo dataframe

dados = pd.merge(dadosn,dadosr, on=['Ano','Setores'])

# Agregar setores em 10 ou 12

# Adicionar inflação (IGP-DI) para calcular variação real do estoque de capital

Infla = [9.52, 10.23, 27.66, 6.95, 11.87, 1.42, 3.64, 8.19,
         8.57, -0.94, 11.28, 4.64, 8.10, 5.57, 3.92, 11.17, 6.6, -0.35]

Ano = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
        2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

Infla = pd.DataFrame({'Ano': Ano, 'Infla': Infla})

Infla['Infla'] = Infla['Infla'] / 100

dados = pd.merge(dados, Infla, on='Ano')

# Calcular PIB nominal anual

dados['PIB'] = dados.groupby('Ano')['vVA'].transform(sum)

# Funções necessárias para calcular produtividade (MFP) setorial
## ([1] shares nominais e [2] taxas de crescimento)

# [1] shares nominais

def sn(x):
    c = []
    for i in range(len(x)):
        if i == 0:
            c.append(0)
        else:
            c.append(0.5 * (x.values[i] + x.values[i - 1]))
    return c

# [2] taxas de crescimento

def gr(x):
    c = []
    for i in range(len(x)):
        if i == 0:
            c.append(0)
        else:
            c.append(np.log(x.values[i]) - np.log(x.values[i - 1]))
    return c

# Aplicar funções para produzir variáveis necessárias nominais e reais

# Nominais

dados['svinfla'] = dados.groupby('Setores')["Infla"].transform(sn)
dados['svPIB'] = dados.groupby('Setores')["PIB"].transform(sn)
dados['svVA'] = dados.groupby('Setores')["vVA"].transform(sn)
dados['svLi'] = dados.groupby('Setores')["vLi"].transform(sn)
dados['svQji'] = dados.groupby('Setores')["vQji"].transform(sn)
dados['svKi'] = dados.groupby('Setores')["vKi"].transform(sn)
dados['svQi'] = dados.groupby('Setores')["vQi"].transform(sn)

# Nominais

dados['grQi'] = dados.groupby('Setores')["rQi"].transform(gr)
dados['grLi'] = dados.groupby('Setores')["rLi"].transform(gr)
dados['gnKin'] = dados.groupby('Setores')["nKi"].transform(gr)
dados['grQji'] = dados.groupby('Setores')["rQji"].transform(gr)
dados['grKi'] = ((1 + dados['gnKin']) / (1 + dados['svinfla']) - 1)

"""
# Calcular produtividades em novo dataframe

df_Bra_Prodi = df_Bra[df_Bra['year'] > 2000]
df_Bra_Prodi['ProdSec'] = df_Bra_Prodi.gGO_QI - (df_Bra_Prodi.vLAB / df_Bra_Prodi.vGO) * df_Bra_Prodi.gH_EMPE - \
                          (df_Bra_Prodi.vCAP / df_Bra_Prodi.vGO) * df_Bra_Prodi.gKi - (
                                      df_Bra_Prodi.vII / df_Bra_Prodi.vGO) * df_Bra_Prodi.gQji
df_Bra_Prodi['gVi'] = (df_Bra_Prodi.vGO/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.ProdSec + \
                      (df_Bra_Prodi.vLAB/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.gH_EMPE + \
                      (df_Bra_Prodi.vCAP/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.gKi

# Calcular e mostrar Domar weights no tempo e taxa de crescimento da produtividade setorial e agregada                      

"""