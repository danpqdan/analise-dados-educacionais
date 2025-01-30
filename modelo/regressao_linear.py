import pandas as pd
from sklearn.linear_model import LinearRegression


def treinar_modelo():
    df_uf = pd.read_excel("./data/media_escolar_por_uf.xlsx")

    colunas_anos_ef = [
        'ideb_pub_ef_2013', 'ideb_pvt_ef_2013',
        'ideb_pub_ef_2015', 'ideb_pvt_ef_2015',
        'ideb_pub_ef_2017', 'ideb_pvt_ef_2017',
        'ideb_pub_ef_2019', 'ideb_pvt_ef_2019',
        'ideb_pub_ef_2021', 'ideb_pvt_ef_2021'
    ]
    colunas_anos_em = [
        'ideb_pub_em_2013', 'ideb_pvt_em_2013',
        'ideb_pub_em_2015', 'ideb_pvt_em_2015',
        'ideb_pub_em_2017', 'ideb_pvt_em_2017',
        'ideb_pub_em_2019', 'ideb_pvt_em_2019',
        'ideb_pub_em_2021', 'ideb_pvt_em_2021'
    ]
    # Remover valores ausentes
    df_uf = df_uf.dropna(subset=colunas_anos_ef + ['ideb_pub_ef_2023', 'ideb_pvt_ef_2023'])
    df_uf = df_uf.dropna(subset=colunas_anos_em + ['ideb_pub_em_2023', 'ideb_pvt_em_2023'])
    
    # Definir variáveis independentes (X) e variável alvo (y)
    X1 = df_uf[colunas_anos_ef]  # Usamos os anos de 2013 a 2021 para públicas e privadas
    X2 = df_uf[colunas_anos_em] 

    y_pub_ef = df_uf['ideb_pub_ef_2023']  # Prevemos IDEB público de 2023
    y_pvt_ef = df_uf['ideb_pvt_ef_2023']  # Prevemos IDEB privado de 2023
    y_pub_em = df_uf['ideb_pub_em_2023']
    y_pvt_em = df_uf['ideb_pvt_em_2023']
    
    
    model_pub_ef = LinearRegression()
    model_pub_ef.fit(X1, y_pub_ef)
    model_pvt_ef = LinearRegression()
    model_pvt_ef.fit(X1, y_pvt_ef)
    model_pub_em = LinearRegression()
    model_pub_em.fit(X2, y_pub_em)
    model_pvt_em = LinearRegression()
    model_pvt_em.fit(X2, y_pvt_em)

    return df_uf, model_pub_ef, model_pvt_ef, model_pub_em, model_pvt_em, colunas_anos_em, colunas_anos_ef



def treinar_modelo_previsao_independente():
    df_uf = pd.read_excel("./data/media_escolar_por_uf.xlsx")

    # Verificar se a leitura do arquivo gerou um DataFrame válido
    if not isinstance(df_uf, pd.DataFrame):
        raise TypeError("Erro na leitura do arquivo. df_uf não é um DataFrame válido.")

    colunas_anos_ef = [
        'ideb_pub_ef_2013', 'ideb_pvt_ef_2013',
        'ideb_pub_ef_2015', 'ideb_pvt_ef_2015',
        'ideb_pub_ef_2017', 'ideb_pvt_ef_2017',
        'ideb_pub_ef_2019', 'ideb_pvt_ef_2019',
        'ideb_pub_ef_2021', 'ideb_pvt_ef_2021',
        'ideb_pub_ef_2023', 'ideb_pvt_ef_2023',
    ]
    colunas_anos_em = [
        'ideb_pub_em_2013', 'ideb_pvt_em_2013',
        'ideb_pub_em_2015', 'ideb_pvt_em_2015',
        'ideb_pub_em_2017', 'ideb_pvt_em_2017',
        'ideb_pub_em_2019', 'ideb_pvt_em_2019',
        'ideb_pub_em_2021', 'ideb_pvt_em_2021',
        'ideb_pub_em_2023', 'ideb_pvt_em_2023'
    ]
    
    # Remover valores ausentes
    df_uf = df_uf.dropna(subset=colunas_anos_ef + ['ideb_pub_ef_2023', 'ideb_pvt_ef_2023'])
    df_uf = df_uf.dropna(subset=colunas_anos_em + ['ideb_pub_em_2023', 'ideb_pvt_em_2023'])
    
    # Verificar novamente o tipo após a limpeza
    if not isinstance(df_uf, pd.DataFrame):
        raise TypeError("Erro após a limpeza de dados. df_uf não é um DataFrame válido.")
    
    # Definir variáveis independentes (X) e variável alvo (y)
    X1 = df_uf[colunas_anos_ef]  # Usamos os anos de 2013 a 2021 para públicas e privadas
    X2 = df_uf[colunas_anos_em] 

    y_pub_ef = df_uf['ideb_pub_ef_2023']  # Prevemos IDEB público de 2023
    y_pvt_ef = df_uf['ideb_pvt_ef_2023']  # Prevemos IDEB privado de 2023
    y_pub_em = df_uf['ideb_pub_em_2023']
    y_pvt_em = df_uf['ideb_pvt_em_2023']
    
    model_pub_ef = LinearRegression()
    model_pub_ef.fit(X1, y_pub_ef)
    model_pvt_ef = LinearRegression()
    model_pvt_ef.fit(X1, y_pvt_ef)
    model_pub_em = LinearRegression()
    model_pub_em.fit(X2, y_pub_em)
    model_pvt_em = LinearRegression()
    model_pvt_em.fit(X2, y_pvt_em)

    return df_uf, model_pub_ef, model_pvt_ef, model_pub_em, model_pvt_em, colunas_anos_em, colunas_anos_ef

