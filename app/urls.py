from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_category/', views.create_category, name='create_category'),
    path('add_keyword/', views.add_keyword, name='add_keyword'),
    path('run_program/', views.run_program, name='run_program'),
    path('results/', views.results, name='results'),
    path('download_csv/', views.download_csv, name='download_csv'),
]
