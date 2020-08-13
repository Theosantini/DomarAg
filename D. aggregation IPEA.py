from glob2 import glob
import numpy as np
import pandas as pd


filenames = glob('D:\OneDrive\Documentos OK\Python Scripts\MIP_*.xlsx')

dataframes = [pd.read_excel(f) for f in filenames]

dadosn = pd.concat(dataframes, ignore_index=True)

var = ['CI', 'Remunerações', 'Valor adicionado bruto ( PIB )','Valor da produção', 'Fator trabalho (ocupações)']

dadosn = (dadosn[dadosn.Variáveis.isin(var)]
               .iloc[:, 0:53]
               .melt(id_vars=["Ano", "Variáveis"], var_name='Setores')
               .pivot_table(index=["Ano", "Setores"], columns="Variáveis", values="value")
               .reset_index()
               .rename(columns = {'CI' : 'vQji', 'Fator trabalho (ocupações)' : 'rLi',
                      'Remunerações' : 'vLi', 'Valor adicionado bruto ( PIB )' : 'vVA',
                      'Valor da produção' : 'vQi'}))






"""""""""
file = "D:\OneDrive\Documentos OK\Python Scripts\MIP_2000_51.xlsx"
data = pd.ExcelFile(file)
print(data.sheet_names)

df = pd.read_excel("D:\OneDrive\Documentos OK\Python Scripts\MIP_2000_51.xlsx")
dfr = pd.DataFrame(df)
dfr.rename(columns={'Unnamed: 1' : 'Variaveis'}, inplace=True)
dfr = dfr.iloc[[57,58,59,68,69], 0:53]
dfr = pd.melt(dfr, id_vars=["Ano", "Variaveis"], var_name='Setores')
dfr = pd.pivot_table(dfr, index=["Ano", "Setores"], columns="Variaveis", values="value")
dfr = dfr.reset_index()
dfr = dfr.rename(columns = {'CI' : 'nQji', 'Fator trabalho (ocupações)' : 'rLi',
                      'Remunerações' : 'nLi', 'Valor adicionado bruto ( PIB )' : 'nVA',
                      'Valor da produção' : 'nQi'})
dfr['nKi'] = dfr['nVA'] - dfr['nLi']
"""""