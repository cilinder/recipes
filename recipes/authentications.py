from rest_framework.authentication import TokenAuthentication


class BearerAuthentication(TokenAuthentication):
    """
    Custom authentication to use Bearer token
    """
    keyword="Bearer"
