from rest_framework.permissions import SAFE_METHODS, BasePermission

# Create your views here.
class DefaultWritePermission(BasePermission):
    message = 'Editing products is restricted to staff users only'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class ObjectLevelOrderGetPermission(BasePermission):
    message = 'Editing order is restricted to staff users only'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS and request.user == obj.OrderCustomerId:
            return True
        return False


class ObjectLevelOrderItemGetPermission(BasePermission):
    message = 'Editing order is restricted to staff users only'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS and request.user == obj.OrderId.OrderCustomerId:
            return True
        return False


class OrderPostPermission(BasePermission):
    message = 'Editing order is restricted to staff user or user issuing POST request'

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return True
        return request.user.is_staff


class StaffPermission(BasePermission):
    message = 'This operation is restricted to staff user only'

    def has_permission(self, request, view):
        return request.user.is_staff


class PaymentPermission(BasePermission):
    message = 'Editing payment is restricted to staff and payment creator only'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        try:
            if request.user == obj.PaymentOrderId.OrderCustomerId:
                return True
        except:
            return False
        return False


class CouponPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.method in SAFE_METHODS + ['PUT']:
            return True
        return False