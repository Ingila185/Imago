from django.urls import path
from .views import search_imago_data

urlpatterns = [
    path('imago-search/', search_imago_data, name='search_imago_data'),
]