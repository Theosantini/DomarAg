# Escrever código da tese em python
import numpy as np
import pandas as pd
import xlrd

# Importar Dados
data = pd.read_excel("D:\OneDrive\Documentos OK\Python Scripts\WIOD_SEA_Nov16 (2).xlsx", sheet_name='DATA')
df = pd.DataFrame(data)
# Filtrar para Brasil
df_bra = df[df['country'] == 'BRA']
# Fazer anos virarem uma coluna só (melt)
df_bra_melt = pd.melt(df_bra, id_vars=["country", "variable", "description", "code"], var_name='year')
# Fazer variable virar colunas (pivot_table)
df_bra_pivot = pd.pivot_table(df_bra_melt, index=["country", "description", "code", "year"], columns="variable",
                              values="value")
df_bra_pivot = df_bra_pivot.reset_index()
# Selecionar colunas não úteis
df_Bra = df_bra_pivot.drop(['country', 'COMP', 'EMP', 'EMPE', 'GO_PI', 'II_PI', 'VA_PI'], axis=1)
# Retirar setores inexistentes (são 8, 56-8=48)
df_Bra = df_Bra[df_Bra["GO"] > 0]
# Agregar setores
# três setores
df_Bra.loc[df_Bra["code"].isin(["A01", "A02", "A03"]), 'tressec'] = "Primary Industries"
df_Bra.loc[df_Bra["code"].isin(
    ["B", "D35", "E36", "F", "C10-C12", "C13-C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24", "C25",
     "C26", "C27", "C28", "C29", "C30", "C31_C32"]), 'tressec'] = "manufacturing"
df_Bra.loc[df_Bra["code"].isin(
    ["G45", "G46", "G47", "H49", "H50", "H51", "H52", "I", "J58", "J59_J60", "J61", "J62_J63", "K64", "L68", "M69_M70",
     "M71", "M72", "N", "O84", "P85", "Q", "R_S", "T"]), 'tressec'] = "services"
# dez setores
df_Bra.loc[df_Bra["code"].isin(["A01", "A02", "A03"]), 'dezsec'] = "Agriculture, forestry and fishing"
df_Bra.loc[df_Bra["code"].isin(["B", "D35", "E36"]), 'dezsec'] = "Mining, quarring; Electricity, gas and water supply"
df_Bra.loc[df_Bra["code"].isin(
    ["C10-C12", "C13-C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28",
     "C29", "C30", "C31_C32", "F"]), 'dezsec'] = "Manufacturing Industries"
df_Bra.loc[df_Bra["code"].isin(["G45", "G46", "G47", "H49", "H50", "H51", "H52",
                                "I"]), 'dezsec'] = "Trade, transport, accommodation and related services"
df_Bra.loc[df_Bra["code"].isin(["J58", "J59_J60", "J61", "J62_J63"]), 'dezsec'] = "Information and communication"
df_Bra.loc[df_Bra["code"].isin(["K64"]), 'dezsec'] = "Financial and insurance activities"
df_Bra.loc[df_Bra["code"].isin(["L68"]), 'dezsec'] = "Real estate activities"
df_Bra.loc[df_Bra["code"].isin(
    ["M69_M70", "M71", "M72", "N"]), 'dezsec'] = "Professional, scientific and support service activities"
df_Bra.loc[df_Bra["code"].isin(
    ["O84", "P85", "Q"]), 'dezsec'] = "Public administration, defence, education, health and social work activities"
df_Bra.loc[df_Bra["code"].isin(["R_S", "T"]), 'dezsec'] = "Other traditional services"
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
# Criar variáveis necessárias
# df_Bra.loc[df_Bra.groupby('code')['GO_QI'],'gGO_QI'] = np.log(df_Bra.GO_QI) - np.log(df_Bra.GO_QI.shift(1))
# teste
x = np.array([1, 2, 3,5,6])


def gr(x):
    c = []
    for i in range(len(x)):
        c.append(np.log(x[i]) - np.log(x[i-1]))
    return c

def it(x):
    c = []
    for i in range(len(x)):
        c.append(0.5*(x[i]+x[i-1]))
    return c

print(gr(x))
print(it(x))
