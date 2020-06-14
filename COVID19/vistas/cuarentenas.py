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
from plotly.subplots import make_subplots


#***************************MENU**************************************


data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')

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


data_comunas = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto29/Cuarentenas-Activas.csv')
cuarentenas = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto29/Cuarentenas-Activas.csv')

data_comunas = data_comunas.rename(columns={'Nombre':'Comuna'})

data_comunas.loc[data_comunas['Comuna'] == 'Independencia Extensión a Total', "Comuna"] = 'Independencia'
data_comunas.loc[data_comunas['Comuna'] == 'Santiago Extensión a Total', "Comuna"] = 'Santiago'
data_comunas.loc[data_comunas['Comuna'] == 'La Pintana Extensión a Total', "Comuna"] = 'La Pintana'
data_comunas.loc[data_comunas['Comuna'] == 'San Ramón Extensión a Total', "Comuna"] = 'San Ramón'
data_comunas.loc[data_comunas['Comuna'] == 'Las Condes Re-ingreso Total', "Comuna"] = 'Las Condes'
data_comunas.loc[data_comunas['Comuna'] == 'Lo Barnechea Re-ingreso total', "Comuna"] = 'Lo Barnechea'
data_comunas.loc[data_comunas['Comuna'] == 'Vitacura Re-ingreso Total', "Comuna"] = 'Vitacura'
data_comunas.loc[data_comunas['Comuna'] == 'Ñuñoa Re-ingreso Total', "Comuna"] = 'Ñuñoa'
data_comunas.loc[data_comunas['Comuna'] == 'Puente Alto Extensión a Total', "Comuna"] = 'Puente Alto'
data_comunas.loc[data_comunas['Comuna'] == 'Quilicura Extensión a Total', "Comuna"] = 'Quilicura'
data_comunas.loc[data_comunas['Comuna'] == 'San Bernardo Extensión a Total', "Comuna"] = 'San Bernardo'
data_comunas.loc[data_comunas['Comuna'] == 'Providencia Re-ingreso total', "Comuna"] = 'Providencia'
data_comunas.loc[data_comunas['Comuna'] == 'Melipilla (Área Urbana)', "Comuna"] = 'Melipilla'
data_comunas.loc[data_comunas['Comuna'] == 'Curacaví (Área Urbana)', "Comuna"] = 'Curacaví'
data_comunas.loc[data_comunas['Comuna'] == 'San José de Maipo (Área Urbana)', "Comuna"] = 'San José de Maipo'
data_comunas.loc[data_comunas['Comuna'] == 'TilTil (Área Urbana)', "Comuna"] = 'Tiltil'
data_comunas.loc[data_comunas['Comuna'] == 'Pozo Almonte (Radio Urbano)', "Comuna"] = 'Pozo Almonte'
data_comunas.loc[data_comunas['Comuna'] == 'Peñalolen', "Comuna"] = 'Peñalolén'

resp = requests.get('https://raw.githubusercontent.com/rgcl/geojson-cl/master/comunas.json')
geo_region = json.loads(resp.content)


def cuarentenas_activas(request):


    fig = px.choropleth_mapbox(data_comunas, geojson=geo_region, color="Alcance",
                           locations="Comuna", featureidkey="properties.NOM_COM",
                           center={"lat": -30.0000000, "lon": -71.0000000},
                           mapbox_style="carto-positron", zoom=3,hover_data=["Fecha de Inicio","Fecha de Término"],height=730
                )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})





    data_c =cuarentenas[['Nombre','Alcance','Fecha de Inicio','Fecha de Término']]


    fig2 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]])

    fig2.add_trace(
        go.Table(
            header=dict(
                values=data_c.columns,
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[data_c[k].tolist() for k in data_c.columns],
                align = "left")
        ),
        row=1, col=1
    )
    fig2.update_layout(
        height=800,
        showlegend=False,
        title_text="Tabla de Cuarentenas Chile",
    )


    tabla = fig2.to_html(full_html=False)
    mapa = fig.to_html(full_html=False)


    
    return render(request,"mapa_cuarentenas.html", {"tabla":tabla,"mapa":mapa,"fecha_casos_fall":fecha_casos_fall,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})



