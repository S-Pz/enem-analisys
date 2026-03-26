import os 
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard ENEM - Gestão Pública", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                           
FILE_ENEM_PROCESSED = os.path.join(BASE_DIR, "../../data/processed/enem_2023_limpo.parquet")
FILE_PIB_PROCESSED = os.path.join(BASE_DIR, "../../data/processed/pib_2023_limpo.parquet")

@st.cache_data
def carregar_dados_dashboard():
    df_enem = pd.read_parquet(FILE_ENEM_PROCESSED)
    df_pib = pd.read_parquet(FILE_PIB_PROCESSED)
    return df_enem, df_pib

if __name__ == "__main__":
    
    st.title("Análise do ENEM para Políticas Públicas")
    
    with st.spinner('Carregando dados...'):
        df_enem, df_pib = carregar_dados_dashboard()
    
    st.sidebar.header("Filtros")
    
    regioes_selecionadas = st.sidebar.multiselect(
        "Selecione as Regiões:",
        options=df_enem['REGIAO'].dropna().unique(),
        default=df_enem['REGIAO'].dropna().unique()
    )
    
    df_filtrado = df_enem[df_enem['REGIAO'].isin(regioes_selecionadas)]

    st.header("1. ESTATÍSTICAS DESCRITIVAS")
    colunas_notas = ['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_CN', 'NU_NOTA_REDACAO']
    notas = df_filtrado[colunas_notas].dropna()
    
    if not notas.empty:
        estatisticas = notas.describe().T
        estatisticas['mediana'] = notas.median()
        
        st.write("Resumo Estatístico (Média, Desvio Padrão, Quartis):")
        st.dataframe(estatisticas.style.format("{:.2f}")) 
    else:
        st.warning("Não há dados suficientes para mostrar estatísticas com os filtros atuais.")

    st.header("2. Disparidades por Tipo de Escola")
    st.markdown("Comparação do desempenho entre redes de ensino (Privada x Pública).")
    
    st.subheader("Proporção de Candidatos por Tipo de Escola")
    
    contagem_escola = df_filtrado['TP_ESCOLA'].value_counts()
    print(contagem_escola)
    fig_pie, ax_pie = plt.subplots(figsize=(3, 2))
    
    cores = sns.color_palette("pastel")[0:len(contagem_escola)]
    
    ax_pie.pie(
        contagem_escola, 
        labels=contagem_escola.index, 
        autopct='%1.1f%%',
        startangle=90,    
        colors=cores,
        wedgeprops={'edgecolor': 'white'}
    )
    
    ax_pie.axis('equal')
    st.pyplot(fig_pie)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição das Notas na prova de Matemática")
        fig_mt, ax_mt = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df_filtrado, x='NU_NOTA_MT', hue='TP_ESCOLA', multiple='stack', bins=30, ax=ax_mt)
        ax_mt.set_xlabel('Nota de Matemática')
        ax_mt.set_ylabel('Frequência')
        st.pyplot(fig_mt)

    with col2:
        st.subheader("Distribuição das Notas na prova de Redação")
        fig_red, ax_red = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df_filtrado, x='NU_NOTA_REDACAO', hue='TP_ESCOLA', multiple='stack', bins=30, ax=ax_red)
        ax_red.set_xlabel('Nota de Redação')
        ax_red.set_ylabel('Frequência')
        st.pyplot(fig_red)

    st.header("3. Distribuição das Notas por Região e Gênero")
    st.markdown("Analise como o desempenho varia geograficamente e entre gêneros.")

    nota_selecionada_box = st.selectbox(
        "Selecione a área de conhecimento para o Boxplot:", 
        colunas_notas,
        format_func=lambda x: x.replace('NU_NOTA_', '')
    )

    fig_box, ax_box = plt.subplots(figsize=(14, 8))
    sns.boxplot(
        data=df_filtrado,
        x='REGIAO',
        y=nota_selecionada_box,
        hue='TP_SEXO',
        palette='Set2',
        ax=ax_box
    )
    
    ax_box.set_title(f'Distribuição das Notas ({nota_selecionada_box}) por Região e Gênero', fontsize=16)
    ax_box.set_xlabel('Região', fontsize=14)
    ax_box.set_ylabel('Nota', fontsize=14)

    ax_box.legend(title='Gênero', loc='upper right')

    ax_box.annotate(
        "Regiões:\nN: Norte\nNE: Nordeste\nCO: Centro-Oeste\nSE: Sudeste\nS: Sul",
        xy=(0.95, 0.05), xycoords='axes fraction',
        fontsize=12, ha='right', va='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
    )
    
    st.pyplot(fig_box)

    st.header("4. Histograma Geral Segmentado")
    st.markdown("Distribuição das frequências de notas.")

    nota_selecionada_hist = st.selectbox(
        "Selecione a área de conhecimento para o Histograma:", 
        colunas_notas,
        key="hist_select",
        format_func=lambda x: x.replace('NU_NOTA_', '')
    )

    fig_hist, ax_hist = plt.subplots(figsize=(14, 8))
    
    sns.histplot(
        data=df_filtrado,
        x=nota_selecionada_hist,
        hue='TP_ESCOLA',
        multiple='stack',
        kde=True,
        palette='Set1',
        bins=30,
        ax=ax_hist
    )
    ax_hist.set_title(f'Histograma das Notas ({nota_selecionada_hist}) Segmentado por Tipo de Escola', fontsize=16)
    ax_hist.set_xlabel('Nota', fontsize=14)
    ax_hist.set_ylabel('Frequência', fontsize=14)

    st.pyplot(fig_hist)

    st.header("5. Matriz de Correlação das Notas")
    fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
    matriz_correlacao = notas.corr()
    sns.heatmap(matriz_correlacao, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1, ax=ax_corr)
    st.pyplot(fig_corr)

    st.header("6. Impacto Socioeconômico: PIB e Renda Familiar")
    st.markdown("Análise da correlação entre o Produto Interno Bruto municipal, a renda familiar dos candidatos e o desempenho nas provas.")

    municipios_padrao = ['Ouro Branco', 'Belo Horizonte', 'Congonhas', 'Conselheiro Lafaiete', 'São João del Rei']
    
    municipios_mg = df_enem[df_enem['SG_UF_PROVA'] == 'MG']['NO_MUNICIPIO_PROVA'].str.strip().dropna().unique()
    
    print (df_enem[df_enem['SG_UF_PROVA'] == 'MG']['NO_MUNICIPIO_PROVA'])
   
    municipios_default_validos = [m for m in municipios_padrao if m in municipios_mg]

    cidades_selecionadas = st.multiselect(
        "Selecione os Municípios de MG para análise:",
        options=municipios_mg,
        default=municipios_default_validos
    )

    if cidades_selecionadas:
    
        enem_municipios = df_enem[(df_enem['NO_MUNICIPIO_PROVA'].isin(cidades_selecionadas)) & (df_enem['SG_UF_PROVA'] == 'MG')]
        pib_filtered = df_pib[df_pib['Nome do Município'].isin(cidades_selecionadas)]

        enem_agg = enem_municipios.groupby('NO_MUNICIPIO_PROVA').agg({
            'RENDA_MEDIA': 'mean',
            'NU_NOTA_CN': 'mean',
            'NU_NOTA_CH': 'mean',
            'NU_NOTA_LC': 'mean',
            'NU_NOTA_MT': 'mean',
            'NU_NOTA_REDACAO': 'mean'
        }).reset_index()

        enem_agg.rename(columns={
            'NU_NOTA_CN': 'Nota Média Ciências da Natureza',
            'NU_NOTA_CH': 'Nota Média Ciências Humanas',
            'NU_NOTA_LC': 'Nota Média Linguagens',
            'NU_NOTA_MT': 'Nota Média Matemática',
            'NU_NOTA_REDACAO': 'Nota Média Redação'
        }, inplace=True)

        enem_pib = enem_agg.merge(pib_filtered, left_on='NO_MUNICIPIO_PROVA', right_on='Nome do Município')

        if not enem_pib.empty:
            
            coluna_pib = 'Produto Interno Bruto per capita, \na preços correntes\n(R$ 1,00)'
            
            if coluna_pib not in enem_pib.columns:
                coluna_pib = [col for col in enem_pib.columns if 'per capita' in str(col).lower()][0]

            colunas_correlacao = [coluna_pib, 'RENDA_MEDIA', 'Nota Média CN', 'Nota Média CH', 'Nota Média LC', 'Nota Média MT', 'Nota Média Redação']
            
            colunas_existentes = [col for col in colunas_correlacao if col in enem_pib.columns]
            
            correlation_pib = enem_pib[colunas_existentes].corr()

            fig_pib, ax_pib = plt.subplots(figsize=(12, 8))
            
            labels_limpos = [c.replace('Produto Interno Bruto per capita, \na preços correntes\n(R$ 1,00)', 'PIB per Capita').replace('RENDA_MEDIA', 'Renda Familiar Média') for c in colunas_existentes]
            
            sns.heatmap(
                correlation_pib, 
                annot=True, 
                fmt=".2f", 
                cmap="coolwarm", 
                cbar=True, 
                ax=ax_pib,
                xticklabels=labels_limpos,
                yticklabels=labels_limpos
            )
            ax_pib.set_title("Correlação entre PIB, Renda e Notas do ENEM", fontsize=16, pad=20)
            
            st.pyplot(fig_pib)
            
            with st.expander("Ver Tabela de Dados Agrupados"):
                st.dataframe(enem_pib[['NO_MUNICIPIO_PROVA', 'RENDA_MEDIA', coluna_pib]].style.format(precision=2))
        else:
            st.warning("Não foi possível cruzar os dados do ENEM com os dados do PIB para os municípios selecionados. Verifique se a grafia está exata nas duas bases.")
    else:
        st.info("Selecione pelo menos um município para gerar a análise.")