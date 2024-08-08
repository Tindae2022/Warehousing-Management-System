from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class SalesManagerRequiredMixins(AccessMixin):
    """
    Verify that the current user is a sales manager
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_sales_manager():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class WarehouseManagerRequiredMixin(AccessMixin):
    """
    Verify that the current user is a sales manager
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_warehouse_manager():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredMixin(AccessMixin):
    """
    Verify that the current user is a customer
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_customer():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class CombinedManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_warehouse_manager or user.is_sales_manager)

    def handle_no_permission(self):
        raise PermissionDenied()


