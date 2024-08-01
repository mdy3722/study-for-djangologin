# accounts/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import EmailVerification, CustomUser
from .serializers import EmailVerificationSendSerializer, EmailVerificationCheckSerializer, UserRegistrationSerializer, CustomAuthTokenSerializer  
import string
import random


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

def generate_temporary_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def send_temporary_password_email(email, temporary_password):
    subject = 'Your New Password'
    message = f'Your new password is {temporary_password}. Please log in and change your password immediately.'
    email_from = 'mdy3722@gmail.com'
    recipient_list = [email,]

    send_mail(subject, message, email_from, recipient_list)
 
def send_username_email(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is {code}. It will expire in 3 minutes.'
    email_from = 'mdy3722@gmail.com'
    recipient_list = [email,]

    send_mail(subject, message, email_from, recipient_list)


@api_view(['POST'])
def send_verification_code(request):
    serializer = EmailVerificationSendSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = f"{random.randint(1000, 9999)}"
        expires_at = timezone.now() + timedelta(minutes=5)
        EmailVerification.objects.create(email=email, code=code, expires_at=expires_at)

        send_username_email(email, code)

        return Response({'message': 'Verification code sent to email.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_code(request):
    serializer = EmailVerificationCheckSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            verification = EmailVerification.objects.get(email=email, code=code)
            if verification.is_expired():
                return Response({'error': 'Verification code expired.'}, status=status.HTTP_400_BAD_REQUEST)
            verification.delete()
            return Response({'message': 'Verification code is valid.'}, status=status.HTTP_200_OK)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인과 로그아웃 - 아직 테스트 X
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 토큰 갱신 -> refresh를 request로 보내면 access 토큰을 새로 발급해줌
@api_view(['POST'])
def token_refresh(request):
    refresh_token = request.data.get('refresh')
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
        return Response({'access': new_access_token}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 새 비밀번호 
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    temporary_password = generate_temporary_password()
    user.set_password(temporary_password)
    user.save()
    
    send_temporary_password_email(email, temporary_password)

    return Response({'message': 'New password sent to email.'}, status=status.HTTP_200_OK)