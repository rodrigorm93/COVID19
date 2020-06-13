from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

from django.shortcuts import render



import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px



from plotly.subplots import make_subplots

import warnings


data_chile = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
data_chile_r = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
grupo_fallecidos = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario.csv')
fallecidos_reg = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo_T.csv')
fallecidos_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto14/FallecidosCumulativo.csv')
casos_diarios_por_region = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo.csv')
casos_diarios_por_regionT = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv')


comb = pd.merge(casos_diarios_por_regionT,fallecidos_reg, how='outer', on=['Region', 'Region'])
comb= comb.fillna(0)

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
#ver el caso de que no se actualicen los registros


casos_act = data_chile_r[data_chile_r['Fecha']=='Casos activos'][ultima_fecha_cl_r].sum()
#dejar el ulktimo registro de recuperados que fue el 2020-06-02



num_cases_cl = str(int(num_cases_cl))+' ('+ultima_fecha_cl+')'
num_death = str(int(num_death))+' ('+ultima_fecha_cl+')'
casos_act = str(int(casos_act))+' ('+ultima_fecha_cl_r+')'

casos_diarios_por_region = casos_diarios_por_region.drop(16, axis=0)

fecha_casos_fall='('+data_chile.columns[-1]+')'
fecha_casos_region = casos_diarios_por_region.columns[-1]
fecha_casos_region = casos_diarios_por_region.loc[:, '2020-03-03': fecha_casos_region]
fecha_casos_region = fecha_casos_region.keys()
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

    #GRAFICO 2: ANIMACION
    gris = '#393e46' 
    rojo = '#ff2e63' 

    data_total_ar = pd.DataFrame({'Region': ('Arica'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': arica,
                              'Fallecidos':comb['Arica y Parinacota_y'].values })

    data_total_ta = pd.DataFrame({'Region': ('Tarapacá'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': tarapaca,
                                'Fallecidos':comb['Tarapacá_y'].values})
    data_total_at = pd.DataFrame({'Region': ('Antofagasta'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': antofagasta,
                                'Fallecidos':comb['Antofagasta_y'].values})
    data_total_ata = pd.DataFrame({'Region': ('Atacama'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': atacama,
                                'Fallecidos':comb['Atacama_y'].values})
    data_total_co = pd.DataFrame({'Region': ('Coquimbo'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': coquimbo,
                                'Fallecidos':comb['Coquimbo_y'].values})
    data_total_va = pd.DataFrame({'Region': ('Valparaíso'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': valparaiso,
                                'Fallecidos':comb['Valparaíso_y'].values})
    data_total_me = pd.DataFrame({'Region': ('Metropolitana'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': metropolitana,
                                'Fallecidos':comb['Metropolitana_y'].values})
    data_total_og = pd.DataFrame({'Region': ('O Higgins'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': o_Higgins,
                                'Fallecidos':comb['O’Higgins_y'].values})
    data_total_mau = pd.DataFrame({'Region': ('Maule'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': maule,
                                'Fallecidos':comb['Maule_y'].values})
    data_total_nu = pd.DataFrame({'Region': ('Ñuble'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': nuble,
                                'Fallecidos':comb['Ñuble_y'].values})
    data_total_bi = pd.DataFrame({'Region': ('Biobío'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': biobio,
                                'Fallecidos':comb['Biobío_y'].values})
    data_total_ara = pd.DataFrame({'Region': ('Araucanía'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': araucania,
                                'Fallecidos':comb['Araucanía_y'].values})
    data_total_lr = pd.DataFrame({'Region': ('Los Ríos'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': los_Ríos,
                                'Fallecidos':comb['Los Ríos_y'].values})
    data_total_ll = pd.DataFrame({'Region': ('Los Lagos'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': los_lagos,
                                'Fallecidos':comb['Los Lagos_y'].values})
    data_total_ay = pd.DataFrame({'Region': ('Aysén'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': aysen,
                                'Fallecidos':comb['Aysén_y'].values})
    data_total_ma = pd.DataFrame({'Region': ('Magallanes'),'Fecha': pd.to_datetime(fecha_casos_region),'Casos': magallanes,
                                'Fallecidos':comb['Magallanes_y'].values})


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
    temp = temp.groupby(['Region', 'Fecha'])['Casos','Fallecidos'].sum().reset_index()
    temp = temp.melt(id_vars=['Region', 'Fecha'], value_vars=['Casos','Fallecidos'], 
                    var_name='Casos', value_name='Count')

    fig = px.bar(temp, y='Region', x='Count', color='Casos', barmode='group', orientation='h',
                text='Count', title='Evolución del Número de Casos por Región', animation_frame='Fecha',
                height=900,color_discrete_sequence= [gris,rojo], range_x=[0, int(metropolitana[-1]+1000)])
    fig.update_traces(textposition='outside')
    fig.update_xaxes(title_text="Número de Casos (acumulados)")
    fig.update_yaxes(title_text="Regiones")

    graph1 = fig.to_html(full_html=False)


    return render(request,"region.html", {"grafico1":graph1,"fecha_casos_fall":fecha_casos_fall,"n_casos":num_cases_cl,"num_rec":casos_act, "num_death":num_death})







