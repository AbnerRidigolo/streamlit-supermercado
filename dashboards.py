import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Leitura e preparação dos dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Criação da coluna de Mês para o filtro
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtrando o dataframe pelo mês selecionado
df_filtered = df[df["Month"] == month]

# ---- Layout do Dashboard ----
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico 1: Faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico 2: Faturamento por tipo de produto (CORRIGIDO)
prod_total = df_filtered.groupby("Product line")[["Total"]].sum().reset_index()
fig_prod = px.bar(prod_total, x="Total", y="Product line", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico 3: Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico 4: Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico 5: Avaliação média por filial (CORRIGIDO)
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_rating, y="Rating", x="City", title="Avaliação Média por Filial")
col5.plotly_chart(fig_rating, use_container_width=True)