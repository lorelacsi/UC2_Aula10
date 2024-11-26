import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    df_recuperacao_veiculos = df_ocorrencias[['cisp', 'recuperacao_veiculos']]

    df_recuperacao_veiculos  = df_recuperacao_veiculos.groupby(['cisp']).sum(['recuperacao_veiculos']).reset_index()

    print(df_recuperacao_veiculos.head())
    print('\nDados obtidos com sucesso')

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()

try:

    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos['recuperacao_veiculos'])
    media_recuperacao_veiculos = np.mean(array_recuperacao_veiculos)
    mediana_recuperacao_veiculos = np.median(array_recuperacao_veiculos)
    soma_recuperacao_veiculos = np.sum(array_recuperacao_veiculos)
    distancia_media_mediana_recuperacao_veiculos = abs((media_recuperacao_veiculos - mediana_recuperacao_veiculos)/mediana_recuperacao_veiculos)*100

    print(f'\nTotal de recuperação de veiculos: {soma_recuperacao_veiculos}')
    print(f'Media de recuperação de veiculos ocorridos ao longo dos anos: {media_recuperacao_veiculos:.2f}')
    print(f'Mediana de recuperação de veiculos ocorridos ao longo dos anos: {mediana_recuperacao_veiculos:.2f}')
    print(f'Diferenca entre media e mediana: {distancia_media_mediana_recuperacao_veiculos}%')

    q1 = np.quantile(array_recuperacao_veiculos, 0.25, method='weibull')
    q3 = np.quantile(array_recuperacao_veiculos, 0.75, method='weibull')
    iqr = q3 - q1

    minimo = np.min(array_recuperacao_veiculos)
    limite_inferior = q1 - (1.5*iqr)
    limite_superior = q3 + (1.5*iqr)
    maximo = np.max(array_recuperacao_veiculos)
    amplitude_total = maximo - minimo

    print(f'Q1 (25%) = {q1}')
    print(f'Q3 (75%) = {q3}')
    print(f'O IQR é {iqr}')
    print(f'Maximo é {maximo}')
    print(f'Minimo é {minimo}')
    print(f'Limite inferior é {limite_inferior}')
    print(f'Limite superior é {limite_superior}')
    print(f'Amplitude total é {amplitude_total}')

    df_recuperacao_veiculos_outliers_superior = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] > limite_superior]

    df_recuperacao_veiculos_outliers_inferior = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] < limite_inferior]

    print('\nDPs com recuperações superiores as demais: ')

    if len(df_recuperacao_veiculos_outliers_superior) == 0:
        print('Não existem DPs com valores discrepantes superiores')
    else:
        print(df_recuperacao_veiculos_outliers_superior.sort_values(
            by='recuperacao_veiculos', ascending=False))
    
    print('\nDPs com recuperações inferiores as demais: ')

    if len(df_recuperacao_veiculos_outliers_inferior) == 0:
        print('Não existem DPs com valores discrepantes inferiores')
    else:
        print(df_recuperacao_veiculos_outliers_inferior.sort_values(
            by='recuperacao_veiculos', ascending=True))

except ImportError as e:
    print(f'Erro ao obter informações sobre recuperação de veículos: {e}')
    exit()

try:

    print('Calculando medidas de distribuição...')

    assimetria = df_recuperacao_veiculos['recuperacao_veiculos'].skew()

    curtose = df_recuperacao_veiculos['recuperacao_veiculos'].kurtosis()

    print('\nMedidas e distribuição: ')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()

try:

    plt.subplots(2, 2, figsize=(16, 7 ))
    plt.suptitle('Análise de recuperação de veículos no RJ', fontsize=20)

    plt.subplot(2, 2, 1)
    plt.boxplot(array_recuperacao_veiculos, vert=False, showmeans=True)
    plt.title('Recuperação de veículos')

    plt.subplot(2, 2, 2)
    plt.hist(array_recuperacao_veiculos, bins=50, edgecolor='black')
    plt.axvline(media_recuperacao_veiculos, color='g', linewidth=1)
    plt.axvline(mediana_recuperacao_veiculos, color='y', linewidth=1)

    plt.subplot(2, 2, 3)  # Configurar o segundo gráfico no lado direito
    plt.text(0.1, 0.9, f'Média: {media_recuperacao_veiculos}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_recuperacao_veiculos}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana_recuperacao_veiculos}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude_total}', fontsize=12)
    plt.title('Medidas Observadas')

    plt.axis('off')

    plt.tight_layout()

    plt.subplot(2, 2, 4)  # Configurar o segundo gráfico no lado direito
    plt.text(0.1, 0.5, f'Assimetria: {assimetria}', fontsize=12)
    plt.text(0.1, 0.4, f'Curtose: {curtose}', fontsize=12)
    plt.title('Medidas Observadas')

    plt.axis('off')

    plt.tight_layout()

    plt.show()

except ImportError  as e:
    print(f'Erro ao obter informações sobre recuperação de veículos: {e}')
    exit()