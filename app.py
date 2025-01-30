import pandas as pd
import streamlit as st
from apresentacao.apresentacao_projeto import exibir_apresentacao_do_projeto, exibir_tema
# from graficos.distribuicao_escolas import 
from graficos.grafico_abandono import gerar_grafico_abandono
from graficos.melhorias.inclusao_tech import simular_impacto_tecnologia
from graficos.tecnologia_escolas import tecnologia_escola , grafico_escolar, grafico_porcento_escolas_tecnologia
from graficos.publicas_privadas import calcular_melhores_escolas, calcular_melhores_escolas_por_estado, prever_ideb, prever_ideb_para_ano
from melhorias.inclusao_tech import calcular_orcamento
# Importe outros gráficos ou funções conforme necessário

def main():
    st.sidebar.title("Apresentação inicial")
    apresentacao_menu = st.sidebar.radio(
        "Selecione uma opção:",
        ["", "Apresentação do projeto", "Apresentação do Tema"],
        key="apresentacao"
    )

    # Seção de dados
    st.sidebar.title("Apresentação dos dados")
    dados_menu = st.sidebar.radio(
        "Selecione uma opção:",
        ["", "Gráfico de Abandono", "Média por UF", "Melhores X Piores"],
        key="dados"
    )

    st.sidebar.title("Conclusão dos dados apresentados")
    conclusao_dados = st.sidebar.radio(
        "Selecione uma opção:",
        ["", "Analisando escolas e estados", "Porque incluir tecnologia", "Escolas técnicas"],
        key="conclusao"
    )

    st.sidebar.title("Melhorias posiveis apresentados")
    melhorias_possiveis = st.sidebar.radio(
        "Selecione uma opção:",
        ["", "Evolução técnologica", "Barreiras da evolução", "Ensino técnico especifico"],
        key="melhorias"
    )

    if apresentacao_menu == "Apresentação do projeto":
        exibir_apresentacao_do_projeto()
    elif apresentacao_menu == "Apresentação do Tema":
        exibir_tema()

    if dados_menu == "Gráfico de Abandono":
        gerar_grafico_abandono()
    elif dados_menu == "Média por UF":
        tecnologia_escola()
        grafico_escolar()
        grafico_porcento_escolas_tecnologia()
    elif dados_menu == "Melhores X Piores":
        st.title("Melhores X Piores")
        st.write("Aqui está a comparação entre as 100 as melhores e piores escolas!")
        calcular_melhores_escolas()

    if conclusao_dados == "Analisando escolas e estados":
        prever_ideb()
        st.header('Previsão pra 2024 com base na regressão anterior')
        prever_ideb_para_ano(ano=2024)
    elif conclusao_dados == "Porque incluir tecnologia":
        simular_impacto_tecnologia()
    elif conclusao_dados == "Escolas técnicas":
        calcular_melhores_escolas_por_estado()


    if melhorias_possiveis == "Evolução técnologica":
        st.title("Cálculo de Orçamento para Melhorar o IDEB")
        # Entrada do usuário: orçamento disponível
        orcamento_disponivel = st.number_input("Informe o orçamento disponível (R$):", min_value=0, step=5000, value=100000)

        if st.button("Calcular Impacto"):
            calcular_orcamento(orcamento_disponivel)

        st.subheader('Investimento em tecnologia nas escolas estaduais somou R$ 602 milhões em 4 anos ')
        st.write('A melhoria educacional pode ser vista direto nos indeces educacionais abaixo')
        st.write('''
                    Média de IDEB EF (público + privado): 21.82
Média de IDEB EM (público + privado): 19.05
Incremento percentual calculado para EF: 0.26%
Incremento percentual calculado para EM: 0.26%
            ''')
    elif melhorias_possiveis == "Barreiras da evolução":
        st.title("Barreiras da evolução")
        st.subheader("Como foi visto no tópico anterior, o investimento tecnológico não é barato")
        st.subheader("Mas há alguns pontos interessantes a se avaliar")

        dificuldades = [
            "Alto custo de pesquisa e desenvolvimento",
            "Resistência à adoção de novas tecnologias",
            "Desigualdade no acesso à tecnologia",
            "Infraestrutura inadequada para suportar inovação",
            "Falta de profissionais qualificados",
            "Questões éticas e regulamentações",
            "Dependência de tecnologia estrangeira",
        ]

        for i, dificuldade in enumerate(dificuldades, 1):
            st.write(f"{i} - {dificuldade}")

    elif melhorias_possiveis == "Ensino técnico especifico":
        st.title("Melhorias possíveis")
        st.subheader("Propostas de melhoria para o ensino técnico")

        melhorias = [
            "Parcerias com empresas para estágios e programas de aprendizagem prática",
            "Laboratórios equipados com tecnologias atualizadas",
            "Currículos alinhados às demandas do mercado de trabalho",
            "Aulas práticas e projetos aplicados para melhor fixação do conhecimento",
            "Plataformas de ensino híbrido (presencial e online) para maior acessibilidade",
            "Incentivo ao empreendedorismo e desenvolvimento de startups",
            "Certificações profissionais reconhecidas pelo mercado",
            "Uso de metodologias ativas, como problem-based learning (PBL)",
        ]

        st.write("Comparação entre os melhores e piores cenários:")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Boas práticas")
            for i, melhoria in enumerate(melhorias, 1):
                st.write(f"✅ {melhoria}")

        with col2:
            st.subheader("Problemas encontrados")
            problemas = [
                "Falta de conexão entre ensino e mercado de trabalho",
                "Tecnologia desatualizada nos laboratórios",
                "Poucas oportunidades de estágio",
                "Aulas teóricas sem aplicação prática",
                "Baixo investimento em cursos de curta duração",
                "Falta de incentivo à inovação",
            ]
            for i, problema in enumerate(problemas, 1):
                st.write(f"❌ {problema}")


if __name__ == "__main__":
    main()
