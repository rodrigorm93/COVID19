from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render


import numpy as np
import pandas as pd
import seaborn as sb
import plotly.graph_objs as go
import datetime
import plotly.express as px
import folium
import warnings
import folium 
from folium import plugins
from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.graph_objs import *
import requests
import json

import warnings

warnings.filterwarnings('ignore')




data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_casos_por_comuna_activos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_casos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv')

grupo_uci_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
fallecidos_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
casos_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto13/CasosNuevosCumulativo.csv')



#***************************MENU**************************************
#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

ultima_fecha_cl_r = data_chile_r.columns
ultima_fecha_cl_r= ultima_fecha_cl_r[-1]


ultima_fecha_region_fallecidos = fallecidos_por_region.columns
ultima_fecha_region_fallecidos= ultima_fecha_region_fallecidos[-1]

num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()



num_death =  grupo_fallecidos[ultima_fecha_cl].sum()
num_rec = data_chile_r.iloc[2,-1].sum()

#ver el caso de que no se actualicen los registros

estado_r='Act'+ultima_fecha_cl
estado_f='Act'+ultima_fecha_cl
estado_a='Act'+ultima_fecha_cl

casos_act = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()
#dejar el ulktimo registro de recuperados que fue el 2020-06-02



num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'
casos_act = str(int(casos_act))+' ('+ultima_fecha_cl_r+')'


fecha_casos_fall='('+data_chile.columns[-1]+')'

#********************************************************************

fecha = data_casos_por_comuna_activos.columns
fecha= fecha[-1]

data_activos_region = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Comuna']=='Total']
data_activos_region = data_activos_region.reset_index()
data_activos_region = data_activos_region[['Region',fecha]]
data_activos_region = data_activos_region.rename(columns={fecha:'Casos Activos'})

data_comunas = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Casos-Comunas/COVID19.csv')

resp_comunas = requests.get('https://raw.githubusercontent.com/rgcl/geojson-cl/master/comunas.json')
geo_comunas = json.loads(resp_comunas.content)

locations = {
        "Chile" : [ -30.0000000,-71.0000000],
        "Arica y Parinacota" : [-18.4745998,-70.2979202],
        "Tarapaca" : [-20.2132607,-70.1502686],
        "Antofagasta" : [-23.6523609,-70.395401],
        "Atacama" : [-27.3667908,-70.331398],
        "Coquimbo" : [-29.9533195,-71.3394699],
        "Valparaiso" : [-33.0359993,-71.629631],
        "Metropolitana" : [-33.4726900,-70.6472400],
        "Del Libertador General Bernardo O’Higgins" : [-34.371944,-71.124528],#
        "Maule" : [-35.426667,-71.671667],#
        #"Ñuble" : [1,1],
        "Biobio" : [-36.772778,-73.063056],
        "La Araucania" : [-38.7396507,-72.5984192],
        "Los Rios" : [-40.293129,-73.0816727],
        "Los Lagos" : [-41.7500000,-73.0000000],
        "Aysen" : [-45.4030304,-72.6918411],
        "Magallanes y la Antartica" : [-53.1625,-70.9225]
        
        }


#FUNCIONES

def grafico_Update_Dropdown(region):

    fecha_cd =casos_por_dia.columns
    fecha_cd= fecha_cd[1:]

    fecha_fd =fallecidos_por_dia.columns
    fecha_fd= fecha_fd[1:]

    fecha_uci=grupo_uci_reg.columns
    fecha_uci= fecha_uci[3:]

    # Initialize figure
    fig = go.Figure()
    
    # Add Traces
    casos_diarios_df = pd.DataFrame({"fecha": fecha_cd, "casos": casos_por_dia[casos_por_dia['Region']==region].iloc[0,1:].values})
    fallecidos_diarios_df = pd.DataFrame({"fecha": fecha_fd, "casos": fallecidos_por_dia[fallecidos_por_dia['Region']==region].iloc[0,1:].values})

    UCI_diarios_df = pd.DataFrame({"fecha": fecha_uci, "casos": grupo_uci_reg[grupo_uci_reg['Region']==region].iloc[0,3:].values})


    max_f = pd.to_numeric(fallecidos_diarios_df.casos).idxmax()

    x_m = fallecidos_diarios_df['fecha'].loc[max_f]


    max_c = pd.to_numeric(casos_diarios_df.casos).idxmax()

    x_c = casos_diarios_df['fecha'].loc[max_c]

    max_uci = pd.to_numeric(UCI_diarios_df.casos).idxmax()

    x_uci = UCI_diarios_df['fecha'].loc[max_uci]


    #Casos por dia
    fig.add_trace(
        go.Scatter(x=casos_diarios_df.fecha,
                   y=casos_diarios_df.casos,
                   name='Casos Diarios',
                   line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=casos_diarios_df.fecha,
                   y=[casos_diarios_df.casos.mean()] * len(casos_diarios_df.fecha),
                   name='Promedio',
                   visible=False,
                    line=dict(color="#2ED456", dash="dash")))

    #Fallecidos por dia
    fig.add_trace(
        go.Scatter(x=fallecidos_diarios_df.fecha,
                   y=fallecidos_diarios_df.casos,
                   name='Fallecidos Diarios',
                   visible=False,
                  line=dict(color="#F11013")))


    fig.add_trace(
        go.Scatter(x=fallecidos_diarios_df.fecha,
                   y=[fallecidos_diarios_df.casos.mean()] * len(fallecidos_diarios_df.fecha),
                   name="Promedio",
                   visible=False,
                   line=dict(color="#10CBF1", dash="dash")))


    #UCI

    fig.add_trace(
        go.Scatter(x=UCI_diarios_df.fecha,
                   y=UCI_diarios_df.casos,
                   name='hosp. en UCI',
                   visible=False,
                  line=dict(color="#1466F4")))

    fig.add_trace(
        go.Scatter(x=UCI_diarios_df.fecha,
                   y=[UCI_diarios_df.casos.mean()] * len(UCI_diarios_df.fecha),
                   name="Promedio",
                   visible=False,
                   line=dict(color="#C42ABD", dash="dash")))


    #maximo y promedio casos diarios

    fall_annotations = [dict(x="2020-03-30",
                             y=fallecidos_diarios_df.casos.mean(),
                             xref="x", yref="y",
                             text="Promedio Fallecidos:<br> %.3f" % fallecidos_diarios_df.casos.mean(),
                             ax=0, ay=-40),
                        dict(x=x_m,
                             y=pd.to_numeric(fallecidos_diarios_df.casos).max(),
                             xref="x", yref="y",
                             text="Maximo Fallecidos:<br> %.3f" % pd.to_numeric(fallecidos_diarios_df.casos).max(),
                             ax=0, ay=-40)]

    casos_annotations = [dict(x="2020-03-10",
                             y=casos_diarios_df.casos.mean(),
                             xref="x", yref="y",
                             text="Promedio Casos:<br> %.3f" % casos_diarios_df.casos.mean(),
                             ax=0, ay=-40),
                        dict(x=x_c,
                             y=pd.to_numeric(casos_diarios_df.casos).max(),
                             xref="x", yref="y",
                             text="Maximo Fallecidos:<br> %.3f" % pd.to_numeric(casos_diarios_df.casos).max(),
                             ax=0, ay=-40)]

    uci_annotations = [dict(x="2020-04-10",
                             y=UCI_diarios_df.casos.mean(),
                             xref="x", yref="y",
                             text="Promedio Casos:<br> %.3f" % UCI_diarios_df.casos.mean(),
                             ax=0, ay=-40),
                        dict(x=x_uci,
                             y=pd.to_numeric(UCI_diarios_df.casos).max(),
                             xref="x", yref="y",
                             text="Maximo UCI:<br> %.3f" % pd.to_numeric(UCI_diarios_df.casos).max(),
                             ax=0, ay=-40)]


    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Casos Diarios",
                         method="update",
                         args=[{"visible": [True, False, False, False,False,False]},
                               {"title": region+' Casos Diarios',
                                "annotations": []}]),

                    dict(label="Casos Promedios",
                         method="update",
                         args=[{"visible": [True, True, False, False,False,False]},
                               {"title": region+' Casos Promedios',
                                "annotations": casos_annotations}]),

                    dict(label="Fallecidos Diarios",
                         method="update",
                         args=[{"visible": [False, False, True, False,False]},
                               {"title": region+" Fallecidos Diarios",
                                "annotations": []}]),

                         dict(label="Fallecidos Promedio",
                         method="update",
                         args=[{"visible": [False, False, True, True,False,False]},
                               {"title": region+" Fallecidos Promedios",
                                "annotations": fall_annotations}]),

                     dict(label="Fallecidos vs Casos",
                         method="update",
                         args=[{"visible": [True, False, True, False,False,False]},
                               {"title": region+" Fallecidos vs Casos",
                                "annotations": []}]),

                     dict(label="Pacientes en UCI",
                         method="update",
                         args=[{"visible": [False, False, False, False,True,False]},
                               {"title": region+" Pacientes en UCI",
                                "annotations": []}]),

                    dict(label="UCI Promedio.",
                         method="update",
                         args=[{"visible": [False, False, False, False,True,True]},
                               {"title": region+" Pacientes en UCI Promedio",
                                "annotations": uci_annotations}]),

                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text='Region: '+region)
    return fig



def mapa_comunas(request):



    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Poblacion'],
                                    hovertemplate = '<b>Región</b>: <b>'+data_comunas['Region']+'</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<b>Población: </b>:%{text}<br>'+
                                            '<b>Casos </b>: %{z}<br>'
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3,height=600,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig2 = px.bar(data_activos_region.sort_values('Casos Activos'), 
                    x='Casos Activos', y='Region',color_discrete_sequence=['#84DCC6'],height=600,
                    title='Número de casos Activos por Región '+fecha, text='Casos Activos', orientation='h')
    fig2.update_xaxes(title_text="Número de Casos Activos")
    fig2.update_yaxes(title_text="Comunas")

 
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    fecha_act = '('+data_casos_por_comuna.columns[-2]+')'

    
    return render(request,"mapa_casos_comunas.html", {"grafico1":graph1,"grafico2":graph2,"fecha_casos_fall":fecha_act,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

def mapa_comunas_busqueda(request):

    zoom =7
   
    
    region = request.GET['region']


    if(region=='Tarapaca'):
        region2 = 'Tarapacá'
    elif(region=='Valparaiso'):
        region2 = 'Valparaíso'
    elif(region=='Del Libertador General Bernardo O’Higgins'):
        region2 = 'O’Higgins'
    elif(region=='Nuble'):
        region2 = 'Ñuble'
    elif(region=='Biobio'):
            region2 = 'Biobío'
    elif(region=='La Araucania'):
            region2 = 'Araucanía'
    elif(region=='Los Rios'):
        region2 = 'Los Ríos'
    elif(region=='Aysen'):
            region2 = 'Aysén'
    elif(region=='Magallanes y la Antartica'):
        region2 = 'Magallanes'
    else:
        region2=region

            
     
    lat = locations[region][0]
    lon = locations[region][1]

    if(region == 'Chile'):
        zoom = 3

        fig2 = px.bar(data_activos_region.sort_values('Casos Activos'), 
                    x='Casos Activos', y='Region',color_discrete_sequence=['#84DCC6'],height=700,
                    title='Número de casos Activos por Región '+fecha, text='Casos Activos', orientation='h')
        fig2.update_xaxes(title_text="Número de Casos Activos")
        fig2.update_yaxes(title_text="Regiones")

        num_cases_cl = data_chile.drop([16],axis=0)
        num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()
        num_death =  grupo_fallecidos[ultima_fecha_cl].sum()

        num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
        num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'
        casos_act = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()


      
    else:
  

        data_casos_por_comuna_maule = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Region']==region]
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.reset_index()
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.drop(data_casos_por_comuna_maule.index[len(data_casos_por_comuna_maule)-1])

        n_casos_activos =data_casos_por_comuna_maule[fecha].sum()
        n_casos_activos = str(int(n_casos_activos))+' ('+fecha+')'

        fig2 = px.bar(data_casos_por_comuna_maule.sort_values(fecha), 
                    x=fecha, y='Comuna',color_discrete_sequence=['#84DCC6'],height=600,
                    title='Número de casos Activos Reg: '+region+' fecha: '+fecha, text=fecha, orientation='h')
        fig2.update_xaxes(title_text="Número de Casos Activos")
        fig2.update_yaxes(title_text="Comunas")

        
        n_casos_region = data_chile[data_chile['Region'] ==region2][ultima_fecha_cl].values
        n_casos_region =  str(int(n_casos_region))+' ('+ultima_fecha_cl+')'

        num_cases_cl = n_casos_region

        
        n_casos_region_f = fallecidos_por_region[fallecidos_por_region['Region']==region2][ultima_fecha_region_fallecidos]
        n_casos_region_f = str(int(n_casos_region_f))+' ('+ultima_fecha_region_fallecidos+')'

        num_death =n_casos_region_f

        fig3 = grafico_Update_Dropdown(region2)
        graph3 = fig3.to_html(full_html=False)




   


    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Poblacion'],
                                    hovertemplate = '<b>Región</b>: <b>'+data_comunas['Region']+'</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<b>Población: </b>:%{text}<br>'+
                                            '<b>Casos </b>: %{z}<br>'
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=zoom,height=600,mapbox_center = {"lat": lat, "lon": lon})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})










 
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)

    fecha_act = '('+data_casos_por_comuna.columns[-2]+')'
    
    

    
    return render(request,"mapa_casos_comunas_busqueda.html", {"region":region,"fecha_act":fecha_act,"grafico1":graph1,"grafico2":graph2,"grafico3":graph3,"n_casos":num_cases_cl,"num_rec":n_casos_activos, "num_death":num_death})
