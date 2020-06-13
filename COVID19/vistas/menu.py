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



data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')


ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]




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

#ver el caso de que no se actualicen los registros


casos_act = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()
#dejar el ulktimo registro de recuperados que fue el 2020-06-02

n_c = int(num_cases_cl)
n_d = int(num_death)
n_ca = int(casos_act)

num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'
casos_act = str(int(casos_act))+' ('+ultima_fecha_cl_r+')'

fecha_casos_fall='('+data_chile.columns[-1]+')'

#********************************************************************
fechas_chile_crec = data_crec_por_dia.columns[-1]
fechas_chile = data_crec_por_dia.loc[:, '2020-03-03': fechas_chile_crec]
fechas_chile = fechas_chile.keys()


def menu(request):

    # Grafico 1:


    casos_por_dia_totales = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos nuevos totales'].iloc[0,1:]
    
    fig2=go.Figure()
    fig2.add_trace(go.Scatter(x=fechas_chile, y=casos_por_dia_totales,mode='lines+markers',
                        name='Número Casos'))
    #fig2.add_trace(go.Scatter(x=fechas_chile, y=fallecidos_por_dia,mode='lines+markers',
                        #name='Falllecidos'))
    fig2.update_layout(title="Numero de Casos por Día",
                    xaxis_title="Date",yaxis_title="Número casos",legend=dict(x=0,y=1,traceorder="normal"))


    
    ultima_fecha = ultima_fecha_cl

    #Grafico4
    data_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos con sintomas'].iloc[0,1:].sum()
    data_sin_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos sin sintomas'].iloc[0,1:].sum()
    data_casos_por_sintomas = pd.DataFrame({'Tipo':['Casos nuevos con sintomas','Casos nuevos sin sintomas'],'Numero de casos':[data_sintomas,data_sin_sintomas]})
    fig4 = px.pie(data_casos_por_sintomas, values='Numero de casos', names='Tipo')
    fig4.update_traces(textposition='inside')
    fig4.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    graph2 = fig2.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)





    return render(request,"principal.html", {"fecha_casos_fall":fecha_casos_fall,"fecha_act":ultima_fecha,"grafico2":graph2,"grafico4":graph4,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

