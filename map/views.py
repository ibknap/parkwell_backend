from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render


class Map(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "map/map.html"

    def get(self, request, search, *args, **kwargs):
        context = {}
        context['search'] = search
        return render(request, self.template_name, context)