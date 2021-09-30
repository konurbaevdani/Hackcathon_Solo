from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=1, required=True)
    password_confirm = serializers.CharField(min_length=1, required=True)
    name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Адрес уже зарегистрирован')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, attrs):
        user = User.objects.create_user(**attrs)
        user.create_activation_code()
        user.send_activation_mail()
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=1, max_length=8, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email,
                                   activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=1)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с такой почтой не существует')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
             user = authenticate(username=email,
                                 password=password,
                                 request=request)
             if not user:
                 raise serializers.ValidationError('Неверный email или пароль >:-(')
        else:
            raise serializers.ValidationError('Email и пароль обязательны')
        attrs['user'] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User do not registered')
        return email

    def send_new_pass(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        send_mail('Password recovery',
                  f'Your new password: {password}',
                  'test@test.com',
                  [email])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old(self, old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Неверный пароль')
        return old_pass

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_pass(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
