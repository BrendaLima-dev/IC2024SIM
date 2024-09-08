!pip install streamlit
!pip install pandas
!pip install matpltlib
!pip install seaborn

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

# Definir o título da página
st.title('Análise dos dados do SIM (Dados do ano 2023)')

# Adicionar uma descrição
st.write('O sistema de Informação sobre Mortalidade (SIM) é crucial para coletar dados, organizar e processar informações sobre dados de mortalidade no Brasil. Ele nos permite construir indicadores e realizar análises epidemiológicas, fundamentais para a tomada de decisões em saúde. Apesar da sua importância, hoje é necessário conhecimento técnico e ferramentas computacionais adequadas para o levantamento dos dados. Neste projeto propomos a construção de um ambiente com ferramentas de visualização acessíveis a usuários sem formação técnica profissional. Este relatório apresenta uma análise preliminar baseada nos dados fornecidos pelo Open Data SUS e seus significados.')

# Ou usar Markdown para formatação mais avançada
st.markdown('## Desenvolvedora\n'
            'Brenda Cristina gomes de Lima\n'
           ' Linkedin:https://www.linkedin.com/in/brendacglima/')


# Leitura do CSV
@st.cache
def load_data():
    return pd.read_csv(r'C:\Users\brenda.lima\Desktop\IC2024\_Testando__202409072135.csv', sep=';', nrows=600)

df = load_data()

# Mapeamento das tabelas e colunas
table_columns = {
    "AtendimentoMedico": ["ASSISTMED", "ATESTANTE"],
    "CID": ["LINHAA", "LINHAB", "LINHAC", "LINHAD", "LINHAII", "CAUSABAS", "CB_PRE", "CAUSAMAT"],
    "CODIFICACAO": ["CODIFICADO"],
    "CircunstanciaObito": ["TIPOBITO", "OBITOGRAV", "CIRCOBITO", "ACIDTRAB", "OBITOPARTO", "TPMORTEOCO", "OBITOPUERP"],
    "Datas": ["NUDIASINF", "DTATESTADO", "DTINVESTIG", "DTRECEBIM", "DTCADINV", "DTCONINV", "DTCONCASO", "DTCADASTRO", "DTRECORIGA", "DIFDATA", "NUDIASOBCO", "NUDIASOBIN", "DTCADINF", "DTOBITO"],
    "EscolaridadeFalecido": ["ESC", "ESC2010", "SERIESCFAL", "ESCFALAGR1"],
    "EscolaridadeMae": ["ESCMAE", "ESCMAE2010", "SERIESCMAE", "ESCMAEAGR1"],
    "FonteDado": ["ORIGEM", "FONTE", "VERSAOSIST", "VERSAOSCB", "FONTEINV", "FONTES", "FONTESINF", "CONTADOR"],
    "HoraObito": ["HORAOBITO"],
    "InfoFalecido": ["NATURAL", "CODMUNNATU", "IDADE", "OCUP", "PESO", "RACACOR", "ESTCIV", "SEXO", "CODMUNRES"],
    "InfoMae": ["PARTO", "IDADEMAE", "QTFILVIVO", "QTFILMORT", "GRAVIDEZ", "SEMANAGESTAC", "GESTACAO", "OCUPMAE"],
    "Investigacao": ["NECROPSIA", "EXAME", "ATESTADO", "TPRESGINFO", "CIRURGIA"],
    "Investigador": ["TPNIVELINV"],
    "LocalObito": ["LOCOCOR", "CODESTAB", "CODMUNOCOR", "COMUNSVOIM"],
    "MomentoObito": ["OBITOPARTO", "TIPOBITOCOR", "MORTEPARTO", "TPOBITOCOR", "TPMORTEOCO"],
    "StatusDO": ["STDOEPIDEM", "STDONOVA"],
    "StatusDeCodificacao": ["STCODIFICA"],
    "StatusInvestigacao": ["TPPOS", "ALTCAUSA"]
}

# Sidebar para seleção de tabelas e colunas
st.sidebar.header('Filtros')

# Seleção de tabelas
selected_tables = st.sidebar.multiselect('Selecione as tabelas', options=table_columns.keys())

# Mostrar filtros das colunas relacionadas às tabelas selecionadas
selected_columns = []
for table in selected_tables:
    selected_columns.extend(table_columns[table])

# Filtro para colunas
selected_columns_filter = st.sidebar.multiselect('Selecione as colunas', options=selected_columns)

# Aplicar os filtros
filtered_df = df.copy()

# Filtrar valores nas colunas selecionadas
for col in selected_columns_filter:
    if col in filtered_df.columns:
        unique_values = df[col].dropna().unique()
        selected_values = st.sidebar.multiselect(f'Selecione valores para {col}', options=unique_values)
        if selected_values:
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

# Exibir tabela completa e os filtros aplicados
st.write("Tabela Completa")
st.dataframe(df)

# Exibir apenas as colunas selecionadas
if selected_columns_filter:
    st.write("Tabela Filtrada (somente colunas selecionadas)")
    st.dataframe(filtered_df[selected_columns_filter])
else:
    st.write("Tabela Filtrada (sem filtro de colunas)")
    st.dataframe(filtered_df)

# Adicionar gráficos dinâmicos com base nas colunas selecionadas
st.sidebar.header('Gráficos')

# Seleção de tipo de gráfico
chart_type = st.sidebar.selectbox('Selecione o tipo de gráfico', ['Nenhum', 'Histograma', 'Gráfico de Barras', 'Gráfico de Dispersão'])

# Gráfico de barras ou histograma
if chart_type in ['Histograma', 'Gráfico de Barras']:
    if selected_columns_filter:
        x_col = st.sidebar.selectbox('Selecione a coluna para o eixo X', options=selected_columns_filter)
        if x_col in filtered_df.columns:
            if chart_type == 'Histograma':
                st.write(f'Histograma para {x_col}')
                plt.figure(figsize=(10, 6))
                sns.histplot(filtered_df[x_col].dropna(), kde=False)
                st.pyplot()
            elif chart_type == 'Gráfico de Barras':
                st.write(f'Gráfico de Barras para {x_col}')
                plt.figure(figsize=(10, 6))
                sns.countplot(data=filtered_df, x=x_col)
                st.pyplot()

        if len(selected_columns_filter) >= 2:
            st.write(f'Tabela de Contagem usando GroupBy para {", ".join(selected_columns_filter)}')
            group_by_columns = selected_columns_filter  # Colunas que você selecionou no filtro

            # Realiza o groupby com as colunas selecionadas e conta os valores
            count_table = filtered_df.groupby(group_by_columns).size().reset_index(name='Contagem')
            
            # Adiciona a linha de total no final da tabela
            total_row = pd.DataFrame({col: ['Total'] for col in group_by_columns}, index=[0])
            total_row['Contagem'] = count_table['Contagem'].sum()
            
            # Concatena a tabela com o total
            count_table = pd.concat([count_table, total_row], ignore_index=True)

            # Exibe a tabela resultante
            st.dataframe(count_table)

# Gráfico de dispersão
if chart_type == 'Gráfico de Dispersão':
    if len(selected_columns_filter) >= 2:
        x_col = st.sidebar.selectbox('Selecione a coluna para o eixo X', options=selected_columns_filter)
        y_col = st.sidebar.selectbox('Selecione a coluna para o eixo Y', options=selected_columns_filter)
        if x_col in filtered_df.columns and y_col in filtered_df.columns:
            st.write(f'Gráfico de Dispersão entre {x_col} e {y_col}')
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=filtered_df, x=x_col, y=y_col)
            st.pyplot()
            
            # Exibir tabela com a contagem de cruzamento de dados usando groupby
            st.write(f'Tabela de Contagem usando GroupBy para o cruzamento entre {x_col} e {y_col}')
            cross_tab = filtered_df.groupby([x_col, y_col]).size().reset_index(name='Contagem')
            total_row = pd.DataFrame({'Contagem': [cross_tab['Contagem'].sum()]}, index=['Total'])
            cross_tab = pd.concat([cross_tab, total_row])
            st.dataframe(cross_tab)
#######

# Carregar o CSV
csv_path = "C:/Users/brenda.lima/Downloads/Dicionario.csv"
df = pd.read_csv(csv_path)

# Função para exibir os dados da nova aba
def mostrar_dicionario():
    st.title("Dicionário de Dados")

    # Selecionar as colunas específicas
    if {'Campo', 'Tipo', 'Descricao', 'AnoInicial'}.issubset(df.columns):
        df_filtrado = df[['Campo', 'Tipo', 'Descricao', 'AnoInicial']]

        # Exibir o DataFrame filtrado
        st.dataframe(df_filtrado)
    else:
        st.error("O CSV não contém as colunas necessárias: 'Campo', 'Tipo', 'Descricao', 'AnoInicial'.")

# Interface de navegação
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.selectbox("Selecione a página", ["Dicionário de Dados", "Outra Página"])

# Exibir conteúdo com base na seleção
if pagina_selecionada == "Dicionário de Dados":
    mostrar_dicionario()
else:
    st.write("Conteúdo de outra página.")
