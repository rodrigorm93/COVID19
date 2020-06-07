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


#***************************MENU**************************************
#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()
num_death =  grupo_fallecidos[ultima_fecha_cl].sum()
num_rec = data_chile_r.iloc[2,-1].sum()

#ver el caso de que no se actualicen los registros

estado_r='Act'+ultima_fecha_cl
estado_f='Act'+ultima_fecha_cl
estado_a='Act'+ultima_fecha_cl

#dejar el ulktimo registro de recuperados que fue el 2020-06-02
if (num_rec==0):
    num_rec = data_chile_r.iloc[2,91].sum()
    estado_r='NoAct('+data_chile_r.columns[91]+')'

num_cases_cl = int(num_cases_cl)
num_rec = int(num_rec)
num_death = int(num_death)

fecha_casos_fall='('+data_chile.columns[-1]+')'

#********************************************************************


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
        "Biobio" : [-37.0000000,-72.5000000],
        "Araucania" : [-38.7396507,-72.5984192],
        "Los Rios" : [-40.293129,-73.0816727],
        "Los Lagos" : [-41.7500000,-73.0000000],
        "Aysen" : [-45.4030304,-72.6918411],
        "Magallanes" : [-53.1548309,-70.911293]
        
        }


def mapa_comunas(request):
    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Region'],
                                    hovertemplate = '<b>Región</b>: <b>%{text}</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<br><b>Casos </b>: %{z}<br>',
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3,height=700,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

 
    graph1 = fig.to_html(full_html=False)

    
    return render(request,"mapa_casos_comunas.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

def mapa_comunas_busqueda(request):

    zoom =7

    
    
    region = request.GET['region']
     
    lat = locations[region][0]
    lon = locations[region][1]

    if(region == 'Chile'):
        zoom = 3
   


    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Region'],
                                    hovertemplate = '<b>Región</b>: <b>%{text}</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<br><b>Casos </b>: %{z}<br>',
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=zoom,height=700,mapbox_center = {"lat": lat, "lon": lon})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

 
    graph1 = fig.to_html(full_html=False)

    
    return render(request,"mapa_casos_comunas_busqueda.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
