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
pacientes_criticos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')

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


def casos_criticos(request):



    #GRAFICO 1
    trace = go.Scatter(
                x=pacientes_criticos.iloc[:,1:].columns,
                y=pacientes_criticos.iloc[0,1:],
                name="P. Criticos",
                text=pacientes_criticos.iloc[0,1:],
                mode='lines+markers',
                line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Número de Pacientes Criticos Fecha: '+ ultima_fecha_cl+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace], layout = layout)

      # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 5},
        mode="lines+markers",
        showlegend=False
    )




    # Update layout
    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=450,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
        )


    data_activos = data_chile_r[data_chile_r['Fecha']=='Casos activos']
    ultima_fecha = data_activos.columns
    ultima_fecha= ultima_fecha[-1]

    trace = go.Scatter(
                x=data_activos.iloc[:,1:].columns,
                y=data_activos.iloc[0,1:],
                name="P. Activos",
                text=data_activos.iloc[0,1:],
                mode='lines+markers',
                line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Número de Pacientes Activos Fecha: '+ ultima_fecha+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace], layout = layout)

      # style all the traces
    fig2.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 5},
        mode="lines+markers",
        showlegend=False
    )




    # Update layout
    fig2.update_layout(
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=450,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
        )


    fig3=px.bar(x=data_activos.iloc[:,1:].columns,y=data_activos.iloc[0,1:])
    fig3.update_layout(title="Distribución del número de Casos Activos",
                    xaxis_title="Fecha",yaxis_title="Numero de Casos",)


    pacientes_ventiladores = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto30/PacientesVMI.csv')
    pacientes_ventiladores = pacientes_ventiladores.fillna(0)

    pc_vmi = pacientes_ventiladores[pacientes_ventiladores['Casos']=='Pacientes VMI'].iloc[0,1:].values

    data_vmi_criticos = pd.DataFrame({'Tipo':['Pacientes VMI','Pacientes criticos'],'Cantidad': [pc_vmi[-1],int(pacientes_criticos['2020-06-23'].values)]})

    fig4 = px.pie(data_vmi_criticos, values='Cantidad', names='Tipo')
    fig4.update_traces(textposition='inside')
    fig4.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)


    #graph2 = fig2.to_html(full_html=False)



    return render(request,"numero_casos_criticos.html", {"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

