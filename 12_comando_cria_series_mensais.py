import pandas as pd
import numpy as np
import os
import shutil

#   Este código foi criado a após verificar a necessidade de disponibilizar os dados em medições do tipo mensal e anual, e tudo isso a partir de medições diárias,
# para chuva a medição é acumulada para mensal e anual, e para nível e vazão é a média.


folders=[".../Series-Diarias/Chuva",
         ".../Series-Diarias/Nivel",
         ".../Series-Diarias/Vazao"]

dir_save_mes=[".../Series-Mensais/Chuva/",
              ".../Series-Mensais/Nivel/",
              ".../Series-Mensais/Vazao/"]
              
dir_save_ano=[".../Series-Anuais/Chuva/",
              ".../Series-Anuais/Nivel/",
              ".../Series-Anuais/Vazao/"]

# Estes 2 contadores foram criados para auxiliar, i para alternar entre os tipos de dados, e erros a partir da observação que existem dataframes vazios. 
i=0
erros=0

for folder in folders:
    dir_save = dir_save_mes[i]
    #dir_save = dir_save_ano[i]
    i=i+1
    tipo = folder.split('/')[-1]

    #acessa as pastas e todos os seus arquivos, que são nomeados da maneira tipo_estação.txt 
    for f in os.listdir(folder):
        file = f'{folder}/{f}'
        cod = f.split('T_')[-1][:-4]
        name = f.split('/')[-1]
        print(name)
        dt = pd.read_csv(file, sep='\t', index_col=0, parse_dates=True)
        dt = dt[[f'{tipo}']]        
        try:
            #configura se a nova série será mensal ou anual.
            dt = dt.resample('M')
            #dt = dt.resample('Y')
            
            #trata o problema da chuva ser diferente.
            if (tipo == 'Chuva'):
                serie = dt.sum().round(3)
                serie.to_csv(str(dir_save) + str(name), sep='\t')
            else:
                serie = dt.mean().round(3)
                serie.to_csv(str(dir_save) + str(name), sep='\t')
        except:
            #aqui será tratado os arquivos vazios, podendo optar por apenas copiar para manter o código, ou basta comentar a linha 55 para ignorar.
            print('Vazio')
            shutil.copyfile(file, str(dir_save) + str(name))
            erros=erros+1

print(erros)
