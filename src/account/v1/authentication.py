from django.core.cache import cache

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomAuthentication(JWTAuthentication):

    def get_validated_token(self, token):
        validated_token = super().get_validated_token(token)

        jti = validated_token["jti"]

        if cache.get(f"blacklist_{jti}"):
            raise AuthenticationFailed("Token is blacklisted")

        return validated_token
