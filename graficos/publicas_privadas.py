import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from graficos.distribuicao_escolas import calcular_totais_escolas_tecnologia_separado
from graficos.melhorias import inclusao_tech
from modelo.regressao_linear import treinar_modelo, treinar_modelo_previsao_independente

@st.cache_data
def calcular_melhores_escolas():
    # Carregar o primeiro arquivo com as escolas
    file_path = './data/institucoes_ideb.xlsx'
    df_escolas = pd.read_excel(file_path)
    
    # Atualizando o nome das colunas conforme o novo cabeçalho
    df_escolas.columns = [
        'Sigla UF', 'Código Município', 'Nome Município', 'Código Escola', 'Nome Escola', 'Rede',
        'Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa', 'Nota SAEB 2017 Nota Média Padronizada (N)',
        'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 'Nota SAEB 2019 Nota Média Padronizada (N)',
        'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa', 'Nota SAEB 2021 Nota Média Padronizada (N)',
        'Nota SAEB 2023 Matemática', 'Nota SAEB 2023 Língua Portuguesa', 'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023', 'Metas 1º ciclo Ideb'
    ]
    
    # Remover as linhas com valores inválidos (como " - ")
    df_escolas.replace(" - ", pd.NA, inplace=True)
    df_escolas.dropna(subset=[
        'Nota SAEB 2017 Nota Média Padronizada (N)',
        'Nota SAEB 2019 Nota Média Padronizada (N)',
        'Nota SAEB 2021 Nota Média Padronizada (N)',
        'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023'
    ], inplace=True)

    # Converter para valores numéricos
    df_escolas[['Nota SAEB 2017 Nota Média Padronizada (N)', 
        'Nota SAEB 2019 Nota Média Padronizada (N)', 
        'Nota SAEB 2021 Nota Média Padronizada (N)', 
        'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']] = df_escolas[[
            'Nota SAEB 2017 Nota Média Padronizada (N)', 
            'Nota SAEB 2019 Nota Média Padronizada (N)', 
            'Nota SAEB 2021 Nota Média Padronizada (N)', 
            'Nota SAEB 2023 Nota Média Padronizada (N)',
            'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']].apply(pd.to_numeric, errors='coerce')

    # Criando as colunas de métricas combinadas
    df_escolas['Nota Média Padronizada Geral'] = df_escolas[[
        'Nota SAEB 2017 Nota Média Padronizada (N)', 
        'Nota SAEB 2019 Nota Média Padronizada (N)', 
        'Nota SAEB 2021 Nota Média Padronizada (N)', 
        'Nota SAEB 2023 Nota Média Padronizada (N)']].mean(axis=1)
    df_escolas['IDEB Geral'] = df_escolas[[
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']].mean(axis=1)
    df_escolas['Métrica Combinada'] = (df_escolas['Nota Média Padronizada Geral'] + df_escolas['IDEB Geral']) / 2

    # Ordenando para obter as 100 melhores escolas
    melhores_escolas = df_escolas.sort_values('Métrica Combinada', ascending=False)
    melhores_escolas_top100 = melhores_escolas.head(100)
    
    # Ordenando para obter as 100 piores escolas
    piores_escolas = df_escolas.sort_values('Métrica Combinada', ascending=True)
    piores_escolas_top100 = piores_escolas.head(100)

    # Exibir as 100 melhores e piores escolas no Streamlit
    st.write("Top 100 Melhores Escolas com base na Nota Média Padronizada e IDEB")
    st.dataframe(melhores_escolas_top100[['Nome Escola', 'Sigla UF', 'Rede', 'Nota Média Padronizada Geral', 'IDEB Geral', 'Métrica Combinada']])
    
    st.write("Top 100 Piores Escolas com base na Nota Média Padronizada e IDEB")
    st.dataframe(piores_escolas_top100[['Nome Escola', 'Sigla UF', 'Rede', 'Nota Média Padronizada Geral', 'IDEB Geral', 'Métrica Combinada']])


    st.header('Notas')
    st.write('''Esses calculos contaram com indeces do ideb e saeb, realizado a média entre 5 anos
             de dados e selecionado aquelas que tiveram um baixo desempenho em ambos.''')


@st.cache_data
def prever_ideb():
    try:
        df_uf, model_pub_ef, model_pvt_ef, model_pub_em, model_pvt_em, colunas_anos_em, colunas_anos_ef = treinar_modelo()
        
               
        # Fazer previsões para 2023
        df_uf['previsto_2023_pub_ef'] = model_pub_ef.predict(df_uf[colunas_anos_ef])
        df_uf['previsto_2023_pvt_ef'] = model_pvt_ef.predict(df_uf[colunas_anos_ef])
        df_uf['previsto_2023_pub_em'] = model_pub_em.predict(df_uf[colunas_anos_em])
        df_uf['previsto_2023_pvt_em'] = model_pvt_em.predict(df_uf[colunas_anos_em])

        # Estimar o IDEB de 2024 assumindo a mesma tendência de crescimento
        df_uf['previsto_2024_pub_ef'] = df_uf['previsto_2023_pub_ef'] + (df_uf['previsto_2023_pub_ef'] - df_uf['ideb_pub_ef_2023'])
        df_uf['previsto_2024_pvt_ef'] = df_uf['previsto_2023_pvt_ef'] + (df_uf['previsto_2023_pvt_ef'] - df_uf['ideb_pvt_ef_2023'])
        df_uf['previsto_2024_pub_em'] = df_uf['previsto_2023_pub_em'] + (df_uf['previsto_2023_pub_em'] - df_uf['ideb_pub_em_2023'])
        df_uf['previsto_2024_pvt_em'] = df_uf['previsto_2023_pvt_em'] + (df_uf['previsto_2023_pvt_em'] - df_uf['ideb_pvt_em_2023'])

        # Avaliação do modelo para 2023
        erro_medio_pub_ef = mean_absolute_error(df_uf['ideb_pub_ef_2023'], df_uf['previsto_2023_pub_ef'])
        r2_pub_ef = r2_score(df_uf['ideb_pub_ef_2023'], df_uf['previsto_2023_pub_ef'])

        erro_medio_pvt_ef = mean_absolute_error(df_uf['ideb_pvt_ef_2023'], df_uf['previsto_2023_pvt_ef'])
        r2_pvt_ef = r2_score(df_uf['ideb_pvt_ef_2023'], df_uf['previsto_2023_pvt_ef'])

        erro_medio_pub_em = mean_absolute_error(df_uf['ideb_pub_em_2023'], df_uf['previsto_2023_pub_em'])
        r2_pub_em = r2_score(df_uf['ideb_pub_em_2023'], df_uf['previsto_2023_pub_em'])

        erro_medio_pvt_em = mean_absolute_error(df_uf['ideb_pvt_em_2023'], df_uf['previsto_2023_pvt_em'])
        r2_pvt_em = r2_score(df_uf['ideb_pvt_em_2023'], df_uf['previsto_2023_pvt_em'])


        # Exibição no Streamlit
        st.title("Análise de escola x estado")
        st.write(f"Erro médio absoluto (Público - Ensino Fundamental 2023): {erro_medio_pub_ef:.4f}")
        st.write(f"Coeficiente de determinação (R²) (Público - Ensino Fundamental 2023): {r2_pub_ef:.4f}")
        st.write(f"Erro médio absoluto (Privado - Ensino Fundamental 2023): {erro_medio_pvt_ef:.4f}")
        st.write(f"Coeficiente de determinação (R²) (Privado - Ensino Fundamental 2023): {r2_pvt_ef:.4f}")
        st.write(f"Erro médio absoluto (Público - Ensino Médio 2023): {erro_medio_pub_em:.4f}")
        st.write(f"Coeficiente de determinação (R²) (Público - Ensino Médio 2023): {r2_pub_em:.4f}")
        st.write(f"Erro médio absoluto (Privado - Ensino Médio 2023): {erro_medio_pvt_em:.4f}")
        st.write(f"Coeficiente de determinação (R²) (Privado - Ensino Médio 2023): {r2_pvt_em:.4f}")

        # Gráficos e visualizações
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df_uf['ideb_pub_ef_2023'], df_uf['previsto_2023_pub_ef'], color='blue', label='Previsões Públicas Ensino final 2023')
        ax.scatter(df_uf['ideb_pvt_ef_2023'], df_uf['previsto_2023_pvt_ef'], color='green', label='Previsões Privadas Ensino final 2023')

        # Definindo os valores mínimo e máximo para a linha de perfeição com base nos dados reais e previstos
        min_val = min(df_uf['ideb_pub_ef_2023'].min(), df_uf['previsto_2023_pub_ef'].min(), 
                      df_uf['ideb_pvt_ef_2023'].min(), df_uf['previsto_2023_pvt_ef'].min())
        max_val = max(df_uf['ideb_pub_ef_2023'].max(), df_uf['previsto_2023_pub_ef'].max(), 
                      df_uf['ideb_pvt_ef_2023'].max(), df_uf['previsto_2023_pvt_ef'].max())

        # Desenhando a linha de perfeição (y = x)
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfeição (Linha de acerto)')

        # Adicionando os nomes dos estados ao lado dos pontos
        for i, row in df_uf.iterrows():
            ax.text(row['ideb_pub_ef_2023'], row['previsto_2023_pub_ef'], row['estado'], fontsize=9, ha='right', color='blue')
            ax.text(row['ideb_pvt_ef_2023'], row['previsto_2023_pvt_ef'], row['estado'], fontsize=9, ha='right', color='green')

        ax.legend()
        ax.set_xlabel("IDEB Real 2023")
        ax.set_ylabel("IDEB Previsto 2023")
        ax.set_title("Previsão x Real para IDEB 2023 (Público e Privado)")
        st.pyplot(fig)

        # informações
        st.subheader('Notas')
        st.subheader('Os dados foram analisados de 2013 a 2022')
        st.subheader('O maior erro da previsão foi cerca de 0.18 pontos no IDEB')

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None, None, None, None, None, None, None, None, None

   
def prever_ideb_para_ano(ano: int):
    # Carregar e treinar o modelo
    df_uf, model_pub_ef, model_pvt_ef, model_pub_em, model_pvt_em, colunas_anos_em, colunas_anos_ef = treinar_modelo_previsao_independente()
       
    # Previsões para o ano de 2023
    if ano > 2023:
        # Previsão para 2023
        previsao_2023_pub_ef = model_pub_ef.predict(df_uf[colunas_anos_ef])
        previsao_2023_pvt_ef = model_pvt_ef.predict(df_uf[colunas_anos_ef])
        previsao_2023_pub_em = model_pub_em.predict(df_uf[colunas_anos_em])
        previsao_2023_pvt_em = model_pvt_em.predict(df_uf[colunas_anos_em])

        # Ajuste de crescimento para o ano futuro
        crescimento_pub_ef = model_pub_ef.coef_.sum()  # Somatório dos coeficientes para o crescimento
        crescimento_pvt_ef = model_pvt_ef.coef_.sum()
        crescimento_pub_em = model_pub_em.coef_.sum()
        crescimento_pvt_em = model_pvt_em.coef_.sum()

        # Calculando a previsão para o ano solicitado com o crescimento
        df_uf[f'previsto_{ano}_pub_ef'] = previsao_2023_pub_ef + (ano - 2023) * crescimento_pub_ef
        df_uf[f'previsto_{ano}_pvt_ef'] = previsao_2023_pvt_ef + (ano - 2023) * crescimento_pvt_ef
        df_uf[f'previsto_{ano}_pub_em'] = previsao_2023_pub_em + (ano - 2023) * crescimento_pub_em
        df_uf[f'previsto_{ano}_pvt_em'] = previsao_2023_pvt_em + (ano - 2023) * crescimento_pvt_em

    else:
        # Caso o ano seja 2023 ou anterior, usa-se o modelo treinado
        df_uf[f'previsto_{ano}_pub_ef'] = model_pub_ef.predict(df_uf[colunas_anos_ef])
        df_uf[f'previsto_{ano}_pvt_ef'] = model_pvt_ef.predict(df_uf[colunas_anos_ef])
        df_uf[f'previsto_{ano}_pub_em'] = model_pub_em.predict(df_uf[colunas_anos_em])
        df_uf[f'previsto_{ano}_pvt_em'] = model_pvt_em.predict(df_uf[colunas_anos_em])
    
    colors = ['#F4A460', '#00BFFF', '#8B4513', '#191970']

        # Criar gráfico com os dados previstos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando as linhas com as cores personalizadas
    ax.plot(df_uf['estado'], df_uf[f'previsto_{ano}_pub_ef'], label=f'Previsão Pública EF {ano}', marker='o', color=colors[0])
    ax.plot(df_uf['estado'], df_uf[f'previsto_{ano}_pvt_ef'], label=f'Previsão Privada EF {ano}', marker='o', color=colors[1])
    ax.plot(df_uf['estado'], df_uf[f'previsto_{ano}_pub_em'], label=f'Previsão Pública EM {ano}', marker='o', color=colors[2])
    ax.plot(df_uf['estado'], df_uf[f'previsto_{ano}_pvt_em'], label=f'Previsão Privada EM {ano}', marker='o', color=colors[3])
    
    # Adicionando os valores de cada ponto no gráfico
    for i, row in df_uf.iterrows():
        ax.text(row['estado'], row[f'previsto_{ano}_pub_ef'], f'{row[f"previsto_{ano}_pub_ef"]:.2f}', 
                fontsize=9, ha='left', color=colors[0])
        ax.text(row['estado'], row[f'previsto_{ano}_pvt_ef'], f'{row[f"previsto_{ano}_pvt_ef"]:.2f}', 
                fontsize=9, ha='left', color=colors[1])
        ax.text(row['estado'], row[f'previsto_{ano}_pub_em'], f'{row[f"previsto_{ano}_pub_em"]:.2f}', 
                fontsize=9, ha='left', color=colors[2])
        ax.text(row['estado'], row[f'previsto_{ano}_pvt_em'], f'{row[f"previsto_{ano}_pvt_em"]:.2f}', 
                fontsize=9, ha='left', color=colors[3])

    # Personalizar o gráfico
    ax.set_title(f"Previsões de IDEB para o ano {ano}")
    ax.set_xlabel('Estado')
    ax.set_ylabel('Índice IDEB')
    # Rotacionando os rótulos dos estados
    ax.set_xticklabels(df_uf['estado'], rotation=90)
    # Exibindo a legenda
    ax.legend()
    # Adicionando a grade
    ax.grid(True)
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)
    st.subheader('''Dados apresentados são baseados em estatisticas e não representão o valor real do resultado''')



@st.cache_data
def calcular_melhores_escolas_por_estado():
    st.title('A importancia das escolas tecnicas')
    st.write('''
                 Note no gráfico abaixo que as escolas lideres são escolas federais como IFs e Colégio de Aplicação que incluem ensino politécnico
                 e grande parte das escolas que lideram o ranking são Privadas. Ou seja ambos oferecem um ensino de qualidade e infra-estrutura aos alunos.
                 ''')
    # Carregar o arquivo com os dados das escolas
    df_escolas = pd.read_excel('./data/institucoes_ideb.xlsx')
    
    # Atualizando o nome das colunas conforme o novo cabeçalho
    df_escolas.columns = [
        'Sigla UF', 'Código Município', 'Nome Município', 'Código Escola', 'Nome Escola', 'Rede',
        'Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa', 'Nota SAEB 2017 Nota Média Padronizada (N)',
        'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 'Nota SAEB 2019 Nota Média Padronizada (N)',
        'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa', 'Nota SAEB 2021 Nota Média Padronizada (N)',
        'Nota SAEB 2023 Matemática', 'Nota SAEB 2023 Língua Portuguesa', 'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023', 'Metas 1º ciclo Ideb'
    ]
    
    # Remover as linhas com valores inválidos (como " - ")
    df_escolas.replace(" - ", pd.NA, inplace=True)
    df_escolas.dropna(subset=[
        'Nota SAEB 2017 Nota Média Padronizada (N)',
        'Nota SAEB 2019 Nota Média Padronizada (N)',
        'Nota SAEB 2021 Nota Média Padronizada (N)',
        'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023'
    ], inplace=True)
    
    # Converter para valores numéricos
    df_escolas[['Nota SAEB 2017 Nota Média Padronizada (N)', 
        'Nota SAEB 2019 Nota Média Padronizada (N)', 
        'Nota SAEB 2021 Nota Média Padronizada (N)', 
        'Nota SAEB 2023 Nota Média Padronizada (N)',
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']] = df_escolas[[
            'Nota SAEB 2017 Nota Média Padronizada (N)', 
            'Nota SAEB 2019 Nota Média Padronizada (N)', 
            'Nota SAEB 2021 Nota Média Padronizada (N)', 
            'Nota SAEB 2023 Nota Média Padronizada (N)',
            'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']].apply(pd.to_numeric, errors='coerce')
    
    # Criando as colunas de métricas combinadas
    df_escolas['Nota Média Padronizada Geral'] = df_escolas[[
        'Nota SAEB 2017 Nota Média Padronizada (N)', 
        'Nota SAEB 2019 Nota Média Padronizada (N)', 
        'Nota SAEB 2021 Nota Média Padronizada (N)', 
        'Nota SAEB 2023 Nota Média Padronizada (N)']].mean(axis=1)
    
    df_escolas['IDEB Geral'] = df_escolas[[
        'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023']].mean(axis=1)
    
    df_escolas['Métrica Combinada'] = (df_escolas['Nota Média Padronizada Geral'] + df_escolas['IDEB Geral']) / 2
    
    # Agrupar por estado e rede (Privada, Estadual)
    df_estado_rede = df_escolas.groupby(['Sigla UF', 'Rede']).agg(
        total_escolas=('Nome Escola', 'count'),
        ideb_medio=('IDEB Geral', 'mean'),
        nota_media_padronizada=('Nota Média Padronizada Geral', 'mean')
    ).reset_index()
    
    # Calcular a diferença entre as médias de IDEB entre as escolas estaduais/municipais e privadas
    estado_rede_estado = df_estado_rede[df_estado_rede['Rede'] == 'Estadual']
    estado_rede_privada = df_estado_rede[df_estado_rede['Rede'] == 'Privada']
    estado_rede_federal = df_estado_rede[df_estado_rede['Rede'] == 'Federal']
    
    # Calcular a diferença de IDEB e nota média padronizada entre as duas redes
    diferenca_ideb = estado_rede_privada['ideb_medio'].mean() - estado_rede_estado['ideb_medio'].mean()
    diferenca_nota_media = estado_rede_privada['nota_media_padronizada'].mean() - estado_rede_estado['nota_media_padronizada'].mean()
    diferenca_ideb_federal = estado_rede_privada['ideb_medio'].mean() - estado_rede_federal['ideb_medio'].mean()
    diferenca_nota_media_federal = estado_rede_privada['nota_media_padronizada'].mean() - estado_rede_federal['nota_media_padronizada'].mean()

    # Exibir as informações agregadas para cada estado e rede
    st.write("### Resumo das Melhores Escolas por Estado e Rede (Privada/Estadual)")
    st.dataframe(df_estado_rede)

    st.subheader('Legenda do dataframe')
    st.write('Federais: especializados na oferta de educação profissional e tecnológica (EPT)')
    st.write('Estaduais: Escola que recebe financiamento do estado para funcionar. incluem o ensino fundamental (escola primária) para crianças e o ensino médio (escola secundária) para os adolescentes que concluíram o fundamental')
    st.write('Privada: A escola particular é toda aquela mantida por pessoa física ou jurídica de direito particular.')
    st.write('Municipal: é administrada pelo município.')
    
    st.header('Notas a se observar')
    st.subheader(f'Diferença total da média entre escolas estaduais/municipais e privadas:')
    st.write(f'Diferença no IDEB médio entre estaduais/municipais e privadas: {diferenca_ideb:.4f}')
    st.write(f'Diferença na Nota Média Padronizada entre estaduais/municipais e privadas: {diferenca_nota_media:.4f}')
    st.subheader(f'Diferença total da média entre escolas federais e privadas:')
    st.write(f'Diferença no IDEB médio entre federais e privadas: {diferenca_ideb_federal:.4f}')
    st.write(f'Diferença na Nota Média Padronizada entre federais e privadas: {diferenca_nota_media_federal:.4f}')



