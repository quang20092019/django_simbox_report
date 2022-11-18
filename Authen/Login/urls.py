from django.urls import path
from .views import IndexClass, LoginClass,ViewUser,ViewProduct,Register,forgotmk
from . import views
urlpatterns = [
    path('', IndexClass.as_view(), name ='IndexClass'),
    path('login', LoginClass.as_view(), name ='login'),
    path('logout', views.logout_request,name = "logout"),
    path('download_csv', views.download_csv,name = "download_csv"),
    path('cdr', views.csv_search,name = "cdr"),
    path('forgotmk', forgotmk.as_view(),name = "forgotmk"),
    path('register', Register.as_view(), name ='register'),
    path('viewproduct', ViewProduct, name ='viewproduct'),
]