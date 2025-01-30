import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from graficos.distribuicao_escolas import calcular_totais_escolas_tecnologia_separado

def tecnologia_escola():
    
    st.title("Porcentagem de escolas tech")
    st.write('''
             O grafico abaixo apresenta a porcentagem de escolas que possuem
             espaço com computadores e não que realmente os utilizam. \n
             Vale notar que a porcentagem se aplica ao numero total nas escolas em seu estado
             e não ao numero total de escolas no país.
             ''')
    df = pd.read_excel("./data/media_escolar_por_uf.xlsx")
    # Exibir as primeiras linhas para garantir que os dados foram lidos corretamente
    st.write(df)

    # Selecionar as colunas de interesse para o gráfico
    colunas_interesse = [
        "estado", "publica_ef_tecnologica_%", "publica_em_tecnologica_%",
        "privado_ef_tecnologica_%", "privado_em_tecnologica_%"
    ]
    df = df[colunas_interesse]

    # Plotando os dados
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando as barras para cada categoria
    df.plot(kind='bar', x='estado', y=["publica_ef_tecnologica_%", "publica_em_tecnologica_%",
                                        "privado_ef_tecnologica_%", "privado_em_tecnologica_%"],
            ax=ax, color=['#191970', '#00BFFF', '#8B4513', '#F4A460'])

    # Adicionando título e labels
    plt.title("Tecnologia nas Escolas: Público vs Privado")
    plt.xlabel("Estado")
    plt.ylabel("Porcentagem")
    plt.xticks(rotation=90)  # Rotacionar os rótulos do eixo X para melhor visualização
    plt.legend(title="Categorias")

    # Ajuste de layout para evitar sobreposição
    plt.tight_layout()

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)  # Exibe o gráfico diretamente no Streamlit

def grafico_escolar():
    # Dados fornecidos
    labels = ['Publica EF', 'Publica EM', 'Privada EF', 'Privada EM']
    sizes = [47227, 21016, 14579, 8738]

    # Cores personalizadas para o gráfico
    colors = ['#191970', '#00BFFF', '#8B4513', '#F4A460']

    # Criando o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'})

    # Adicionando título
    st.header("Distribuição de Escolas por Tipo (Pública/Privada e EF/EM)")
    st.write('''
        Grafíco responsavel por apresentar a quantia geral de escolas e como elas estão distribuidas
             para Ensino Fundamental Final(Privado e Publico) e Ensino Médio(Privado e Publico)
    ''')

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)  # Exibe o gráfico diretamente no Streamlit

def grafico_porcento_escolas_tecnologia():
    df = pd.read_excel("./data/media_escolar_por_uf.xlsx")

    # Calcular os totais das escolas públicas e privadas separadas para EF e EM
    totais = calcular_totais_escolas_tecnologia_separado(df)

    # Somar os totais
    total_geral = (
        totais['EF_pub_sem_tecnologia'] + totais['EF_pub_com_tecnologia'] +
        totais['EF_pvt_sem_tecnologia'] + totais['EF_pvt_com_tecnologia'] +
        totais['EM_pub_sem_tecnologia'] + totais['EM_pub_com_tecnologia'] +
        totais['EM_pvt_sem_tecnologia'] + totais['EM_pvt_com_tecnologia']
    )

    # Evitar divisão por zero
    if total_geral == 0:
        st.error("O total geral é zero, não é possível calcular as porcentagens.")
        return

    # Calcular porcentagens
    porcentagens = [
        totais['EF_pub_com_tecnologia'] / total_geral * 100,
        totais['EM_pub_com_tecnologia'] / total_geral * 100,
        totais['EF_pvt_com_tecnologia'] / total_geral * 100,
        totais['EM_pvt_com_tecnologia'] / total_geral * 100,
        totais['EF_pub_sem_tecnologia'] / total_geral * 100,
        totais['EM_pub_sem_tecnologia'] / total_geral * 100,
        totais['EF_pvt_sem_tecnologia'] / total_geral * 100,
        totais['EM_pvt_sem_tecnologia'] / total_geral * 100
    ]

    labels = [
        'EF Pública com tecnologia',
        'EM Pública com tecnologia',
        'EF Privada com tecnologia',
        'EM Privada com tecnologia',
        'EF Pública sem tecnologia',
        'EM Pública sem tecnologia',
        'EF Privada sem tecnologia',
        'EM Privada sem tecnologia'
    ]


    # Criar o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(labels, porcentagens, color=['#191970', '#00BFFF', '#8B4513', '#F4A460', '#191970', '#00BFFF', '#8B4513', '#F4A460'])

    # Adicionar títulos e rótulos ao gráfico
    ax.set_xlabel('Porcentagem (%)')
    ax.set_title('Porcentagem de Escolas com e sem Tecnologia (EF e EM)')

    # Adicionar os totais à direita de cada barra
    for bar, label in zip(bars, labels):
        # Posição do texto: no final da barra, ajustando o valor
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f'{bar.get_width():.0f}', va='center', ha='left', fontsize=10)


    # Informações
    st.write('''
            Note que abaixo estamos calculando os numeros totais em porcentagem, 
                com tecnologia e sem tecnologia.
            ''')

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)

    # Exibir os totais no Streamlit
    st.write("Totais de Escolas com e sem Tecnologia separadas por EF e EM")
    st.write(f"Total de escolas públicas de EF com tecnologia: {totais['EF_pub_com_tecnologia']:.0f}")
    st.write(f"Total de escolas públicas de EM com tecnologia: {totais['EM_pub_com_tecnologia']:.0f}")

    st.write(f"Total de escolas privadas de EF com tecnologia: {totais['EF_pvt_com_tecnologia']:.0f}")
    st.write(f"Total de escolas privadas de EM com tecnologia: {totais['EM_pvt_com_tecnologia']:.0f}")

    st.write(f"Total de escolas públicas de EF sem tecnologia: {totais['EF_pub_sem_tecnologia']:.0f}")
    st.write(f"Total de escolas públicas de EM sem tecnologia: {totais['EM_pub_sem_tecnologia']:.0f}")

    st.write(f"Total de escolas privadas de EF sem tecnologia: {totais['EF_pvt_sem_tecnologia']:.0f}")
    st.write(f"Total de escolas privadas de EM sem tecnologia: {totais['EM_pvt_sem_tecnologia']:.0f}")
