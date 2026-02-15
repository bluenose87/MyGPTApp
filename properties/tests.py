from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import ComplianceRecord, Property


class ComplianceStatusTests(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            address_line1="1 Test Lane",
            city="Bristol",
            postcode="BS1 1AA",
            bedrooms=2,
            landlord_name="Landlord Test",
        )

    def test_overdue_record(self):
        record = ComplianceRecord.objects.create(
            property=self.property,
            compliance_type=ComplianceRecord.ComplianceType.GAS_SAFETY,
            issue_date=timezone.localdate() - timedelta(days=365),
            expiry_date=timezone.localdate() - timedelta(days=1),
        )
        self.assertTrue(record.is_overdue)
        self.assertEqual(record.status, "overdue")

    def test_due_soon_record(self):
        record = ComplianceRecord.objects.create(
            property=self.property,
            compliance_type=ComplianceRecord.ComplianceType.EICR,
            issue_date=timezone.localdate() - timedelta(days=100),
            expiry_date=timezone.localdate() + timedelta(days=15),
        )
        self.assertTrue(record.is_due_soon)
        self.assertEqual(record.status, "due_soon")

    def test_ok_record(self):
        record = ComplianceRecord.objects.create(
            property=self.property,
            compliance_type=ComplianceRecord.ComplianceType.EPC,
            issue_date=timezone.localdate() - timedelta(days=50),
            expiry_date=timezone.localdate() + timedelta(days=80),
        )
        self.assertFalse(record.is_due_soon)
        self.assertFalse(record.is_overdue)
        self.assertEqual(record.status, "ok")
