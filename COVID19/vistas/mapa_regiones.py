from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render



import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import requests
import json

import warnings

warnings.filterwarnings('ignore')




data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_casos_por_comuna_activos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


def int_format(value, decimal_points=3, seperator=u','):
       value = str(value)
       if len(value) <= decimal_points:
           return value
       # say here we have value = '12345' and the default params above
       parts = []
       while value:
           parts.append(value[-decimal_points:])
           value = value[:-decimal_points]
       # now we should have parts = ['345', '12']
       parts.reverse()
       # and the return value should be u'12.345'
       return seperator.join(parts)


#***************************MENU**************************************
#Lenar con 0 filas nulas
data_crec_por_dia = data_crec_por_dia.fillna(0)

ultima_fecha_cl_r = data_crec_por_dia.columns
ultima_fecha_cl_r= ultima_fecha_cl_r[-1]

casos_act_data = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()
casos_totales_data = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos totales'][ultima_fecha_cl_r].sum()
casos_fallecidos_data = data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'][ultima_fecha_cl_r].sum()
casos_recuperados_data = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos recuperados por FIS'][ultima_fecha_cl_r].sum()

num_recuFIS = int_format(int(casos_recuperados_data))
num_cases_cl = int_format(int(casos_totales_data))
num_death = int_format(int(casos_fallecidos_data))
casos_act = int_format(int(casos_act_data))

num_cases_cl = str(num_cases_cl)+' ('+ultima_fecha_cl_r+')'
num_death = str(num_death)+' ('+ultima_fecha_cl_r+')'
casos_act = str(casos_act)+' ('+ultima_fecha_cl_r+')'
num_recuFIS = str(num_recuFIS)+' ('+ultima_fecha_cl_r+')'

fecha_casos = ' ('+ultima_fecha_cl_r+')'

#********************************************************************

data_region = data_chile[['Region',ultima_fecha_cl_r]]
data_region = data_region.rename(columns={ultima_fecha_cl_r:'Casos'})

resp = requests.get('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/geo-json/regiones.json')
geo_region = json.loads(resp.content)



fecha = data_casos_por_comuna_activos.columns
fecha= fecha[-1]
data_activos_region = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Comuna']=='Total']
data_activos_region = data_activos_region.reset_index()
data_activos_region = data_activos_region[['Region',fecha]]
data_activos_region = data_activos_region.rename(columns={fecha:'Casos Activos'})
data_activos_region.loc[data_activos_region['Region'] == 'Magallanes y la Antartica', "Region"] = 'Magallanes'
data_activos_region.loc[data_activos_region['Region'] == 'Del Libertador General Bernardo O’Higgins', "Region"] = 'O’Higgins'

data_f = fallecidos_por_region[['Region',ultima_fecha_cl_r]]
data_f = data_f.rename(columns={ultima_fecha_cl_r:'Fallecidos'})
data_f = data_f.drop([16],axis=0)

#funciones
datos = data_chile[['Region',ultima_fecha_cl_r]].drop([16],axis=0)
datos = datos.rename(columns={ultima_fecha_cl_r:'Casos'})

button_layer_1_height = 1.08

def casos_regiones():
    fig = go.Figure()

    fig.add_trace(go.Bar(x=datos['Casos'].values, y=datos['Region'],orientation='h',
                        name="Casos Acumulados",marker_color='lightsalmon')
                 )
    fig.update_layout(height=700)


    fig.add_trace(go.Bar(x=data_activos_region['Casos Activos'].values, y=data_activos_region['Region'],orientation='h',
                        name='Casos Activos',visible=False,marker_color='#84DCC6')
                 )
    fig.update_layout(height=700)

    fig.add_trace(go.Bar(x=data_f['Fallecidos'].values, y=data_f['Region'],orientation='h',
                        name='Fallecidos',visible=False,marker_color='#ff2e63')
                 )
    fig.update_layout(height=700)



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Acumulados",
                         method="update",
                         args=[{"visible": [True, False, False]},
                               {"title": "Total de Casos Acumulados "+ultima_fecha_cl_r,
                                "annotations": []}]),
                    dict(label="Activos",
                         method="update",
                         args=[{"visible": [False, True, False]},
                               {"title": "Total de Casos Activos "+fecha,
                                "annotations": []}]),
                    dict(label="Fallecidos",
                         method="update",
                         args=[{"visible": [False, False, True]},
                               {"title": "Total de Fallecidos "+ultima_fecha_cl_r,
                                "annotations": []}]),
                    
                                

                ]),
            direction="down",
            pad={"r": 20, "t": 1},
            showactive=True,
            x=0.3,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
            )
           
        ])

    # Set title
    fig.update_layout(title_text="Regiones")
    fig.update_layout(
    annotations=[
        dict(text="Casos", x=0.2, xref="paper", y=1.06, yref="paper",
                             align="left", showarrow=False)
    ])

    return fig

def mapa_region(request):


    fig2 = casos_regiones()

    fig = go.Figure(go.Choroplethmapbox(geojson=geo_region, locations=data_region.Region, z=data_region.Casos,
                                    colorscale="Viridis", zmin=0, zmax=6000,
                                    featureidkey="properties.NOM_REG",
                                    marker_opacity=0.2, marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3,height=700,mapbox_center = {"lat": -30.0000000, "lon": -71.0000000})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    
    return render(request,"mapa_casos_regiones.html", {"grafico1":graph1,"grafico2":graph2,"fecha_casos":ultima_fecha_cl_r,"casos_act":casos_act,"n_casos":num_cases_cl,"num_rec":num_recuFIS, "num_death":num_death})

