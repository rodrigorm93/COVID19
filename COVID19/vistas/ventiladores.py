
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

import warnings

warnings.filterwarnings('ignore')

data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
num_vent = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


ultima_fecha_cl_vt = num_vent.columns
ultima_fecha_cl_vt= ultima_fecha_cl_vt[-1]


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


#VENTILADORES

ult_vent=num_vent.columns[-1]

dates_vent = num_vent.loc[:, '2020-04-14': ult_vent]
dates_vent = dates_vent.keys()

ventiladores_oc =[]
ventiladores_dis = []
ventiladores_total = []
for i in dates_vent:
    oc = num_vent[num_vent['Ventiladores']=='ocupados'][i].sum()
    dis = num_vent[num_vent['Ventiladores']=='disponibles'][i].sum()
    total = num_vent[num_vent['Ventiladores']=='total'][i].sum()

    ventiladores_oc.append(oc)
    ventiladores_dis.append(dis)
    ventiladores_total.append(total)


pacientes_ventiladores = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto30/PacientesVMI.csv')
pacientes_ventiladores = pacientes_ventiladores.fillna(0)

pc_vmi = pacientes_ventiladores[pacientes_ventiladores['Casos']=='Pacientes VMI'].iloc[0,1:].values
pc_no_vmi = pacientes_ventiladores[pacientes_ventiladores['Casos']=='Pacientes no VM'].iloc[0,1:].values
pc_vmi_noinv = pacientes_ventiladores[pacientes_ventiladores['Casos']=='Pacientes VM no invasiva'].iloc[0,1:].values

fecha_vmi_pacientes = pacientes_ventiladores.columns[-1]
fecha_vmi_pacientes = pacientes_ventiladores.loc[:, '2020-04-11': fecha_vmi_pacientes]
fecha_vmi_pacientes = fecha_vmi_pacientes.keys()

data_vmi = pd.DataFrame({'Tipo':['Pacientes VMI','Pacientes no VM','Pacientes VM no invasiva'],'Cantidad': [pc_vmi[-1],pc_no_vmi[-1],pc_vmi_noinv[-1]]})




def num_ventiladores(request):


   

    #GRAFICO 1
    trace = go.Scatter(
                x=dates_vent,
                y=ventiladores_dis,
                text=ventiladores_dis,
                name="Disponibles",
                mode='lines+markers',
                line_color='green')
    trace2 = go.Scatter(
                    x=dates_vent,
                    y=ventiladores_oc,
                    name="Ocupados",
                    text=ventiladores_oc,
                    mode='lines+markers',
                    line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Numero de Ventiladores Fecha: '+ ult_vent+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace,trace2], layout = layout)

      # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 8},
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

    ventiladiores = num_vent.drop([0],axis=0)
    #GRAFICO 2
    fig2 = make_subplots(rows=1, cols=2)
    colors = ['green','red']
    trace1 = go.Pie(
                    labels=ventiladiores['Ventiladores'],
                    values=ventiladiores[ult_vent],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                    marker=dict(colors=colors, 
                                line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de ventiladores Fecha: '+ult_vent+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)


    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)

    num_vent_total = num_vent[num_vent['Ventiladores']=='total'][ultima_fecha_cl_vt].sum()
    num_vent_total = int_format(int(num_vent_total))

    num_vent_total_oc = num_vent[num_vent['Ventiladores']=='ocupados'][ultima_fecha_cl_vt].sum()
    num_vent_total_oc = int_format(int(num_vent_total_oc))


    num_vent_total_disp = num_vent[num_vent['Ventiladores']=='disponibles'][ultima_fecha_cl_vt].sum()
    num_vent_total_disp = int_format(int(num_vent_total_disp))

    fecha_casos_fall='('+ultima_fecha_cl_vt+')'


    return render(request,"numero_ventiladores.html", {"num_vent":num_vent_total_oc,"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_vent_total,"num_rec":num_vent_total_disp})



def pacientes_ventiladores_fun(request):

    #GRAFICO 1
 
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_vmi,text=pc_vmi, name='VMI'))
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_no_vmi,text=pc_no_vmi, name='No VM'))
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_vmi_noinv,text=pc_vmi_noinv, name='VM no invasiva'))


    fig1.layout.update(title_text='Pacientes Hospitalizados en UCI con Ventilación Mecánica',xaxis_showgrid=False, yaxis_showgrid=False,
                    font=dict(
                size=15,
                color="Black"    
            ))
    fig1.layout.plot_bgcolor = 'White'
    fig1.layout.paper_bgcolor = 'White'

          # style all the traces
    fig1.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.8},
        marker={"size": 8},
        mode="lines",
        showlegend=False
    )




    # Update layout
    fig1.update_layout(
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


    #GRAFICO 2
    fig2 = px.pie(data_vmi, values='Cantidad', names='Tipo')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')

    ultima_fecha_vmi = fecha_vmi_pacientes[-1]

    num_vmi = pc_vmi[-1]
    num_vmi_no = pc_no_vmi[-1]
    num_vmi_no_inv = pc_vmi_noinv[-1]

    num_vmi = int_format(int(num_vmi))
    num_vmi_no = int_format(int(num_vmi_no))
    num_vmi_no_inv = int_format(int(num_vmi_no_inv))

    fecha_casos_vmi = ' ('+ultima_fecha_vmi+')'

    graph1 = fig1.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)



    return render(request,"pacientes_vmi.html", {"grafico1":graph1,"fecha_casos_vmi":fecha_casos_vmi,"grafico2":graph2,"num_vmi":num_vmi,"num_vmi_no":num_vmi_no, "num_vmi_no_inv":num_vmi_no_inv})
