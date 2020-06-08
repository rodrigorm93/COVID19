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
import plotly.express as px

import warnings

warnings.filterwarnings('ignore')


#***************************MENU**************************************


data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')

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


cuarentenas = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto29/Cuarentenas-Activas.csv')

resp = requests.get('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/Cuarentenas/Cuarentenas-Geo.geojson')
geo_region = json.loads(resp.content)


def cuarentenas_activas(request):

    fig = px.choropleth_mapbox(cuarentenas, geojson=geo_region, color="Alcance",
                           locations="Nombre", featureidkey="properties.Nombre",
                           center={"lat": -30.0000000, "lon": -71.0000000},
                           mapbox_style="carto-positron", zoom=3,hover_data=["Fecha de Inicio","Fecha de Término"],
                           height=730
            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    graph1 = fig.to_html(full_html=False)

    data_c =cuarentenas[['Nombre','Alcance','Fecha de Inicio','Fecha de Término']]

    tabla= data_c.to_html()

    
    return render(request,"mapa_cuarentenas.html", {"grafico1":graph1,"tabla":tabla,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})



