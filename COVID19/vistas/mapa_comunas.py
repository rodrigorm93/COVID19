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


#***************************MENU**************************************
#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

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

#dejar el ulktimo registro de recuperados que fue el 2020-06-02
if (num_rec==0):
    num_rec = data_chile_r.iloc[2,91].sum()
    estado_r='NoAct('+data_chile_r.columns[91]+')'


num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'

num_rec = int(num_rec)



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


def mapa_comunas(request):



    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Region'],
                                    hovertemplate = '<b>Región</b>: <b>%{text}</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<b>Casos </b>: %{z}<br>'+
                                            '<b>Fecha: </b>:'+data_casos_por_comuna.columns[-2]
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3,height=730,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig2 = px.bar(data_activos_region.sort_values('Casos Activos'), 
                    x='Casos Activos', y='Region',color_discrete_sequence=['#84DCC6'],height=700,
                    title='Número de casos Activos por Región '+fecha, text='Casos Activos', orientation='h')
    fig2.update_xaxes(title_text="Número de Casos Activos")
    fig2.update_yaxes(title_text="Comunas")

 
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    fecha_act = '('+data_casos_por_comuna.columns[-2]+')'

    
    return render(request,"mapa_casos_comunas.html", {"grafico1":graph1,"grafico2":graph2,"fecha_casos_fall":fecha_act,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

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
        fig2.update_yaxes(title_text="Comunas")

        num_cases_cl = data_chile.drop([16],axis=0)
        num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()
        num_death =  grupo_fallecidos[ultima_fecha_cl].sum()

        num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
        num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'

      
    else:
  

        data_casos_por_comuna_maule = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Region']==region]
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.reset_index()
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.drop(data_casos_por_comuna_maule.index[len(data_casos_por_comuna_maule)-1])

        n_casos_activos =data_casos_por_comuna_maule[fecha].sum()
        n_casos_activos = str(int(n_casos_activos))+' ('+fecha+')'

        fig2 = px.bar(data_casos_por_comuna_maule.sort_values(fecha), 
                    x=fecha, y='Comuna',color_discrete_sequence=['#84DCC6'],height=700,
                    title='Número de casos Activos Reg: '+region+' fecha: '+fecha, text=fecha, orientation='h')
        fig2.update_xaxes(title_text="Número de Casos Activos")
        fig2.update_yaxes(title_text="Comunas")

        
        n_casos_region = data_chile[data_chile['Region'] ==region2][ultima_fecha_cl].values
        n_casos_region =  str(int(n_casos_region))+' ('+ultima_fecha_cl+')'

        num_cases_cl = n_casos_region

        
        n_casos_region_f = fallecidos_por_region[fallecidos_por_region['Region']==region2][ultima_fecha_region_fallecidos]
        n_casos_region_f = str(int(n_casos_region_f))+' ('+ultima_fecha_region_fallecidos+')'

        num_death =n_casos_region_f

   


    fig = go.Figure(go.Choroplethmapbox(geojson=geo_comunas, locations=data_comunas.Comuna, z=data_comunas.Casos,
                                    colorscale="Viridis", zmin=0, zmax=1000,
                                    featureidkey="properties.NOM_COM",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0, text=data_comunas['Region'],
                                    hovertemplate = '<b>Región</b>: <b>%{text}</b>'+
                                            '<br><b>Comuna </b>: %{properties.NOM_COM}<br>'+
                                            '<b>Casos </b>: %{z}<br>'+
                                            '<b>Fecha: </b>:'+data_casos_por_comuna.columns[-2]
                                    
                                       
                                   ))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=zoom,height=730,mapbox_center = {"lat": lat, "lon": lon})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


  

 
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)

    fecha_act = '('+data_casos_por_comuna.columns[-2]+')'


    
    return render(request,"mapa_casos_comunas_busqueda.html", {"region":region,"fecha_act":fecha_act,"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
