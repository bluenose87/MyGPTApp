from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ComplianceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "compliance_type",
                    models.CharField(
                        choices=[
                            ("gas_safety", "Gas Safety"),
                            ("eicr", "EICR"),
                            ("epc", "EPC"),
                            ("fire_alarm", "Fire Alarm"),
                            ("pat_test", "PAT Test"),
                        ],
                        max_length=40,
                    ),
                ),
                ("issue_date", models.DateField()),
                ("expiry_date", models.DateField()),
                ("notes", models.TextField(blank=True)),
            ],
            options={"ordering": ["expiry_date"]},
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address_line1", models.CharField(max_length=255)),
                ("address_line2", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(max_length=120)),
                ("postcode", models.CharField(max_length=20)),
                ("bedrooms", models.PositiveSmallIntegerField(default=1)),
                ("landlord_name", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Tenancy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_name", models.CharField(max_length=120)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("monthly_rent", models.DecimalField(decimal_places=2, max_digits=8)),
                ("deposit_amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tenancies",
                        to="properties.property",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="compliancerecord",
            name="property",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="compliance_records",
                to="properties.property",
            ),
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="compliance_docs/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(blank=True, max_length=255)),
                (
                    "compliance_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="properties.compliancerecord",
                    ),
                ),
            ],
        ),
    ]
