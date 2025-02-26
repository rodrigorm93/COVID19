from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render
import os

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import requests
import json

from datetime import date
import datetime
from statsmodels.tsa.api import Holt,SimpleExpSmoothing,ExponentialSmoothing
#import plotly.figure_factory as ff
from plotly.subplots import make_subplots


import warnings

warnings.filterwarnings('ignore')



now = date.today()


total_fallecimientos_mes = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Total-Defunciones/total_fallecimientos_mes.csv', sep=',')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')


seasonal_periods_casos = 6



ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

confirmed_chile = data_chile.loc[:, '2020-03-03': ultima_fecha_cl]
dates_chile = confirmed_chile.keys()
days_chile = np.array([i for i in range(len(dates_chile))]).reshape(-1, 1)

casos_chile = []

for i in dates_chile:
   
    casos_chile.append(data_chile[i].iloc[16])


#funcion 


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



año_2010 =[]
año_2011 =[]
año_2012 =[]
año_2013 =[]
año_2014 =[]
año_2015 =[]
año_2016 =[]
año_2017 =[]
año_2018 =[]
año_2019 =[]
año_2020 =[]

registros_meses = ['January','February','March','April','May','June','July','August','September','October','November','December']

for i in registros_meses:
    reg_año_2010 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2010][i].sum()
    reg_año_2011 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2011][i].sum()
    reg_año_2012 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2012][i].sum()
    reg_año_2013 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2013][i].sum()
    reg_año_2014 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2014][i].sum()
    reg_año_2015 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2015][i].sum()
    reg_año_2016 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2016][i].sum()
    reg_año_2017 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2017][i].sum()
    reg_año_2018 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2018][i].sum()
    reg_año_2019 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2019][i].sum()
    reg_año_2020 = total_fallecimientos_mes[total_fallecimientos_mes['Años']==2020][i].sum()

    año_2010.append(reg_año_2010)
    año_2011.append(reg_año_2011)
    año_2012.append(reg_año_2012)
    año_2013.append(reg_año_2013)
    año_2014.append(reg_año_2014)
    año_2015.append(reg_año_2015)
    año_2016.append(reg_año_2016)
    año_2017.append(reg_año_2017)
    año_2018.append(reg_año_2018)
    año_2019.append(reg_año_2019)
    año_2020.append(reg_año_2020)


def total_defunciones_chile(request):

    trace = go.Scatter(
                    x=registros_meses,
                    y=año_2010,
                    name="2010",
                    text=año_2010,
                    mode='lines+markers',
                    line_color='#800080')
    trace2 = go.Scatter(
                    x=registros_meses,
                    y=año_2011,
                    name="2011",
                    text=año_2011,
                    mode='lines+markers',
                    line_color='green')
    trace3 = go.Scatter(
                    x=registros_meses,
                    y=año_2012,
                    name="2012",
                    text=año_2012,
                    mode='lines+markers',
                    line_color='#000080')
    trace4 = go.Scatter(
                    x=registros_meses,
                    y=año_2013,
                    name="2013",
                    text=año_2013,
                    mode='lines+markers',
                    line_color='#00FFFF')
    trace5 = go.Scatter(
                    x=registros_meses,
                    y=año_2014,
                    name="2014",
                    text=año_2014,
                    mode='lines+markers',
                    line_color='#EAAC38')
    trace6 = go.Scatter(
                    x=registros_meses,
                    y=año_2015,
                    name="2015",
                    text=año_2015,
                    mode='lines+markers',
                    line_color='#000000')
    trace7 = go.Scatter(
                    x=registros_meses,
                    y=año_2016,
                    name="2016",
                    text=año_2016,
                    mode='lines+markers',
                    line_color='#808080')
    trace8 = go.Scatter(
                    x=registros_meses,
                    y=año_2017,
                    name="2017",
                    text=año_2017,
                    mode='lines+markers',
                    line_color='#008080')
    trace9 = go.Scatter(
                    x=registros_meses,
                    y=año_2018,
                    name="2018",
                    text=año_2018,
                    mode='lines+markers',
                    line_color='#00FF00')
    trace10 = go.Scatter(
                    x=registros_meses,
                    y=año_2019,
                    name="2019",
                    text=año_2019,
                    mode='lines+markers',
                    line_color='#800000')
    trace11 = go.Scatter(
                    x=registros_meses,
                    y=año_2020,
                    name="2020",
                    text=año_2020,
                    mode='lines+markers',
                    line_color='red')


    layout = go.Layout(template="ggplot2",title_text = '<b>Numero de Defunciones  entre 2010- '+str(now)+' </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11], layout = layout)
    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 5},
        mode="lines+markers",
        #showlegend=False
    )

    # Update layout
    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        #legend=dict(traceorder="reversed"),
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )

    graph1 = fig.to_html(full_html=False)

    suma_4meses = total_fallecimientos_mes
    col_list= ['January','February','March','April','May']
    suma_4meses['Total 4 Meses'] = suma_4meses[col_list].sum(axis=1)

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=registros_meses,
        y=año_2017,
        name="2017",
        yaxis="y",
        text=año_2017
    ))

    # Add traces
    fig2.add_trace(go.Scatter(
        x=registros_meses,
        y=año_2018,
        name="2018",
        yaxis="y",
        text=año_2018
    ))

    fig2.add_trace(go.Scatter(
        x=registros_meses,
        y=año_2019,
        name="2019",
        yaxis="y",
         text=año_2019
    ))
    fig2.add_trace(go.Scatter(
        x=registros_meses,
        y=año_2020,
        name="2020",
        yaxis="y",
        text=año_2020
    ))

    # style all the traces
    fig2.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 7},
        mode="lines+markers",
        #showlegend=False
    )
    # Update layout
    fig2.update_layout(
        dragmode="zoom",
        hovermode="x",
        #legend=dict(traceorder="reversed"),
        #height=600,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )

    total_fallecimientos_mes_trans = total_fallecimientos_mes.drop(['Total 4 Meses'], axis=1).T
    #tabla1 = total_fallecimientos_mes_trans.to_html()

    fig5 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]])

    fig5.add_trace(
        go.Table(
            header=dict(
                values=total_fallecimientos_mes_trans.columns,
                font=dict(size=15),
                align="left"
            ),
            cells=dict(
                values=[total_fallecimientos_mes_trans[k].tolist() for k in total_fallecimientos_mes_trans.columns],
                align = "left",font=dict(size=13))
        ),
        row=1, col=1
    )
    fig5.update_layout(
        showlegend=False,
        title_text="Tabla de Defunsiones"
    )

    #tabla1 = ff.create_table(total_fallecimientos_mes_trans,height_constant=20)


    #GRAFICO 3
    suma_4meses = total_fallecimientos_mes
    col_list= ['January','February','March','April','May','June']
    suma_4meses['Total 5 Meses'] = suma_4meses[col_list].sum(axis=1)
    data_ord = suma_4meses.sort_values('Total 4 Meses').reset_index()
    data_ord = data_ord.drop(['index'], axis=1)
    #total 4 primero meses
    fig3 = px.bar(data_ord, x='Años', y='Total 5 Meses',
             hover_data=['Total 5 Meses'], color='Total 5 Meses',
             labels={'pop':'population of Canada'}, height=500)

    graph2 = fig2.to_html(full_html=False)
    graph3= fig3.to_html(full_html=False)

    tabla1 = fig5.to_html(full_html=False)

    return render(request,"numero_defunciones_chile.html", {"grafico3":graph3,"grafico1":graph1,"grafico2":graph2,"tabla1":tabla1,"num_recuFIS":num_recuFIS,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

def modelo_predictivo(request):
    
   
    
    days_chile2 = np.array([i for i in range(len(dates_chile))])

    datewise = pd.DataFrame({'Days Since': list(days_chile2), 'Confirmed':casos_chile})



    '''
    es=ExponentialSmoothing(np.asarray(datewise['Confirmed']),seasonal_periods=seasonal_periods_casos,trend='add', seasonal='mul').fit()

    days_in_future_cl = 20
    future_forcast_cl = np.array([i for i in range(len(dates_chile)+days_in_future_cl)]).reshape(-1, 1)
    adjusted_dates_cl = future_forcast_cl[:-days_in_future_cl]
    start_cl = '03/03/2020'
    start_date_cl = datetime.datetime.strptime(start_cl, '%m/%d/%Y')
    future_forcast_dates_cl = []
    for i in range(len(future_forcast_cl)):
        future_forcast_dates_cl.append((start_date_cl + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))
        
    Predict_df_cl_1= pd.DataFrame()
    Predict_df_cl_1["Fecha"] = list(future_forcast_dates_cl[-days_in_future_cl:])
    Predict_df_cl_1["N° Casos"] =np.round(list(es.forecast(20)))
    '''

    Predict_df_cl_1 = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Predicciones/Predict_df_cl_1.csv')


    fechas_chile_crec = data_crec_por_dia.columns[-1]
    fechas_chile = data_crec_por_dia.loc[:, '2020-03-03': fechas_chile_crec]
    fechas_chile = fechas_chile.keys()

    fecha_chile_df = []
    future_f = np.array([i for i in range(len(fechas_chile))]).reshape(-1, 1)
    start_cl = '03/03/2020'
    start_date_cl = datetime.datetime.strptime(start_cl, '%m/%d/%Y')

    for i in range(len(future_f)):
        fecha_chile_df.append((start_date_cl + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))
            

    data_chile = pd.DataFrame({'Fecha': fecha_chile_df, 'Confirmed':casos_chile})

       
    fig=go.Figure()
    #fig.add_trace(go.Scatter(x=np.array(future_forcast_dates_cl), y=datewise["Confirmed"], mode='lines+markers',name="Casos Reales",text=datewise["Confirmed"]))
    fig.add_trace(go.Scatter(x=data_chile['Fecha'], y=data_chile["Confirmed"],
                        mode='lines+markers',name="Casos Reales",text=datewise["Confirmed"]))
    fig.add_trace(go.Scatter(x=Predict_df_cl_1['Fecha'], y=Predict_df_cl_1["N° Casos"],
                        mode='lines+markers',name="Predicción",text=Predict_df_cl_1["N° Casos"]))

    fig.update_layout(title="Proyección de casos en 20 días",
                    xaxis_title="Fecha",yaxis_title="Número de Casos",legend=dict(x=0,y=1,traceorder="normal"))


      # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 4},
        mode="lines+markers",
        #showlegend=False
    )




    # Update layout
    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        #legend=dict(traceorder="reversed"),
        #height=500,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )                     

    graph1 = fig.to_html(full_html=False)



    fig2 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]])

    fig2.add_trace(
        go.Table(
            header=dict(
                values=Predict_df_cl_1.columns,
                font=dict(size=15),
                align="left"
            ),
            cells=dict(
                values=[Predict_df_cl_1[k].tolist() for k in Predict_df_cl_1.columns],
                align = "left",font=dict(size=13))
        ),
        row=1, col=1
    )
    fig2.update_layout(
        showlegend=False,
        title_text="Tabla de Proyecciones a 20 días",
    )



    
    graph2 = fig2.to_html(full_html=False)

    return render(request,"predicciones.html", {"grafico1":graph1,"tabla1":graph2,"num_recuFIS":num_recuFIS,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})




def modelo_predictivo_fall(request):
    
   
    
    days_chile2 = np.array([i for i in range(len(dates_chile))])

    datewise = pd.DataFrame({'Days Since': list(days_chile2), 'Confirmed':casos_chile})

    es=ExponentialSmoothing(np.asarray(datewise['Confirmed']),seasonal_periods=seasonal_periods_casos,trend='add', seasonal='mul').fit()

    days_in_future_cl = 20
    future_forcast_cl = np.array([i for i in range(len(dates_chile)+days_in_future_cl)]).reshape(-1, 1)
    adjusted_dates_cl = future_forcast_cl[:-days_in_future_cl]
    start_cl = '03/03/2020'
    start_date_cl = datetime.datetime.strptime(start_cl, '%m/%d/%Y')
    future_forcast_dates_cl = []
    for i in range(len(future_forcast_cl)):
        future_forcast_dates_cl.append((start_date_cl + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))
        
    Predict_df_cl_1= pd.DataFrame()
    Predict_df_cl_1["Fecha"] = list(future_forcast_dates_cl[-days_in_future_cl:])
    Predict_df_cl_1["N° Casos"] =np.round(list(es.forecast(20)))

       
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=np.array(future_forcast_dates_cl), y=datewise["Confirmed"],
                        mode='lines+markers',name="Casos Reales"))
    fig.add_trace(go.Scatter(x=Predict_df_cl_1['Fecha'], y=Predict_df_cl_1["N° Casos"],
                        mode='lines+markers',name="Predicción",))

    fig.update_layout(title="Proyección de casos en 20 días",
                    xaxis_title="Fecha",yaxis_title="Número de Casos",legend=dict(x=0,y=1,traceorder="normal"))


    
             

    graph1 = fig.to_html(full_html=False)




    fig2 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]])

    fig2.add_trace(
        go.Table(
            header=dict(
                values=Predict_df_cl_1.columns,
                font=dict(size=15),
                align="left"
            ),
            cells=dict(
                values=[Predict_df_cl_1[k].tolist() for k in Predict_df_cl_1.columns],
                align = "left",font=dict(size=13))
        ),
        row=1, col=1
    )
    fig2.update_layout(
        showlegend=False,
        title_text="Tabla de Proyecciones a 20 días",
    )



    
    graph2 = fig2.to_html(full_html=False)

    return render(request,"predicciones_fallecidos.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"tabla1":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

