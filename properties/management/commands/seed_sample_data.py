from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from properties.models import ComplianceRecord, Property, Tenancy


class Command(BaseCommand):
    help = "Create sample properties, tenancies, and compliance records."

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        p1, _ = Property.objects.get_or_create(
            address_line1="10 High Street",
            city="Manchester",
            postcode="M1 1AA",
            defaults={"bedrooms": 2, "landlord_name": "Alex Carter", "address_line2": ""},
        )
        p2, _ = Property.objects.get_or_create(
            address_line1="22 King Road",
            city="Leeds",
            postcode="LS1 2BB",
            defaults={"bedrooms": 3, "landlord_name": "Jamie Smith", "address_line2": "Flat 4"},
        )

        Tenancy.objects.get_or_create(
            property=p1,
            tenant_name="Priya Shah",
            defaults={
                "start_date": today - timedelta(days=120),
                "end_date": None,
                "monthly_rent": 1150,
                "deposit_amount": 1150,
            },
        )
        Tenancy.objects.get_or_create(
            property=p2,
            tenant_name="Tom Wilson",
            defaults={
                "start_date": today - timedelta(days=30),
                "end_date": None,
                "monthly_rent": 1450,
                "deposit_amount": 1450,
            },
        )

        ComplianceRecord.objects.get_or_create(
            property=p1,
            compliance_type=ComplianceRecord.ComplianceType.GAS_SAFETY,
            defaults={
                "issue_date": today - timedelta(days=340),
                "expiry_date": today - timedelta(days=5),
                "notes": "Needs urgent renewal",
            },
        )
        ComplianceRecord.objects.get_or_create(
            property=p1,
            compliance_type=ComplianceRecord.ComplianceType.EICR,
            defaults={
                "issue_date": today - timedelta(days=1000),
                "expiry_date": today + timedelta(days=20),
                "notes": "Book contractor",
            },
        )
        ComplianceRecord.objects.get_or_create(
            property=p2,
            compliance_type=ComplianceRecord.ComplianceType.EPC,
            defaults={
                "issue_date": today - timedelta(days=30),
                "expiry_date": today + timedelta(days=330),
                "notes": "All good",
            },
        )

        self.stdout.write(self.style.SUCCESS("Sample data created/verified."))
