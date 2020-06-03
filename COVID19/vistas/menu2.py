from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render
import os

import numpy as np
import pandas as pd
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error,mean_squared_error
import plotly.graph_objs as go
import datetime
import plotly.express as px
import folium
import warnings
import folium 
from folium import plugins
from math import sqrt
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots

from datetime import date

from joblib import dump, load

from statsmodels.tsa.api import Holt,SimpleExpSmoothing,ExponentialSmoothing

now = date.today()


total_fallecimientos_mes = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Total-Defunciones%202010-2020/total_fallecimientos_mes.csv', sep=',')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')


ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

confirmed_chile = data_chile.loc[:, '2020-03-03': ultima_fecha_cl]
dates_chile = confirmed_chile.keys()
days_chile = np.array([i for i in range(len(dates_chile))]).reshape(-1, 1)

casos_chile = []

for i in dates_chile:
   
    casos_chile.append(data_chile[i].iloc[16])



#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

#ver el caso de que no se actualicen los registros


num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()
num_death =  grupo_fallecidos[ultima_fecha_cl].sum()
num_rec = data_chile_r.iloc[2,-1].sum()
num_rec = int(num_rec)

estado_r='Act'+ultima_fecha_cl
estado_f='Act'+ultima_fecha_cl
estado_a='Act'+ultima_fecha_cl

if (num_rec==0):
    num_rec = data_chile_r.iloc[2,len(data_chile_r.columns)-2].sum()
    fecha = data_chile_r.columns[-2]
    estado_r='NoAct('+data_chile_r.columns[-2]+')'

num_cases_cl = int(num_cases_cl)
num_rec = int(num_rec)
num_death = int(num_death)



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
                    mode='lines+markers',
                    line_color='#800080')
    trace2 = go.Scatter(
                    x=registros_meses,
                    y=año_2011,
                    name="2011",
                    mode='lines+markers',
                    line_color='green')
    trace3 = go.Scatter(
                    x=registros_meses,
                    y=año_2012,
                    name="2012",
                    mode='lines+markers',
                    line_color='#000080')
    trace4 = go.Scatter(
                    x=registros_meses,
                    y=año_2013,
                    name="2013",
                    mode='lines+markers',
                    line_color='#00FFFF')
    trace5 = go.Scatter(
                    x=registros_meses,
                    y=año_2014,
                    name="2014",
                    mode='lines+markers',
                    line_color='#FFFF00')
    trace6 = go.Scatter(
                    x=registros_meses,
                    y=año_2015,
                    name="2015",
                    mode='lines+markers',
                    line_color='#000000')
    trace7 = go.Scatter(
                    x=registros_meses,
                    y=año_2016,
                    name="2016",
                    mode='lines+markers',
                    line_color='#808080')
    trace8 = go.Scatter(
                    x=registros_meses,
                    y=año_2017,
                    name="2017",
                    mode='lines+markers',
                    line_color='#008080')
    trace9 = go.Scatter(
                    x=registros_meses,
                    y=año_2018,
                    name="2018",
                    mode='lines+markers',
                    line_color='#00FF00')
    trace10 = go.Scatter(
                    x=registros_meses,
                    y=año_2019,
                    name="2019",
                    mode='lines+markers',
                    line_color='#800000')
    trace11 = go.Scatter(
                    x=registros_meses,
                    y=año_2020,
                    name="2020",
                    mode='lines+markers',
                    line_color='red')


    layout = go.Layout(template="ggplot2",title_text = '<b>Numero de Fallecidos entre 2010- '+str(now)+' </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11], layout = layout)

    graph1 = fig.to_html(full_html=False)

    suma_4meses = total_fallecimientos_mes
    col_list= ['January','February','March','April','May']
    suma_4meses['Total 4 Meses'] = suma_4meses[col_list].sum(axis=1)



    fig2 = px.bar(x=suma_4meses['Total 4 Meses'], y=suma_4meses['Años'], 
             title='Total de Fallecidos en los meses de Enero a Mayo',
              text=suma_4meses['Total 4 Meses'], 
             orientation='h', )
    fig2.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig2.update_layout(template = 'plotly_white')
    fig2.update_xaxes(title_text="Número de Fallecidos")
    fig2.update_yaxes(title_text="Años")

    graph2 = fig2.to_html(full_html=False)

    return render(request,"numero_defunciones_chile.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

def modelo_predictivo(request):
    
    seasonal_periods = 6
    
    days_chile2 = np.array([i for i in range(len(dates_chile))])

    datewise = pd.DataFrame({'Days Since': list(days_chile2), 'Confirmed':casos_chile})

    es=ExponentialSmoothing(np.asarray(datewise['Confirmed']),seasonal_periods=seasonal_periods,trend='add', seasonal='mul').fit()

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
                        mode='lines+markers',name="Predicción de Casos",))

    fig.update_layout(title="Proyección de casos en 20 días",
                    xaxis_title="Fecha",yaxis_title="Número de Casos",legend=dict(x=0,y=1,traceorder="normal"))

    graph1 = fig.to_html(full_html=False)
    
    graph2 = Predict_df_cl_1.to_html()

    return render(request,"predicciones.html", {"grafico1":graph1,"tabla1":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


def modelo_predictivo_fallecidos(request):
    data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')

    seasonal_periods = 15

    fechas_chile_crec = data_crec_por_dia.columns[-1]
    fechas_chile = data_crec_por_dia.loc[:, '2020-03-03': fechas_chile_crec]
    fechas_chile = fechas_chile.keys()
    fallecidos_por_dia =[]
    for i in fechas_chile:
        f = data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'][i].sum()
        fallecidos_por_dia.append(f)
    
    days_fallecidos_chile = np.array([i for i in range(len(fechas_chile))])

    data_ch_fallecidos = pd.DataFrame({'Días': list(days_fallecidos_chile), 'Fallecidos': [int(x) for x in fallecidos_por_dia]})
    casos_f = data_ch_fallecidos['Fallecidos']+1
    data_ch_fallecidos = pd.DataFrame({'Días': list(days_fallecidos_chile), 'Fallecidos':casos_f})
        

    es=ExponentialSmoothing(np.asarray(data_ch_fallecidos['Fallecidos']),seasonal_periods=seasonal_periods,trend='add', seasonal='mul').fit()


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
    Predict_df_cl_1["N° Fallecidos"] =np.round(list(es.forecast(20)))
        
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=np.array(future_forcast_dates_cl), y=data_ch_fallecidos["Fallecidos"],
                            mode='lines+markers',name="Fallecidos Reales"))
    fig.add_trace(go.Scatter(x=Predict_df_cl_1['Fecha'], y=Predict_df_cl_1["N° Fallecidos"],
                            mode='lines+markers',name="Predicción de Fallecidos",))

    fig.update_layout(title="Proyección de Fallecidos en 20 días",
                        xaxis_title="Fecha",yaxis_title="Número de Fallecidos",legend=dict(x=0,y=1,traceorder="normal"))

    graph1 = fig.to_html(full_html=False)
    
    graph2 = Predict_df_cl_1.to_html()

    return render(request,"predicciones_fallecidos.html", {"grafico1":graph1,"tabla1":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
