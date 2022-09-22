from asyncore import write
from operator import index
import streamlit as st

#from st_aggrid import AgGrid
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from funciones import *

df= st.session_state['saved_nets']





with st.sidebar:
    st.header('Herramienta de análisis y representación de datos')
    st.subheader('Subir archivo excel')
    
    st.subheader('Selección de datos')
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

with st.expander("Ver dataframe en memoria"):
    if df.empty==True:
        st.warning('Importe una tabla de otra página o suba un arhivo de excel.')
    df_ini= df.copy()
    st.write(df_ini)
fig= bar_plot(df, Selec_A)
st.pyplot(fig)

if st.button('Subir XLSX'):
    df= upload_xlsx()