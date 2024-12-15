from django.urls import path, include


app_name = 'authentication' 
urlpatterns = [
    path('APi-v1/', include('apps.authentication.v1.urls')),

]
