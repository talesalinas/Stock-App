from django.urls import path
from . import views
# API KEY pk_1bb06023916a4c8093d29b42fb4518a3

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('mystocks', views.mystocks, name="mystocks"),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('delete_stock.html', views.delete_stock, name="delete_stock")
]
