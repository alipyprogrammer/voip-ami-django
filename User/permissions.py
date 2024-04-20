from rest_framework.permissions import BasePermission ,SAFE_METHODS
from .models import User


# class IsManger(BasePermission):
#     def has_object_permission(self ,request, view):
#         return bool( 
#             request.method in SAFE_METHODS or
#             request.user and
#             request.user.Manager
#         )

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Manager)



class ListeningHamkadehPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.isListeningHamkadeh)





class Listening5040Permission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.isListening5040)


class ForwardPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.isForward)




class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):


        if request.method in SAFE_METHODS :
            return True

        return obj.author == request.user  

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user  





# class ISBlogManager(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.Manager or request.user.BlogManager )


# class ISProductManager(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.Manager or request.user.ProductManager )

# class ISOrderingManager(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.Manager or request.user.OrderingManager )

