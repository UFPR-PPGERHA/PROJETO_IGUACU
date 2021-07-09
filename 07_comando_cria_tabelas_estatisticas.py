import pandas as pd
import numpy as np
import os

#   Este código irá acessar a pasta com dados de chuva, nivel e vazao, e irá criar dados estatisticos e salvar nas pasta dir_save

folders=[".../Resultados_Uniao/Chuva",
         ".../Resultados_Uniao/Nivel",
         ".../Resultados_Uniao/Vazao"]

#   Caso você queira alternar entre estatisticas mensais e anuais, é só alter a linha comentada 13/14 e na 29/30
#dir_save=".../Estatisticas/Mensal/"
dir_save=".../Estatisticas/Anual/"

for folder in folders:    #Navega por todos os 3 tipos: chuva, nivel e vazao
    list_dts = []
    tipo = folder.split('/')[-1]      #Anota qual tipo está trabalhando para utilizar na hora de nomear o arquivo .txt
    for f in os.listdir(folder):    #Navega por todas as estações do diretório
        #   Este bloco junta todas as estações em apenas um dataset para que sejam calculadas as propriedades estatisticas
        file = f'{folder}/{f}'
        cod = f.split('T_')[-1][:-4]
        dt = pd.read_csv(file, sep='\t', index_col=0, parse_dates=True)
        dt = dt[[f'{tipo}']]
        dt.columns = [f'{cod}']
        list_dts.append(dt)
    dt = pd.concat(list_dts, axis=1)
    
    #dt = dt.resample('M')
    dt = dt.resample('Y')

    #   Este bloco irá salvar em variáveis as propriedades estatisticas
    dt_count = dt.count().round(3)
    dt_average = dt.mean().round(3)
    dt_std = dt.std().round(3)
    dt_min = dt.min().round(3)
    dt_max = dt.max().round(3)
    dt_sum = dt.sum().round(3)

    #   Este bloco irá salvar os arquivos .txt com seus devidos nomes no dir_save
    dt_count.to_csv(dir_save + tipo + "_count.txt", sep='\t')
    dt_average.to_csv(dir_save + tipo + "_average.txt", sep='\t')
    dt_std.to_csv(dir_save + tipo + "_std.txt", sep='\t')
    dt_min.to_csv(dir_save + tipo + "_min.txt", sep='\t')
    dt_max.to_csv(dir_save + tipo + "_max.txt", sep='\t')
    dt_sum.to_csv(dir_save + tipo + "_sum.txt", sep='\t')
