from typing import Set, Optional

import jwt
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from mds.server.settings import JWT_AUTH
from .jwt_decode import jwt_multi_decode
from ..blacklist.models import BlacklistedToken


class JwtUser:
    """
    Inspired by django.contrib.auth.models.AnonymousUser
    """

    _id: str
    _scopes: Set[str] = set()
    _provider_id: Optional[str] = None
    """If provided, restrict access to data owned by given provider"""

    def __init__(self, sub, scopes, provider_id):
        self._id = sub
        self._scopes = scopes
        self._provider_id = provider_id

    def __str__(self):
        return "JwtUser {}".format(self._id)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return "admin" in self._scopes

    @property
    def scopes(self):
        return self._scopes

    @property
    def provider_id(self):
        return self._provider_id


class StatelessJwtAuthentication(BaseAuthentication):
    public_keys = []
    secret_keys = []

    def __init__(self) -> None:

        if JWT_AUTH["JWT_PUBLIC_KEYS"]:
            delimiter = "-----END PUBLIC KEY-----"
            self.public_keys = [
                k + delimiter for k in JWT_AUTH["JWT_PUBLIC_KEYS"].split(delimiter) if k
            ]

        if JWT_AUTH["JWT_SECRET_KEYS"]:
            self.secret_keys = [
                k.strip() for k in JWT_AUTH["JWT_SECRET_KEYS"].split(" ") if k
            ]

    def authenticate(self, request):
        encoded_jwt = self.extract_token(request)
        if encoded_jwt is None:
            return None

        try:
            payload = jwt_multi_decode(self.public_keys, self.secret_keys, encoded_jwt)
        except jwt.ExpiredSignature:
            msg = _("Signature has expired.")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _("Error decoding signature.")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.build_user(payload)

        return user, None

    @staticmethod
    def build_user(payload):
        """
        Returns a user from the JWT payload

        Fields looked-for in the payload:
            * sub (required): identifier for the owner of the token. Could be a human user, a provider's server, ...
            * jti (required): identifier for the JWT (make it possible to blacklist the token)
            * scopes (required): space-delimited permissions
            * provider_id (optional, required for provider): asked by https://github.com/CityOfLosAngeles/mobility-data-specification/tree/dev/agency#authorization
        """
        required_fields = {"sub", "jti", "scopes"}
        missing_fields = required_fields - payload.keys()

        if missing_fields:
            msg = _("Invalid payload, missing fields: %(fields)s")
            raise exceptions.AuthenticationFailed(
                msg % {"fields": ", ".join(missing_fields)}
            )

        # Possible optimization: add (couple of minutes) cache on blacklist retrieval
        try:
            BlacklistedToken.objects.get(pk=payload["jti"])
            msg = _("Blacklisted token.")
            raise exceptions.AuthenticationFailed(msg)
        except BlacklistedToken.DoesNotExist:
            # We are good !
            pass

        # See https://tools.ietf.org/html/rfc6749#section-3.3
        scopes = set(payload["scopes"].split(" "))

        return JwtUser(payload["sub"], scopes, payload.get("provider_id", None))

    @staticmethod
    def extract_token(request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        auth_header_prefix = "Bearer ".lower()
        auth = smart_text(auth_header)

        if not auth.lower().startswith(auth_header_prefix):
            return None

        return auth[len(auth_header_prefix) :]
