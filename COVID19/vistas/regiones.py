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
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_casos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv')
data_casos_por_comuna_activos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv')
grupo_uci_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
tipo_cama = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto24/CamasHospital_Diario.csv')


casos_diarios_por_region = casos_diarios_por_region.drop(16, axis=0)
fecha_casos_region = casos_diarios_por_region.columns[-1]
fecha_casos_region = casos_diarios_por_region.loc[:, '2020-03-03': fecha_casos_region]
fecha_casos_region = fecha_casos_region.keys()

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


data_casos_por_comuna =data_casos_por_comuna.drop(['Tasa'], axis=1)

fecha_comuna = data_casos_por_comuna.columns
fecha_comuna= fecha_comuna[-1]


#***************************MENU**************************************
#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


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

#********************************************************************
arica = []
tarapaca = []
antofagasta = []
atacama = []
coquimbo = []
valparaiso = []
metropolitana = []
o_Higgins = []
maule = []
nuble = []
biobio = []
araucania = []
los_Ríos = []
los_lagos = []
aysen = []
magallanes = []

for i in fecha_casos_region:
    
    arica.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Arica y Parinacota'][i].sum())
    tarapaca.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Tarapacá'][i].sum())
    antofagasta.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Antofagasta'][i].sum())
    atacama.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Atacama'][i].sum())
    coquimbo.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Coquimbo'][i].sum())
    valparaiso.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Valparaíso'][i].sum())
    metropolitana.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Metropolitana'][i].sum())
    o_Higgins.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='O’Higgins'][i].sum())
    maule.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Maule'][i].sum())
    nuble.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Ñuble'][i].sum())
    biobio.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Biobío'][i].sum())
    araucania.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Araucanía'][i].sum())
    los_Ríos.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Los Ríos'][i].sum())
    los_lagos.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Los Lagos'][i].sum())
    aysen.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Aysén'][i].sum())
    magallanes.append(casos_diarios_por_region[casos_diarios_por_region['Region']=='Magallanes'][i].sum()) 




def regiones(request):
  

    ultima_fecha_cl = data_chile.columns
    ultima_fecha_cl= ultima_fecha_cl[-1]

    confirmados = data_chile.loc[:, '2020-03-03': ultima_fecha_cl]
    dates_chile = confirmados.keys()
    datos = data_chile[['Region',ultima_fecha_cl]].drop([16],axis=0)

    #GRAFICO 1
    titulo ='COVID-19: Total de Casos acumulados'

    fig = px.bar(datos.sort_values(ultima_fecha_cl), 
             x=ultima_fecha_cl, y="Region", 
             title=titulo,
              text=ultima_fecha_cl, 
             orientation='h')
    fig.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig.update_layout(template = 'plotly_white')

    #GRAFICO 2: ANIMACION
    gris = '#393e46' 

    data_total_ar = pd.DataFrame({'Region': ('Arica'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': arica})
    data_total_ta = pd.DataFrame({'Region': ('Tarapacá'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': tarapaca})
    data_total_at = pd.DataFrame({'Region': ('Antofagasta'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': antofagasta})
    data_total_ata = pd.DataFrame({'Region': ('Atacama'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': atacama})
    data_total_co = pd.DataFrame({'Region': ('Coquimbo'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': coquimbo})
    data_total_va = pd.DataFrame({'Region': ('Valparaíso'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': valparaiso})
    data_total_me = pd.DataFrame({'Region': ('Metropolitana'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': metropolitana})
    data_total_og = pd.DataFrame({'Region': ('O Higgins'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': o_Higgins})
    data_total_mau = pd.DataFrame({'Region': ('Maule'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': maule})
    data_total_nu = pd.DataFrame({'Region': ('Ñuble'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': nuble})
    data_total_bi = pd.DataFrame({'Region': ('Biobío'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': biobio})
    data_total_ara = pd.DataFrame({'Region': ('Araucanía'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': araucania})
    data_total_lr = pd.DataFrame({'Region': ('Los Ríos'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': los_Ríos})
    data_total_ll = pd.DataFrame({'Region': ('Los Lagos'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': los_lagos})
    data_total_ay = pd.DataFrame({'Region': ('Aysén'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': aysen})
    data_total_ma = pd.DataFrame({'Region': ('Magallanes'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': magallanes})



    # Apilar los __DataFrames__ uno encima del otro
    apilados= pd.concat([data_total_ar, data_total_ta], axis=0)
    apilados= pd.concat([apilados, data_total_at], axis=0)
    apilados= pd.concat([apilados, data_total_ata], axis=0)
    apilados= pd.concat([apilados, data_total_co], axis=0)
    apilados= pd.concat([apilados, data_total_va], axis=0)
    apilados= pd.concat([apilados, data_total_me], axis=0)
    apilados= pd.concat([apilados, data_total_og], axis=0)
    apilados= pd.concat([apilados, data_total_mau], axis=0)
    apilados= pd.concat([apilados, data_total_nu], axis=0)
    apilados= pd.concat([apilados, data_total_bi], axis=0)
    apilados= pd.concat([apilados, data_total_ara], axis=0)
    apilados= pd.concat([apilados, data_total_lr], axis=0)
    apilados= pd.concat([apilados, data_total_ll], axis=0)
    apilados= pd.concat([apilados, data_total_ay], axis=0)
    apilados= pd.concat([apilados, data_total_ma], axis=0)

    def location(row):
        if row['Region']=='Arica':
                return 'Arica'
        elif row['Region']=='Tarapacá':
                return 'Tarapacá'
            
        elif row['Region']=='Antofagasta':
                return 'Antofagasta'
            
        elif row['Region']=='Atacama':
                return 'Atacama'
        elif row['Region']=='Coquimbo':
                return 'Coquimbo'
        elif row['Region']=='Valparaíso':
                return 'Valparaíso'
        elif row['Region']=='Metropolitana':
                return 'Metropolitana'
        elif row['Region']=='O Higgins':
                return 'O Higgins'
        elif row['Region']=='Ñuble':
                return 'Ñuble'
        elif row['Region']=='Biobío':
                return 'Biobío'
        elif row['Region']=='Araucanía':
                return 'Araucanía'
        elif row['Region']=='Los Ríos':
                return 'Los Ríos'
        elif row['Region']=='O’Higgins':
                return 'O’Higgins'
        elif row['Region']=='Los Lagos':
                return 'Los Lagos'
        elif row['Region']=='Aysén':
                return 'Aysén'
        elif row['Region']=='Maule':
                return 'Maule'
        else:
            return 'Magallanes'
            

    temp = apilados.copy()
    temp['Region'] = temp.apply(location, axis=1)
    temp['Fecha'] = temp['Fecha'].dt.strftime('%Y-%m-%d')
    temp = temp.groupby(['Region', 'Fecha'])['Casos'].sum().reset_index()
    temp = temp.melt(id_vars=['Region', 'Fecha'], value_vars=['Casos'], 
                    var_name='Casos', value_name='Count')

    fig2 = px.bar(temp, y='Region', x='Count', color='Casos', barmode='group', orientation='h',
                text='Count', title='Evolución del Número de Casos por Días', animation_frame='Fecha',
                height=700,color_discrete_sequence= [gris], range_x=[0, int(metropolitana[-1]+1000)])
    fig2.update_traces(textposition='outside')
    fig2.update_xaxes(title_text="Numero de Casos (acumulados)")
    fig2.update_yaxes(title_text="Regiones")

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)



    return render(request,"region.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"estado_r":estado_r,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})



def busqueda_region(request):

    ultima_fecha_cl = data_chile.columns
    ultima_fecha_cl= ultima_fecha_cl[-1]

    ultima_fecha_region_fallecidos = fallecidos_por_region.columns
    ultima_fecha_region_fallecidos= ultima_fecha_region_fallecidos[-1]

    fecha =fecha_comuna
    #ultima_fecha_cl = fecha_comuna


    if request.GET['region']:

        region = request.GET['region']
        print(region)


        if(region=='Tarapaca'):
            region2 = 'Tarapacá'
        elif(region=='Valparaiso'):
            region2 = 'Valparaíso'
        elif(region=='Del Libertador General Bernardo O’Higgins'):
            region2 = 'O’Higgins'
        elif(region=='Nuble'):
            region2 = 'Ñuble'
        elif(region=='Biobio'):
            region2 = 'Biobío'
        elif(region=='La Araucania'):
            region2 = 'Araucanía'
        elif(region=='Los Rios'):
            region2 = 'Los Ríos'
        elif(region=='Aysen'):
            region2 = 'Aysén'
        elif(region=='Magallanes y la Antartica'):
            region2 = 'Magallanes'
        else:
            region2=region
            



        n_casos_region = data_chile[data_chile['Region'] ==region2][ultima_fecha_cl].values
        n_casos_region =  str(int(n_casos_region))+' ('+ultima_fecha_cl+')'



        
        n_casos_region_f = fallecidos_por_region[fallecidos_por_region['Region']==region2][ultima_fecha_region_fallecidos]
        n_casos_region_f = str(int(n_casos_region_f))+' ('+ultima_fecha_region_fallecidos+')'




        
        data_casos_por_comuna_maule = data_casos_por_comuna[data_casos_por_comuna['Region']==region2]

        data_casos_por_comuna_maule = data_casos_por_comuna_maule.sort_values(fecha_comuna)

        total_maule= data_casos_por_comuna_maule[fecha_comuna].sum()
        total_maule = str(total_maule)

        fig = px.bar(x=data_casos_por_comuna_maule['Comuna'], y=data_casos_por_comuna_maule[fecha_comuna],
                        title='Numero de casos Totales Confirmados en la Region '+region2+' Fecha: '+fecha,
                    text=data_casos_por_comuna_maule[fecha_comuna],
                        
            )
        fig.update_xaxes(title_text="Comunas")
        fig.update_yaxes(title_text="Número de Casos")


        #grafico2 
        data_casos_por_comuna_maule = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Region']==region]
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.reset_index()
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.drop(data_casos_por_comuna_maule.index[len(data_casos_por_comuna_maule)-1])


        fig2 = px.bar(data_casos_por_comuna_maule.sort_values(fecha), 
                    x=fecha, y='Comuna',color_discrete_sequence=['#84DCC6'],height=900,
                    title='Número de casos Activos Reg: '+region+' fecha: '+fecha, text=fecha, orientation='h')
        fig2.update_xaxes(title_text="Número de Casos Activos")
        fig2.update_yaxes(title_text="Comunas")

        n_casos_activos =data_casos_por_comuna_maule[fecha].sum()
        n_casos_activos = str(int(n_casos_activos))+' ('+fecha+')'



        #tabla
        data = data_casos_por_comuna_maule[['Comuna',fecha]]
        data = data.rename(columns={fecha:'N° Casos Activos'})


        #grafico 3


        data = data_casos_por_comuna_maule.drop(['index','Region','Codigo region','Codigo comuna','Poblacion'], axis=1)

        fecha_casos_comuna = data.columns[-1]
        fecha_casos_comuna = data.loc[:, '2020-04-13': fecha_casos_comuna]
        fecha_casos_comuna = fecha_casos_comuna.keys()

        fig3 = go.Figure()
        for comuna in data['Comuna']:
            fig3.add_trace(go.Scatter(x=fecha_casos_comuna, y=data[data['Comuna']==comuna].iloc[0,1:], name=comuna))


        fig3.layout.update(title_text='Evolución de Casos Activos Fecha: '+fecha,xaxis_showgrid=False, yaxis_showgrid=False,font=dict(
                    size=15,
                    color="Black"    
                ))
        fig3.layout.plot_bgcolor = 'White'
        fig3.layout.paper_bgcolor = 'White'

        graph1 = fig.to_html(full_html=False)
        graph2 = fig2.to_html(full_html=False)
        graph3 = fig3.to_html(full_html=False)
        tabla1 = data.to_html()




        return render(request,"por_comuna_casos.html", {"region":region,"grafico1":graph1,"grafico2":graph2,"tabla1":graph3,"n_casos":n_casos_region,"num_death":n_casos_region_f,"n_casos_activos":n_casos_activos})

    else:
        mensaje='ERROR'
        return HttpResponse(mensaje)


def examenes_pcr(request):

    exa_pcr = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR.csv')
    exa_pcr = exa_pcr.fillna(0)

    fecha = exa_pcr.columns
    fecha =fecha[-1]

    colum = exa_pcr.drop(['Codigo region','Poblacion','Region'],axis=1)
    list_col = colum.columns
    exa_pcr['Total'] = exa_pcr[list_col].sum(axis=1)
    exa_pcr= exa_pcr.drop(['Codigo region','Poblacion'],axis=1)

    #Grafico 1
    titulo ='Total de Examenes PCR realizados Fecha: '+fecha

    fig = px.bar(exa_pcr.sort_values('Total'),
                x='Region', y='Total',
                title=titulo,
                text= 'Total'
                
    )
    fig.update_xaxes(title_text="Regiones")
    fig.update_yaxes(title_text="Numero de casos")

    #Grafico 2

    fig2 = px.pie(exa_pcr, values='Total', names='Region')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')

    
    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)
    
    return render(request,"num_examenes_pcr.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


def busqueda_hospitalizacion_region(request):


    #GRAFICO 1
    fig = px.bar(x=grupo_uci_reg[ultima_fecha_cl], y=grupo_uci_reg['Region'], 
             title='Numero de personas Hospitalizadas en UCI por Región: '+ultima_fecha_cl,
             orientation='h',
             width=800, height=700)
    fig.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig.update_layout(template = 'plotly_white')
    fig.update_yaxes(title_text="Regiones")
    fig.update_xaxes(title_text='Número de personas Hospitalizadas')


    #GRAFICO 2

    trace1 = go.Pie(
                labels=grupo_uci_reg['Region'],
                values=grupo_uci_reg[ultima_fecha_cl],
                hoverinfo='label+percent', 
                textfont_size=12,
                marker=dict(line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de personas Hospitalizadas por Región </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)


    #GRAFICO 3

    fecha_tpc = tipo_cama.columns[-1]

    titulo ='Número de pacientes hospitalizados según el tipo de cama.: '+fecha_tpc

    fig3 = px.bar(x=tipo_cama['Tipo de cama'], y=tipo_cama[fecha_tpc],
            title=titulo,
           text=tipo_cama[fecha_tpc]
            
        )
    fig3.update_xaxes(title_text="Tipo de Cama")
    fig3.update_yaxes(title_text="Numero de Casos")


    #Garfico4

    fig4 = make_subplots(rows=1, cols=2)
    trace1 = go.Pie(
                    labels=tipo_cama['Tipo de cama'],
                    values=tipo_cama[fecha_tpc],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                    marker=dict(line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de pacientes Hosp. según el tipo de cama </b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig4 = go.Figure(data = [trace1], layout = layout)

    
    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)


    return render(request,"hospitalizaciones_region.html", {"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})
