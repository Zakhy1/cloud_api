from rest_framework import permissions


class CustomIsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
        # return obj.owner == request.user or request.user in obj.accesses
