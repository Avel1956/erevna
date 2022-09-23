from asyncore import write
from operator import index
import streamlit as st

#from st_aggrid import AgGrid
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from funciones import *







with st.sidebar:
    st.header('Herramienta de análisis y representación de datos')
    # st.subheader('Subir archivo excel')
    # uploaded_file = st.file_uploader('xlsx')             
    # df=pd.read_excel(uploaded_file, 'Productos')
    
    st.subheader('Selección de datos')
    data= st.radio(
    "What's your favorite movie genre",
    ('Produccion', 'Contractual', 'Externo'))

    if data == 'Produccion':
        if st.session_state('saved_prod') is not None:

            df= st.session_state('saved_prod')
        else:
            st.warning('No hay redes de productos en memoria')
    if data== 'Contractual':
        if st.session_state('saved_contractual') is not None:

            df= st.session_state('saved_contractual')
        else:
            st.warning('No hay redes contractuales en memoria')
    if data== 'Externo':
        uploaded_file = st.file_uploader('csv\excel')
        if uploaded_file is not None:
        #read csv
            try:
                df=pd.read_csv(uploaded_file)

            #read xls or xlsx
            except: 
               
                df=pd.read_excel(uploaded_file)
            
            # except:
            #     st.warning('tipo de archivo no reconocido')



    else:
        st.warning('you need to upload a csv or excel file.')
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
st.write(df)
with st.expander("Ver dataframe en memoria"):
    if df.empty==True:
        st.warning('Importe una tabla de otra página o suba un arhivo de excel.')
    df_ini= df.copy()
    st.write(df_ini)
fig= bar_plot(df, Selec_A)
st.pyplot(fig)

