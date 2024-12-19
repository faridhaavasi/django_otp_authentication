from django.urls import path
from apps.authentication.v1.views.sigin import MobileSetApiView, SetOtpCode, SetInformationApiView
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('setmobileApi', MobileSetApiView.as_view(), name='setmobileApi'),
    path('setotpApi', SetOtpCode.as_view(), name='setotpApi'),
    path('setinformationApi', SetInformationApiView.as_view(), name='setinformationApi'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]


