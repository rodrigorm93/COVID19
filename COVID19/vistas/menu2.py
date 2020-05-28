from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render


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
now = date.today()


total_fallecimientos_mes = pd.read_csv('https://raw.githubusercontent.com/rodrigorm93/Datos-Chile/master/Total-Defunciones/total_fallecimientos_mes.csv', sep=',')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')


ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]
num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()
num_death =  grupo_fallecidos[ultima_fecha_cl].sum()
num_rec = data_chile_r.iloc[2,-1].sum()

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
                    name="Fallecidos 2010",
                    mode='lines+markers',
                    line_color='#800080')
    trace2 = go.Scatter(
                    x=registros_meses,
                    y=año_2011,
                    name="Fallecidos 2011",
                    mode='lines+markers',
                    line_color='green')
    trace3 = go.Scatter(
                    x=registros_meses,
                    y=año_2012,
                    name="Fallecidos 2012",
                    mode='lines+markers',
                    line_color='#000080')
    trace4 = go.Scatter(
                    x=registros_meses,
                    y=año_2013,
                    name="Fallecidos 2013",
                    mode='lines+markers',
                    line_color='#00FFFF')
    trace5 = go.Scatter(
                    x=registros_meses,
                    y=año_2014,
                    name="Fallecidos 2014",
                    mode='lines+markers',
                    line_color='#FFFF00')
    trace6 = go.Scatter(
                    x=registros_meses,
                    y=año_2015,
                    name="Fallecidos 2015",
                    mode='lines+markers',
                    line_color='#000000')
    trace7 = go.Scatter(
                    x=registros_meses,
                    y=año_2016,
                    name="Fallecidos 2016",
                    mode='lines+markers',
                    line_color='#808080')
    trace8 = go.Scatter(
                    x=registros_meses,
                    y=año_2017,
                    name="Fallecidos 2017",
                    mode='lines+markers',
                    line_color='#008080')
    trace9 = go.Scatter(
                    x=registros_meses,
                    y=año_2018,
                    name="Fallecidos 2018",
                    mode='lines+markers',
                    line_color='#00FF00')
    trace10 = go.Scatter(
                    x=registros_meses,
                    y=año_2019,
                    name="Fallecidos 2019",
                    mode='lines+markers',
                    line_color='#800000')
    trace11 = go.Scatter(
                    x=registros_meses,
                    y=año_2020,
                    name="Fallecidos 2020",
                    mode='lines+markers',
                    line_color='red')


    layout = go.Layout(template="ggplot2", width=1000, height=600,title_text = '<b>Numero de Fallecidos entre 2010- '+str(now)+' </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11], layout = layout)

    graph1 = fig.to_html(full_html=False)


    return render(request,"numero_defunciones_chile.html", {"grafico1":graph1,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})