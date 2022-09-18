import streamlit as st

#from st_aggrid import AgGrid
import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np


df_prods= st.session_state['saved_nets']
df_prods['index']= np.arange(1, df_prods.shape[0] + 1)
df_prods.index = df_prods['index']
 
st.write(df_prods.index)
st.header('Analisis de la red seleccionada')
st.dataframe(df_prods)


#AgGrid(df_prods)

# if st.button('Limpiar'):
#     df_prods= pd.DataFrame()
#     st.session_state['saved_nets']= df_prods





df_arranged= df_prods.copy()

# fig = plt.figure(figsize=(10, 4))
# sns.barplot( data = df_prods, x = "index", y = "densidad" )
# st.pyplot(fig)

