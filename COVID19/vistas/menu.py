from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render


import numpy as np
import pandas as pd
import seaborn as sb
import plotly.graph_objs as go
import datetime
import plotly.express as px
import folium
import warnings
import folium 
from folium import plugins
from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.graph_objs import *


import warnings

warnings.filterwarnings('ignore')

data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
pacientes_criticos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos.csv')


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

   

data_chile_map = data_chile.drop([16,9],axis=0)
data_chile_map = data_chile_map.reset_index()
data_chile_map = data_chile_map.drop('index',axis=1)

total =len(data_chile.columns)

fechas_chile_crec = data_crec_por_dia.columns[-1]
fechas_chile = data_crec_por_dia.loc[:, '2020-03-03': fechas_chile_crec]
fechas_chile = fechas_chile.keys()

casos_por_dia_totales =[]
fallecidos_por_dia =[]
recuperados_por_dia=[]
for i in fechas_chile:
    c_t = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos nuevos totales'][i].sum()
    f = data_crec_por_dia[data_crec_por_dia['Fecha']=='Fallecidos'][i].sum()
    r = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos recuperados'][i].sum()

    fallecidos_por_dia.append(f)
    casos_por_dia_totales.append(c_t)
    recuperados_por_dia.append(r)


activos_por_dia = []
for i in fechas_chile:
    activos = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos activos'][i].sum()
    activos_por_dia.append(activos)

def menu(request):

    # Adding Location data (Latitude,Longitude)
    locations = {
        "Arica y Parinacota" : [-18.4745998,-70.2979202],
        "Tarapacá" : [-20.2132607,-70.1502686],
        "Antofagasta" : [-23.6523609,-70.395401],
        "Atacama" : [-27.3667908,-70.331398],
        "Coquimbo" : [-29.9533195,-71.3394699],
        "Valparaíso" : [-33.0359993,-71.629631],
        "Metropolitana" : [-33.4726900,-70.6472400],
        "O’Higgins" : [-48.4862300,-72.9105900],
        "Maule" : [-35.5000000,-71.5000000],
        #"Ñuble" : [1,1],
        "Biobío" : [-37.0000000,-72.5000000],
        "Araucanía" : [-38.7396507,-72.5984192],
        "Los Ríos" : [-40.293129,-73.0816727],
        "Los Lagos" : [-41.7500000,-73.0000000],
        "Aysén" : [-45.4030304,-72.6918411],
        "Magallanes" : [-53.1548309,-70.911293]
            
    
    }

    data_chile_map["Lat"] = ""
    data_chile_map["Long"] = ""

    for index in data_chile_map.Region :
        data_chile_map.loc[data_chile_map.Region == index,"Lat"] = locations[index][0]
        data_chile_map.loc[data_chile_map.Region == index,"Long"] = locations[index][1]
        


    chile = folium.Map(location=[-30.0000000,-71.0000000], zoom_start=1,max_zoom=8,min_zoom=4)


    for i in range(0,len(data_chile_map[data_chile[ultima_fecha_cl]>0].Region)):
        folium.Circle(
            location=[data_chile_map.loc[i,"Lat"],data_chile_map.loc[i,"Long"]],
            
        
        tooltip = "<h5 style='text-align:center;font-weight: bold'>"+data_chile_map.iloc[i].Region+"</h5>"+
                        "<hr style='margin:10px;'>"+
                        "<ul style='color: #444;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
            "<li>Confirmed: "+str(data_chile_map.iloc[i,total-1])+"</li>"+
            "</ul>",
        
            radius=(int(np.log2(data_chile_map.iloc[i,total-1]+1)))*14000,

            color='#ff6600',
            fill_color='#ff8533',
            fill=True).add_to(chile)




    m=chile._repr_html_() #updated


    # Grafico 1:


    num_active = data_chile_r.iloc[4,-1].sum()

    datos_chile_rdca = pd.DataFrame({'Fecha':[ultima_fecha_cl],'Fallecidos':[num_death],'Cases Confirmados (Acumulados)': [num_cases_cl],'Recuperados':[num_rec],
                                    'Activos': [num_active] })
    temp = datos_chile_rdca

    confirmed = '#393e46' 
    death = '#ff2e63' 
    recovered = '#21bf73' 
    active = '#fe9801' 

    tm = temp.melt(id_vars="Fecha", value_vars=['Activos', 'Fallecidos','Recuperados'])
    fig = px.treemap(tm, path=["variable"], values="value",color_discrete_sequence=[recovered,active,death])

    fig.layout.update(title_text='Activos vs. Recuperados '+fechas_chile[-1],xaxis_showgrid=False, yaxis_showgrid=False,font=dict(
            size=15,
            color="Black"    
        ))
  

    #Grafico 2
    #trace = go.Scatter(
                    #x=fechas_chile,
                   # y=casos_por_dia_totales,
                   # name="growth",
                   # mode='lines+markers',
                   # line_color='red')

    #layout = go.Layout(template="ggplot2", title_text = '<b>Numero de Casos por Día '+ultima_fecha_cl+'</b>',
                    #font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    #fig2 = go.Figure(data = [trace], layout = layout)


    
    fig2=go.Figure()
    fig2.add_trace(go.Scatter(x=fechas_chile, y=casos_por_dia_totales,mode='lines+markers',
                        name='Número Casos'))
    #fig2.add_trace(go.Scatter(x=fechas_chile, y=fallecidos_por_dia,mode='lines+markers',
                        #name='Falllecidos'))
    fig2.update_layout(title="Numero de Casos por Día",
                    xaxis_title="Date",yaxis_title="Número casos",legend=dict(x=0,y=1,traceorder="normal"))


    #Grafico 3

    data_rfa = pd.DataFrame({'Fecha': pd.to_datetime(fechas_chile),'Activos':activos_por_dia, 
                                'Fallecidos': fallecidos_por_dia,'Recuperados':recuperados_por_dia})

    rest_grouped = data_rfa.groupby('Fecha')['Recuperados', 'Fallecidos', 'Activos'].sum().reset_index()

    temp = rest_grouped.melt(id_vars="Fecha", value_vars=['Recuperados', 'Fallecidos', 'Activos'],
                    var_name='Casos', value_name='count')


    fig5 = px.area(temp, x="Fecha", y="count", color='Casos',
                title='Casos - Chile: Area Plot', color_discrete_sequence = ['green', 'red', 'orange'])

    graph = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig5.to_html(full_html=False)
    ultima_fecha = ultima_fecha_cl

    #Grafico4
    data_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos con sintomas'].iloc[0,1:].sum()
    data_sin_sintomas = data_chile_r[data_chile_r['Fecha']=='Casos nuevos sin sintomas'].iloc[0,1:].sum()
    data_casos_por_sintomas = pd.DataFrame({'Tipo':['Casos nuevos con sintomas','Casos nuevos sin sintomas'],'Numero de casos':[data_sintomas,data_sin_sintomas]})
    fig4 = px.pie(data_casos_por_sintomas, values='Numero de casos', names='Tipo')
    fig4.update_traces(textposition='inside')
    fig4.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    graph4 = fig4.to_html(full_html=False)





    return render(request,"principal.html", {"mapa": m,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"fecha_act":ultima_fecha, "grafico1":graph,"grafico2":graph2,"grafico3":graph3,"grafico4":graph4,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


def casos_criticos(request):




    #GRAFICO 1
    trace = go.Scatter(
                x=pacientes_criticos.iloc[:,1:].columns,
                y=pacientes_criticos.iloc[0,1:],
                name="Pacientes Criticos",
                mode='lines+markers',
                line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Número de Pacientes Criticos Fecha: '+ ultima_fecha_cl+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig = go.Figure(data = [trace], layout = layout)


    data_activos = data_chile_r[data_chile_r['Fecha']=='Casos activos']
    ultima_fecha = data_activos.columns
    ultima_fecha= ultima_fecha[-1]

    trace = go.Scatter(
                x=data_activos.iloc[:,1:].columns,
                y=data_activos.iloc[0,1:],
                name="Pacientes Activos",
                mode='lines+markers',
                line_color='red')

    layout = go.Layout(template="ggplot2",title_text = '<b>Número de Pacientes Activos Fecha: '+ ultima_fecha+'</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace], layout = layout)


    fig3=px.bar(x=data_activos.iloc[:,1:].columns,y=data_activos.iloc[0,1:])
    fig3.update_layout(title="Distribucion del número de Casos Activos",
                    xaxis_title="Fecha",yaxis_title="Numero de Casos",)

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)


    #graph2 = fig2.to_html(full_html=False)



    return render(request,"numero_casos_criticos.html", {"grafico1":graph1,"grafico3":graph3,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
