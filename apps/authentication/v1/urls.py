from django.urls import path
from apps.authentication.v1.views.sigin import MobileSetApiView, SetOtpCode

urlpatterns = [
    path('setmobileApi', MobileSetApiView.as_view(), name='setmobileApi'),
    path('setotpApi', SetOtpCode.as_view(), name='setotpApi'),

]


