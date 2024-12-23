import random
import threading
import uuid
from datetime import timedelta
from django.utils.timezone import now
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.authentication.models import OTP
from apps.user.models import CustomUser as User
from apps.authentication.v1.serializers.sigin_serializers import (
    MobileSetSerializer,
    VerifyOTPSerializer,
    SetInformationSerializer
)

def send_sms_otp(mobile: str, otp: str):
    '''
    send sms to mobile
    '''
    print(f'Sending OTP {otp} to {mobile}') 

class MobileSetApiView(GenericAPIView):
    serializer_class = MobileSetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            user_mobile = User.objects.filter(mobile=mobile).exists()
            if user_mobile:
                return Response({'message': 'You have already registered, please login.'}, status=status.HTTP_303_SEE_OTHER)
            
            recent_otp = OTP.objects.filter(mobile=mobile, created_at__gte=now() - timedelta(minutes=3)).exists()
            if recent_otp:
                return Response({'message': 'Please wait before requesting another OTP'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            token = str(uuid.uuid4())
            otp_send = random.randint(100000, 999999)
            OTP.objects.create(token=token, mobile=mobile, code=otp_send)

            threading.Thread(target=send_sms_otp, args=(mobile, otp_send)).start()
            User.objects.get_or_create(mobile=mobile)

            return Response({'token': token,'otp': otp_send , 'message': 'OTP sent successfully. Please verify.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetOtpCode(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            code = serializer.validated_data['code']
            mobile = OTP.objects.get(token=token).mobile
            
            otp = OTP.objects.filter(token=token, code=code).exists()
            if otp:
                return Response({'message': 'OTP verified successfully', 'token': token}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetInformationApiView(GenericAPIView):
    serializer_class = SetInformationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            mobile = OTP.objects.get(token=token).mobile
            user = User.objects.get(mobile=mobile)
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.email = serializer.validated_data['email']
            user.is_verify = True
            user.set_password(serializer.validated_data['password'])
            user.save()
     
            return Response({'message': 'information  set successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

        