from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .mixins import ResidentRequiredMixin, SpecialistRequiredMixin, TSZHMemberRequiredMixin


class ResidentDashboardView(ResidentRequiredMixin, TemplateView):
    template_name = 'users/dashboards/resident.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте данные для жильца
        return context


class SpecialistDashboardView(SpecialistRequiredMixin, TemplateView):
    template_name = 'users/dashboards/specialist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте данные для специалиста
        return context


class TSZHDashboardView(TSZHMemberRequiredMixin, TemplateView):
    template_name = 'users/dashboards/tszh.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте данные для члена ТСЖ
        return context
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return '/'
