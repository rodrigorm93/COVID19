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
from plotly.graph_objs import *
from plotly.subplots import make_subplots

data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_uci = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario.csv')
grupo_uci_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto8/UCI.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
grupo_casos_genero= pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario.csv')
data_casos_por_comuna = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/2020-06-01-CasosConfirmados.csv')
num_vent = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto20/NumeroVentiladores.csv')
pacientes_criticos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto23/PacientesCriticos.csv')
data_casos_por_comuna_activos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv')




fecha_comuna='2020-06-01'
ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

fecha_grupo_fallecidos=grupo_fallecidos.columns[-1]

#grupos de edad: numero de casos
fecha_grupo_edad = grupo_casos_genero.columns[-1]
death_cl = grupo_fallecidos.loc[:, '2020-04-09': ultima_fecha_cl]
dates_d = death_cl.keys()

grupo_edad = grupo_casos_genero.iloc[0:17,0]
data_casos_grupo_edad_mf = pd.DataFrame({'Grupo de edad': grupo_edad, fecha_grupo_edad : 0})

fila = 0
for grupo in data_casos_grupo_edad_mf['Grupo de edad']:
    suma_casos_MF = grupo_casos_genero[grupo_casos_genero['Grupo de edad'] == grupo].iloc[:,-1].sum()
    data_casos_grupo_edad_mf.iloc[fila,1] = suma_casos_MF
    fila=fila+1




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


   #ventiladores 

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
        #print(locations[index][0])
        


    chile = folium.Map(location=[-30.0000000,-71.0000000], zoom_start=4,max_zoom=6,min_zoom=4,height=500,width="80%")


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
    trace = go.Scatter(
                    x=fechas_chile,
                    y=casos_por_dia_totales,
                    name="growth",
                    mode='lines+markers',
                    line_color='red')

    layout = go.Layout(template="ggplot2", title_text = '<b>Numero de Casos por día</b>',
                    font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace], layout = layout)


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





    return render(request,"principal.html", {"mapa": m,"estado_r":estado_r,"fecha_act":ultima_fecha, "grafico1":graph,"grafico2":graph2,"grafico3":graph3,"grafico4":graph4,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


def regiones(request):
  

    ultima_fecha_cl = data_chile.columns
    ultima_fecha_cl= ultima_fecha_cl[-1]

    confirmados = data_chile.loc[:, '2020-03-03': ultima_fecha_cl]
    dates_chile = confirmados.keys()
    datos = data_chile[['Region',ultima_fecha_cl]].drop([16],axis=0)

    #GRAFICO 1
    titulo ='COVID-19: Total de Casos acumulados'

    fig2 = px.bar(datos.sort_values(ultima_fecha_cl), 
             x=ultima_fecha_cl, y="Region", 
             title=titulo,
              text=ultima_fecha_cl, 
             orientation='h')
    fig2.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig2.update_layout(template = 'plotly_white')
    graph1 = fig2.to_html(full_html=False)



    #GRAFICO 2
    datos = data_chile[['Region',ultima_fecha_cl]].drop([16],axis=0)

    fig = px.scatter(datos, y=datos.loc[:,ultima_fecha_cl],
                        x= datos.loc[:,"Region"],
                        color= "Region", hover_name="Region",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title='COVID-19: Numero Total de casos por Region',
                        size = np.power(datos[ultima_fecha_cl]+1,0.3)-0.5,
                        size_max = 30,
                        width=900,
                        height =600,
                        )
    fig.update_coloraxes(colorscale="hot")
    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(title_text="Numero casos")
    fig.update_xaxes(title_text="Regiones")

    graph2 = fig.to_html(full_html=False)


  

    return render(request,"region.html", {"grafico1":graph1,"estado_r":estado_r,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


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

        data_casos_por_comuna_maule = data_casos_por_comuna_maule.sort_values('Casos Confirmados')

        total_maule= data_casos_por_comuna_maule['Casos Confirmados'].sum()
        total_maule = str(total_maule)

        fig = px.bar(x=data_casos_por_comuna_maule['Comuna'], y=data_casos_por_comuna_maule['Casos Confirmados'],
                        title='Numero de casos Totales Confirmados en la Region '+region2+' Fecha: '+fecha,
                    text=data_casos_por_comuna_maule['Casos Confirmados'],
                        
            )


            #grafico2 
        data_casos_por_comuna_maule = data_casos_por_comuna_activos[data_casos_por_comuna_activos['Region']==region]
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.reset_index()
        data_casos_por_comuna_maule = data_casos_por_comuna_maule.drop(data_casos_por_comuna_maule.index[len(data_casos_por_comuna_maule)-1])


        fig2 = px.bar(data_casos_por_comuna_maule.sort_values(fecha), 
                    x=fecha, y='Comuna',color_discrete_sequence=['#84DCC6'],height=900,
                    title='Número de casos Activos en la Región '+region+' fecha: '+fecha, text=fecha, orientation='h')
        fig2.update_xaxes(title_text="Número de Casos Activos")
        fig2.update_yaxes(title_text="Comunas")

        n_casos_activos =data_casos_por_comuna_maule[fecha].sum()
        n_casos_activos = str(int(n_casos_activos))+' ('+fecha+')'

        #tabla
        data = data_casos_por_comuna_maule[['Comuna',fecha]]
        data = data.rename(columns={fecha:'N° Casos Activos'})

        graph1 = fig.to_html(full_html=False)
        graph2 = fig2.to_html(full_html=False)
        tabla1 = data.to_html()


        return render(request,"por_comuna_casos.html", {"grafico1":graph1,"grafico2":graph2,"tabla1":tabla1,"n_casos":n_casos_region,"num_death":n_casos_region_f,"n_casos_activos":n_casos_activos})

    else:
        mensaje='ERROR'
        return HttpResponse(mensaje)


def busqueda_hospitalizacion_region(request):


    #GRAFICO 1
    fig = px.bar(x=grupo_uci_reg[ultima_fecha_cl], y=grupo_uci_reg['Region'], 
             title='Numero de personas Hospitalizadas en UCI por Región: '+ultima_fecha_cl,
             orientation='h',
             width=800, height=700)
    fig.update_traces(marker_color='#008000', opacity=0.8, textposition='inside')

    fig.update_layout(template = 'plotly_white')
    fig.update_yaxes(title_text="Age Group")
    fig.update_xaxes(title_text='Number of Hospitalized')


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

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)


    return render(request,"hospitalizaciones_region.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


def busqueda_casos_por_grupo(request):

    #GRAFICO 1

    titulo ='Casos por grupo de edad Fecha: '+fecha_grupo_edad

    fig = px.bar(data_casos_grupo_edad_mf.sort_values(fecha_grupo_edad),
                    x='Grupo de edad', y=fecha_grupo_edad,
                    title=titulo,
                    text=fecha_grupo_edad 
                    )
    fig.update_xaxes(title_text="Grupos de Edad")
    fig.update_yaxes(title_text="Numero de casos")

   
   #GRAFICO 2

    trace1 = go.Pie(
                labels=data_casos_grupo_edad_mf['Grupo de edad'],
                values=data_casos_grupo_edad_mf[fecha_grupo_edad],
                hoverinfo='label+percent', 
                textfont_size=12,
                marker=dict(#colors=colors, 
                            line=dict(color='#000000', width=2)))
    layout = go.Layout(title_text = '<b>Porcentaje de Casos por Grupo de Edad: '+fecha_grupo_edad+'</b>',
                  font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
    fig2 = go.Figure(data = [trace1], layout = layout)

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)

    return render(request,"casos_grupo.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})



def busqueda_fallecidos_por_grupo(request):

    #GRAFICO 1
    
    titulo ='Fallecidos por grupo de edad Fecha: '+fecha_grupo_fallecidos


    fig = px.bar(grupo_fallecidos.sort_values(fecha_grupo_fallecidos),
                    x='Grupo de edad', y=fecha_grupo_fallecidos,
                    title=titulo,
                    text=fecha_grupo_fallecidos 
                    )
    fig.update_xaxes(title_text="Grupos de Edad")
    fig.update_yaxes(title_text="Numero de casos")

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



    return render(request,"fallecidos_grupo.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})




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

        layout = go.Layout(template="ggplot2",title_text = '<b>Numero Fallecidos '+ grupo_edad +' :'+ ultima_fecha_cl+'</b>',
                            font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'))
        fig = go.Figure(data = [trace], layout = layout)

        graph1 = fig.to_html(full_html=False)
        graph2 = fig2.to_html(full_html=False)


        return render(request,"grupo_edad_f.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

    else:
        mensaje='ERROR'
        return HttpResponse(mensaje)

def busqueda_hosp_por_grupo(request):

    #GRAFICO 1
    titulo ='Numero de personas Hopitalizadas Fecha: '+ultima_fecha_cl

    fig = px.bar(x=grupo_uci['Grupo de edad'], y=grupo_uci[ultima_fecha_cl],
                title=titulo,
            text=grupo_uci[ultima_fecha_cl]
                
    )
    fig.update_xaxes(title_text="Grupo Edad")
    fig.update_yaxes(title_text="Numero de Casos")

    #Grafico 2

    colors = ['gold', 'darkorange', 'crimson','mediumturquoise', 'sandybrown', 'grey',  'lightgreen','navy','deeppink','purple']
    
    
 
    fig2 = px.pie(grupo_uci, values=ultima_fecha_cl, names='Grupo de edad')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)



    return render(request,"hospitalizaciones_grupo_edad.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})


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



    return render(request,"numero_ventiladores.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

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



    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)


    #graph2 = fig2.to_html(full_html=False)



    return render(request,"numero_casos_criticos.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})

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
    fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    
    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)
    
    return render(request,"num_examenes_pcr.html", {"grafico1":graph1,"grafico2":graph2,"estado_r":estado_r,"n_casos":num_cases_cl,"num_rec":num_rec, "num_death":num_death})