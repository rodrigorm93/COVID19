"""COVID19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from COVID19.vistas.menu import menu
from COVID19.vistas.predicciones import total_defunciones_chile,modelo_predictivo
from COVID19.vistas.ventiladores import pacientes_ventiladores,num_ventiladores
from COVID19.vistas.grupo_edad import busqueda_fallecidos_por_grupo,busqueda_por_grupo_edad,busqueda_hosp_por_grupo
from COVID19.vistas.regiones import busqueda_region,examenes_pcr
from COVID19.vistas.mapa_comunas import mapa_comunas,mapa_comunas_busqueda
from COVID19.vistas.mapa_regiones import mapa_region
from COVID19.vistas.cuarentenas import cuarentenas_activas
from COVID19.vistas.mapa_mundo import mapa_mundo
from COVID19.vistas.evolucionCasosRegiones import regiones
from COVID19.vistas.hopitalizacionesRegiones import busqueda_hospitalizacion_region
from COVID19.vistas.casos_criticos import casos_criticos
from COVID19.vistas.casos_grupo_edad import busqueda_casos_por_grupo


urlpatterns = [
    path('', mapa_comunas),
    path('region/', regiones),
    path('buscar_region/', busqueda_region),
    path('Hospitalizacion/', busqueda_hospitalizacion_region),
    path('grupo_casos/', busqueda_casos_por_grupo),
    path('grupo_fallecidos/', busqueda_fallecidos_por_grupo),
    path('buscar_grupo_edad/', busqueda_por_grupo_edad),
    path('grupo_hosp/', busqueda_hosp_por_grupo),
    path('ventiladores/', num_ventiladores),
    path('n_casos_criticos/', casos_criticos),
    path('menu/', menu),
    path('defunciones_chile/', total_defunciones_chile),
    path('predicciones/', modelo_predictivo),
    path('examenes_pcr/', examenes_pcr),
    path('pacientes_vmi/', pacientes_ventiladores),
    path('mapa_comunas/', mapa_comunas),
    path('mapa_comunas_busqueda/', mapa_comunas_busqueda),
    path('cuarentenas_mapa/', cuarentenas_activas),
    path('mapa_regiones/', mapa_region),
    path('casos_mapa_mundo/', mapa_mundo),

    

    
]
