from django.core.exceptions import PermissionDenied

class ResidentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_resident:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class SpecialistRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_specialist:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class TSZHMemberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_tszh_member:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)