from rest_framework import permissions
from django.shortcuts import get_object_or_404

from ads.models import Selection, Ad
from users.models import User


class SelectionPermission(permissions.BasePermission):
    message = 'Not permitted current user'

    def has_permission(self, request, view):
        selection = get_object_or_404(Selection, pk=view.kwargs["pk"])
        if selection.owner_id == request.user.id:
            return True
        return False


class AdPermission(permissions.BasePermission):
    message = 'Not permitted current user'

    def has_permission(self, request, view):
        if request.user.role in (User.MEMBER, User.ADMIN):
            return True
        ad = get_object_or_404(Ad, pk=view.kwargs["pk"])
        if ad.author_id == request.user.id:
            return True
        return False
