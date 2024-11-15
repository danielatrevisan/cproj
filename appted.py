import streamlit as st
import pandas as pd
from datetime import datetime

# ID of the Google Sheets file
file_id = "1KLmqRbECQwOUvOpU3v60PKWQsfVrpmau5yDKcVkOXMw"
url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid=0"

# Título do aplicativo
st.title("Análise de TEDs")

# Carregar e processar os dados
df = pd.read_csv(url, header=2, nrows=86)
df.columns = df.columns.str.replace('\n', ' ', regex=True).str.replace('  ', ' ').str.strip()

# Conversão de datas
df['INÍCIO DA VIGÊNCIA'] = pd.to_datetime(df['INÍCIO DA VIGÊNCIA'], errors='coerce', dayfirst=True)
df['FIM DA VIGÊNCIA'] = pd.to_datetime(df['FIM DA VIGÊNCIA'], errors='coerce', dayfirst=True)
df['DATA FINAL PARA ENCAMINHAMENTO'] = pd.to_datetime(df['DATA FINAL PARA ENCAMINHAMENTO'], errors='coerce', dayfirst=True)

# Data atual
current_date = datetime.now()

# Cálculos de contagem
teds_firmados_total = df[df['INÍCIO DA VIGÊNCIA'].notna()].shape[0]
teds_finalizados_total = df[df['FIM DA VIGÊNCIA'] < current_date].shape[0]
teds_vigentes_total = df[df['FIM DA VIGÊNCIA'] >= current_date].shape[0]
teds_vigentes_calculado = teds_firmados_total - teds_finalizados_total

# Exibir resumo das contagens
st.subheader("Resumo das Contagens")
st.write(f"Total de TEDs Firmados: {teds_firmados_total}")
st.write(f"Total de TEDs Finalizados: {teds_finalizados_total}")
st.write(f"Total de TEDs Vigentes (calculado): {teds_vigentes_calculado}")
st.write(f"Total de TEDs Vigentes (diretamente contado): {teds_vigentes_total}")

# Contagem de TEDs por ano
firmados_por_ano = df['INÍCIO DA VIGÊNCIA'].dt.year.value_counts().sort_index()
finalizados_por_ano = df[df['FIM DA VIGÊNCIA'] < current_date]['FIM DA VIGÊNCIA'].dt.year.value_counts().sort_index()
tabela_ano = pd.DataFrame({
    "Ano": firmados_por_ano.index,
    "TEDs Firmados": firmados_por_ano.values,
    "TEDs Finalizados": finalizados_por_ano.reindex(firmados_por_ano.index, fill_value=0).values
})
st.subheader("Contagem de TEDs por Ano")
st.dataframe(tabela_ano)

# Status atual de TEDs
teds_prestacao_contas = df[(df['FIM DA VIGÊNCIA'] < current_date) & 
                           (df['DATA FINAL PARA ENCAMINHAMENTO'] > current_date)].shape[0]
tabela_status = pd.DataFrame({
    "Status": ["TEDs Vigentes", "TEDs no Período de Prestação"],
    "Quantidade": [teds_vigentes_total, teds_prestacao_contas]
})
st.subheader("Status Atual de TEDs")
st.dataframe(tabela_status)

# Lista de TEDs no período de prestação de contas
teds_prestacao_contas_lista = df[(df['FIM DA VIGÊNCIA'] < current_date) & 
                                 (df['DATA FINAL PARA ENCAMINHAMENTO'] > current_date)][['Seq.', 'TED/ANO']]
st.subheader("Lista de TEDs no Período de Prestação de Contas")
st.dataframe(teds_prestacao_contas_lista)
