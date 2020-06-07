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

data_region = data_chile[['Region',ultima_fecha_cl]]
data_region = data_region.rename(columns={ultima_fecha_cl:'Casos'})

resp = requests.get('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/geo-json/regiones.json')
geo_region = json.loads(resp.content)

def mapa_region(request):

    datos = data_chile[['Region',ultima_fecha_cl]].drop([16],axis=0)



    fig = go.Figure(go.Choroplethmapbox(geojson=geo_region, locations=data_region.Region, z=data_region.Casos,
                                    colorscale="Viridis", zmin=0, zmax=6000,
                                    featureidkey="properties.NOM_REG",
                                    marker_opacity=0.2, marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3,height=700,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    titulo ='COVID-19: Total de Casos acumulados'

    fig2 = px.bar(datos.sort_values(ultima_fecha_cl), 
             x=ultima_fecha_cl, y="Region", 
             title=titulo,
              text=ultima_fecha_cl, 
             orientation='h',height=700)
    fig2.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig2.update_layout(template = 'plotly_white')

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)


    
    return render(request,"mapa_casos_regiones.html", {"grafico1":graph1,"grafico2":graph2,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

