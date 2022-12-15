import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities



####funciones de tronsformacion de datos
#####
#funcion de filtrado productos
##
def find_items_prod(opciones, df):
    
    
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

#funcion de filtrado de personal
##
def find_items_contr(opciones, df):
    
    
    st.write(opciones)
    #st.write(df['combination'])
    
    df_final_per= pd.DataFrame()
    df_final_net= pd.DataFrame()
    df_final_vinc= pd.DataFrame()
    df_final_form= pd.DataFrame()
    df_final_gen= pd.DataFrame()
    border_list= [] 

    for item in opciones[0]:#Semestre
        if item== 'todos':
            df_final_per= df
        else:
            df_per= df.loc[df['Semestre']== item]
            df_final_per= pd.concat([df_final_per, df_per])
        
    #tipo de red
    df_final_net= df_final_per.copy()
    
        
    if opciones[1]== ['personas-instituciones']:
        df_final_net.rename(columns = {'Nombre':'Source', 'Entidad':'Target'}, inplace = True)
    
    if opciones[1]== ['personas-proyectos']:
        df_final_net.rename(columns = {'Nombre':'Source', 'Proyecto':'Target'}, inplace = True)
    
            
    for item in opciones[2]:#vinculacion
        if item== 'todos':
            df_final_vinc= df_final_net.copy()
           
        else:
            df_vinc= df_final_net.loc[df_final_net['Rol']== item]
            df_final_vinc= pd.concat([df_final_net, df_vinc])
    
    
    for item in opciones[3]:#formacion
        if item== 'todos':
            df_final_form= df_final_vinc.copy()
        
        else:
            df_form= df_final_vinc.loc[df_final_vinc['Formación']== item]
            df_final_form= pd.concat([df_final_form, df_form])
    
    
    for item in opciones[4]:#genero
        if item== 'todos':
            df_final_gen= df_final_form.copy()
        else:
            df_gen= df_final_form.loc[df_final_form['Género']== item]
            df_final_gen= pd.concat([df_final_gen, df_gen])
    
    return df_final_gen


def find_items_sem(opciones, df):
    
    
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
            df_final_proy= df_final_per.copy()
           
        else:
            df_proy= df_final_net.loc[df_final_net['proyecto']== item]
            df_final_proy= pd.concat([df_final_proy, df_proy])
    for item in opciones[2]:
        if item== 'todos':
            df_final_tiprod= df_final_proy.copy()
        else:
            df_tiprod= df_final_proy.loc[df_final_proy['tipo_prod']== item]
            df_final_tiprod= pd.concat([df_final_tiprod, df_tiprod])
    for item in opciones[3]:
        if item== 'todos':
            df_final_subprod= df_final_tiprod.copy()
        else:
            df_subprod= df_final_tiprod.loc[df_final_tiprod['subproducto']== item]
            df_final_subprod= pd.concat([df_final_subprod, df_subprod])


    #st.write(str(df_final_subprod))        
    border_df= df_final_subprod['borders']      
    
    for list in border_df:
        for item in list:
            border_list.append(item)

    filtered_df= pd.DataFrame(border_list, columns=['source', 'target'])
    return filtered_df
#convertir dataframe en csv
##
def convert_df(df):
   return df.to_csv().encode('utf-8')
###funciones de manipulacion de redes
####
#cambiar el color de la red y resaltar un nodo especifico
##
def sel_prop(net, name):
    #vector inicial seleccion
    nx.set_edge_attributes(net, '#f2542d', "color"  )
    nx.set_node_attributes(net, 0, "sel")
     #vector inicial de colores
    nx.set_node_attributes(net, '#040f0f', "color")
     #Aplicacion del valor de seleccion al nodo seleccionado
    net.nodes[name]["sel"] = 1
     #Aplicacion de color al nodo (y los bordes conectados a este)
    net.nodes[name]["color"] = '#0e9594'
    return net


#metricas de la red
##
def red_metrics(G, query):
    num_nodes= G.number_of_nodes()
    num_bordes= G.number_of_edges()
    dens_red= nx.density(G)
    #comm_red= nx.communicability(G)
    esta_conectada= nx.is_connected(G)
    no_componentes= nx.number_connected_components(G)
    componentes= nx.connected_components(G)
    componente_mayor= max(componentes, key = len)
    comunidades= greedy_modularity_communities(G)
    red_metrics= {'Tipo red': [query],
    'num_nodos': [num_nodes],
    'num_bordes': [num_bordes], 
    'densidad': [dens_red],
    #'Comunicabilidad': [comm_red],
    'Está completamente conectada': [esta_conectada],
    'Cuantas subredes': [no_componentes]} 
    red_metrics_df = pd.DataFrame(data = red_metrics)
    return red_metrics_df

###funciones de generacion de graficos
####

#para un dataframe dado, figura de un grafico de barras con los conteos de ocurrencias
#de los elementos unicos de la columna x del dataframe
##
def bar_plot(df, x):
    custom_style = {'axes.labelcolor': 'gray',
                'grid.color': 'None',
                'axes.edgecolor': 'gray',
                'axes.facecolor': 'None',
                'grid.color': 'gray',
                'xtick.color': 'gray',
                'ytick.color': 'grey'}
    sns.set_style("dark", rc=custom_style)
    
    fig = plt.figure(figsize=(10, 4))
    
    fig.patch.set_facecolor('None')
    ax= sns.countplot(x= x, data= df, order = df[x].value_counts().index )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    #fig.legend(loc='upper right')
    return fig