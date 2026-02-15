from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from properties.models import ComplianceRecord


class Command(BaseCommand):
    help = "Send a weekly digest of overdue and due-soon compliance records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            default="",
            help="Comma-separated email list. Defaults to ADMINS if omitted.",
        )

    def handle(self, *args, **options):
        records = ComplianceRecord.objects.select_related("property")
        overdue = [r for r in records if r.is_overdue]
        due_soon = [r for r in records if r.is_due_soon]

        recipient_arg = options["to"].strip()
        if recipient_arg:
            recipients = [email.strip() for email in recipient_arg.split(",") if email.strip()]
        else:
            recipients = [email for _, email in getattr(settings, "ADMINS", [])]

        if not recipients:
            self.stdout.write(self.style.WARNING("No recipients specified. Use --to or set ADMINS."))
            return

        lines = [
            "Weekly Compliance Digest",
            "",
            f"Overdue: {len(overdue)}",
        ]
        lines += [f"- {r.property} | {r.get_compliance_type_display()} | expired {r.expiry_date}" for r in overdue]
        lines += ["", f"Due Soon (<=30 days): {len(due_soon)}"]
        lines += [f"- {r.property} | {r.get_compliance_type_display()} | due {r.expiry_date}" for r in due_soon]

        send_mail(
            subject="Weekly property compliance digest",
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f"Digest sent to {', '.join(recipients)}"))
