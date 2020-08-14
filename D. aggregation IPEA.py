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

# Manipular e organizar matriz insumo produto 2000-2017 para obter apenas variáveis essenciais

var = ['CI', 'Remunerações', 'Valor adicionado bruto ( PIB )','Valor da produção', 'Fator trabalho (ocupações)']

dadosn = (dadosn[dadosn.Variáveis.isin(var)]
               .iloc[:, 0:53]
               .melt(id_vars=["Ano", "Variáveis"], var_name='Setores')
               .pivot_table(index=["Ano", "Setores"], columns="Variáveis", values="value")
               .reset_index()
               .rename(columns = {'CI' : 'vQji', 'Fator trabalho (ocupações)' : 'rLi',
                      'Remunerações' : 'vLi', 'Valor adicionado bruto ( PIB )' : 'vVA',
                      'Valor da produção' : 'vQi'})
               .assign(vKi = lambda x: x.vVA - x.vLi))

### Importar matrizes de insumo-produto valores constantes

filenamesr = glob('D:\OneDrive\Documentos OK\Python Scripts\MIPdeflacionados\deflac_*.xlsx')

dataframesr = [pd.read_excel(f) for f in filenamesr]

# Juntar tabelas em uma

dadosr = pd.concat(dataframesr, ignore_index=True)

# Manipular e organizar matriz insumo produto 2000-2017 para obter apenas variáveis essenciais

var = ['CI', 'Valor da produção']

dadosr = (dadosr[dadosr.Variáveis.isin(var)]
               .iloc[:, 0:53]
               .melt(id_vars=["Ano", "Variáveis"], var_name='Setores')
               .pivot_table(index=["Ano", "Setores"], columns="Variáveis", values="value")
               .reset_index()
               .rename(columns = {'CI' : 'rQji',
                      'Valor da produção' : 'rQ'}))

### Juntar dadosn e dadosr no mesmo dataframe

dados = pd.concat([dadosn,dadosr], ignore_index=False, axis=1)

# Agregar setores em 10

# Adicionar inflação e calcular variação real do estoque de capital

# Calcular PIB nominal anual


