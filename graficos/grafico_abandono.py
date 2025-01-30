import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import streamlit as st

# Função para criar o gráfico
def gerar_grafico_abandono():
    st.title("Apresentação do Projeto")
    df = pd.read_excel('./data/dados_abandono_escolar.xlsx')

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.25
    index = df['ano']

    # Barras para matrículas
    bar1 = ax1.bar(index - bar_width, df['nm total ef'], bar_width, label='Ensino Fundamental EF', color='blue')
    bar2 = ax1.bar(index, df['nm total em'], bar_width, label='Ensino Médio EM', color='green')
    bar3 = ax1.bar(index + bar_width, df['nm total et'], bar_width, label='Ensino Técnico ET', color='red')

    ax2 = ax1.twinx()

    # Cálculo das porcentagens de abandono
    df['porcentagem abandono total ef'] = (df['nm total ef'] / df["% abandono total ef"].astype(float)) / 100
    df['porcentagem abandono cti'] = (df['nm total et'] / df["% abandono cti"].astype(float)) / 100
    df['porcentagem abandono total em'] = (df['nm total em'] / df["% abandono total em"].astype(float)) / 100

    # Linhas para abandono
    ax2.plot(df['ano'], df['porcentagem abandono total ef'], color='#36454F', marker='o', label='Abandono Total EF', linewidth=2)
    ax2.plot(df['ano'], df['porcentagem abandono cti'], color='orange', marker='o', label='Abandono CTI', linewidth=2)
    ax2.plot(df['ano'], df['porcentagem abandono total em'], color='black', marker='o', label='Abandono Total EM', linewidth=2)

    # Configurações do gráfico
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Matrículas', color='blue')
    ax2.set_ylabel('Abandono de Matrícula', color='black')
    ax1.set_title('Gráfico de Matrículas e Abandonos por Ano')

    ax1.set_xticks(index)
    ax1.set_xticklabels(df['ano'], rotation=45)

    ax1.set_ylim(0, 13000000)
    ax2.set_ylim(0, 100000)

    # Adicionar grades ao eixo Y da esquerda (matrículas)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Função para formatar os valores do eixo Y em milhões
    def millions(x, pos):
        return '%dM' % (x * 1e-6)

    formatter = FuncFormatter(millions)
    ax1.yaxis.set_major_formatter(formatter)

    # Definir cores dos eixos para diferenciar melhor
    ax1.spines['left'].set_color('blue')
    ax2.spines['right'].set_color('black')

    ax1.tick_params(axis='y', colors='blue')
    ax2.tick_params(axis='y', colors='black')

    # Adicionar valores nas linhas de abandono
    for i, txt in enumerate(df['porcentagem abandono total ef']):
        ax2.annotate(f'{int(txt)}', (df['ano'][i], df['porcentagem abandono total ef'][i]), 
                     textcoords="offset points", xytext=(5,5), ha='center', fontsize=8, color='#36454F')

    for i, txt in enumerate(df['porcentagem abandono cti']):
        ax2.annotate(f'{int(txt)}', (df['ano'][i], df['porcentagem abandono cti'][i]), 
                     textcoords="offset points", xytext=(5,5), ha='center', fontsize=8, color='orange')

    for i, txt in enumerate(df['porcentagem abandono total em']):
        ax2.annotate(f'{int(txt)}', (df['ano'][i], df['porcentagem abandono total em'][i]), 
                     textcoords="offset points", xytext=(5,5), ha='center', fontsize=8, color='black')

    # Legendas
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    st.pyplot(fig)

    #informações
    st.header("Informações importantes")
    st.write('''
                1 - Note que o Y esquerdo é demarcado em M(Milhões)\n
                2 - A linha demarca o Y direito com os valores em m(Mil)
             ''')

