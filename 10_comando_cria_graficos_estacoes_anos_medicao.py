import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#   O objetivo deste código é gerar gráficos que analisem a completude do banco de dados, criando 10 gráficos, analisando a cada 5 anos, de 5 até 55 anos,
# o número de estações com medições presentes, com 10 medidas de proporção de amostras durante o ano, interando em 10%, de 10% até 90%.

# Primeiro bloco carrega o dataframe, podendo ser um dos 3 tipos, obrigatóriamente com medida anual, podendo ser obtida no codigo:

#f = ".../Vazao_count.txt"
#cores = 'Greens'

#f = ".../Chuva_count.txt"
#cores = 'Blues'

f = ".../Nivel_count.txt"
cores = 'Oranges'

dt = pd.read_csv(f, sep='\t', index_col=0, parse_dates=True)

dt = dt/365

# Este bloco irá configurar a maneira como iremos fazer a analise, de 5 à 55 anos, de 10% à 90%.

anos = np.arange(5, 50+5, 5)
percs = np.arange(0.1, 1, 0.1)

for ano in anos:
    list_dts = []
    for perc in percs:
        dt_pivot = dt.copy()
        #Está mascara verifica se a quantidade da amostras satisfaz a porcentagem, caso satisfaça coloca 1, caso contrario NAN.
        mask = (dt_pivot <= perc)
        dt_pivot[mask] = np.nan
        dt_pivot[~mask] = 1
        #Está mascara 2 irá verificar quais anos possuem a medição com tal porcentagem, caso tenha ele adiciona em cods, caso contrario descarta e não entrarará na conta.
        mask2 = (dt_pivot.sum(axis=0) > ano)
        cods = dt_pivot.columns[mask2]
        dt_pivot = dt_pivot[cods].sum(axis=1)

        list_dts.append(dt_pivot)

    dt2 = pd.concat(list_dts, axis=1)
    dt2.columns = percs.round(3)
    
    #neste bloco apenas configurações do gráfico

    dt2.columns = ['> %1.0f%%' % (l * 100) for l in dt2.columns]

    fig, ax = plt.subplots(figsize=(8, 5))
    dt2.plot(ax=ax, cmap=cores)

    plt.title("Quantidade de estações com no mínimo " + str(ano) + " anos com medição")

    plt.xlabel('Ano')
    plt.ylabel('Número de estações')

    plt.legend(title="Dados por Ano")

    plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.6)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2)

    plt.tight_layout()

#aqui deverá ser configurado o tipo de dado que foi estudado, deverá ser o mesmo tipo do dataframe carregado.    
    
    #plt.savefig("Vazões_com_" + str(ano) + "_anos_de_medicao.png",dpi=300)
    #plt.savefig("Chuvas_com_" + str(ano) + "_anos_de_medicao.png",dpi=300)
    plt.savefig("Cotas_com_" + str(ano) + "_anos_de_medicao.png",dpi=300)
