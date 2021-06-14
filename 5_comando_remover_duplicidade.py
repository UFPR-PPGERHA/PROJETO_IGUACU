from numpy import string_
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import shutil

#   Este código irá tratar dos casos de duplicidade, isso acontece quando duas estações tem coordenadas iguais. O código irá juntar os 2 arquivos em 1.

def concat_dataframes_hidroweb(list_dts):
    dts_1, dts_2 = [], []
    for i in range(len(list_dts)):
        dt = list_dts[i]
        name = dt.columns.to_list()
        name.remove('Nivel_Consistencia')

        if len(name) > 1:
            print('ERRO: nao funciona para dt com mais de uma coluna de dados')

        dts_1.append(dt[dt.Nivel_Consistencia == 1][name[0]])
        dts_2.append(dt[dt.Nivel_Consistencia == 2][name[0]])

    # Concatena os dados fazendo a média se houver sobreposição
    dt_1 = pd.concat(dts_1, axis=1).mean(axis=1)
    dt_2 = pd.concat(dts_2, axis=1).mean(axis=1)

    # Junta os dois dataframes em colunas separadas
    dt = pd.concat([dt_1, dt_2], axis=1)
    dt.columns = ['NC_1', 'NC_2']

    # Onde não existe dado CONSISTIDO, coloca o bruto.
    mask = dt['NC_2'].isna()
    dt['NC_2'][mask] = dt['NC_1']
    del dt['NC_1']

    # Adiciona o nivel de consistencia ao dataframe
    dt['Nivel_Consistencia'] = 2
    dt.loc[mask, 'Nivel_Consistencia'] = 1

    # Inverte as colunas de posição
    dt = dt[dt.columns[::-1]]

    dt.columns = ['Nivel_Consistencia', name[0]]
    return dt



f = ['.../Coords_Vazoes.txt',
     '.../Coords_Chuvas.txt',
     '.../Coords_Nivel.txt']

cod_home = ['.../Vazoes/vazoes_T_',
            '.../Chuvas/chuvas_T_0',
            '.../Nivel/cotas_T_']

# Este codigo funcionando apenas para vazoes, chuvas e nivel

dir_save = ['.../Resultados_Uniao/Vazao/',
            '.../Resultados_Uniao/Chuva/',
            '.../Resultados_Uniao/Nivel/']

for i in range(3):
    i=1
    dt = pd.read_csv(f[i], sep='\t', index_col=0)

    dt['Coords'] = list(zip(dt['Longitude'], dt['Latitude']))
    dt['Coords'] = dt['Coords'].apply(Point)
    dt = gpd.GeoDataFrame(dt, geometry='Coords')

    cods_todos = dt.index.to_list()
    cods_rodados = []
    ponto = []
    # Navega por todos as estações no diretório
    for cod in cods_todos:
        # Toda estação ja comparada entrará para cods_rodados
        if not cod in cods_rodados:
            # Este bloco irá detectar duplicidades caso exista intercessção de dois pontos nas coordenadas geográficas
            ponto = dt.loc[cod, 'Coords']
            mask = dt['Coords'].intersects(ponto)
            dt_intersecao = dt[mask]['Coords']
            list_dts = []
            # Este if irá tratar da peculiaridade dos dados tipo Chuva, em alguns momentos os codigos apresentavam 7 digitos ao inves de 8
            if (i==1):
                name = (cod_home[i].split('/')[-1][:-2])
            else:
                name = (cod_home[i].split('/')[-1][:-1])
            cod_novo = ''
            for cod_intersecao in dt_intersecao.index.to_list(): #Caso tenha intercessão ele entrara nesse for, caso contrario não entrará.
                #Nesta parte ele trata do novo nome do arquivo .txt, tendo cuidado para o caso de ter 3 ou mais arquivos, e tratando da peculiaridade dos dados da chuva
                if (i==1):
                    cod_novo = cod_novo + '_0' + str(cod_intersecao)
                else:
                    cod_novo = cod_novo + '_' + str(cod_intersecao)

                f_cod = f'{cod_home[i]}{cod_intersecao}.txt'

                df = pd.read_csv(f_cod, sep='\t', index_col=0, parse_dates=True)
                
                list_dts.append(df)   #Aqui ele irá listar os dataframes na repetidos
                cods_rodados.append(cod_intersecao)   #Aqui ele vai atualizar as estações verificadas
            
            name = name + cod_novo
            if (len(dt_intersecao)) > 1:      #Caso tenha interecessão eu irá juntar, caso contrário apenas fará uma copia do arquivo para o destino
                uniao = concat_dataframes_hidroweb(list_dts )
                uniao.to_csv(f'{dir_save[i]}/{name}.txt', sep='\t', header=True, index='False')
            else:
                shutil.copyfile(f_cod, f'{dir_save[i]}{name}.txt')
    exit()
