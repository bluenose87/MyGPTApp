from django.contrib import admin

from .models import ComplianceRecord, Document, Property, Tenancy


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("address_line1", "city", "postcode", "landlord_name", "bedrooms")
    search_fields = ("address_line1", "postcode", "landlord_name")


@admin.register(Tenancy)
class TenancyAdmin(admin.ModelAdmin):
    list_display = ("tenant_name", "property", "start_date", "end_date", "monthly_rent")
    list_filter = ("start_date",)
    search_fields = ("tenant_name",)


@admin.register(ComplianceRecord)
class ComplianceRecordAdmin(admin.ModelAdmin):
    list_display = ("property", "compliance_type", "issue_date", "expiry_date", "status")
    list_filter = ("compliance_type",)
    search_fields = ("property__address_line1", "property__postcode")
    inlines = [DocumentInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("compliance_record", "description", "uploaded_at")
