from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('list/<categoryname>', views.list, name='list'),
    path('article/<articleid>', views.article, name='article'),
    path('comment/<articleid>/', views.comment, name='comment'),
    path('admin/', views.admin, name='admin'),
    path('adminsetting/', views.adminsetting, name='adminsetting'),
    path('<userName>/', views.homepage, name='homepage'),
    path('<userName>/addarticle/', views.addarticle, name='addarticle'),
    path('<userName>/updarticle/<articleid>/', views.updarticle, name='updarticle'),
    path('<userName>/delarticle/<articleid>/', views.delarticle, name='delarticle'),
]
