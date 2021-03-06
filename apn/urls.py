"""apn URL Configuration

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
from django.urls import include, path
from rest_framework import routers
from apn.negocios import views

router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'contatos', views.ContatoViewSet)
router.register(r'negocios/categorias', views.NegocioCategoriaViewSet)
router.register(r'negocios/regioes-entrega', views.NegocioRegiaoEntregaViewSet)
router.register(r'negocios/(?P<negocio_id>\d+)/contatos',
                views.ContatoViewSet)
router.register(r'negocios/(?P<negocio_id>\d+)/produtos',
                views.ProdutoViewSet)
router.register(r'negocios', views.NegocioViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'regioes-entrega', views.RegiaoEntregaViewSet)
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.home),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
