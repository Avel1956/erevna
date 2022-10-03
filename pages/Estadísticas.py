from asyncore import write
from operator import index
import streamlit as st

#from st_aggrid import AgGrid
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from funciones import *
from gsheetsdb import connect


# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=0)
    dataframe = pd.DataFrame(list(rows))
    return dataframe

sheet_url = st.secrets["gsheet"]

df = run_query(f'SELECT * FROM "{sheet_url}"')

st.write(df)
df= pd.DataFrame()


try:
    df_prod= pd.read_pickle('output/master_df.pkl')
except:
    df_prod= pd.DataFrame()

try:
    df_contr= pd.read_pickle('input/contr_source.pkl') 
except:
    df_contr= pd.DataFrame()




with st.sidebar:
    st.header('Estadísticas de la Alianza')
    # st.subheader('Subir archivo excel')
    # uploaded_file = st.file_uploader('xlsx')             
    # df=pd.read_excel(uploaded_file, 'Productos')
    
    st.subheader('Selección de datos')
    data= st.radio(
    "Origen de los datos",
    ('Externo','Produccion', 'Contractual'))

    if data == 'Produccion':
        if df_prod is not None:

            df= df_prod
        else:
            st.warning('No hay redes de productos en memoria')
            pass
    if data== 'Contractual':
        if df_contr is not None:

            df= df_contr
        else:
            st.warning('No hay redes contractuales en memoria')
            pass
    if data== 'Externo':
        uploaded_file = st.file_uploader('csv\excel')
        if uploaded_file is not None:
        #read csv
            try:
                df=pd.read_csv(uploaded_file)

            #read xls or xlsx
            except: 
                try:
                    df=pd.read_excel(uploaded_file)
               
                except:
                    st.warning('tipo de archivo no reconocido')
                    



 
        
    Selec_A= st.selectbox(
            
            'Seleccione la columna principal',
            list(df.columns),
            key= 'col_y'
            )
    Selec_B= st.selectbox(
            'Seleccione la columna secundaria',
            df.columns, 
            key= 'col_x'
            )

df_str= df.copy()

st.write(df_str)
with st.expander("Ver dataframe en memoria"):
    if df.empty==True:
        st.warning('Importe una tabla de otra página o suba un arhivo de excel.')
    df_ini= df.copy()
    st.write(df_ini)

res_prods = df["SUBPRODUCTO"].value_counts()
n_rows = len(df)

md_results = f"Hasta la fecha la Alianza ha generado **{n_rows:.2f}** nuevos productos:"

st.markdown(md_results)
st.table(res_prods)
try:

    fig= bar_plot(df, Selec_A)
    st.pyplot(fig)

except:
    st.warning('La (o las) columnas seleccionadas no son adecuadas para este tipo de gráfico')

