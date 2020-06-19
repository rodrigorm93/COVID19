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
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
data_casos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv')
data_casos_por_comuna_activos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv')

fallecidos_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_T.csv')


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

ultima_fecha_cl_r = data_chile_r.columns
ultima_fecha_cl_r= ultima_fecha_cl_r[-1]


ultima_fecha_region_fallecidos = fallecidos_por_region.columns
ultima_fecha_region_fallecidos= ultima_fecha_region_fallecidos[-1]

num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl = num_cases_cl[ultima_fecha_cl].sum()



num_death =  grupo_fallecidos[ultima_fecha_cl].sum()
num_rec = data_chile_r.iloc[2,-1].sum()

#ver el caso de que no se actualicen los registros

estado_r='Act'+ultima_fecha_cl
estado_f='Act'+ultima_fecha_cl
estado_a='Act'+ultima_fecha_cl

casos_act = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()
#dejar el ulktimo registro de recuperados que fue el 2020-06-02



num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'
casos_act = str(int(casos_act))+' ('+ultima_fecha_cl_r+')'


fecha_casos_fall='('+data_chile.columns[-1]+')'

#********************************************************************

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
