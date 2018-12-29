from rest_framework import routers, viewsets

from . import models
from . import serializers


class BlacklistedToken(viewsets.ModelViewSet):
    queryset = models.BlacklistedToken.objects.all()
    serializer_class = serializers.BlacklistedTokenSerializer


router = routers.DefaultRouter()
router.register(r"tokens", BlacklistedToken)

urls = router.urls
