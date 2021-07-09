import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#   Este código cria dez arquivos .txt com uma matriz, onde as linhas são os anos, e as colunas são as estações, e adiciona um X caso contenha amostragem suficiente
# para satisfazer a porcentagem desejada. Podendo ser configurado para analisar por mês, ou por ano.

'''folders = [".../Estatisticas/Anual/Vazao_count.txt",
     ".../Estatisticas/Anual/Chuva_count.txt",
     ".../Estatisticas/Anual/Nivel_count.txt"]'''

folders = [".../Estatisticas/Mensal/Vazao_count.txt",
     ".../Estatisticas/Mensal/Chuva_count.txt",
     ".../Estatisticas/Mensal/Nivel_count.txt"]

#dir_save=".../Analise-periodo-comum/Anuais/"
dir_save=".../Analise-periodo-comum/Mensais/"

percs = np.arange(0.1, 1, 0.1)

for f in folders:
    #carrega o dataframe, e caso seja ano deverá dividir o somatório por 365.25 e caso seja por mês dividir por 30.437 
    dt = pd.read_csv(f, sep='\t', index_col=0, parse_dates=True)
    #dt = dt/365.25
    dt = dt/30.437 

    #verifica o tipo do dado entre: Chuva, Vazao e Nivel
    tipo = f.split('/')[-1][:-10]
    dir_save_novo = str(dir_save+tipo+'/')

    for perc in percs:
        dt_pivot = dt.copy()

        #verifica se possui amostra suficiente para a porcentagem, caso sim coloca um x, caso contrario coloca NAN
        mask = (dt_pivot <= perc)
        dt_pivot[mask] = np.nan
        dt_pivot[~mask] = 'x'
        #salva em txt o arquivo para sua respectiva porcentagem.
        dt_pivot.to_csv(dir_save_novo + tipo + '_' + str((perc*100).round(0)) + '%.txt', sep='\t')
