from django.urls import path
from . import views

app_name = "eventsd"

urlpatterns = [
    path("", views.EventListView.as_view(), name="event-list"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event-details"),
    path(
        "<int:pk>/signup/", views.SignupFormView.as_view(), name="event-signup"
    ),
    path(
        "applications/",
        views.ApplicationListView.as_view(),
        name="application-list",
    ),
    path(
        "applications/<int:pk>/",
        views.ApplicationStatusView.as_view(),
        name="application-detail",
    ),
    path(
        "applications/<int:pk>/confirm/",
        views.ApplicationConfirmationView.as_view(),
        name="application-confirm",
    ),
    path("centers", views.CenterListView.as_view(), name="center-list"),
    path(
        "centers.json",
        views.CenterJSONListView.as_view(),
        name="center-list-json",
    ),
]
