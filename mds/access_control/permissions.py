from rest_framework.permissions import BasePermission

from mds.access_control.authenticate import RemoteUser


def require_scopes(*required_roles):
    class ScopePermission(BasePermission):
        """
        Allows access only to authenticated users with a specific scope
        (or admin rights)
        """

        _required_roles = set(required_roles)

        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False

            if request.user.is_staff:
                return True

            if isinstance(request.user, RemoteUser):
                return self._required_roles.issubset(request.user.scopes)

            return False

    return ScopePermission
