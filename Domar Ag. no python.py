## Brasil - Domar Aggregation TD
# Importar programas necessários

import numpy as np
import pandas as pd

# Importar Dados

data = pd.read_excel("D:\OneDrive\Documentos OK\Python Scripts\WIOD_SEA_Nov16 (2).xlsx", sheet_name='DATA')
df = pd.DataFrame(data)

# Filtrar para Brasil

df_bra = df[df['country'] == 'BRA']

# Fazer anos virarem uma coluna só (melt)

df_bra_melt = pd.melt(df_bra, id_vars=["country", "variable", "description", "code"], var_name='year')

# Fazer variable virar colunas (pivot_table)

df_bra_pivot = pd.pivot_table(df_bra_melt, index=["country", "description", "code", "year"], columns="variable",values="value")

df_bra_pivot = df_bra_pivot.reset_index()

# Selecionar colunas não úteis

df_Bra = df_bra_pivot.drop(['country', 'COMP', 'EMP', 'EMPE', 'GO_PI', 'II_PI', 'VA_PI', 'VA_QI'], axis=1)

# Retirar setores inexistentes (são 8, 56-8=48)

df_Bra = df_Bra[df_Bra["GO"] > 0]

# Agregar setores

# dez setores
df_Bra.loc[df_Bra["code"].isin(["A01", "A02", "A03"]), 'dezsec'] = "Agricultura, silvicultura e pesca"
df_Bra.loc[df_Bra["code"].isin(["B", "D35", "E36"]), 'dezsec'] = "Mineração, eletricidade, gás e abastecimento de água"
df_Bra.loc[df_Bra["code"].isin(
    ["C10-C12", "C13-C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28",
     "C29", "C30", "C31_C32", "F"]), 'dezsec'] = "Indústria"
df_Bra.loc[df_Bra["code"].isin(["G45", "G46", "G47", "H49", "H50", "H51", "H52",
                                "I"]), 'dezsec'] = "Comércio, transporte, acomodação e serviços relacionados"
df_Bra.loc[df_Bra["code"].isin(["J58", "J59_J60", "J61", "J62_J63"]), 'dezsec'] = "Serviços de informação e comunicação"
df_Bra.loc[df_Bra["code"].isin(["K64"]), 'dezsec'] = "Atividades financeiras e de seguros"
df_Bra.loc[df_Bra["code"].isin(["L68"]), 'dezsec'] = "Atividades imobiliárias"
df_Bra.loc[df_Bra["code"].isin(
    ["M69_M70", "M71", "M72", "N"]), 'dezsec'] = "Atividades profissionais, científicas e de serviços de suporte"
df_Bra.loc[df_Bra["code"].isin(
    ["O84", "P85", "Q"]), 'dezsec'] = "Atividades de administração pública, defesa, educação, saúde e assistência social"
df_Bra.loc[df_Bra["code"].isin(["R_S", "T"]), 'dezsec'] = "Outros serviços"

# Calcular PIB nominal anual

df2 = df_Bra.groupby('year')['VA'].sum()
df2 = pd.DataFrame(df2).reset_index()
df2.rename(columns={'VA': 'PIB'}, inplace=True)
df_Bra = pd.merge(df_Bra, df2, on='year')

# Adicionar inflação do período

infla = [9.52, 10.23, 27.66, 6.95, 11.87, 1.42, 3.64, 8.19, 8.57, -0.94, 11.28, 4.64, 8.10, 5.57, 3.92]
year = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
infla = pd.DataFrame({'year': year, 'infla': infla})
infla['infla'] = infla['infla'] / 100
df_Bra = pd.merge(df_Bra, infla, on='year')


# Criar variáveis necessárias ([1] shares nominais e [2] taxas de crescimento)

# [1] shares nominais

def sn(x):
    c = []
    for i in range(len(x)):
        if i == 0:
            c.append(0)
        else:
            c.append(0.5 * (x.values[i] + x.values[i - 1]))
    return c


df_Bra['vinfla'] = df_Bra.groupby('code')["infla"].transform(sn)
df_Bra['vPIB'] = df_Bra.groupby('code')["PIB"].transform(sn)
df_Bra['vVA'] = df_Bra.groupby('code')["VA"].transform(sn)
df_Bra['vLAB'] = df_Bra.groupby('code')["LAB"].transform(sn)
df_Bra['vII'] = df_Bra.groupby('code')["II"].transform(sn)
df_Bra['vCAP'] = df_Bra.groupby('code')["CAP"].transform(sn)
df_Bra['vGO'] = df_Bra.groupby('code')["GO"].transform(sn)
df_Bra['vGO10'] = df_Bra.groupby(['dezsec', 'year'])['vGO'].transform('sum')


# [2] taxas de crescimento

def gr(x):
    c = []
    for i in range(len(x)):
        if i == 0:
            c.append(0)
        else:
            c.append(np.log(x.values[i]) - np.log(x.values[i - 1]))
    return c


df_Bra['gGO_QI'] = df_Bra.groupby('code')["GO_QI"].transform(gr)
df_Bra['gH_EMPE'] = df_Bra.groupby('code')["H_EMPE"].transform(gr)
df_Bra['gKinom'] = df_Bra.groupby('code')["K"].transform(gr)
df_Bra['gQji'] = df_Bra.groupby('code')["II_QI"].transform(gr)
df_Bra['gKi'] = ((1 + df_Bra['gKinom']) / (1 + df_Bra['vinfla']) - 1)

# substituir Nas por 0 e Calcular produtividades em novo dataframe

df_Bra = df_Bra.fillna(0)
df_Bra_Prodi = df_Bra[df_Bra['year'] > 2000]
df_Bra_Prodi['ProdSec'] = df_Bra_Prodi.gGO_QI - (df_Bra_Prodi.vLAB / df_Bra_Prodi.vGO) * df_Bra_Prodi.gH_EMPE - \
                          (df_Bra_Prodi.vCAP / df_Bra_Prodi.vGO) * df_Bra_Prodi.gKi - (
                                      df_Bra_Prodi.vII / df_Bra_Prodi.vGO) * df_Bra_Prodi.gQji
df_Bra_Prodi['gVi'] = (df_Bra_Prodi.vGO/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.ProdSec + \
                      (df_Bra_Prodi.vLAB/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.gH_EMPE + \
                      (df_Bra_Prodi.vCAP/(df_Bra_Prodi.vLAB+df_Bra_Prodi.vCAP))*df_Bra_Prodi.gKi


# Tabelas de produtividade (Domar) por 10-macrosetores

df_Bra_Prodi['VA_GDP'] = df_Bra_Prodi.vVA / df_Bra_Prodi.vPIB
df_Bra_Prodi['II_GDP'] = df_Bra_Prodi.vII / df_Bra_Prodi.vPIB
df_Bra_Prodi['D_Weight'] = df_Bra_Prodi.vGO / df_Bra_Prodi.vPIB
df_Bra_Prodi['MFP10'] = df_Bra_Prodi.ProdSec * (df_Bra_Prodi.vGO / df_Bra_Prodi.vGO10)

df_Bra_Prodi10 = df_Bra_Prodi.groupby(['dezsec', 'year'])[['VA_GDP', 'II_GDP', 'D_Weight', 'MFP10']].agg(sum).reset_index()

df_Bra_Prodi10mean = df_Bra_Prodi10.groupby('dezsec')[['VA_GDP', 'II_GDP', 'D_Weight', 'MFP10']].agg("mean").reset_index()
'''
# Separar entre 2000 a 2008 e 2009 a 2014

'''