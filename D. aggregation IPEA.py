from glob2 import glob
import numpy as np
import pandas as pd

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
