from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render


import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from plotly.subplots import make_subplots



data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]



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
fechas_chile_crec = data_crec_por_dia.columns[-1]
fechas_chile = data_crec_por_dia.loc[:, '2020-03-03': fechas_chile_crec]
fechas_chile = fechas_chile.keys()



def grafico_Update_Dropdown_chile(data_crec_por_dia):
    
    data_crec_por_dia = data_crec_por_dia.fillna(0)


    fecha_casos_totales =data_crec_por_dia.columns
    fecha_casos_totales= fecha_casos_totales[1:]

    # Initialize figure
    fig = go.Figure()
    
    # Add Traces
    casos_totales_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                     "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos nuevos con sintomas'].iloc[0,1:].values})
 
    
    fallecidos_totales_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                          "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos nuevos sin sintomas'].iloc[0,1:].values})
    
    casos_nuevos_totales_df = pd.DataFrame({"fecha": fecha_casos_totales, 
                                          "casos": data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos nuevos totales'].iloc[0,1:].values})

    
    #Casos por dia
    fig.add_trace(
        go.Scatter(x=casos_nuevos_totales_df.fecha,
                   y=casos_nuevos_totales_df.casos,
                   name='Casos Totales',
                   text=casos_nuevos_totales_df.casos,
                   mode='lines+markers',
                   line=dict(color="#2EECEA")))

    #Casos por dia
    fig.add_trace(
        go.Scatter(x=casos_totales_df.fecha,
                   y=casos_totales_df.casos,
                   name='Con Sintomas',
                   text=casos_totales_df.casos,
                   mode='lines+markers',
                   visible=False,
                   line=dict(color="#33CFA5")))

    #activos

    fig.add_trace(
        go.Scatter(x=fallecidos_totales_df.fecha,
                   y=fallecidos_totales_df.casos,
                   name='Sin sintomas',
                   text=fallecidos_totales_df.casos,
                   mode='lines+markers',
                   visible=False,
                  line=dict(color="#1466F4")))
    



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    
                    dict(label="Casos Totales",
                         method="update",
                         args=[{"visible": [True, False,False]},
                               {"title": 'Casos Diarios: Totales',
                                "annotations": []}]),
                    
                    dict(label="Con sintomas",
                         method="update",
                         args=[{"visible": [False, True,False]},
                               {"title":'Casos Diarios: con sintomas',
                                "annotations": []}]),

                    dict(label="Sin sintomas",
                         method="update",
                         args=[{"visible": [False, False,True]},
                               {"title": 'Casos Diarios: sin sintomas',
                                "annotations": []}]),
                    
                    

                

                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text='Casos Diarios')

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

    return fig



def menu(request):

    # Grafico 1:

    fig1 =  grafico_Update_Dropdown_chile(data_crec_por_dia)


    #Grafico4
    data_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos con sintomas'].iloc[0,1:].sum()
    data_sin_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos sin sintomas'].iloc[0,1:].sum()
    data_casos_por_sintomas = pd.DataFrame({'Tipo':['Casos nuevos con sintomas','Casos nuevos sin sintomas'],'Numero de casos':[data_sintomas,data_sin_sintomas]})
    fig4 = px.pie(data_casos_por_sintomas, values='Numero de casos', names='Tipo')
    fig4.update_traces(textposition='inside')
    fig4.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    graph2 = fig1.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)



    return render(request,"principal.html", {"fecha_act":ultima_fecha_cl,"grafico2":graph2,"grafico4":graph4,"num_recuFIS":num_recuFIS,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

