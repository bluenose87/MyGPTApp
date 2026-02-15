from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("properties/", views.property_list, name="property_list"),
    path("tenancies/", views.tenancy_list, name="tenancy_list"),
    path("compliance/", views.compliance_list, name="compliance_list"),
    path("export/properties/", views.export_properties_csv, name="export_properties_csv"),
    path("export/tenancies/", views.export_tenancies_csv, name="export_tenancies_csv"),
    path("export/compliance/", views.export_compliance_csv, name="export_compliance_csv"),
]
