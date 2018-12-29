from rest_framework import serializers

from . import models


class BlacklistedTokenSerializer(serializers.ModelSerializer):
    """A blacklisted JWT
    """

    id = serializers.CharField(help_text="Unique JWT identifier (jti)")
    added = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.BlacklistedToken
        fields = ("id", "added")
