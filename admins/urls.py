from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("customers", views.customers, name="customers"),
    path("customers/add/", views.add_customer, name="add_customer"),
    path("customers/delete/<int:customer_id>/", views.delete_customer, name="delete_customer"),
    path("customers/<int:customer_id>/", views.get_customer_details, name="get_customer_details"),
    path('customers/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path("executives", views.executives, name="executives"),
    path("executives/add/", views.add_executive, name="add_executive"),
    path("executives/delete/<int:executive_id>/", views.delete_executive, name="delete_executive"),
    path("executives/details/<int:executive_id>/", views.executive_details, name="executive_details"),
    path('executives/edit/<int:executive_id>/', views.edit_executive, name='edit_executive'),
    path("call", views.call, name="call"),
    path("calls/create/", views.create_call, name="create_call"),
    path("jobs", views.jobs, name="jobs"),
    path("amc", views.amc, name="amc"),
    path('amc/add/', views.add_amc, name='add_amc'),
    path("amc/delete/<int:amc_id>/", views.delete_amc, name="delete_amc"),
    path("amc/<int:amc_id>/", views.get_amc_details, name="get_amc_details"),
    path("amc/edit/<int:amc_id>/", views.edit_amc, name="edit_amc"),
    path("todo", views.todo, name="todo"),
    path("settings", views.settings, name="settings"),
]
