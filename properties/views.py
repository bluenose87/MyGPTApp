import csv
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from .models import ComplianceRecord, Property, Tenancy


def dashboard(request):
    records = ComplianceRecord.objects.select_related("property")
    overdue = [r for r in records if r.is_overdue]
    due_soon = [r for r in records if r.is_due_soon]
    ok = [r for r in records if r.status == "ok"]

    context = {
        "total_properties": Property.objects.count(),
        "active_tenancies": Tenancy.objects.filter(end_date__isnull=True).count(),
        "overdue": overdue,
        "due_soon": due_soon,
        "ok": ok,
        "compliance_by_type": ComplianceRecord.objects.values("compliance_type").annotate(total=Count("id")),
    }
    return render(request, "properties/dashboard.html", context)


def property_list(request):
    return render(request, "properties/property_list.html", {"properties": Property.objects.all()})


def tenancy_list(request):
    return render(request, "properties/tenancy_list.html", {"tenancies": Tenancy.objects.select_related("property")})


def compliance_list(request):
    records = ComplianceRecord.objects.select_related("property")
    return render(request, "properties/compliance_list.html", {"records": records})


def export_properties_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="properties.csv"'
    writer = csv.writer(response)
    writer.writerow(["Address 1", "Address 2", "City", "Postcode", "Bedrooms", "Landlord"])
    for p in Property.objects.all():
        writer.writerow([p.address_line1, p.address_line2, p.city, p.postcode, p.bedrooms, p.landlord_name])
    return response


def export_tenancies_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tenancies.csv"'
    writer = csv.writer(response)
    writer.writerow(["Property", "Tenant", "Start", "End", "Monthly Rent", "Deposit"])
    for t in Tenancy.objects.select_related("property"):
        writer.writerow([str(t.property), t.tenant_name, t.start_date, t.end_date or "", t.monthly_rent, t.deposit_amount])
    return response


def export_compliance_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="compliance.csv"'
    writer = csv.writer(response)
    writer.writerow(["Property", "Type", "Issue Date", "Expiry Date", "Status", "Days Until Due"])
    for c in ComplianceRecord.objects.select_related("property"):
        writer.writerow([str(c.property), c.get_compliance_type_display(), c.issue_date, c.expiry_date, c.status, c.days_until_due])
    return response
