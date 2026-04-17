"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usuarios.views import UsuarioViewSet
from notas.views import (
    ProfesoresView, ProfesoresViewDetalle, MateriasView, MateriasViewDetalle, 
    TrimestresView, TrimestresViewDetalle, CortesView, CortesViewDetalle, 
    NotasView, NotasViewDetalle, EvaluacionesView, EvaluacionesViewDetalle, 
    EstadisticasDashboardView
)
from biblioteca.views import ApuntesView, ApuntesViewDetalle

router = DefaultRouter()
router.register('usuario', UsuarioViewSet, basename='usuarios'), # type: ignore

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='refresh token'),

    #* ===================== VISTA DE NOTAS =====================
    path('api/profesores/', ProfesoresView.as_view(), name='profesores'),
    path('api/profesores/<int:pk>/', ProfesoresViewDetalle.as_view(), name='profesores_detalle'),

    path('api/materias/', MateriasView.as_view(), name='materias'),
    path('api/materias/<int:pk>/', MateriasViewDetalle.as_view(), name='materias_detalle'),

    path('api/trimestres/', TrimestresView.as_view(), name='trimestres'),
    path('api/trimestres/<int:pk>/', TrimestresViewDetalle.as_view(), name='trimestres_detalle'),

    path('api/cortes/', CortesView.as_view(), name='cortes'),
    path('api/cortes/<int:pk>/', CortesViewDetalle.as_view(), name='cortes_detalle'),

    path('api/notas/', NotasView.as_view(), name='notas'),
    path('api/notas/<int:pk>/', NotasViewDetalle.as_view(), name='notas_detalle'),

    path('api/evaluaciones/', EvaluacionesView.as_view(), name='evaluaciones'),
    path('api/evaluaciones/<int:pk>/', EvaluacionesViewDetalle.as_view(), name='evaluaciones_detalle'),

    #* ===================== VISTA DE BIBLIOTECA =====================
    path('api/apuntes/', ApuntesView.as_view(), name='apuntes'),
    path('api/apuntes/<int:pk>/', ApuntesViewDetalle.as_view(), name='apuntes_detalle'),

    #* ===================== DASHBOARD DE NOTAS =====================
    path('api/estadisticas/dashboard/', EstadisticasDashboardView.as_view(), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
