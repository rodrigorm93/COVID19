from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render



import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from plotly.subplots import make_subplots


data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
data_crec_por_dia = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')



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



#***************************MENU**************************************
#Lenar con 0 filas nulas
data_chile_r = data_chile_r.fillna(0)

ultima_fecha_cl = data_chile.columns
ultima_fecha_cl= ultima_fecha_cl[-1]

ultima_fecha_cl_r = data_chile_r.columns
ultima_fecha_cl_r= ultima_fecha_cl_r[-1]


ultima_fecha_region_fallecidos = fallecidos_por_region.columns
ultima_fecha_region_fallecidos= ultima_fecha_region_fallecidos[-1]

nultima_fecha_region_fallecidos = fallecidos_por_region.columns
ultima_fecha_region_fallecidos= ultima_fecha_region_fallecidos[-1]

num_cases_cl = data_chile.drop([16],axis=0)
num_cases_cl_data = num_cases_cl[ultima_fecha_cl].sum()



num_death_data =  grupo_fallecidos[ultima_fecha_cl].sum()

casos_act_data = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()


#recuperados
num_recuFIS_data = data_crec_por_dia[data_crec_por_dia['Fecha']=='Casos recuperados por FIS'][ultima_fecha_cl_r].sum()

num_recuFIS = int_format(int(num_recuFIS_data))
num_cases_cl = int_format(int(num_cases_cl_data))
num_death = int_format(int(num_death_data))
casos_act = int_format(int(casos_act_data))


fecha_casos = ' ('+ultima_fecha_cl+')'



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
    
    return render(request,"num_examenes_pcr.html", {"grafico1":graph1,"grafico2":graph2,"num_recuFIS":num_recuFIS,"fecha_casos":fecha_casos,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})
