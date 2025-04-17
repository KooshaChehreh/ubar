import random
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from rest_framework.response import Response
from user.models.otp import OTP
from user.models.user import User, UserLoginAttempt
from user.serializers import (
    LoginObtainOTPInputSerializer,
    LoginVerifyPasswordInputSerializer,
    LoginVerifyOTPInputSerializer,
    ProfileInputSerializer,
    UsersSerializer
    
)
from user.sms import send_obtain_otp_sms
from user.exceptions import *
from user.jwt_auth import (
    generate_access_token,
)
from utils import get_client_ip


@api_view(["POST"])
@authentication_classes([])
def login_obtain_otp(request):
    serializer = LoginObtainOTPInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data["phone"]
    ip_address = get_client_ip(request=request)
    otp_code = random.randint(settings.OTP_LOWER_BOUND, settings.OTP_UPPER_BOUND)
    try:
        otp = OTP.objects.get(phone=phone)
        if otp.limited_at is not None:
            if (timezone.now() - otp.limited_at).seconds > settings.OTP_BAN_TIME_SEC:
                # ban time passed, now unban
                otp.limited_at = None
                otp.save()
            else:
                raise PhoneLimited
        if otp.sent_at is not None:
            if (timezone.now() - otp.sent_at).seconds < settings.OTP_RESEND_DELAY_SEC:
                raise WaitToResendOTP
        otp.delete()
    except OTP.DoesNotExist:
        pass
    response_data = None

    user = User.objects.filter(phone=phone).first()
    if user is None:
        otp = OTP.objects.create(code=otp_code, phone=phone, ip_address=ip_address)
        send_obtain_otp_sms(phone=phone, code=otp_code)
        otp.sent_at = timezone.now()
        otp.save()
        response_data = {
            "verify_by_password_available": False,
            "no_existing_account_with_phone": True,
        }
    else:
        if user.is_suspended():
            raise AccountSuspended
        response_data = {
            "verify_by_password_available": True,
            "no_existing_account_with_phone": False,
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
def login_verify_password(request):
    serializer = LoginVerifyPasswordInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data["phone"]
    password = serializer.validated_data["password"]
    ip_address = get_client_ip(request=request)
    try:
        login_attempt : UserLoginAttempt = UserLoginAttempt.objects.get(ip_address=ip_address)
        target_user: User = User.objects.get(phone=phone)
        if login_attempt.retries_count == settings.PASSWORD_MAX_RETRY_COUNTS:
                target_user.limited_at = timezone.now()
                target_user.save()
                raise UserNowLimited
        
        if target_user.is_suspended():
            raise AccountSuspended
        if not target_user.check_password(entered_password=password):
            login_attempt.retries_count += 1
            raise InvalidPhoneOrPassword

        access_token = generate_access_token(target_user)
        response_data = {
            "access_token": access_token,
            "signup_required": False,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        raise InvalidPhoneOrPassword


@api_view(["POST"])
@authentication_classes([])
def login_verify_otp(request):
    serializer = LoginVerifyOTPInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ip_address = get_client_ip(request=request)
    phone = serializer.validated_data["phone"]
    code = serializer.validated_data["code"]
    try:
        otp: OTP = OTP.objects.get(ip_address=ip_address)
        if otp.limited_at is not None:
            if (timezone.now() - otp.limited_at).seconds > settings.OTP_BAN_TIME_SEC:
                # ban time passed, now unban
                otp.limited_at = None
                otp.save()
            else:
                raise PhoneLimited
        if otp.code != code:
            otp.retries_count += 1
            if otp.retries_count == settings.OTP_MAX_RETRY_COUNTS:
                otp.limited_at = timezone.now()
                otp.save()
                raise PhoneNowLimited
            otp.save()
            raise InvalidPhoneOrOTP

        if (timezone.now() - otp.created_at).seconds > settings.OTP_EXPIRE_TIME_SEC:
            raise OTPExpired
        otp.delete()

        user: User = User.objects.create(phone=phone)
        signup_required = True
        access_token = generate_access_token(user)

        response_data = {
            "access_token": access_token,
            "signup_required": signup_required,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except OTP.DoesNotExist:
        # TODO: add sleep() to avoid timing attacks
        raise InvalidPhoneOrOTP
    


@api_view(["POST"])
def profile(request):
    serializer = ProfileInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data["phone"]
    password = serializer.validated_data["password"]
    email = serializer.validated_data["email"]
    name = serializer.validated_data["name"]
    family = serializer.validated_data["family"]
    
    try:
        target_user: User = User.objects.get(phone=phone)
        if target_user.is_suspended():
            raise AccountSuspended
        
        user_data = {
            "password": password,
            "email": email,
            "name": name,
            "family": family,
        }

        user_serializer = UsersSerializer(target_user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        response_data = {
            "message": "Profile updated successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        raise InvalidPhoneOrPassword