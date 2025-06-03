"""Funções usadas no eda e pre-processing de dados."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import power_transform
from scipy import stats
from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
import regex as re


def classificar_idh(valor):
    """função para classificacão do idh."""

    if valor >= 0.800:
        return 'Muito Alto'
    elif valor >= 0.700:
        return 'Alto'
    elif valor >= 0.550:
        return 'Médio'
    else:
        return 'Baixo'


def obter_dados_idh(df):
    """função para construir as colunas dependentes para cálculo do idh"""

    # dicionario que recebe os parâmetros usados nas etapas intermediárias do cálculo
    data = {
        'Expectativa de Vida': [72, 80, 65],
        'Taxa de Alfabetização': [95, 99, 80],
        'PIB_per_capita': [10000, 40000, 3000]}

    # Constroi o índice de vida normalizado a partir da expectativa de vida.
    df['idx_vida'] = (df['Expectativa de Vida'] - 20) / (85 - 20)

    # Índice de educação
    df['idx_educ'] = df['Taxa de Alfabetização'] / 100

    # Índice de renda
    df['idx_renda'] = (np.log(df['PIB_per_capita']) -
                       np.log(100)) / (np.log(75000) - np.log(100))

    # Constroi o IDH estimado a partir das colunas anteriores
    df['IDH_estimado'] = (df['idx_vida'] * df['idx_educ']
                          * df['idx_renda']) ** (1/3)

    return df


def contagem_nulos(df=pd.DataFrame):
    """Função que conta a quantidade de nulos"""
    return df.isna().sum()


def tratamento_depara(df_depara, df_correcao):
    """Função que substitui os valores da coluna pais para o nome padrão."""

    depara = df_depara.set_index(df_depara['Pais'])['pais_corrigido'].to_dict()
    df_correcao['pais'] = df_correcao['pais'].replace(depara)
    return df_correcao['pais']


def gerar_grafico_valores_nulos(df=pd.DataFrame, dados_nulos=pd.Series):
    """Função para gerar um gráfico para visualização de linhas vazias."""
    plt.figure(figsize=(15, 3))
    plt.title('Quantidade de valores por coluna: presença de nulos.')
    plt.xticks(rotation=60)
    plt.bar(dados_nulos.index, df.shape[0]-dados_nulos)
    return plt.show()


def grafico_mosaico_feat_paises(tbl_agrupada=pd.DataFrame):
    """Função para gerar gráfico mosaico de analise"""

    # layout do mosaico de gráficos
    layout = [
        ["A", "B"],
        ["C", "C"],]

    # construção da figura
    fig, ax = plt.subplot_mosaic(layout, figsize=(10, 5))

    ax['A'].set_title('Histograma dos países')
    ax['A'].set_xlabel('')
    # gráfico com a distribuição dos dados por quantidade
    sns.histplot(data=tbl_agrupada[['qtde_kg']],
                 x=tbl_agrupada['pct_qtde_total_pais'], ax=ax['A'],
                 bins=60, color='lightgrey', kde=True)

    # título do gráfico B
    ax['B'].set_title(
        'Concentração dos países pelo consumo histórico: países ')
    ax['B'].set_xlabel('')
    # gráfico stripplot para visualizar a distribuição dos dados
    sns.stripplot(data=tbl_agrupada,
                  x='pct_qtde_total_pais',
                  color='lightgrey',
                  ax=ax['B'],
                  size=5)

    # sobreposição do gráfico striplot para aplicar o filtro de cor.
    filtro = tbl_agrupada['pct_qtde_total_pais'] <= 0.0000001
    sns.stripplot(data=tbl_agrupada[filtro],
                  x='pct_qtde_total_pais',
                  color='lightblue',
                  ax=ax['B'],
                  size=5)

    ax['C'].set_title('Países')

    # Gráfico de barras com países filtrados
    tbl_agrupada[filtro][['qtde_kg']].plot.bar(
        ax=ax['C'], legend=False, color='lightblue')

    # titulo superior do gráfico.
    plt.suptitle('Distribuição dos Países x Quantidade Total (1970-2024)')

    # ajuste do espaço entre os gráficos.
    fig.tight_layout()

    return plt.show()


def graficos_analise_outliers(df=pd.DataFrame, scale=False, metodo_scale: str = "box-cox"):
    """Função que gera """
    # retorna apenas 1 vizualiação dos dados.
    if scale is False:

        df.select_dtypes(include='number').plot.box(figsize=(10, 4))
        plt.xticks(rotation=60)
        return plt.show()

    # comparação de distribuição com transformação.
    else:
        fig, ax = plt.subplots(2, 1, figsize=(20, 10), sharex=True)

        # Gráfico original com clipagem dos dados
        df.select_dtypes(include='number').plot.box(ax=ax[0])
        ax[0].set_title('Dados sem scale.')

        # clipagem de limite e scale dos dados
        df_clip = df.select_dtypes(include='number')
        scaled_data = power_transform(df_clip, method=metodo_scale)
        scaled_df = pd.DataFrame(scaled_data, columns=df_clip.columns)

        # Gráfico transformado
        scaled_df.plot.box(ax=ax[1])
        ax[1].set_title(f'Scale dos dados com método {metodo_scale}.')

        plt.suptitle('Análise de Outliers')
        plt.xticks(rotation=60)

        return plt.show()


def graficos_ditribuicao(df, scale=False, metodo_scale='box-cox'):
    """
    Plota gráficos de distribuição para as colunas numéricas de um DataFrame.

    Parâmetros:
    - df: pd.DataFrame, o dataset.
    - scale: bool, se True aplica power_transform.
    - metodo_scale: str, método de transformação: 'box-cox' ou 'yeo-johnson'.

    Retorna:
    - None, apenas plota os gráficos.
    """

    # Seleciona apenas colunas numéricas
    num_cols = df.select_dtypes(include='number').columns
    n_cols = len(num_cols)

    # Caso queira aplicar a transformação
    if scale:
        df_scaled = df.copy()
        df_scaled[num_cols] = power_transform(
            df_scaled[num_cols], method=metodo_scale)
        df_to_plot = df_scaled
        title_suffix = f' (Scaled: {metodo_scale})'
    else:
        df_to_plot = df
        title_suffix = ' (Original)'

    # Definindo número de linhas e colunas do grid
    n_rows = (n_cols + 2) // 3  # até 3 gráficos por linha

    plt.figure(figsize=(15, n_rows * 4))

    for idx, col in enumerate(num_cols, 1):
        plt.subplot(n_rows, 4, idx)
        sns.histplot(df_to_plot[col], kde=True, bins=30, color='skyblue')
        plt.title(f'Distribuição de {col}{title_suffix}')
        plt.xlabel('')
        plt.ylabel('')

    plt.tight_layout()
    plt.show()


def graficos_qq_plots(df, scale=False, metodo_scale='box-cox'):
    """
    Plota QQ-Plots para as colunas numéricas de um DataFrame.

    Parâmetros:
    - df: pd.DataFrame, o dataset.
    - scale: bool, se True aplica power_transform.
    - metodo_scale: str, método de transformação: 'box-cox' ou 'yeo-johnson'.

    Retorna:
    - None, apenas plota os gráficos.
    """

    # Seleciona colunas numéricas
    num_cols = df.select_dtypes(include='number').columns
    n_cols = len(num_cols)

    # Aplica transformação se necessário
    if scale:
        df_scaled = df.copy()
        df_scaled[num_cols] = power_transform(
            df_scaled[num_cols], method=metodo_scale)
        df_to_plot = df_scaled
        title_suffix = f' (Scaled: {metodo_scale})'
    else:
        df_to_plot = df
        title_suffix = ' (Original)'

    # Define grid de subplots
    n_cols_subplot = 3  # até 3 plots por linha
    # arredonda para cima
    n_rows = (n_cols + n_cols_subplot - 1) // n_cols_subplot

    fig, axes = plt.subplots(n_rows, n_cols_subplot,
                             figsize=(5 * n_cols_subplot, 4 * n_rows))
    axes = axes.ravel()

    for ax, col in zip(axes, num_cols):
        stats.probplot(df_to_plot[col], dist="norm", plot=ax)
        ax.set_title(f'QQ-Plot de {col}{title_suffix}')
        ax.set_xlabel('')
        ax.set_ylabel('')

    # Remove eixos extras se houver
    for idx in range(len(num_cols), len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    plt.show()


def teste_shapiro_wilk_norm(df=pd.DataFrame, scale=False, metodo_scale='box-cox'):
    """Função que analista a normalidade dos dados aplicando o teste Shapiro-Wilk

    Aplica o teste de Shapiro-Wilk para várias colunas numéricas.

    Parâmetros:
    - df: pd.DataFrame
    - scale: bool, se True aplica power_transform antes do teste
    - metodo_scale: str, 'box-cox' ou 'yeo-johnson'

    Retorna:
    - pd.DataFrame com estatísticas do teste
    """
    num_cols = df.select_dtypes(include='number').columns
    results = []

    if scale:
        df_scaled = df.copy()
        df_scaled[num_cols] = power_transform(
            df_scaled[num_cols], method=metodo_scale)
        df_to_test = df_scaled
    else:
        df_to_test = df

    for col in num_cols:
        data = df_to_test[col].dropna()
        stat, p_value = shapiro(data)
        results.append({
            'coluna': col,
            'statistic': stat,
            'p_value': p_value,
            'normal': p_value > 0.05
        })
        df_resultado = pd.DataFrame(results)
    return df_resultado


def vif_analise(df):
    """Função para gerar a métrica VIF para verificar multicolinearidade dos dados."""
    # VIF
    tbl_vif_data = pd.DataFrame()
    tbl_vif_data['Feature'] = df.columns
    tbl_vif_data['VIF'] = [
        variance_inflation_factor(df.values, i)
        for i in range(df.shape[1])]

    return tbl_vif_data
