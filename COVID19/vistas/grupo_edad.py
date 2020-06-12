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

#grupos de edad: numero de casos
fecha_grupo_edad = grupo_casos_genero.columns[-1]
death_cl = grupo_fallecidos.loc[:, '2020-04-09': ultima_fecha_cl]
dates_d = death_cl.keys()

#grupos de edad: numero de casos
fecha_grupo_edad = grupo_casos_genero.columns[-1]
fecha_grupo_fallecidos=grupo_fallecidos.columns[-1]


grupo_edad = grupo_casos_genero.iloc[0:17,0]
data_casos_grupo_edad_mf = pd.DataFrame({'Grupo de edad': grupo_edad, fecha_grupo_edad : 0})

fila = 0
for grupo in data_casos_grupo_edad_mf['Grupo de edad']:
    suma_casos_MF = grupo_casos_genero[grupo_casos_genero['Grupo de edad'] == grupo].iloc[:,-1].sum()
    data_casos_grupo_edad_mf.iloc[fila,1] = suma_casos_MF
    fila=fila+1



casso_m = grupo_casos_genero[grupo_casos_genero['Sexo'] == 'M']
casso_f = grupo_casos_genero[grupo_casos_genero['Sexo'] == 'F']

#https://stackoverrun.com/es/q/8510875
#https://www.it-swarm.dev/es/python/anadir-una-fila-pandas-dataframe/1066944305/
f = casso_f.columns[1:]
data_suma_casos_f = pd.DataFrame(index=np.arange(0, 1), columns=(f) )

for date in data_suma_casos_f:
    data_suma_casos_f[date].iloc[0] = casso_f[date].sum()
data_suma_casos_f['Sexo'].iloc[0] = 'F'

m = casso_m.columns[1:]
data_suma_casos_m = pd.DataFrame(index=np.arange(0, 1), columns=(f) )

for date in data_suma_casos_m:
    data_suma_casos_m[date].iloc[0] = casso_m[date].sum()
data_suma_casos_m['Sexo'].iloc[0] = 'M'


union = pd.concat([data_suma_casos_m, data_suma_casos_f])





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

   


    #GRAFICO3

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(x=data_suma_casos_m.columns, y=data_suma_casos_f.iloc[0], name='M'))
    fig3.add_trace(go.Scatter(x=data_suma_casos_f.columns, y=data_suma_casos_m.iloc[0], name='F'))

    fig3.layout.update(title_text='Total de casos por genero : '+fecha_grupo_edad,xaxis_showgrid=False, yaxis_showgrid=False,
                height=600,font=dict(
                size=15,
                color="Black"    
            ))
    fig3.layout.plot_bgcolor = 'White'
    fig3.layout.paper_bgcolor = 'White'


    #GRAFICO4
    data = union[['Sexo',fecha_grupo_edad]]
    fig4 = px.pie(data, values=fecha_grupo_edad, names='Sexo')
    fig4.update_traces(textposition='inside')
    fig4.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')

    graph1 = fig.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)




    return render(request,"casos_grupo.html", {"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})


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



    return render(request,"fallecidos_grupo.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})


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


        return render(request,"grupo_edad_f.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})

    else:
        mensaje='ERROR'
        return HttpResponse(mensaje)

def busqueda_hosp_por_grupo(request):

    #GRAFICO 1
    fig = grupos_hosp()

    #Grafico 2

    colors = ['gold', 'darkorange', 'crimson','mediumturquoise', 'sandybrown', 'grey',  'lightgreen','navy','deeppink','purple']
    
    
 
    fig2 = px.pie(grupo_uci, values=ultima_fecha_cl, names='Grupo de edad')
    fig2.update_traces(textposition='inside')
    fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


    graph1 = fig.to_html(full_html=False)

    graph2 = fig2.to_html(full_html=False)

    fecha_uci = grupo_uci.columns
    fecha_uci= fecha_uci[-1]


    return render(request,"hospitalizaciones_grupo_edad.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"fecha_uci":fecha_uci,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})
