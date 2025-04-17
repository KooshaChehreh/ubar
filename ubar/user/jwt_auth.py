import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from user.models.user import User


def generate_access_token(user: User) -> str:
    """
    Generate a JWT access token for the given user.
    Args:
        user (User): The user for which the JWT token is to be generated.

    Returns:
        str: A signed JWT token.
    """
    time_now = timezone.now()
    base_payload = {
        "exp": time_now + timedelta(seconds=settings.JWT_EXPIRATION_SECS),  # Expiration time
        "iat": time_now,  # Issued at
        "id": user.id, 
        "phone": user.phone,  
    }

    token = jwt.encode(
        base_payload,
        settings.JWT_PRIVATE_KEY,
        "RS256",
    )

    return token

