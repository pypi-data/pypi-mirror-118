from django import views
from ..forms import EventSignupForm
from .. import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    UpdateView,
    DetailView,
    ListView,
)
from django.db import transaction


class SignupFormView(
    LoginRequiredMixin,
    views.generic.FormView,
):

    form_class = EventSignupForm
    template_name = "eventsd/signup_form_view.html"

    def dispatch(self, request, *args, **kwargs):
        self.event = self.get_event()
        return super().dispatch(request, *args, **kwargs)

    def get_event(self):
        try:
            return models.Event.objects.get_open_events().get(
                pk=self.kwargs["pk"]
            )
        except ObjectDoesNotExist:
            raise Http404(_("Évènement non trouvé."))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["form_object"] = self.event.form
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["event"] = self.event
        return context

    def form_valid(self, form):
        with transaction.atomic():
            attendee = models.Attendee.objects.create(
                owner=self.request.user,
                event=self.event,
                first_name=form.cleaned_data.pop("first_name"),
                last_name=form.cleaned_data.pop("last_name"),
                dob=form.cleaned_data.pop("dob"),
                status=models.SelectionStatus.ENROLLED.value,
            )

            for (id, value) in form.cleaned_data.items():
                models.FormAnswer.objects.create(
                    attendee=attendee,
                    question_id=int(id),
                    answer=value,
                )

        return super().form_valid(form)


class ApplicationListView(
    LoginRequiredMixin,
    ListView,
):
    template_name = "eventsd/application_list.html"

    def get_queryset(self):
        return (
            models.Attendee.objects.filter(
                owner=self.request.user,
            )
            .order_by("status")
            .prefetch_related()
        )


class ApplicationStatusView(
    LoginRequiredMixin,
    DetailView,
):
    template_name = "eventsd/application_detail.html"

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get("pk")
        obj = get_object_or_404(
            models.Attendee,
            owner=self.request.user,
            id=id,
        )
        return obj


class ApplicationConfirmationView(
    LoginRequiredMixin,
    UpdateView,
):
    fields = ["status"]
    template_name = "eventsd/application_coonfirm.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status_value"] = models.SelectionStatus.CONFIRMED.value
        return context

    def get_object(self):
        return get_object_or_404(
            models.Attendee,
            owner=self.request.user,
            status=models.SelectionStatus.ACCEPTED.value,
            id=self.kwargs.get("pk"),
        )

    def form_valid(self, form):
        if not form.cleaned_data["status"] == models.SelectionStatus.CONFIRMED:
            raise Http404()
        return super().form_valid(form)
