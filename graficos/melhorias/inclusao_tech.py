from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
from graficos.distribuicao_escolas import calcular_totais_escolas_tecnologia_separado
from modelo.regressao_linear import treinar_modelo, treinar_modelo_previsao_independente


def simular_impacto_tecnologia(incremento_percentual=1.2, proporcao=0.1):
    try:
        # Treinar o modelo e calcular totais
        df, model_pub_ef, model_pvt_ef, model_pub_em, model_pvt_em, colunas_anos_em, colunas_anos_ef = treinar_modelo()
        totais = calcular_totais_escolas_tecnologia_separado(df)
        
        # Calcular a quantidade de escolas que terão tecnologia implantada (10% das escolas sem tecnologia)
        incremento_escolas = {
            'EF_pub': totais['EF_pub_sem_tecnologia'] * proporcao,
            'EF_pvt': totais['EF_pvt_sem_tecnologia'] * proporcao,
            'EM_pub': totais['EM_pub_sem_tecnologia'] * proporcao,
            'EM_pvt': totais['EM_pvt_sem_tecnologia'] * proporcao,
        }

        somas_ef = df[['ideb_pub_ef_2021', 'ideb_pvt_ef_2021', 'ideb_pub_ef_2023', 'ideb_pvt_ef_2023']].sum(axis=1)
        somas_em = df[['ideb_pub_em_2021', 'ideb_pvt_em_2021', 'ideb_pub_em_2023', 'ideb_pvt_em_2023']].sum(axis=1)

        # Calcular a média para EF e EM
        media_ef = somas_ef.mean()
        media_em = somas_em.mean()

        # Calcular o incremento percentual no IDEB (0,22% por cada 1% de incremento nos gastos)
        incremento_percentual_ef = incremento_percentual * 0.22
        incremento_percentual_em = incremento_percentual * 0.22

        reais_2023_pub_ef = df['ideb_pub_ef_2023']
        reais_2023_pvt_ef = df['ideb_pvt_ef_2023']
        reais_2023_pub_em = df['ideb_pub_em_2023']
        reais_2023_pvt_em = df['ideb_pvt_em_2023']

        # Prever valores para 2023
        previsao_2023_pub_ef = model_pub_ef.predict(df[colunas_anos_ef])
        previsao_2023_pvt_ef = model_pvt_ef.predict(df[colunas_anos_ef])
        previsao_2023_pub_em = model_pub_em.predict(df[colunas_anos_em])
        previsao_2023_pvt_em = model_pvt_em.predict(df[colunas_anos_em])

        # Calcular o erro de previsão (erro absoluto médio)
        erro_pub_ef = abs(reais_2023_pub_ef - previsao_2023_pub_ef).mean()
        erro_pvt_ef = abs(reais_2023_pvt_ef - previsao_2023_pvt_ef).mean()
        erro_pub_em = abs(reais_2023_pub_em - previsao_2023_pub_em).mean()
        erro_pvt_em = abs(reais_2023_pvt_em - previsao_2023_pvt_em).mean()

        st.title('Inclusão da tecnologia')
        st.subheader('O modelo de regressão resultante das análises demonstrou influência do aumento dos gastos públicos por aluno sobre o desempenho dos alunos. O modelo consegue explicar uma variação de 34% do Ideb, sendo que uma alteração de 1% nos investimentos por aluno aumenta em 0,22% a nota do Ideb.')
        st.write('Fonte: https://repositorio.ufsm.br/handle/1/26951?utm_source=chatgpt.com')
        st.write('Importante lembrar que o incremento % para o calculo foi apenas entre os anos de 2020 e 2023 onde houve o maior investimento tecnologico')
        st.write('fonte: https://www.educacao2.go.gov.br/sala-de-imprensa/noticias3/4896-investimento-em-tecnologia-nas-escolas-estaduais-somou-r-602-milhoes-em-4-anos.html')

        # Exibir as médias e incrementos percentuais no Streamlit
        st.write(f"Média de IDEB EF (público + privado): {media_ef:.2f}")
        st.write(f"Média de IDEB EM (público + privado): {media_em:.2f}")
        st.write(f"Incremento percentual calculado para EF: {incremento_percentual_ef:.2f}%")
        st.write(f"Incremento percentual calculado para EM: {incremento_percentual_em:.2f}%")

        st.divider()

        st.subheader('Taxa de impacto ao ensino fundamental pra 10% das escolas Brasileiras')

        # Exibir os erros de previsão para 2023
        st.write(f"Erro médio de previsão para 2023 Ensino F. público: {erro_pub_ef:.2f}")
        st.write(f"Erro médio de previsão para 2023 Ensino F. privado: {erro_pvt_ef:.2f}")

        st.subheader('Taxa de impacto ao ensino medio pra 10% das escolas Brasileiras')
        st.write(f"Erro médio de previsão para 2023 Ensino M. público: {erro_pub_em:.2f}")
        st.write(f"Erro médio de previsão para 2023 Ensino M. privado: {erro_pvt_em:.2f}")
        # Ajustar as previsões para 2024 com base no erro médio de 2023
        df['previsto_2024_pub_ef'] = model_pub_ef.predict(df[colunas_anos_ef]) + erro_pub_ef
        df['previsto_2024_pvt_ef'] = model_pvt_ef.predict(df[colunas_anos_ef]) + erro_pvt_ef
        df['previsto_2024_pub_em'] = model_pub_em.predict(df[colunas_anos_em]) + erro_pub_em
        df['previsto_2024_pvt_em'] = model_pvt_em.predict(df[colunas_anos_em]) + erro_pvt_em

        # Calcular o impacto no IDEB com base no incremento percentual fornecido
        df['impacto_tecnologia_ef_pub'] = df['previsto_2024_pub_ef'] * (1 + incremento_percentual_ef / 100)
        df['impacto_tecnologia_ef_pvt'] = df['previsto_2024_pvt_ef'] * (1 + incremento_percentual_ef / 100)
        df['impacto_tecnologia_em_pub'] = df['previsto_2024_pub_em'] * (1 + incremento_percentual_em / 100)
        df['impacto_tecnologia_em_pvt'] = df['previsto_2024_pvt_em'] * (1 + incremento_percentual_em / 100)

        # Calcular os totais de impacto por tipo de ensino (EF e EM) independente de público ou privado
        df['total_impacto_ef'] = df['impacto_tecnologia_ef_pub'] + df['impacto_tecnologia_ef_pvt']
        df['total_impacto_em'] = df['impacto_tecnologia_em_pub'] + df['impacto_tecnologia_em_pvt']

        # Exibir o impacto no Streamlit
        st.write(df[['estado', 'total_impacto_ef', 'total_impacto_em']])

        # Criar gráfico de linha para mostrar o IDEB real e o impactado pela tecnologia
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotar o IDEB real e o impacto com a tecnologia
        ax.plot(df['estado'], df['total_impacto_ef'], label="Impacto Tecnologia - EF", color='blue', marker='o')
        ax.plot(df['estado'], df['total_impacto_em'], label="Impacto Tecnologia - EM", color='green', marker='o')

        # Adicionar os valores reais de IDEB para EF e EM
        ax.plot(df['estado'], reais_2023_pub_ef + reais_2023_pvt_ef, label="Real IDEB - EF", linestyle='--', color='blue')
        ax.plot(df['estado'], reais_2023_pub_em + reais_2023_pvt_em, label="Real IDEB - EM", linestyle='--', color='green')

        # Habilitar o grid
        ax.grid(True)

        # Configurar o gráfico
        ax.set_xlabel('Estado')
        ax.set_ylabel('IDEB')
        ax.set_title('Impacto da Tecnologia no IDEB - Comparação Real vs Previsão 2024')
        ax.legend()

        
        # Exibir o gráfico no Streamlit
        st.subheader('Importante calcular a taxa de Erro informada acima')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao simular o impacto da tecnologia: {e}")
