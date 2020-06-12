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

data_region = data_chile[['Region',ultima_fecha_cl]]
data_region = data_region.rename(columns={ultima_fecha_cl:'Casos'})

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

data_f = fallecidos_por_region[['Region',ultima_fecha_cl]]
data_f = data_f.rename(columns={ultima_fecha_cl:'Fallecidos'})
data_f = data_f.drop([16],axis=0)

#funciones
datos = data_chile[['Region',ultima_fecha_cl]].drop([16],axis=0)
datos = datos.rename(columns={ultima_fecha_cl:'Casos'})

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
                               {"title": "Total de Casos Acumulados",
                                "annotations": []}]),
                    dict(label="Activos",
                         method="update",
                         args=[{"visible": [False, True, False]},
                               {"title": "Total de Casos Activos",
                                "annotations": []}]),
                    dict(label="Fallecidos",
                         method="update",
                         args=[{"visible": [False, False, True]},
                               {"title": "Total de Fallecidos",
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
    
    return render(request,"mapa_casos_regiones.html", {"grafico1":graph1,"grafico2":graph2,"fecha_casos_fall":fecha_casos_fall,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

