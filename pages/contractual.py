import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
from funciones import *

df_contract= pd.read_pickle('input/contr_source.pkl') #archivo de personal de la Alianza
df_contract['Semestre']= df_contract.Semestre.astype(str)
df_contract['ID']= df_contract.ID.astype(str)
df_contract['CVLAC']= df_contract.CVLAC.astype(str)

st.set_page_config(layout="wide")

###Establecimiento de parametros de seleccion
with st.sidebar:
    st.title('Visualización de las redes contractuales de la Alianza SÉNECA')
    st.write('Seleccione las características de la red')
    #[0]
    periodo = st.multiselect('Seleccione el rango de periodos a consultar',  
    ['todos','2019-1', '2020-2', '2021-1', '2021-2'], default= '2019-1')
    
    #[1]
    tipo_red= st.selectbox('Tipo(s) de red',('personas-instituciones', 
    'personas-proyectos'))
    #[2]
    tipo_vinculacion= st.multiselect('Tipo de vinculación',
     ['Acompañamiento conceptual y metodológico',
     'Asesor', 
     'ASESOR NACIONAL',
     'COINVESTIGADOR',
     'COINVESTIGADOR ENTIDAD INTERNACIONAL',
     'COINVESTIGADOR SECTOR PRODUCTIVO',
     'DIRECTOR CIENTÍFICO',
     'ESTUDIANTE DE DOCTORADO',
     'ESTUDIANTE DE MAESTRíA',
     'ESTUDIANTE DE PREGRADO',
     'INVESTIGADOR', 
     'INVESTIGADOR PRINCIPAL',
     'JOVEN INVESTIGADOR',
     'PERSONAL DE APOYO',
     'Subdirectora de Fortalecimiento',
     'todos'], 
     default= 'todos')
    #[3]
    formacion= st.multiselect('Seleccione el nivel de formación',
    ['todos', 
    'Doctorado',
    'Especialización',
    'Maestría/Magister',
    'Posdoctorado',
    'Pregrado/Universitario',
    'Secundaria'], default= 'todos')
    #[4]
    genero = st.multiselect('Seleccione el genero de los participantes', 
    ['todos', 'Femenino', 'Masculino'], default= 'todos')
    
    
    
    query= (periodo, tipo_red, tipo_vinculacion, formacion, genero) 
    saved_nets= pd.DataFrame()
    st.write('Usted seleccionó: ', query)



df_contract_filtered= find_items_contr(query, df_contract)
st.header("Redes contractuales")
st.markdown('---')
with st.expander("Ver los datos seleccionados"):
        df_ini= df_contract_filtered.copy()
        st.dataframe(df_ini)
        
G=nx.from_pandas_edgelist(df_contract_filtered, 'Source', 'Target')

name = st.selectbox('Seleccione el nodo principal ',
    list(G.nodes()))
color_net = sel_prop(G, name) 
nx.write_graphml_lxml(color_net, "output\\contractnet.graphml")
name_target = st.selectbox(
    'Seleccione el nodo objetivo ',
    list(G.nodes()))

nx.write_graphml_lxml(color_net, "output\\net.graphml")
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
#Creación de caja de selección del nodo 2 
node_metrics_df = pd.DataFrame(data = node_metrics)
try:
    camino_mas_corto = nx.shortest_path(color_net, source = name, target = name_target)
except:
    camino_mas_corto = "No existe un camino entre los nodos seleccionados"


red_metrics_df = red_metrics(color_net, query)
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
PG.save_graph('output\\contractual.html')

st.write(G)



col1, col2= st.columns([3,1])

with col1:
    st.write('Red seleccionada')
    Htmlcontract = open('output\\contractual.html', 'r', encoding='utf-8')
    components.html(Htmlcontract.read(), height=600)
with col2:
    st.subheader('Métricas de red')

    #st.dataframe(red_metrics_df)
    st.subheader('Métricas del nodo seleccionado')
    st.dataframe(node_metrics_df)
    









# Htmlcontract = open('output\\contract_complete.html', 'r', encoding='utf-8')
# components.html(Htmlcontract.read(), height=600)