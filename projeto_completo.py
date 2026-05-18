# %%
import pandas as pd

df = pd.read_csv(
    r'C:\\Users\\Aline\\Desktop\\projetos git\\customer_shopping_behavior.csv')


df.head()  # verificar as 5 primeiras linhas do dataframe

# %%
df.info()
# %%
df.describe(include='all')  # include='all' para incluir colunas não numéricas
# %%
df.isnull().sum()  # verificar a quantidade de valores nulos
# %%
# Prrencher os valores nulos da coluna 'Review Rating' com a mediana da categoria correspondente
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.median())
)
# %%
df.isnull().sum()  # verificar novamente a quantidade de valores nulos
# %%
# Normalizar nomes de colunas (ex.: Customer ID -> customer_id)
df.columns = (
    df.columns.str.lower()
    .str.strip()
    .str.replace(' ', '_', regex=False)
    .str.replace(r'[^a-z0-9_]', '', regex=True)
)
# reduzir múltiplos '_' para apenas um
df.columns = df.columns.str.replace(r'_+', '_', regex=True)
# remover '_' no início/fim
df.columns = df.columns.str.replace(r'^_|_$', '', regex=True)
df = df.rename(columns={'purchase_amount_usd': 'purchase_amount'})
df.columns
# %%
# Criando uma coluna(feature) chamada grupo_etário
labels = ['Young_Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels) # qcut faz cortar em 4 grupos iguais
# %%
df[['age','age_group']].head(10) # verificar as 10 primeiras linhas
# %%
# Criando outra coluna (feature) chamada frequencia de compras em dias
frequency_mapping = {    # primeiro criamos um dicionario
    'Fortnightly': 14,   # depois usamos a função map para substituir o texto da coluna para a qtde de dias
    'Weekly': 7,         
    'Montly': 30,
    'Quarterly': 90,
    'Bi-weekly': 14,
    'Annually': 365,
    'Every 3 months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
# %%
# verificaar os resultados vendo a coluna antiga ao lado da coluna nova
df[['purchase_frequency_days', 'frequency_of_purchases']].head(10)
# %%
# Colunas desconto aplicado e codigo promocional usado
df[['discount_applied','promo_code_used']].head(10)
# %%
# Verificar se as colunas de desconto aplicado e codigo promocional usado são a mesma coluna
(df['discount_applied'] == df['promo_code_used']).all()
# %%
# Remover a coluna de codigo promocional usado, pois ela é a mesma coluna de desconto aplicado
df = df.drop('promo_code_used', axis=1)
# %%
df.columns
# %%
from sqlalchemy import create_engine
# Conectar no PostgreSQL
username = 'postgres'
password = '1234'
host = 'localhost'
port = '5432'
database = 'customer_behavior'

engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

# Carregando o dataframe para o PostgreSQL
table_name = 'customer'
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f'Dataframe carregado com sucesso para a tabela {table_name} in database {database}')


# %%
