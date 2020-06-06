
from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render


import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
num_vent = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores.csv')





ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)


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



#VENTILADORES


dates_vent = num_vent.loc[:, '2020-04-14': ultima_fecha_cl]
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
                name="Ventiladores Disponibles",
                mode='lines+markers',
                line_color='green')
    trace2 = go.Scatter(
                    x=dates_vent,
                    y=ventiladores_oc,
                    name="Ventiladores Ocupados",
                    mode='lines+markers',
                    line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Numero de Ventiladores Fecha: '+ ultima_fecha_cl+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace,trace2], layout = layout)

    ventiladiores = num_vent.drop([0],axis=0)
    #GRAFICO 2
    fig2 = make_subplots(rows=1, cols=2)
    colors = ['green','red']
    trace1 = go.Pie(
                    labels=ventiladiores['Ventiladores'],
                    values=ventiladiores[ultima_fecha_cl],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                    marker=dict(colors=colors, 
                                line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de ventiladores Fecha: '+ultima_fecha_cl+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)


    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)



    return render(request,"numero_ventiladores.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})



def pacientes_ventiladores(request):

    #GRAFICO 1
 
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_vmi, name='Pacientes VMI'))
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_no_vmi, name='Pacientes no VM'))
    fig1.add_trace(go.Scatter(x=fecha_vmi_pacientes, y=pc_vmi_noinv, name='Pacientes VM no invasiva'))


    fig1.layout.update(title_text='Pacientes Hospitalizados en UCI con Ventilación Mecánica',xaxis_showgrid=False, yaxis_showgrid=False,
                    font=dict(
                size=15,
                color="Black"    
            ))
    fig1.layout.plot_bgcolor = 'White'
    fig1.layout.paper_bgcolor = 'White'

    fig2 = px.pie(data_vmi, values='Cantidad', names='Tipo')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')

    graph1 = fig1.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)



    return render(request,"pacientes_vmi.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
