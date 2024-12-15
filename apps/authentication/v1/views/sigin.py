from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
import random
import threading
from apps.authentication.models import OTP
from apps.user.models import CustomUser as user
from apps.authentication.v1.serializers.sigin_serializers import (
    MobileRegisterSerializer, 
    MobileSetSerializer, 
    VerifyOTPSerializer,
    SetInformationSerializer,
    )




