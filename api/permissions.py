from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)
    



#     # super().has_permission(request, view)
# from rest_framework.permissions import BasePermission, SAFE_METHODS

# class IsAdminOrReadOnly(BasePermission):
#     """
#     فقط سوپر یوزرها اجازه POST/PUT/PATCH/DELETE دارند.
#     بقیه فقط GET/HEAD/OPTIONS.
#     """
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_superuser)
