from rest_framework import serializers
from apps.user.models import CustomUser as User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class MobileSetSerializer(serializers.Serializer):
    mobile = serializers.CharField(write_only=True, required=True)

    def validate_mobile(self, mobile):
        if mobile.startswith('09'):
            return mobile
        raise serializers.ValidationError('Mobile must start with 09.')


class VerifyOTPSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)



class MobileRegisterSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    

    def validate_mobile(self, value):
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("This mobile is already registered.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        # here data has all the fields which have validated values
         # so we can create a User instance out of it
        user = User(**data)
         
        # get the password from the data
        password = data.get('password')
         
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
         
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(MobileRegisterSerializer, self).validate(data)    
    

class SetInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
