import pandas as pd
import requests
from io import BytesIO
from zipfile import BadZipFile, ZipFile

# Este código utiliza a função (download_dados_hidroweb_2.py) que pode ser obtida no link:(https://github.com/joaohuf/Ferramentas_HidroWeb)
# Caso queira ir direto para o codigo, olhe a partir da linha 62.

# Link onde estão os dados das estações convencionais
BASE_URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'

# Faz o download dos dados
def download(codigo, formato, dir, tipo_especifico=False, save_zip=False):
    
    # Faz o download de uma estação convencional do hidroweb, usando o código dela
    # codigo - Int - Número do código da estação
    # formato => Int -  Número entre 1 e 3 que indica o tipo de arquivo para download (1-mdb, 2-txt, 3-csv)
    # dir => path - Diretório para salvar os dados
    # save_zip => True/False - Determina se é para salvas o .zip original ou descompactar tudo
    # tipo específico => faz a extração de arquivos que contenham essa string no nome
    
    print(f'Baixando a estação: {codigo}')
    # Arruma os parâmetros e faz o request dos dados
    params = {'tipo': formato, 'documentos': codigo}
    r = requests.get(BASE_URL, params=params)

    # Checa se é um arquivo zip válido
    if not isinstance(r.content, bytes):
        print(f'Arquivo {codigo} inválído')
        return

    # Sava o arquivo como o .zip original
    if save_zip:
        print(f'Salvando dados {codigo} como zip')
        with open(f'{dir}estacao_{codigo}.zip', 'wb') as f:
            f.write(r.content)
    # Descompacta cada .zip que está dentro do .zip
    else:
        print(f'Extraindo dados da estação {codigo} do zip')
        unzip_station_data(r.content, dir, tipo_especifico)
        
def unzip_station_data(station_raw_data, dir, tipo_especifico):

    try:
        main_zip_bytes = BytesIO(station_raw_data)
        main_zip = ZipFile(main_zip_bytes)

        for inner_file_name in main_zip.namelist():
            print(inner_file_name)
            inner_file_content = main_zip.read(inner_file_name)
            inner_file_bytes = BytesIO(inner_file_content)
            if not tipo_especifico:
                with ZipFile(inner_file_bytes, 'r') as zipObject:
                    zipObject.extractall(dir)
            elif tipo_especifico in inner_file_name:
                with ZipFile(inner_file_bytes, 'r') as zipObject:
                    zipObject.extractall(dir)
    except BadZipFile:
        print('Sem nenhum .zip')

        
#Carrega a lista das estações da bacia do Iguaçu contida em Coords_Bruto.txt obtida no arquivo (1_comando_selecao_da_bacia.py)
f = '.../Coords_Bruto.txt'
bacias = pd.read_csv(f, '\t')
codigos = bacias['Codigo']
dir_save = '.../Bruto'

#Irá baixar as estações da lista para a pasta Bruto, caso aconteça problemas, irá baixar no fomato .ZIP
for i in range(len(codigos)):
    try:
        download_dados_hidroweb_2.download(codigos[i], formato=2, dir=dir_save, save_zip=False)
    except:
        download_dados_hidroweb_2.download(codigos[i], formato=2, dir=dir_save, save_zip=True)
