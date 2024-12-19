from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
import random
import threading
import uuid
from apps.authentication.models import OTP
from apps.user.models import CustomUser as User
from apps.authentication.v1.serializers.sigin_serializers import (
    MobileRegisterSerializer, 
    MobileSetSerializer, 
    VerifyOTPSerializer,
    SetInformationSerializer,
    )
def send_sms_otp(mobile: str, otp: str):
    '''
        send sms otp in mobile number by kavenegar
    '''
    return f'send {otp} in {mobile}'


class MobileSetApiView(GenericAPIView):
    serializer_class = MobileSetSerializer
    def post(self, request):
        seriaizer = self.serializer_class(data=request.data)
        if seriaizer.is_valid():
            mobile = seriaizer.validated_data['mobile']
            user_mobile = User.objects.filter(mobile=mobile).exists() # bool
            if user_mobile:
                return Response({'meesage': 'You have already registered, please login.'})
            else:
                user = User(mobile=mobile)
                user.save()
                token = str(uuid.uuid4())
                otp_send = random.randint(100000, 999999)
                OTP.objects.create(token=token,mobile=mobile, code=otp_send)
                threading.Thread(send_sms_otp,args=(mobile, otp_send)).start()
                return Response({'token': token, 'otp': otp_send})
        return Response(seriaizer.errors)

class SetOtpCode(GenericAPIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        seriaizer = self.serializer_class(data=request.data)
        if seriaizer.is_valid():
            token = seriaizer.validated_data['token']
            code = seriaizer.validated_data['code']
            otp = OTP.objects.filter(token=token, code=code).exists()
            if otp:
                return Response({'message': 'otp is valid'})
            return Response({'message': 'otp is invalid'})
        return Response(seriaizer.errors)
    
