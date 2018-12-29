from django.db import models


class BlacklistedToken(models.Model):
    """A blacklisted JWT
    """

    id = models.CharField(primary_key=True, max_length=50)
    added = models.DateTimeField(auto_now=True)
