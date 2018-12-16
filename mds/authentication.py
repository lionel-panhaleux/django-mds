import jwt
from django.contrib.auth.models import EmptyManager, Group, Permission
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .server.settings import JWT_AUTH


class JwtUser:
    """
    See django.contrib.auth.models.AnonymousUser
    """

    id = None
    pk = None
    username = ""
    is_staff = False
    is_active = False
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def __init__(self, sub):
        self.id = sub

    def __str__(self):
        return "JwtUser {}".format(self.id)

    def save(self):
        raise NotImplementedError("Not provided for JwtUser.")

    def delete(self):
        raise NotImplementedError("Not provided for JwtUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Not provided for JwtUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Not provided for JwtUser.")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return False

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username


class StatelessJwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        encoded_jwt = self.extract_token(request)
        if encoded_jwt is None:
            return None

        try:
            payload = self.decode_jwt(encoded_jwt)
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
        """
        if not payload["sub"]:
            msg = _("Invalid payload.")
            raise exceptions.AuthenticationFailed(msg)

        return JwtUser(payload["sub"])

    @staticmethod
    def decode_jwt(encoded_jwt):
        if JWT_AUTH["JWT_PUBLIC_KEY"]:
            return jwt.decode(
                encoded_jwt, JWT_AUTH["JWT_PUBLIC_KEY"], algorithms="RS256"
            )

        if JWT_AUTH["JWT_SECRET_KEY"]:
            return jwt.decode(
                encoded_jwt, JWT_AUTH["JWT_SECRET_KEY"], algorithms="HS256"
            )

        raise Exception("JWT authentication configuration is incomplete")

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
