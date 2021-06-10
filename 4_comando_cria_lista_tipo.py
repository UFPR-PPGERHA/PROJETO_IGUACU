import os
import pandas as pd
import numpy as np

#   Este codigo deve ser executado apos comando_filtrar_dados, irá acessar as 5 pastas e criar um txt listando as estções pertencentes


#   Lista dos diretorios a serem trabalhados.
list_dir = ['.../Sedimento',
            '.../Chuvas',
            '.../Vazoes',
            '.../Qualidade',
            '.../Nivel']

f = '.../relacao_estacoes_HidroWeb.txt'

dt = pd.read_csv(f, sep='\t', index_col = False)

#   Navega em cada um dos 5 diretórios.
for dir in list_dir:
    cods = []
    tipo = dir.split('/')[-1]
    
    #   Navega em cada um dos arquivos.
    for f in os.listdir(dir):
        cod = np.int64(f.split('_')[-1][:-4])
        cods.append(cod)

    mask = dt['Codigo'].isin(cods)

    #   Cria um arquivo txt, com a lista de todos as estações em cada diretorio.
    dt_pivot = dt[mask]
    dt_pivot.to_csv('Coords_'+ tipo + '.txt', sep='\t', index=False)
