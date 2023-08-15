"""
URL configuration for dev_day project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import add_recipe, add_rating, add_info, realtime_reg, search_recipe

urlpatterns = [
    path('recipe/', add_recipe),
    path('rating/', add_rating),
    path('', add_info),
    path('cv/', realtime_reg),
    path('search/', search_recipe),
]
