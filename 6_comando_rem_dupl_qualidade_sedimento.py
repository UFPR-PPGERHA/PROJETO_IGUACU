import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import shutil

#   Este código irá tratar dos casos de duplicidade, isso acontece quando duas estações tem coordenadas iguais. O código irá juntar os 2 arquivos em 1.

#   Este codigo funcionando apenas para Qualidade e sedimento
f = ['.../Coords_Qualidade.txt',
     '.../Coords_Sedimento.txt']

cod_home = ['/home/seb/Projeto-iguacu/Estacoes/Qualidade/qualagua_T_',
            '/home/seb/Projeto-iguacu/Estacoes/Sedimento/sedimentos_T_']

dir_save = ['/home/seb/Projeto-iguacu/Estacoes/Resultados_Uniao/Qualidade/',
            '/home/seb/Projeto-iguacu/Estacoes/Resultados_Uniao/Sedimento/']

for i in range(2):
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
            name = (cod_home[i].split('/')[-1][:-1])
            cod_novo = ''
            for cod_intersecao in dt_intersecao.index.to_list():    #Caso tenha intercessão ele entrara nesse for, caso contrario não entrará.
                #Nesta parte ele trata do novo nome do arquivo .txt, tendo cuidado para o caso de ter 3 ou mais arquivos
                cod_novo = cod_novo + '_' + str(cod_intersecao)

                f_cod = f'{cod_home[i]}{cod_intersecao}.txt'
                df = pd.read_csv(f_cod, sep='\t', index_col=0, parse_dates=True)
                
                list_dts.append(df)   #Aqui ele irá listar os dataframes na repetidos
                cods_rodados.append(cod_intersecao)   #Aqui ele vai atualizar as estações verificadas
            
            name = name + cod_novo
            if (len(dt_intersecao)) > 1:    #Caso tenha interecessão eu irá juntar, caso contrário apenas fará uma copia do arquivo para o destino
                uniao = pd.concat(list_dts)
                uniao.to_csv(f'{dir_save[i]}/{name}.txt', sep='\t', header=True, index='Data')
            else:
                shutil.copyfile(f_cod, f'{dir_save[i]}{name}.txt')
