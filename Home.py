

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from pyvis.network import Network
from funciones import *





df= pd.read_pickle('output/master_df.pkl')



#Opciones por defecto

st.set_page_config(layout="wide")
with st.sidebar:
    st.title('Visualización de las redes de colaboración de la Alianza SÉNECA')
    st.write('Seleccione el tipo de red')
    periodo = st.multiselect('Seleccione el rango de periodos a consultar',  
    ['todos','1.0', '2.0', '3.0', '4.0', '5.0', '6.0',
     '7.0', '8.0', '9.0', '10.0'], default= 'todos')
    tipo_red= st.multiselect('Tipo(s) de red',['todos', 'aut_net', 'group_net', 'inst_net'], default= 'inst_net')
    proyecto = st.multiselect('Seleccione el (o los) proyectos participantes en la red', 
    ['todos', 'Proy1', 'Proy2', 'Proy3', 'Proy4', 'Proy5', 'Proy6', 'Proy7', 'Proy8', 'Proy9',
     'Proy10', 'Proy11', 'Proy12', 'Proy13', 'Proy14', 'Proy15'], default= 'todos')
    tipo_prod= st.multiselect('Tipo de producto', ['Nuevo_Conocimiento', 'Apropiación', 'todos'], default= 'todos')
    tipo_sub_prod = st.multiselect('Seleccione el tipo de subproducto', 
    ['todos', 'Artículo A1', 'Artículo A2', 'Artículo B', 'Artículo C',
     'Capítulo de libro A', 'Capítulo de libro A1', 'Ponencia'], default= 'todos')
    
    
    
    query= (periodo, tipo_red, proyecto, tipo_prod, tipo_sub_prod ) 
    saved_nets= pd.DataFrame()
    st.write('Usted seleccionó: ', query)

#########################################
#########################################
#Productos
#########################################
#########################################

st.header("Red de colaboracion en productos")

with st.expander("Ver todas las combinaciones posibles"):
    df_ini= df.copy()
    st.dataframe(df_ini)

st.subheader("Red seleccionada") 

df_sel= find_items(query, df)
st.write(df_sel) 

G=nx.from_pandas_edgelist(df_sel, 'source', 'target')

   #######seleccion de nodos
    
name = st.selectbox('Seleccione el nodo principal ',
    list(G.nodes()))
color_net = sel_prop(G, name) 
nx.write_graphml_lxml(color_net, "output\\net.graphml")
#Creación de caja de selección del nodo 2 

name_target = st.selectbox(
    'Seleccione el nodo objetivo ',
    list(G.nodes()))
color_net = sel_prop(G, name) 
nx.write_graphml_lxml(color_net, "output\\net.graphml")
    # #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# #Cálculo de métricas de la red
# #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# #Centralidad (degree)
# #diccionario de los grados de cada nodo
dict_grado= dict(color_net.degree(color_net.nodes()))
#aplicar atributo de grado a los nodos
nx.set_node_attributes(color_net, dict_grado, 'grado')
# #Mostrar centralidad del nodo seleccionado
med_cent = nx.betweenness_centrality(color_net)
eig_cent = nx.eigenvector_centrality(color_net)

    
# #Asignacion como atributo de cada nodo
nx.set_node_attributes(color_net, med_cent, 'betweenness')
nx.set_node_attributes(color_net, eig_cent, 'eigenvector')

# #Diccionario de métricas de nodo seleccionado 
node_metrics = {'Nodo': [name], 
    'Grado': [color_net.nodes[name]['grado']],
'Centralidad de mediacion':[color_net.nodes[name]['betweenness']],
'Centralidad de eigenvector': [color_net.nodes[name]['eigenvector']]
}
# #Dataframe a partir del diccionario de métricas para representación  
node_metrics_df = pd.DataFrame(data = node_metrics)
# #--------------------------------
# #Camino más corto entre nodos (shortest path) 
try:
    camino_mas_corto = nx.shortest_path(color_net, source = name, target = name_target)
except:
    camino_mas_corto = "No existe un camino entre los nodos seleccionados"

# #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# #Estadísticas de red 

# #Dataframe de métricas de la red para representación  
red_metrics_df = red_metrics(color_net, query)

#######
###Guardar metricas con un nombre específico
#######

try:

    saved_nets= st.session_state['saved_nets']
except:
    pass

if st.button('Guardar red'):
    rdata= red_metrics_df.copy()
    
    
    saved_nets= pd.concat([saved_nets, rdata])
    st.session_state['saved_nets'] = saved_nets
    

csv = convert_df(saved_nets)

st.download_button(
   "Descargar",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

######inicializar objeto pyvis
PG = Network(height='600px',
            width='100%',
            bgcolor='#020202',
                    
            font_color='white'
            ) 
PG.from_nx(G)
PG.repulsion(node_distance=420,
                    central_gravity=0.33,
                    spring_length=110,
                    spring_strength=0.10,
                    damping=0.95
                    )


# guardar y leer el grafico como HTML (Streamlit Sharing)
PG.save_graph('output\\PG.html')
HtmlFile = open('output\\PG.html', 'r', encoding='utf-8')
st.write(G)

col1, col2= st.columns([3,1])

with col1:
    st.subheader('Red seleccionada')
    Htmlprod = open('output\\PG.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=600)
with col2:
    st.subheader('Métricas de red')
    st.write('La densidad de la red es:')
    red_metrics_df_transp= red_metrics_df.transpose()
    st.dataframe(red_metrics_df_transp)
    st.subheader('Métricas del nodo seleccionado')
    st.dataframe(node_metrics_df)


 