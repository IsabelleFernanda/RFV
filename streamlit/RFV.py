import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
import timeit
import io
from io import BytesIO




# FUNÇÕES 
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def recencia_class(x, r, q_dict):
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'


# CONFIGURAÇÕES DA PÁGINA 
st.set_page_config(
    page_title='RFV',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown('# RFV')
st.markdown('---')

if 'menu' not in st.session_state:
    st.session_state.menu = 'Home'

if 'df_recencia' not in st.session_state:
    st.session_state.df_recencia = None
if 'df_frequencia' not in st.session_state:
    st.session_state.df_frequencia = None
if 'df_valor' not in st.session_state:
    st.session_state.df_valor = None



titulo_principal = """
        <div style="
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            width: 80%;
            margin: auto;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        ">
            <h1 style="color: #333;">RFV</h1>
            <p style="font-size: 16px; text-align: justify;">
                RFV significa recência, frequência e valor, e é utilizado para segmentação de clientes 
                baseado no comportamento de compras dos clientes. Esse método agrupa clientes em clusters 
                similares, permitindo ações de marketing e CRM mais direcionadas, personalizando conteúdos 
                e ajudando na retenção de clientes.
            </p>
            <h3>Para cada cliente, calculamos:</h3>
            <ul style="text-align: left;">
                <li><b>Recência (R):</b> Quantidade de dias desde a última compra.</li>
                <li><b>Frequência (F):</b> Quantidade total de compras no período.</li>
                <li><b>Valor (V):</b> Total de dinheiro gasto nas compras do período.</li>
            </ul>
        </div>
        """

# SIDEBAR

with st.sidebar:
    data_file_1 = st.file_uploader("INSIRA UM ARQUIVO PARA INICIARMOS A ANÁLISE", type=['csv', 'xlsx'])
    if data_file_1 is None:
        st.stop()
    df_compras = pd.read_csv(data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'])

    selected = option_menu(
        'Menu',
        ['Home','Recência (R)', 'Frequência (F)', 'Valor (V)', 'Análise RFV'],
        icons=['house', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill'],
        menu_icon='cast',
        default_index=0,
        styles={
            'nav-link-selected': {'background-color': '#157806'},
        }
    )

if selected != st.session_state.menu:
    st.session_state.menu = selected
    st.rerun()
    
if selected == "Home":
    st.markdown(titulo_principal, unsafe_allow_html=True)
   

if selected == 'Recência (R)':
    st.markdown("<h1 style='font-size: 2em;'>Recência (R)</h1>", unsafe_allow_html=True) 
    st.markdown('Quantos dias faz que o cliente fez a sua última compra?')
    dia_atual = df_compras['DiaCompra'].max()
    df_recencia = df_compras.groupby('ID_cliente')['DiaCompra'].max().reset_index()
    df_recencia['Recencia'] = (dia_atual - df_recencia['DiaCompra']).dt.days
    st.session_state.df_recencia = df_recencia
    st.write(df_recencia.head(10))

if selected == 'Frequência (F)':
    st.markdown("<h1 style='font-size: 2em;'>Frequência (F)</h1>", unsafe_allow_html=True)
    st.markdown("Quantas vezes cada cliente comprou com a gente?")
    df_frequencia = df_compras.groupby('ID_cliente')['CodigoCompra'].count().reset_index()
    df_frequencia.columns = ['ID_cliente','Frequencia']
    st.session_state.df_frequencia = df_frequencia
    st.write(df_frequencia.head(10))

if selected == 'Valor (V)':
    st.markdown("<h1 style='font-size: 2em;'>Valor (V)</h1>", unsafe_allow_html=True)
    st.markdown("Qual o valor que cada cliente gastou no periodo ?")
    df_valor = df_compras.groupby('ID_cliente')['ValorTotal'].sum().reset_index()
    df_valor.columns = ['ID_cliente','Valor']
    st.session_state.df_valor = df_valor
    st.write(df_valor.head(10))

if selected == 'Análise RFV':
    st.markdown("<h1 style='font-size: 2em;'>Segmentação utilizando o RFV</h1>", unsafe_allow_html=True)
    st.write("""
             Uma forma eficaz de segmentar os clientes é através da criação de quartis para cada componente do RFV (Recência, Frequência e Valor). Nesse sistema, os clientes são classificados em quatro grupos: o melhor quartil recebe a letra 'A', o segundo melhor 'B', o terceiro 'C' e o pior 'D'.  
             A definição do melhor ou pior quartil varia conforme a métrica:  

            - **Recência (R):** Quanto menor a recência, melhor é o cliente, pois significa que ele comprou recentemente. Por isso, o menor quartil é classificado como 'A'.  
            - **Frequência (F):** Neste caso, a lógica se inverte: quanto maior a frequência de compras, melhor é o cliente. Assim, o maior quartil recebe a letra 'A'.  

            Essa classificação facilita a criação de estratégias direcionadas, ajudando a identificar os clientes mais valiosos e aqueles que precisam de ações específicas para aumentar seu engajamento.
             """
    )


    df_RF = pd.merge(st.session_state.df_recencia, st.session_state.df_frequencia, on='ID_cliente')
    df_RFV = pd.merge(df_RF, st.session_state.df_valor, on='ID_cliente')
    st.write('## ')
  

    st.write('Quartis para o RFV')
    quartis = df_RFV.quantile(q=[0.25,0.5,0.75])
    st.write(quartis)

    st.write('Tabela após a criação dos grupos')
    df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class,
                                                        args=('Recencia', quartis))
    df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class,
                                                        args=('Frequencia', quartis))
    df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class,
                                                    args=('Valor', quartis))
    df_RFV['RFV_Score'] = (df_RFV.R_quartil 
                            + df_RFV.F_quartil 
                            + df_RFV.V_quartil)
    st.write(df_RFV.head())

    st.write('Quantidade de clientes por grupos')
    st.write(df_RFV['RFV_Score'].value_counts())

    st.write('#### Clientes com menor recência, maior frequência e maior valor gasto')
    st.write(df_RFV[df_RFV['RFV_Score']=='AAA'].sort_values('Valor', ascending=False).head(10))

    st.write('### Ações de marketing/CRM')

    dict_acoes = {'AAA': 'Enviar cupons de desconto, Pedir para indicar nosso produto pra algum amigo, Ao lançar um novo produto enviar amostras grátis pra esses.',
        'DDD': 'Churn! clientes que gastaram bem pouco e fizeram poucas compras, fazer nada',
        'DAA': 'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar',
        'CAA': 'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar'
        }

    df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
    st.write(df_RFV.head())


    # df_RFV.to_excel('./auxiliar/output/RFV_.xlsx')
    df_xlsx = to_excel(df_RFV)
    st.download_button(label='📥 Download',
                            data=df_xlsx ,
                            file_name= 'RFV_.xlsx')

    st.write('Quantidade de clientes por tipo de ação')
    st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))
