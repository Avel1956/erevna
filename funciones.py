import pandas as pd
import streamlit as st
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
def find_items(opciones, df):
    
    
    st.write(opciones)
    #st.write(df['combination'])
    
    df_final_per= pd.DataFrame()
    df_final_net= pd.DataFrame()
    df_final_proy= pd.DataFrame()
    df_final_tiprod= pd.DataFrame()
    df_final_subprod= pd.DataFrame()
    border_list= [] 

    for item in opciones[0]:
        if item== 'todos':
            df_final_per= df
        else:
            df_per= df.loc[df['periodo']== item]
            df_final_per= pd.concat([df_final_per, df_per])
        
    for item in opciones[1]:
        if item== 'todos':
            df_final_net= df_final_per.copy()
            
        else:
            df_net= df_final_per.loc[df_final_per['tipo_red']== item]
            df_final_net= pd.concat([df_final_net, df_net])
            
    for item in opciones[2]:
        if item== 'todos':
            df_final_proy= df_final_net.copy()
           
        else:
            df_proy= df_final_net.loc[df_final_net['proyecto']== item]
            df_final_proy= pd.concat([df_final_proy, df_proy])
    for item in opciones[3]:
        if item== 'todos':
            df_final_tiprod= df_final_proy.copy()
        else:
            df_tiprod= df_final_proy.loc[df_final_proy['tipo_prod']== item]
            df_final_tiprod= pd.concat([df_final_tiprod, df_tiprod])
    for item in opciones[4]:
        if item== 'todos':
            df_final_subprod= df_final_tiprod.copy()
        else:
            df_subprod= df_final_tiprod.loc[df_final_tiprod['subproducto']== item]
            df_final_subprod= pd.concat([df_final_subprod, df_subprod])
        
    st.write(df_final_subprod)        
    border_df= df_final_subprod['borders']      
    
    for list in border_df:
        for item in list:
            border_list.append(item)

    filtered_df= pd.DataFrame(border_list, columns=['source', 'target'])
    return filtered_df

def sel_prop(net, name):
    #vector inicial seleccion
    nx.set_edge_attributes(net, '#8E9F7D', "color"  )
    nx.set_node_attributes(net, 0, "sel")
     #vector inicial de colores
    nx.set_node_attributes(net, 'white', "color")
     #Aplicacion del valor de seleccion al nodo seleccionado
    net.nodes[name]["sel"] = 1
     #Aplicacion de color al nodo (y los bordes conectados a este)
    net.nodes[name]["color"] = '#B2F227'
    return net

def convert_df(df):
   return df.to_csv().encode('utf-8')

def red_metrics(G, query):
    num_nodes= G.number_of_nodes()
    num_bordes= G.number_of_edges()
    dens_red= nx.density(G)
    comm_red= nx.communicability(G)
    esta_conectada= nx.is_connected(G)
    no_componentes= nx.number_connected_components(G)
    componentes= nx.connected_components(G)
    componente_mayor= max(componentes, key = len)
    comunidades= greedy_modularity_communities(G)
    red_metrics= {'Tipo red': [query],
    'num_nodos': [num_nodes],
    'num_bordes': [num_bordes], 
    'densidad': [dens_red],
    'Comunicabilidad': [comm_red],
    'Está completamente conectada': [esta_conectada],
    'Cuantas subredes': [no_componentes]} 
    red_metrics_df = pd.DataFrame(data = red_metrics)
    return red_metrics_df