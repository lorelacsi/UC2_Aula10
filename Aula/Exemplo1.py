import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    df_roubo_veiculo = df_roubo_veiculo.groupby(['munic']).sum(['roubo_veiculo']).reset_index()

    print(df_roubo_veiculo.head())
    print('\nDados obtidos com sucesso')

except Exception as e:
    print(f'Erro ao obter dados: {e}')
    exit()


try:
    print('\nCalculando informações sobre padrão de roubo de veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia_media_mediana_roubo = abs((media_roubo_veiculo - mediana_roubo_veiculo)/mediana_roubo_veiculo)#*100
    
    print(f'Media de roubo de veiculos: {media_roubo_veiculo}')
    print(f'Mediana de roubo de veiculos: {mediana_roubo_veiculo}')
    print(f'Diferenca entre media e mediana: {distancia_media_mediana_roubo}')

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de dispersão: ')
    print('Máximo: ', maximo)
    print('Mínimo: ', minimo)
    print('Amplitude: ', amplitude)

    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')


    iqr = q3 - q1 
   
    limite_superior = q3 + (1.5 * iqr)

    limite_inferior = q1 - (1.5 * iqr)

    print('\nMedidas de posição: ')
    print('Mínimo: ', minimo)
    print(f'Limite inferior: {limite_inferior}')
    print(f'Q1 (25%) = {q1}')
    print(f'Q2 (50%) = {q2}')
    print(f'Q3 (75%) = {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite superior: {limite_superior}')
    print('Máximo: ', maximo)

    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
    print('\nMunicipios com outliers inferiores: ')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending= True))

    print('\nMunicipios com outliers superiores')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))  
          
except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()


try:

    plt.subplots(1, 2, figsize=(16, 7 ))
    plt.suptitle('Análise de roubo de veículos no RJ')

    plt.subplot(1, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('Boxplot dos Dados')

    plt.subplot(1, 2, 2)  # Configurar o segundo gráfico no lado direito
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana_roubo}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.title('Medidas Observadas')

# Tirar os eixos
    plt.axis('off')

# Ajustar o layout
    plt.tight_layout()

    plt.show()

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()