import streamlit as st

def exibir_apresentacao_do_projeto():
    st.title("Apresentação do Projeto")
    st.markdown(
        """
        <details>
        <summary><h1>📊 Análise de Dados Educacionais - Desafio</h1></summary>
        
        ## 🎯 Objetivo
        1. **Extrair insights**
        2. **Gerar visualizações e relatórios**
        3. **Utilizar inteligência artificial (IA)**
        
        ## 🛠 Resolução
        1. **Acesso a dados com BigQuery**
        2. **Definição de tema de análise**
        3. **Análise dos dados com Python, R ou SQL**
        4. **Criação de visualizações com gráficos**
        5. **Incorporação de IA**
        6. **Proposição de melhorias**
        
        ## 💡 Dicas
        1. **Escolha um recorte do cenário encontrado**
        2. **Documente o código**
        3. **Visualizações são chaves**
        4. **Aproveite o BigQuery**
        </details>
        """,
        unsafe_allow_html=True
    )


import streamlit as st

def exibir_tema():
    # Título da página
    st.title("A Importância da Inovação Tecnológica nas Escolas")
    
    # Descrição geral
    st.write("""
    A inovação tecnológica tem se mostrado cada vez mais essencial para o desenvolvimento educacional,
    promovendo novas oportunidades de aprendizado, além de impactar diretamente nas metodologias de ensino,
    na melhoria do desempenho dos alunos e na evolução das escolas.
    Nesta análise, exploraremos a importância dessa transformação digital nas escolas brasileiras e o impacto
    no desempenho acadêmico dos alunos.
    """)

    # Seção de Pesquisa
    st.subheader("Pontos de Pesquisa")
    st.write("""
    Para compreender melhor a importância da inovação tecnológica nas escolas, investigamos os seguintes pontos:
    - Quantos alunos estão fora da escola atualmente?
    - Quantas escolas se preocupam com a evolução tecnológica em suas práticas educacionais?
    - Qual o impacto da evolução tecnológica nas notas dos alunos?
    - Quais as escolas com melhores e piores índices no IDEB (Índice de Desenvolvimento da Educação Básica)?
    - Nessas melhores escolas, a tecnologia teve impacto no desempenho?
    """)

    # Resultados
    st.subheader("Resultados Preliminares da Pesquisa")

    # 1. Quantos alunos fora da escola
    st.markdown("**1. Quantos alunos temos fora da escola atualmente?**")
    st.write("""
    De acordo com os dados mais recentes do **Censo Escolar**, cerca de **134.018 (mil)** crianças e adolescentes
    estão fora da escola no Brasil, especialmente nas regiões Norte e Nordeste. Esse número pode ser afetado
    por fatores como desigualdade socioeconômica, falta de infraestrutura escolar, e questões tecnológicas
    que dificultam o acesso à educação de qualidade.
    """)
    
    # 2. Escolas e evolução tecnológica
    st.markdown("**2. Quantas escolas se preocupam com a evolução tecnológica?**")
    st.write("""
    Segundo levantamento realizado em **2024**, aproximadamente **17%** das escolas públicas e **6%** das escolas privadas
    implementaram alguma forma de tecnologia em seus processos educacionais, como lousas digitais, acesso
    à internet, plataformas de ensino a distância e dispositivos móveis para os alunos.
    No entanto, a distribuição e o acesso a essas tecnologias variam bastante entre as escolas das regiões
    urbanas e rurais.
    """)

    # 3. Impacto da evolução tecnológica nas notas
    st.markdown("**3. Qual o impacto da evolução tecnológica nas notas?**")
    st.write("""
    Estudos realizados com escolas que adotaram inovações tecnológicas mostraram que **0,22%** dos alunos
    apresentaram melhoria no desempenho acadêmico, especialmente em disciplinas como Matemática e Ciências,
    quando usaram recursos tecnológicos interativos e plataformas online para estudos e revisões.
    O impacto varia, entretanto, dependendo da forma como as tecnologias são implementadas e do suporte
    pedagógico oferecido aos professores e alunos.
    """)

    # 4. Melhores e piores escolas no IDEB
    st.markdown("**4. Quais as escolas com melhores e piores índices no IDEB?**")
    st.write("""
    O **Índice de Desenvolvimento da Educação Básica (IDEB)** é um indicador importante do desempenho das escolas
    no Brasil. As escolas com melhores índices geralmente estão localizadas em áreas mais desenvolvidas e têm
    mais recursos para investir em infraestrutura e inovação. A seguir, listamos as **x** escolas com os melhores
    e piores índices IDEB:
    - **Melhores Escolas:**
      - OBJETIVO COLEGIO INTEGRADO (IDEB: 8.4)
      - COLEGIO CLASSE A UNIDADE II (IDEB: 8.3)
    - **Piores Escolas:**
      - CENTRO DE EDUCACAO INDIGENA - JUTAI (IDEB: 1.8)
      - ESCOLA ESTADUAL BELEM DO SOLIMOES (IDEB: 1.7)
    """)

    # 5. Impacto da tecnologia nas melhores escolas
    st.markdown("**5. Nessas melhores escolas, a tecnologia teve impacto no desempenho?**")
    st.write("""
    Nas melhores escolas do Brasil, a implementação de tecnologias educacionais foi um dos fatores que
    contribuiu para os bons índices no IDEB. O uso de plataformas digitais, ensino híbrido, e o treinamento
    constante de professores para o uso das novas tecnologias ajudaram a melhorar o aprendizado e o engajamento
    dos alunos. No entanto, a simples presença de tecnologia não é suficiente: ela deve ser bem aplicada e integrada
    ao currículo escolar.
    """)

    # Conclusão
    st.subheader("Conclusão")
    st.write("""
    A inovação tecnológica tem o potencial de transformar a educação, oferecendo novas oportunidades de aprendizado
    e melhorando os resultados acadêmicos dos alunos. No entanto, é fundamental garantir que as tecnologias sejam
    implementadas de maneira adequada, com suporte contínuo a professores e alunos, para que o impacto seja positivo.
    Além disso, a redução do número de alunos fora da escola e a melhoria na infraestrutura escolar são passos essenciais
    para que todos tenham acesso a uma educação de qualidade.
    """)
