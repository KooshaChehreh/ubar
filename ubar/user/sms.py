from rest_framework.response import Response
from rest_framework import status


def send_obtain_otp_sms(phone, code):
    print(f"the OTP code {code} is for {phone}")
    return Response(status=status.HTTP_200_OK)

