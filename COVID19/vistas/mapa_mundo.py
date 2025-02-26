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

import warnings

warnings.filterwarnings('ignore')



mundo = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
geo_mundo = json.loads(mundo.content)


data_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

ultima_fecha_cl = data_confirmed.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


data_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

ultima_fecha_cl = data_confirmed.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


data_confirmed.loc[data_confirmed['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

data_confirmed.loc[data_confirmed['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
data_confirmed = data_confirmed.append({'Country/Region':'French Guiana',ultima_fecha_cl: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_cl])}, ignore_index=True)

data_confirmed.loc[data_confirmed['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
data_confirmed.loc[data_confirmed['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'

d = data_confirmed.groupby(['Country/Region']).sum()

paises = data_confirmed['Country/Region'].drop_duplicates()
paises = sorted(paises)

data_mundo_mapa = pd.DataFrame({'Country': paises,'Casos':d[ultima_fecha_cl]})



#casos recuperados
ultima_fecha_cl = recoveries_df.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


recoveries_df.loc[recoveries_df['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

recoveries_df.loc[recoveries_df['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
recoveries_df = recoveries_df.append({'Country/Region':'French Guiana',ultima_fecha_cl: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_cl])}, ignore_index=True)

recoveries_df.loc[recoveries_df['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
recoveries_df.loc[recoveries_df['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'



d2 = recoveries_df.groupby(['Country/Region']).sum()

paises = recoveries_df['Country/Region'].drop_duplicates()
paises = sorted(paises)
v = d2[ultima_fecha_cl].apply(str)
data_mundo_mapa_rec = pd.DataFrame({'Country': paises,'Recuperados':v})



#casos fallecidos
ultima_fecha_cl = deaths_data.columns
ultima_fecha_cl= ultima_fecha_cl[-1]


deaths_data.loc[deaths_data['Country/Region'] == 'US', "Country/Region"] = 'United States of America'

deaths_data.loc[deaths_data['Country/Region'] == 'US', "Country/Region"] = 'United States of America'
deaths_data.loc[deaths_data['Country/Region'] == 'Congo (Kinshasa)', "Country/Region"] = 'Democratic Republic of the Congo'

#AGREGAR French Guiana COMO PAIS Y NO PROVICNCIA DE FRANCIA PERO SE SUMAR A EL TOTAL DE FRANCIA IGUAL
deaths_data = deaths_data.append({'Country/Region':'French Guiana',ultima_fecha_cl: int(data_confirmed[data_confirmed['Province/State']=='French Guiana'][ultima_fecha_cl])}, ignore_index=True)

deaths_data.loc[deaths_data['Country/Region'] == "Cote d'Ivoire", "Country/Region"] = 'Ivory Coast'
deaths_data.loc[deaths_data['Country/Region'] == 'Congo (Brazzaville)', "Country/Region"] = 'Republic of the Congo'
deaths_data.loc[deaths_data['Country/Region'] == 'Tanzania', "Country/Region"] = 'United Republic of Tanzania'
deaths_data.loc[deaths_data['Country/Region'] == 'Korea, South', "Country/Region"] = 'South Korea'



d2 = deaths_data.groupby(['Country/Region']).sum()

paises = deaths_data['Country/Region'].drop_duplicates()
paises = sorted(paises)

data_mundo_mapa_death = pd.DataFrame({'Country': paises,'Fallecidos':d2[ultima_fecha_cl]})

data_cd = pd.merge(data_mundo_mapa, data_mundo_mapa_death, on='Country')
data_cdr =  pd.merge(data_cd, data_mundo_mapa_rec, on='Country')

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


casos_mundo = data_confirmed[ultima_fecha_cl].sum()
casos_mundo = int_format(int(casos_mundo))


muertes_mundo = deaths_data[ultima_fecha_cl].sum()
muertes_mundo = int_format(int(muertes_mundo))


recuperados_mundo = recoveries_df[ultima_fecha_cl].sum()
recuperados_mundo = int_format(int(recuperados_mundo))

fecha_casos = ' ('+ultima_fecha_cl+')'


def mapa_mundo(request):

    fig = go.Figure(go.Choroplethmapbox(geojson=geo_mundo, locations=data_cdr.Country, z=data_cdr.Casos,
                                    colorscale="Viridis", zmin=0, zmax=100000,
                                    featureidkey="properties.name",
                                    colorbar = dict(thickness=20, ticklen=3),
                                    marker_opacity=0.2, marker_line_width=0,  
                                    text=data_cdr['Fallecidos'],
                                      hovertemplate = '<b>País</b>: <b>'+data_cdr['Country']+'</b>'+
                                            '<br><b>Casos </b>: %{z}<br>'+
                                            '<b>Fallecidos: </b>:%{text}<br>'+
                                            '<b>Recuperados</b>: <b>'+data_cdr['Recuperados'] 
                                   
                                   
                                   ))



    fig.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=1,height=700,mapbox_center = {"lat": 0, "lon": 0})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    graph1 = fig.to_html(full_html=False)




    return render(request,"mapa_mundo.html", {"fecha_act":ultima_fecha_cl,"fecha_casos":fecha_casos,"grafico1":graph1,"casos_mundo":casos_mundo,"muertes_mundo":muertes_mundo,"recuperados_mundo":recuperados_mundo})
