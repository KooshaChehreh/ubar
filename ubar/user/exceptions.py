from rest_framework.exceptions import APIException


class AccountSuspended(APIException):
    status_code = 400
    default_code = "account_suspended"
    default_detail = {
        "code": default_code,
        "message": "حساب کاربری تعلیق شده است و امکان ورود وجود ندارد.",
    }


class InvalidPhoneOrOTP(APIException):
    status_code = 400
    default_code = "invalid_phone_or_otp"
    default_detail = {
        "code": default_code,
        "message": "کد یا شماره وارد شده اشتباه است.",
    }


class InvalidPhoneOrPassword(APIException):
    status_code = 400
    default_code = "invalid_phone_or_password"
    default_detail = {
        "code": default_code,
        "message": "کلمه عبور یا شماره وارد شده اشتباه است.",
    }


class OTPExpired(APIException):
    status_code = 400
    default_code = "otp_expired"
    default_detail = {
        "code": default_code,
        "message": "کد منقضی شده است.",
    }


class PhoneLimited(APIException):
    status_code = 400
    default_code = "phone_limited"
    default_detail = {
        "code": default_code,
        "message": "این شماره تلفن به دلیل ورود بیش از اندازه کد اشتباه، موقتا مسدود شده است.",
    }


class PhoneNowLimited(APIException):
    status_code = 400
    default_code = "phone_now_limited"
    default_detail = {
        "code": default_code,
        "message": "شماره به دلیل ورود بیش از اندازه کد اشتباه، موقتا مسدود شد.",
    }


class WaitToResendOTP(APIException):
    status_code = 400
    default_code = "wait_for_resend_otp"
    default_detail = {
        "code": default_code,
        "message": "کد قبلی هنوز منقضی نشده است. برای دریافت کد جدید منتظر بمانید و مجددا درخواست دهید.",
    }

