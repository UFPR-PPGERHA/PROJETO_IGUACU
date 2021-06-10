import os
import shutil
import pandas as pd
import numpy as np
from numpy import dtype
from datetime import datetime

#   Este codigo utiliza as funções de do codigo (hidroweb_files_to_dataframe_2) que pode ser obtido em: (https://github.com/joaohuf/Ferramentas_HidroWeb)

#   Caso não queira ver a documentação de (hidroweb_files_to_dataframe_2) vá até a linha 193.

BASE_URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'

def Dataframe_from_txt_Hidroweb_VAZAO(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[9], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 13:44]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Vazao')


def Dataframe_from_txt_Hidroweb_CHUVA(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[8], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 10:41]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Chuva')


def Dataframe_from_txt_Hidroweb_NIVEL(filename):
    """
    Entrada:
        - filename: Nome do arquivo de Vazao do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Nivel de Consistência e Vazao
                Sendo o index do dataframe a Data da medição.
    """
    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[9], engine='python', decimal=",")
    # As colunas 'NivelConsistencia' e 'EstacaoCodigo' correspondem a data e hora
    dt = dt.set_index(['NivelConsistencia', 'EstacaoCodigo'])
    # Pega a matriz de dados e coloca a coluna com o número do dia da medição
    dt = dt.iloc[:, 13:44]
    dt.columns = range(1, 32)

    return checagem_final_hidroweb(dt, 'Nivel')


def Dataframe_from_txt_Hidroweb_SEDIMETOS(filename):
    """
    Entrada:
        - filename: Nome do arquivo de sedimentos do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Hora, Vazao, Area Molhada, Largura, Velocidade e Concentração
                Sendo o index do dataframe a data da amostragem.
    """

    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, sep="\t|;", header=[6], engine='python', decimal=",")
    # Reseta o index
    dt = dt.reset_index(drop=True)
    # Cria o dataframe só com dados de:
    # Data, Hora, Vazão, Área Molhada, Largura, Velocidade, Concentração
    dt = dt.iloc[:, [0, 1, 2, 8, 9, 10, 11, 12]]
    dt.columns = ['Nivel_Consistencia','Data', 'Hora', 'Vazao', 'Area Molhada', 'Largura', 'Velocidade', 'Concentracao']

    dt['Hora'] = dt['Hora'].map(lambda x: str(x)[11:])

    # Exclui ou substitue os NaNs ou vazios
    dt = dt.dropna(subset=['Data'])
    dt.replace('', '00:00:00', inplace=True)
    dt['Hora'] = dt['Hora'].fillna('00:00:00')
    # Soma a data e tempo como strings
    dt['Data'] = dt['Data'].astype(str) + ' ' + dt['Hora'].astype(str)
    del dt['Hora']

    return checagem_final_hidroweb_2(dt)


def Dataframe_from_txt_Hidroweb_QUALIDADE(filename):
    """
    Entrada:
        - filename: Nome do arquivo de sedimentos do guidaizinho que será aberto
    Saída
        - saida: dataframe com os dados de Data, Hora, Vazao, Area Molhada, Largura, Velocidade e Concentração
                Sendo o index do dataframe a data da amostragem.
    """

    # Cria o dataframe a partir dos dados do CSV, pulando as linhas de cabeçalho
    dt = pd.read_csv(filename, index_col=None, sep=";", header=[10], engine='python', decimal=",")
    # Reseta o index
    dt = dt.reset_index(drop=True)
    # Cria o dataframe só com dados de:
    # Data, Hora, Vazão, Área Molhada, Largura, Velocidade, Concentração

    # O nome das colunas com os dado reais estao desalinhados e precisa arrumar, por isso essas duas linhas
    dt = dt.iloc[:, [0, 1, 2, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 39, 41, 42, 43, 59, 124, 132]]
    dt.columns = ['Nivel_Consistencia',
                  'Data',
                  'Hora',
                  'Prof',
                  'T_Ar',
                  'T_Amostra',
                  'pH',
                  'Cor',
                  'Turb',
                  'Cond',
                  'Dureza_T',
                  'Dureza',
                  'DQO',
                  'DBO',
                  'OD',
                  'ST',
                  'SF',
                  'SV',
                  'SST',
                  'SSF',
                  'SSV',
                  'SDT',
                  'SDF',
                  'SDV',
                  'SSed',
                  'Alc_CO3',
                  'Alc_HCO3',
                  'Alc_OH',
                  'Cloretos',
                  'SO2',
                  'S2',
                  'Fluoretos',
                  'PO4_T',
                  'NT',
                  'NH3',
                  'NO3',
                  'NO2',
                  'Col',
                  'N_Org',
                  'PT'
                  ]

    dt['Hora'] = dt['Hora'].map(lambda x: str(x)[11:])

    # Exclui ou substitue os NaNs ou vazios
    dt = dt.dropna(subset=['Data'])
    dt.replace('', '00:00:00', inplace=True)
    dt['Hora'] = dt['Hora'].fillna('00:00:00')

    # Soma a data e tempo como strings
    dt['Data'] = dt['Data'].astype(str) + ' ' + dt['Hora'].astype(str)
    del dt['Hora']

    return checagem_final_hidroweb_2(dt)


def format_Date(data):
    try:
        return datetime.strptime(data, '%d/%m/%Y')
    except ValueError:
        try:
            return datetime.strptime(data, '%d/%m/%Y %H:%M')
        except ValueError:
            try:
                return datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                print(data)
                print('AVISO: formato de data não existe: data foi excluida')
                #messagebox.showinfo('AVISO: formato de data não existe: data foi excluida')
                return np.nan
              
              

#   Este código irá acessar as estações na pasta bruto, deverá separar nas 5 pastas coorespondentes que devem existir.
# Alem disso irá deixar no formato dataframe adequado para o uso.

Dir_bruto = ".../Bruto"

#Navega pelos arquivos em Dir_bruto
for f in os.listdir(Dir_bruto):
    file = f'{Dir_bruto}/{f}'
    cod = (f.split('_')[-1][:-4])

    #Irá filtrar os dados removendo informações não utilizadas, e separando em suas respectivas pastas.
    if 'sedimentos' in f:
        dt = Dataframe_from_txt_Hidroweb_SEDIMETOS(file)
        dir_save = '.../Sedimento'
    elif 'chuvas' in f:
        dt = Dataframe_from_txt_Hidroweb_CHUVA(file)
        dir_save = '.../Chuvas'
    elif 'vazoes' in f:
        dt = Dataframe_from_txt_Hidroweb_VAZAO(file)
        dir_save = '.../Vazoes'
    elif 'qualagua' in f:
        dt = Dataframe_from_txt_Hidroweb_QUALIDADE(file)
        dir_save = '.../Qualidade'
    elif 'cotas' in f:
        dt = Dataframe_from_txt_Hidroweb_NIVEL(file)
        dir_save = '.../Nivel'
    else:
        #Caso o arquivo não esteja em nenhum dos 5 grupos selecionados, será salvo na pasta outras sem ser filtrado.
        dir_save = '.../Outros'
        shutil.copyfile(file, f'{dir_save}/{f}')
        continue
    dt.to_csv(f'{dir_save}/{f}', sep='\t', header=True, index='False')
