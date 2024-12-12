import streamlit as st
import pandas as pd
import plotly.express as px
import warnings 

warnings.simplefilter(action='ignore', category=UserWarning)

st.set_page_config(layout="wide")

with open("dashbStyle.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

## @st.cache_data ==> Sintaxe para armazenar dados no cache do navegador
@st.cache_data
def carrega_dados(arq):
    arq = f"https://gestaovirtus.com.br/temp/{arq}.csv"
    dados = pd.read_csv(arq, sep=",", decimal=".")
    return dados

#arq = "https://gestaovirtus.com.br/temp/dados_1_10.csv"
arq = st.query_params["a"]

df = carrega_dados(arq)
df["validade"] = pd.to_datetime(df["Válido até"])
df=df.sort_values("Grupo do Material")
#df["month"] = df["validade"].apply(lambda x: str(x.year) + "-" + str(x.month))
# filtros
#month = st.sidebar.selectbox("Vencendo em", df["validade"].unique())
#grupo = st.sidebar.selectbox("Grupo do Material", df["Grupo do Material"].unique())
a = df["Situação do Material"].unique()
tipos = ['Todos']
for t in a:
    tipos.append(t)
a = df["Grupo do Material"].unique()
grupos = ['Todos']
for t in a:
    grupos.append(t)
a = df["Dias2"].unique()
dias = ['Todos']
for t in a:
    dias.append(t)

dias2 = dias.sort()
dias = ["Todos","Em 30","Em 60","Em 90","Em 120","Em 150","Em 180","Em +180"]
#print("========================",dias2,type(dias2))
#print("dias=",dias,"dias.sort=",dias.sort())
#exit()

grupo = st.sidebar.selectbox("Grupo do Material", grupos)
tipo  = st.sidebar.selectbox("Situação do Material", tipos)
dia   = st.sidebar.selectbox("Dias a Vencer", dias)

#exit()
# filtro 1
if ((grupo=="Todos") and (tipo=="Todos")):
    df1 = df[(df["Grupo do Material"] != grupo) & (df["Situação do Material"] != tipo)]
if ((grupo=="Todos") and (tipo!="Todos")):
    df1 = df[(df["Grupo do Material"] != grupo) & (df["Situação do Material"] == tipo)]
if ((grupo!="Todos") and (tipo=="Todos")):
    df1 = df[(df["Grupo do Material"] == grupo) & (df["Situação do Material"] != tipo)]
if ((grupo!="Todos") and (tipo!="Todos")):
    df1 = df[(df["Grupo do Material"] == grupo) & (df["Situação do Material"] == tipo)]
# filtro 2
if ((grupo=="Todos") and (dia=="Todos")):
    df2 = df1[(df1["Grupo do Material"] != grupo) & (df1["Dias2"] != dia) & (df1["Situação do Material"]!="Vencido")]
if ((grupo=="Todos") and (dia!="Todos")):
    df2 = df1[(df1["Grupo do Material"] != grupo) & (df1["Dias2"] == dia) & (df1["Situação do Material"]!="Vencido")]
if ((grupo!="Todos") and (dia=="Todos")):
    df2 = df1[(df1["Grupo do Material"] == grupo) & (df1["Dias2"] != dia) & (df1["Situação do Material"]!="Vencido")]
if ((grupo!="Todos") and (dia!="Todos")):
    df2 = df1[(df1["Grupo do Material"] == grupo) & (df1["Dias2"] == dia) & (df1["Situação do Material"]!="Vencido")]
df2=df2.sort_values("Dias2")

# métricas - total
itens_total = df1.groupby("ID").count().reset_index()
saldo_total = df1["Quantidade"].sum()
valor_total = df1["Valor Total"].sum()
itens_total = itens_total["ID"].count()
# métricas - vencidos
df_vencidos = df1[(df["Situação do Material"]=="Vencido")]
itens_venc = df_vencidos.groupby("ID").count().reset_index()
saldo_venc = df_vencidos["Quantidade"].sum()
valor_venc = df_vencidos["Valor Total"].sum()
itens_venc = itens_venc["ID"].count()
itens_vencaliq = round(itens_venc / itens_total * 100,1)
saldo_vencaliq = round(saldo_venc / saldo_total * 100,1)
valor_vencaliq = round(valor_venc / valor_total * 100,1)
# métricas - bloqueados
df_bloqueado = df1[(df["Situação do Material"]=="Bloqueado")]
itens_bloq = df_bloqueado.groupby("ID").count().reset_index()
saldo_bloq = df_bloqueado["Quantidade"].sum()
valor_bloq = df_bloqueado["Valor Total"].sum()
itens_bloq = itens_bloq["ID"].count()
itens_bloqaliq = round(itens_bloq / itens_total * 100,1)
saldo_bloqaliq = round(saldo_bloq / saldo_total * 100,1)
valor_bloqaliq = round(valor_bloq / valor_total * 100,1)
# métricas - disponíveis
df_disponivel = df1[(df["Situação do Material"]=="Disponível")]
itens_disp = df_disponivel.groupby("ID").count().reset_index()
saldo_disp = df_disponivel["Quantidade"].sum()
valor_disp = df_disponivel["Valor Total"].sum()
itens_disp = itens_disp["ID"].count()
itens_dispaliq = round(itens_disp / itens_total * 100,1)
saldo_dispaliq = round(saldo_disp / saldo_total * 100,1)
valor_dispaliq = round(valor_disp / valor_total * 100,1)
#

def toDecimal(v,d):
    v = round(v,d)
    if (d<1):
        v = f'{v:,.1f}'
        for z in range(0, 9):
            zz = '.'+str(z)
            v = v.replace(zz,'')
    if (d==1):
        v = f'{v:,.1f}'
    if (d==2):
        v = f'{v:,.2f}'
    if (d==3):
        v = f'{v:,.3f}'
    if (d==4):
        v = f'{v:,.4f}'
    if (d>=5):
        v = f'{v:,.5f}'
    v = v.replace(',','_')
    v = v.replace('.',',')
    v = v.replace('_','.')
    return v

#exit

# quadros do dash
row1 = st.columns(4)
with row1[0]:
    st.markdown("**ARMAZENADOS**")
    st.markdown(f'**:blue[Itens:]** :gray[{toDecimal(itens_total,0)}] => 100,0%')
    st.markdown(f"**:blue[Saldo:]** :gray[{toDecimal(saldo_total,0)}] => 100,0%")
    st.markdown(f"**:blue[Valor(R$):]** :gray[{toDecimal(valor_total,2)}] => 100,0%")
with row1[1]:
    st.markdown("**VENCIDOS**")
    st.markdown(f'**:red[Itens:]** :gray[{toDecimal(itens_venc,0)}] => {toDecimal(itens_vencaliq,1)}%')
    st.markdown(f"**:red[Saldo:]** :gray[{toDecimal(saldo_venc,0)}] => {toDecimal(saldo_vencaliq,1)}%")
    st.markdown(f"**:red[Valor(R$):]** :gray[{toDecimal(valor_venc,2)}] => {toDecimal(valor_vencaliq,1)}%")
with row1[2]:
    st.markdown("**BLOQUEADOS**")
    st.markdown(f'**:orange[Itens:]** :gray[{toDecimal(itens_bloq,0)}] => {toDecimal(itens_bloqaliq,1)}%')
    st.markdown(f"**:orange[Saldo:]** :gray[{toDecimal(saldo_bloq,0)}] => {toDecimal(saldo_bloqaliq,1)}%")
    st.markdown(f"**:orange[Valor(R$):]** :gray[{toDecimal(valor_bloq,2)}] => {toDecimal(valor_bloqaliq,1)}%")
with row1[3]:
    st.markdown("**DISPONÍVEIS**")
    st.markdown(f'**:green[Itens:]** :gray[{toDecimal(itens_disp,0)}] => {toDecimal(itens_dispaliq,1)}%')
    st.markdown(f"**:green[Saldo:]** :gray[{toDecimal(saldo_disp,0)}] => {toDecimal(saldo_dispaliq,1)}%")
    st.markdown(f"**:green[Valor(R$):]** :gray[{toDecimal(valor_disp,2)}] => {toDecimal(valor_dispaliq,1)}%")
  
# definição das colunas
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# gráfico 1
fig_g1 = px.bar(df1, x="Situação do Material", y="Valor Total", color="Grupo do Material", title="Produtos Armazenados - Geral")
col1.plotly_chart(fig_g1, use_container_width=True)
# grafico 2
fig_g2 = px.pie(df2, names="Dias2", values="Valor Total", color="Dias2", title="Produtos Armazenados - A Vencer")
col2.plotly_chart(fig_g2, use_container_width=True)
# grid do filtro 
#col3.subheader("Registros do Filtro")
#col4.subheader("Registros do Filtro")
#col3.write(df1)
#col4.write(df2)
#st.write(df1)

config = {
    "_index": st.column_config.DateColumn("validade", format="MMM YYYY"),
    "Quantidade": st.column_config.NumberColumn("Saldo (und)"),
    "Valor Total": st.column_config.NumberColumn("Total (R$)"),
    "Situação do Material": st.column_config.TextColumn("Situação"),
    "Dias2": st.column_config.TextColumn("Vencendo"),
}
#st.data_editor(df1, disabled_columns=['Dias','validade','month'])
#st.data_editor(df1, disabled_columns=['Dias'])
with col3:
    st.dataframe(df1, column_config=config, hide_index=True)
with col4:
    st.dataframe(df2, column_config=config, hide_index=True)


