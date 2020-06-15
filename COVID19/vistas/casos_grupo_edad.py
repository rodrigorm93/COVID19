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

data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
grupo_casos_genero= pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario.csv')



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





#grupos genero 
fecha_grupo_edad = grupo_casos_genero.columns[-1]
fecha_grupo_edad_2 = '('+fecha_grupo_edad+')'
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


total = data_casos_grupo_edad_mf[fecha_grupo_edad].sum()
ninos = data_casos_grupo_edad_mf.iloc[0:3][fecha_grupo_edad].sum()
jovenes = data_casos_grupo_edad_mf.iloc[3:6][fecha_grupo_edad].sum()
adultos = data_casos_grupo_edad_mf.iloc[6:12][fecha_grupo_edad].sum()
adultos_mayores = data_casos_grupo_edad_mf.iloc[12:17][fecha_grupo_edad].sum()


num_recuFIS = int_format(int(ninos))
num_cases_cl = int_format(int(jovenes))
num_death = int_format(int(adultos))
casos_act = int_format(int(adultos_mayores))

data_div_edad = pd.DataFrame({'Division Edad': ['Niños','Jóvenes','Adultos','Adultos mayores'], 
                              'Total Casos': [ninos,jovenes,adultos,adultos_mayores]})


# funciones
def casos_grupo_edad():
    fig = go.Figure()


    fig.add_trace( go.Pie(
                    labels=data_casos_grupo_edad_mf['Grupo de edad'],
                    values=data_casos_grupo_edad_mf[fecha_grupo_edad],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                    marker=dict(#colors=colors, 
                                line=dict(color='#000000', width=2)))

                 )


    fig.add_trace (go.Pie(
                    labels=data_div_edad['Division Edad'],
                    values=data_div_edad['Total Casos'],
                    hoverinfo='label+percent', 
                    textfont_size=12,
                     visible=False,
                    marker=dict(#colors=colors, 
                                line=dict(color='#000000', width=2)))

                  )



    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Casos por Grupos",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Procentaje Casos por Edad",
                                "annotations": []}]),
                    dict(label="Distribución por Edad",
                         method="update",
                         args=[{"visible": [False,True]},
                               {"title": "Procentaje Casos por Distribución por Edad",
                                "annotations": []}]),

                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text="Procentaje de Casos")

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

    #GRAFICO2
    fig2 = casos_grupo_edad()



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





    return render(request,"casos_grupo.html", {"num_recuFIS":num_recuFIS,"grafico1":graph1,"grafico3":graph3,"grafico4":graph4,"fecha_casos_fall":fecha_grupo_edad_2,"grafico2":graph2,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})
