from rest_framework import permissions
from .models import Profile

class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        else:
            return False

class ProfileExists(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = Profile.objects.filter(user=request.user).all()
        if not profile:
            return True
        else:
            return False
