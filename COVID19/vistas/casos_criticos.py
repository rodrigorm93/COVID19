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
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


#***************************MENU**************************************

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


def casos_criticos(request):


    ultima_fecha_cl = pacientes_criticos.columns[-1]
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
        #height=450,
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
        #height=450,
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



    return render(request,"numero_casos_criticos.html", {"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"grafico2":graph2,"num_recuFIS":num_recuFIS,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

