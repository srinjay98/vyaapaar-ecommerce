from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == 'seller'
        )


class IsSellerOrReadOnly(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        # Allow read-only requests
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Allow only product owner
        return obj.seller == request.user