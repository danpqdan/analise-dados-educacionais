from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st



def calcular_totais_escolas_tecnologia_separado(df):
    # Calcular o total de escolas públicas e privadas com e sem tecnologia para EF e EM
    totais = {
        # EF Público
        'EF_pub_com_tecnologia': df['qnt_un_pub_ef_tecnologica(2023)'].sum(),
        'EF_pub_sem_tecnologia': (
            df['qnt_un_pub_ef_tecnologica(2023)'] / (df['publica_ef_tecnologica_%'] / 100)
        ).sum() - df['qnt_un_pub_ef_tecnologica(2023)'].sum(),

        # EF Privado
        'EF_pvt_com_tecnologia': df['qnt_un_pvt_ef_tecnologica(2023)'].sum(),
        'EF_pvt_sem_tecnologia': (
            df['qnt_un_pvt_ef_tecnologica(2023)'] / (df['privado_ef_tecnologica_%'] / 100)
        ).sum() - df['qnt_un_pvt_ef_tecnologica(2023)'].sum(),

        # EM Público
        'EM_pub_com_tecnologia': df['qnt_un_pub_em_tecnologica(2023)'].sum(),
        'EM_pub_sem_tecnologia': (
            df['qnt_un_pub_em_tecnologica(2023)'] / (df['publica_em_tecnologica_%'] / 100)
        ).sum() - df['qnt_un_pub_em_tecnologica(2023)'].sum(),

        # EM Privado
        'EM_pvt_com_tecnologia': df['qnt_un_pvt_em_tecnologica(2023)'].sum(),
        'EM_pvt_sem_tecnologia': (
            df['qnt_un_pvt_em_tecnologica(2023)'] / (df['privado_em_tecnologica_%'] / 100)
        ).sum() - df['qnt_un_pvt_em_tecnologica(2023)'].sum(),
    }
    return totais



