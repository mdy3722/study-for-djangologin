# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager, Permission
from django.utils import timezone

"""
장고의 기본 사용자 모델을 확장하여 CustomUser 생성
이때 username은 장고의 기본적인 AbstractUser모델의 username필드인데 우리는 사용 안하니까 None으로..
groups, user_permissions : 장고의 기본 권한 시스템 관련 필드,, 잘 모름
super user : 모든 관리 권한을 갖는 사용자

"""

# 유저 관리자, 슈퍼유저 생성 코드
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nickname, password, **extra_fields)

# 마인더리 앱의 사용자
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True, default='default_nickname')
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    USERNAME_FIELD = 'email'    # 우리 앱에서의 사용자 조회 시 사용되는 필드는 이메일 필드, 즉 이메일 필드를 사용자명으로 사용
    REQUIRED_FIELDS = ['nickname']

    objects = CustomUserManager()  # 커스텀 매니저 설정

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
