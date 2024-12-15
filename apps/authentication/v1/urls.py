from django.urls import path
from apps.authentication.v1.views.sigin import MobileSetApiView

urlpatterns = [
    path('setmobileApi', MobileSetApiView.as_view(), name='setmobileApi'),

]


