from django.contrib.auth.mixins import PermissionRequiredMixin


class UserIsStaff(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.is_staff