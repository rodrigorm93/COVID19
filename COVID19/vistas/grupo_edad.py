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




grupo_casos_genero= pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
grupo_uci = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
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

#grupos de edad: numero de casos
ultima_fecha_fallecidos = grupo_fallecidos.columns[-1]
fecha_grupo_edad = grupo_casos_genero.columns[-1]
death_cl = grupo_fallecidos.loc[:, '2020-04-09': ultima_fecha_fallecidos]
dates_d = death_cl.keys()

#grupos de edad: numero de casos
fecha_grupo_edad = grupo_casos_genero.columns[-1]
fecha_grupo_fallecidos=grupo_fallecidos.columns[-1]




#FUNCIONES:

def grupos_hosp():   
    
    fig = go.Figure()

    fecha_uci = grupo_uci.columns
    fecha_uci= fecha_uci[-1]
    fecha_uci_evo = grupo_uci.columns[1:]

    m_39 = grupo_uci[grupo_uci['Grupo de edad']=='<=39'].iloc[0,1:]
    m_40_49 = grupo_uci[grupo_uci['Grupo de edad']=='40-49'].iloc[0,1:]
    m_50_59 = grupo_uci[grupo_uci['Grupo de edad']=='50-59'].iloc[0,1:]
    m_60_69 = grupo_uci[grupo_uci['Grupo de edad']=='60-69'].iloc[0,1:]
    m_70 = grupo_uci[grupo_uci['Grupo de edad']=='>=70'].iloc[0,1:]


    fig.add_trace(go.Bar(x=grupo_uci['Grupo de edad'], y=grupo_uci[fecha_uci],
                            name="Pacientes UCI",marker_color='lightsalmon')
                     )
    fig.update_xaxes(title_text="Grupo Edad")
    fig.update_yaxes(title_text="Numero de Casos")

        #Casos por dia
    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_39,
                       name='<=39',
                       visible=False,
                       line=dict(color="#33CFA5")))

    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Número de Casos")

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_40_49,
                       name='40-49',
                       visible=False,
                       line=dict(color="#2A75C4")))

    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Número de Casos")

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_50_59,
                       name='50-59',
                       visible=False,
                       line=dict(color="#2AC44B")))

    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Número de Casos")

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_60_69,
                       name='60-69',
                       visible=False,
                       line=dict(color="#9A2AC4")))

    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Número de Casos")

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_70,
                       name='>=70',
                       visible=False,
                       line=dict(color="#2AAFC4")))

    fig.update_xaxes(title_text="Fecha")
    fig.update_yaxes(title_text="Número de Casos")



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Total Casos",
                         method="update",
                         args=[{"visible": [True, False, False, False,False,False]},
                               {"title": "Total Casos",
                                "annotations": []}]),
                    dict(label="<=39",
                         method="update",
                         args=[{"visible": [False, True, False, False,False,False]},
                               {"title": "Evolución de Casos <=39",
                                "annotations": []}]),
                    dict(label="40-49",
                         method="update",
                         args=[{"visible": [False, False, True, False,False,False]},
                               {"title": "Evolución de Casos 40-49",
                                "annotations": []}]),
                    dict(label="50-59",
                         method="update",
                         args=[{"visible": [False, False, False, True,False,False]},
                               {"title": "Evolución de Casos 50-59",
                                "annotations": []}]),
                    dict(label="60-69",
                         method="update",
                         args=[{"visible": [False, False, False, False,True,False]},
                               {"title": "Evolución de Casos 60-69",
                                "annotations": []}]),
                    dict(label=">=70",
                         method="update",
                         args=[{"visible": [False, False, False, False,False,True]},
                               {"title": "Evolución de Casos >=70",
                                "annotations": []}]),
                      dict(label="Comparacion",
                         method="update",
                         args=[{"visible": [False, True, True, True,True,True]},
                               {"title": "Evolución de Casos Comparacion",
                                "annotations": []}]),
                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text="Total Casos")

    return fig


def grupos_fallecidos():   
    
    fig = go.Figure()

    fecha_ul = grupo_fallecidos.columns[-1]
    fecha_uci_evo = grupo_fallecidos.columns[1:]

    m_39 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='<=39'].iloc[0,1:]
    m_40_49 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='40-49'].iloc[0,1:]
    m_50_59 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='50-59'].iloc[0,1:]
    m_60_69 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='60-69'].iloc[0,1:]
    m_70 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='70-79'].iloc[0,1:]
    m_80_89 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='80-89'].iloc[0,1:]
    m_90 = grupo_fallecidos[grupo_fallecidos['Grupo de edad']=='>=90'].iloc[0,1:]



    titulo ='Fallecidos por grupo de edad Fecha: '+fecha_ul


    fig = px.bar(grupo_fallecidos.sort_values(fecha_ul),
                    x='Grupo de edad', y=fecha_ul,
                    title=titulo,
                    text=fecha_ul 
                    )
      
    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_39,
                       name='<=39',
                       visible=False,
                       line=dict(color="#33CFA5")))



    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_40_49,
                       name='40-49',
                       visible=False,
                       line=dict(color="#2A75C4")))

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_50_59,
                       name='50-59',
                       visible=False,
                       line=dict(color="#2AC44B")))


    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_60_69,
                       name='60-69',
                       visible=False,
                       line=dict(color="#9A2AC4")))

 

    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_70,
                       name='70-79',
                       visible=False,
                       line=dict(color="#2AAFC4")))

    
    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_80_89,
                       name='80-89',
                       visible=False,
                       line=dict(color="#4C1C40")))

 
    
    fig.add_trace(go.Scatter(x=fecha_uci_evo,
                       y=m_90,
                       name='>=90',
                       visible=False,
                       line=dict(color="#CF676B")))

 


    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Total Fallecidos",
                         method="update",
                         args=[{"visible": [True, False, False, False,False,False,False,False]},
                               {"title": "Total Casos",
                                "annotations": []}]),
                    dict(label="<=39",
                         method="update",
                         args=[{"visible": [False, True, False, False,False,False,False,False]},
                               {"title": "Evolución de Casos <=39",
                                "annotations": []}]),
                    dict(label="40-49",
                         method="update",
                         args=[{"visible": [False, False, True, False,False,False,False,False]},
                               {"title": "Evolución de Casos 40-49",
                                "annotations": []}]),
                    dict(label="50-59",
                         method="update",
                         args=[{"visible": [False, False, False, True,False,False,False,False]},
                               {"title": "Evolución de Casos 50-59",
                                "annotations": []}]),
                    dict(label="60-69",
                         method="update",
                         args=[{"visible": [False, False, False, False,True,False,False,False]},
                               {"title": "Evolución de Casos 60-69",
                                "annotations": []}]),
                    dict(label="70-79",
                         method="update",
                         args=[{"visible": [False, False, False, False,False,True,False,False]},
                               {"title": "Evolución de Casos >=70",
                                "annotations": []}]),
                    dict(label="80-89",
                         method="update",
                         args=[{"visible": [False, False, False, False,False,False,True,False]},
                               {"title": "Evolución de Casos 80-89",
                                "annotations": []}]),
                    dict(label=">=90",
                         method="update",
                         args=[{"visible": [False, False, False, False,False,False,False,True]},
                               {"title": "Evolución de Casos >=90",
                                "annotations": []}]),
                    
                      dict(label="Comparacion",
                         method="update",
                         args=[{"visible": [False, True, True, True,True,True,True,True]},
                               {"title": "Comparacion",
                                "annotations": []}]),
                    
                    
                    
                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text="Total Fallecidos")

    return fig


def busqueda_fallecidos_por_grupo(request):

 

    fig = grupos_fallecidos()

    graph1 = fig.to_html(full_html=False)

    #Grafico 2

    trace1 = go.Pie(
                labels=grupo_fallecidos['Grupo de edad'],
                values=grupo_fallecidos[fecha_grupo_fallecidos],
                hoverinfo='label+percent', 
                textfont_size=12,
                marker=dict(line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de personas fallecidas : '+fecha_grupo_fallecidos+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)

    graph2 = fig2.to_html(full_html=False)



    return render(request,"fallecidos_grupo.html", {"grafico1":graph1,"grafico2":graph2,"num_recuFIS":num_recuFIS,"fecha_casos":fecha_casos,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})


def busqueda_por_grupo_edad(request):


    if request.GET['edad']:

        grupo_edad = request.GET['edad']

        fallecidos_por_grupo = []


        for i in dates_d :
            f_j = grupo_fallecidos[grupo_fallecidos['Grupo de edad']==grupo_edad][i].sum()
            fallecidos_por_grupo.append(f_j)


        data_fallecidos = pd.DataFrame({'Tipo':['Edad Seleccionada','Total'],'Fallecidos': [grupo_fallecidos[grupo_fallecidos['Grupo de edad']==grupo_edad][fecha_grupo_fallecidos].sum(),grupo_fallecidos[fecha_grupo_fallecidos].sum()]})

        fig2 = make_subplots(rows=1, cols=2)

        trace1 = go.Pie(
                        labels=data_fallecidos['Tipo'],
                        values=data_fallecidos['Fallecidos'],
                        hoverinfo='label+percent', 
                        textfont_size=12,
                        marker=dict(line=dict(color='#000000', width=2)))
        layout = go.Layout(title_text = '<b>Porcentajes de Fallecidos : '+fecha_grupo_fallecidos+'</b>',
                        font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
        fig2 = go.Figure(data = [trace1], layout = layout)


        trace = go.Scatter(
                x=grupo_fallecidos.iloc[:,1:].columns,
                y=fallecidos_por_grupo,
                name="Pacientes Criticos",
                mode='lines+markers',
                line_color='red')

        layout = go.Layout(template="ggplot2",title_text = '<b>Numero Fallecidos '+ grupo_edad +' :'+ fecha_grupo_fallecidos+'</b>',
                            font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
        fig = go.Figure(data = [trace], layout = layout)

        graph1 = fig.to_html(full_html=False)
        graph2 = fig2.to_html(full_html=False)


        return render(request,"grupo_edad_f.html", {"grafico1":graph1,"grafico2":graph2,"n_casos":num_cases_cl,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

    else:
        mensaje='ERROR'
        return HttpResponse(mensaje)

def busqueda_hosp_por_grupo(request):

    #GRAFICO 1
    fig = grupos_hosp()

    #Grafico 2

    colors = ['gold', 'darkorange', 'crimson','mediumturquoise', 'sandybrown', 'grey',  'lightgreen','navy','deeppink','purple']
    
    
    ultima_fecha_cl = grupo_uci.columns[-1]
    fig2 = px.pie(grupo_uci, values=ultima_fecha_cl, names='Grupo de edad')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)

    fecha_uci = grupo_uci.columns
    fecha_uci= fecha_uci[-1]


    return render(request,"hospitalizaciones_grupo_edad.html", {"grafico1":graph1,"fecha_uci":fecha_uci,"grafico2":graph2,"num_recuFIS":num_recuFIS,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})
