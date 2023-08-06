from .. import models
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse


class EventListView(ListView):
    template_name = "eventsd/event_list.html"

    def get_queryset(self):
        return models.Event.objects.get_open_events().prefetch_related(
            "center"
        )


class EventDetailView(DetailView):
    template_name = "eventsd/event_detail.html"

    def get_queryset(self):
        return models.Event.objects.get_open_events()


class CenterListView(ListView):
    template_name = "eventsd/center_list.html"
    model = models.Center


class CenterJSONListView(View):
    http_method_names = ("get",)
    fields = (
        "id",
        "name",
        "address",
        "lng",
        "lat",
    )

    def get(self, request):
        return JsonResponse(
            {"centers": list(models.Center.objects.values(*self.fields))}
        )
