import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    return pd.read_excel('./data/institucoes_ideb.xlsx')

def calcular_orcamento(orçamento_disponivel, aumento_percentual_ideb=0.22):
    df = carregar_dados()
    quantidade_escolar = df['Código da Escola'].nunique()  # Total de escolas únicas
    criancas_por_sala = 30
    custo_por_crianca = 1500
    
    # Quantidade total de crianças atendidas com o orçamento disponível
    total_criancas_atendidas = orçamento_disponivel // custo_por_crianca
    
    # Quantidade de escolas atendidas (assumindo 30 crianças por sala)
    escolas_atendidas = total_criancas_atendidas // criancas_por_sala
    escolas_atendidas = min(escolas_atendidas, quantidade_escolar)

    # Cálculo do impacto no IDEB
    if escolas_atendidas > 0:
        aumento_percentual_investimento = (orçamento_disponivel / (escolas_atendidas * criancas_por_sala * custo_por_crianca)) * 100
        impacto_ideb = (aumento_percentual_investimento * aumento_percentual_ideb) / 100
    else:
        impacto_ideb = 0

    # Exibição no Streamlit
    st.subheader("Resumo do Orçamento")
    st.write(f"**Orçamento Disponível:** R$ {orçamento_disponivel:,.2f}")
    st.write(f"**Escolas que podem ser melhoradas:** {escolas_atendidas}")
    st.write(f"**Crianças Impactadas:** {total_criancas_atendidas}")
    st.write(f"**Impacto Estimado no IDEB:** {impacto_ideb:.4f}%")

    


