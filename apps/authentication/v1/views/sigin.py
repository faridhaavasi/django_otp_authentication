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

def send_sms(mobile, otp_code):
    print(f"Sending OTP {otp_code} to {mobile}")

class SendOTPApiView(GenericAPIView):
    serializer_class = MobileSetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
    
        mobile = serializer.validated_data['mobile']
        if not mobile:
            return Response({'error': 'Mobile is required'}, status=status.HTTP_400_BAD_REQUEST)
        mobile_is_available = user.objects.filter(mobile=mobile).exists()
        if mobile_is_available:
            return Response('you are mobile_is_available you can login')

        otp_code = f"{random.randint(100000, 999999)}"

        refresh = RefreshToken.for_user(request.user)    
        refresh['mobile'] = mobile  
        token = str(refresh.access_token)

        OTP.objects.create(
            mobile=mobile,
            defaults={'token': token, 'code': otp_code}
        )

        sms_thread = threading.Thread(target=send_sms, args=(mobile, otp_code))
        sms_thread.start()

        return Response({'token': token}, status=status.HTTP_200_OK)



class VerifyOTPApiView(GenericAPIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serialzer = self.serializer_class(data=request.data)
        code = serialzer.validated_data['otp']
        token = serialzer.validated_data['token']
        if not token or not code:
            return Response({'error': 'Token and code are required'}, status=status.HTTP_400_BAD_REQUEST)


        otp_is_avalible = OTP.objects.get(code=code)
        if otp_is_avalible:
            token = otp_is_avalible.token
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            mobile = validated_token.get('mobile')
            user = user(
                mobile=mobile,
                is_verify = True,
                is_active = False,
            )
            user.save()
            return Response({'message': 'registred and you can complet information', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterApiView(GenericAPIView):
    serializer_class = MobileRegisterSerializer
    def post(self, request):
        Serializer = self.serializer_class(data=request.data)
        if Serializer.is_valid():
            token = Serializer.validated_data['token']
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            mobile = validated_token.get('mobile')
            user.objects.create_user(
                mobile = mobile, 
                password = Serializer.validated_data['password'], 
                is_active = True
            )
            return Response({'message': 'registered ! you can set information'}, status=status.HTTP_200_OK)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetInformationApiView(GenericAPIView):
    serializer_class = SetInformationSerializer
    def put(self, request):
        user_obj = user.objects.get(pk=request.user.id)

        serializer = self.serializer_class(instance=user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response({"message": "User information updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






