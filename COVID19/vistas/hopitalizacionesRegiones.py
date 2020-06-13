
from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render



import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from plotly.subplots import make_subplots

import warnings



fallecidos_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_T.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
casos_diarios_por_regionT = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv')

data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
grupo_uci_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
tipo_cama = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario.csv')


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
def busqueda_hospitalizacion_region(request):




    titulo = 'Numero de personas Hospitalizadas en UCI por Región '+ultima_fecha_cl
    fig = px.bar(grupo_uci_reg.sort_values(ultima_fecha_cl), 
             x=ultima_fecha_cl, y="Region", 
             title=titulo,
              text=ultima_fecha_cl, 
             orientation='h',height=700)
    fig.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')
    fig.update_yaxes(title_text="Regiones")
    fig.update_xaxes(title_text='Número de personas Hospitalizadas')

    fig.update_layout(template = 'plotly_white')

    total_pac_uci = grupo_uci_reg[ultima_fecha_cl].sum()

    total_pac_uci = str(int(total_pac_uci))+' ('+ultima_fecha_cl_r+')'


    #GRAFICO 2

    trace1 = go.Pie(
                labels=grupo_uci_reg['Region'],
                values=grupo_uci_reg[ultima_fecha_cl],
                hoverinfo='label+percent', 
                textfont_size=12,
                marker=dict(line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de personas Hospitalizadas por Región </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)


   

    #GRAFICO 3

    fecha_tpc = tipo_cama.columns[-1]

    titulo ='Número de pacientes hospitalizados según el tipo de cama.: '+fecha_tpc

    fig3 = px.bar(x=tipo_cama['Tipo de cama'], y=tipo_cama[fecha_tpc],
            title=titulo,
           text=tipo_cama[fecha_tpc]
            
        )
    fig3.update_xaxes(title_text="Tipo de Cama")
    fig3.update_yaxes(title_text="Numero de Casos")


    #Garfico4

    fig4 = make_subplots(rows=1, cols=2)
    trace1 = go.Pie(
                    labels=tipo_cama['Tipo de cama'],
                    values=tipo_cama[fecha_tpc],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de pacientes Hosp. según el tipo de cama </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig4 = go.Figure(data = [trace1], layout = layout)

    
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)


    return render(request,"hospitalizaciones_region.html", {"total_pac_uci":total_pac_uci,"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})
