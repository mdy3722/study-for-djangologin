# accounts/serializers.py
import re  # re : 정규 표현식을 지원하는 모듈. 문자열의 패턴 매칭, 검색, 치환 등을 수행 가능
from rest_framework import serializers
from .models import CustomUser, EmailVerification

class EmailVerificationSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmailVerificationCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'password']

    def validate_password(self, value):
        """
        비밀번호가 8~12 자리 영소문자, 숫자, 특수문자 조합으로 이루어졌는지 검증합니다.
        """
        if not re.match(r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', value):
            raise serializers.ValidationError(
                "비밀번호는 8~12 자리의 영소문자, 숫자, 특수문자 조합이어야 합니다."
            )
        return value    

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()