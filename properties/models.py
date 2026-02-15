from datetime import timedelta

from django.db import models
from django.utils import timezone


class Property(models.Model):
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120)
    postcode = models.CharField(max_length=20)
    bedrooms = models.PositiveSmallIntegerField(default=1)
    landlord_name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.address_line1}, {self.city}"


class Tenancy(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="tenancies")
    tenant_name = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.tenant_name} ({self.property})"


class ComplianceRecord(models.Model):
    class ComplianceType(models.TextChoices):
        GAS_SAFETY = "gas_safety", "Gas Safety"
        EICR = "eicr", "EICR"
        EPC = "epc", "EPC"
        FIRE_ALARM = "fire_alarm", "Fire Alarm"
        PAT_TEST = "pat_test", "PAT Test"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="compliance_records")
    compliance_type = models.CharField(max_length=40, choices=ComplianceType.choices)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["expiry_date"]

    def __str__(self) -> str:
        return f"{self.get_compliance_type_display()} - {self.property}"

    @property
    def days_until_due(self) -> int:
        return (self.expiry_date - timezone.localdate()).days

    @property
    def is_overdue(self) -> bool:
        return self.days_until_due < 0

    @property
    def is_due_soon(self) -> bool:
        return 0 <= self.days_until_due <= 30

    @property
    def status(self) -> str:
        if self.is_overdue:
            return "overdue"
        if self.is_due_soon:
            return "due_soon"
        return "ok"

    @classmethod
    def due_soon_cutoff(cls):
        return timezone.localdate() + timedelta(days=30)


class Document(models.Model):
    compliance_record = models.ForeignKey(
        ComplianceRecord,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    file = models.FileField(upload_to="compliance_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.description or self.file.name
