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
from user.models.user import User
from user.serializers import (
    LoginObtainOTPInputSerializer,
    LoginVerifyPasswordInputSerializer,
)
from user.sms import send_obtain_otp_sms
from user.exceptions import *
from user.jwt_auth import (
    generate_access_token,
)



@api_view(["POST"])
@authentication_classes([])
def login_obtain_otp(request):
    serializer = LoginObtainOTPInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data["phone"]
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
        response_data = {
            "verify_by_password_available": False,
            "no_existing_account_with_phone": True,
        }
    else:
        if user.is_suspended():
            raise AccountSuspended
        has_password = bool(user.password)
        response_data = {
            "verify_by_password_available": has_password,
            "no_existing_account_with_phone": False,
        }
    otp = OTP.objects.create(code=otp_code, phone=phone)
    send_obtain_otp_sms(phone=phone, code=otp_code)
    otp.sent_at = timezone.now()
    otp.save()
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
def login_verify_password(request):
    serializer = LoginVerifyPasswordInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data["phone"]
    password = serializer.validated_data["password"]
    device_model = serializer.validated_data["device_model"]
    device_ip = serializer.validated_data["device_ip"]
    try:
        target_user: User = User.objects.get(phone=phone)
        if target_user.is_suspended():
            raise AccountSuspended
        if not target_user.check_password(entered_password=password):
            raise InvalidPhoneOrPassword

        access_token, refresh_token = generate_access_token(target_user)
        response_data = {
            "access_token": access_token,
            "signup_required": False,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        raise InvalidPhoneOrPassword
