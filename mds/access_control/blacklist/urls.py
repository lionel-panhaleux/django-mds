from rest_framework import routers, viewsets

from ..authentication.permissions import require_scopes
from ..authentication.scopes import SCOPE_ADMIN

from . import models
from . import serializers


# class BlacklistPermission(BasePermission):
#     """
#     Allows access only to authenticated users.
#     """
#
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated
#


class BlacklistedToken(viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_ADMIN),)
    queryset = models.BlacklistedToken.objects.all()
    serializer_class = serializers.BlacklistedTokenSerializer


router = routers.DefaultRouter()
router.register(r"tokens", BlacklistedToken)

urls = router.urls
