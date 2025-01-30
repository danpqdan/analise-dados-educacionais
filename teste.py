import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Carregar os dados do arquivo Excel
df = pd.read_excel("data/media_escolar_por_uf.xlsx")

# Verificar se há valores ausentes e remover linhas com NaN (se necessário)
df = df.dropna(subset=['ideb_pub_ef_2013', 'ideb_pub_em_2013', 'ideb_pvt_em_2013', 'ideb_pub_ef_2023'])

# Garantir que as colunas estejam no formato adequado (se necessário, converta para numérico)
df['ideb_pub_ef_2013'] = pd.to_numeric(df['ideb_pub_ef_2013'], errors='coerce')
df['ideb_pub_em_2013'] = pd.to_numeric(df['ideb_pub_em_2013'], errors='coerce')
df['ideb_pvt_em_2013'] = pd.to_numeric(df['ideb_pvt_em_2013'], errors='coerce')
df['ideb_pub_ef_2023'] = pd.to_numeric(df['ideb_pub_ef_2023'], errors='coerce')

# Excluir qualquer linha com valores NaN após conversão
df = df.dropna(subset=['ideb_pub_ef_2013', 'ideb_pub_em_2013', 'ideb_pvt_em_2013', 'ideb_pub_ef_2023'])

# Seleção das variáveis para treino e previsão
X = df[['ideb_pub_ef_2013', 'ideb_pub_em_2013', 'ideb_pvt_em_2013']]  # Variáveis independentes (2013)
y = df['ideb_pub_ef_2023']  # Variável dependente (Nota de 2023)

# Criar e treinar o modelo de regressão linear
model = LinearRegression()
model.fit(X, y)

# Fazer previsões para 2025 (com base nas variáveis de 2013)
X_2025 = df[['ideb_pub_ef_2013', 'ideb_pub_em_2013', 'ideb_pvt_em_2013']]  # Usando 2013 para prever 2025
y_pred_2025 = model.predict(X_2025)

# Adicionar as previsões ao DataFrame
df['predito_2025'] = y_pred_2025

# Calcular o aumento de 0.2% sobre as notas de 2023
df['aumento_02'] = df['ideb_pub_ef_2023'] * 1.002  # Aumento de 0.2%

# Plotar o gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df['ideb_pub_ef_2023'], df['predito_2025'], color='blue', label='Previsões para 2025')
plt.plot(df['ideb_pub_ef_2023'], df['aumento_02'], color='red', linestyle='--', label='Aumento de 0.2%')
plt.xlabel('Nota de 2023')
plt.ylabel('Nota prevista para 2025')
plt.title('Comparação entre as previsões de 2025 e o aumento de 0.2%')
plt.legend()
plt.show()


import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Carregar os dados do arquivo Excel
df = pd.read_excel("data/institucoes_ideb.xlsx")
df.columns = [
    'Sigla UF', 'Código Município', 'Nome Município', 'Código Escola', 'Nome Escola', 'Rede',
    'Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa', 'Nota SAEB 2017 Nota Média Padronizada (N)',
    'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 'Nota SAEB 2019 Nota Média Padronizada (N)',
    'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa', 'Nota SAEB 2021 Nota Média Padronizada (N)',
    'Nota SAEB 2023 Matemática', 'Nota SAEB 2023 Língua Portuguesa', 'Nota SAEB 2023 Nota Média Padronizada (N)',
    'IDEB 2017', 'IDEB 2019', 'IDEB 2021', 'IDEB 2023', 'Metas 1º ciclo Ideb'
]

# Verificar se há valores ausentes e remover linhas com NaN (se necessário)
df = df.dropna(subset=[
    'Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa', 
    'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 
    'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa', 
    'Nota SAEB 2023 Matemática', 'Nota SAEB 2023 Língua Portuguesa'
])

# Garantir que as colunas estejam no formato adequado (se necessário, converta para numérico)
df['Nota SAEB 2017 Matemática'] = pd.to_numeric(df['Nota SAEB 2017 Matemática'], errors='coerce')
df['Nota SAEB 2017 Língua Portuguesa'] = pd.to_numeric(df['Nota SAEB 2017 Língua Portuguesa'], errors='coerce')
df['Nota SAEB 2019 Matemática'] = pd.to_numeric(df['Nota SAEB 2019 Matemática'], errors='coerce')
df['Nota SAEB 2019 Língua Portuguesa'] = pd.to_numeric(df['Nota SAEB 2019 Língua Portuguesa'], errors='coerce')
df['Nota SAEB 2021 Matemática'] = pd.to_numeric(df['Nota SAEB 2021 Matemática'], errors='coerce')
df['Nota SAEB 2021 Língua Portuguesa'] = pd.to_numeric(df['Nota SAEB 2021 Língua Portuguesa'], errors='coerce')
df['Nota SAEB 2023 Matemática'] = pd.to_numeric(df['Nota SAEB 2023 Matemática'], errors='coerce')
df['Nota SAEB 2023 Língua Portuguesa'] = pd.to_numeric(df['Nota SAEB 2023 Língua Portuguesa'], errors='coerce')

# Excluir qualquer linha com valores NaN após conversão
df = df.dropna(subset=[
    'Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa', 
    'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 
    'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa', 
    'Nota SAEB 2023 Matemática', 'Nota SAEB 2023 Língua Portuguesa'
])

# Seleção das variáveis para treino e previsão
# Usando as notas de Matemática e Língua Portuguesa dos anos anteriores como variáveis independentes
X = df[['Nota SAEB 2017 Matemática', 'Nota SAEB 2017 Língua Portuguesa',
        'Nota SAEB 2019 Matemática', 'Nota SAEB 2019 Língua Portuguesa', 
        'Nota SAEB 2021 Matemática', 'Nota SAEB 2021 Língua Portuguesa']]  # Variáveis independentes

# Variável dependente é o IDEB de 2023
y = df['IDEB 2023']  # Ajuste para o nome correto da coluna

# Criar e treinar o modelo de regressão linear
model = LinearRegression()
model.fit(X, y)

# Fazer previsões para as escolas
y_pred_2023 = model.predict(X)

# Adicionar as previsões ao DataFrame
df['predito_IDEB_2023'] = y_pred_2023

# Mostrar as previsões e comparar com os valores reais
print(df[['Nome Escola', 'IDEB 2023', 'predito_IDEB_2023']])

# Plotar as previsões (gráfico de comparação)
plt.figure(figsize=(10, 6))
plt.scatter(df['IDEB 2023'], df['predito_IDEB_2023'], color='blue', label='Previsões vs Reais')
plt.plot([df['IDEB 2023'].min(), df['IDEB 2023'].max()], 
         [df['IDEB 2023'].min(), df['IDEB 2023'].max()], color='red', linestyle='--', label='Linha Ideal')

plt.xlabel('IDEB 2023 Real')
plt.ylabel('IDEB 2023 Previsto')
plt.title('Comparação entre o IDEB de 2023 Real e o Previsto')
plt.legend()
plt.show()
