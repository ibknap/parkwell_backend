from django.http.response import JsonResponse
from django.views.generic import TemplateView, View


class Map(TemplateView):
    template_name = "map/map.html"