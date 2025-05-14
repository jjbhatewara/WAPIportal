from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("calllist", views.calllist, name="calllist"),
    path("calllist/<int:call_id>/update_status", views.update_call_status, name="update_call_status"),
    path("jobsheet", views.jobsheet, name="jobsheet"),
]