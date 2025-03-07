from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils.timezone import now

def check_mou_expiry():
    from .models import MOU  # ✅ Move import inside function to avoid early access
    today = now().date()
    expiring_mous = MOU.objects.filter(end_date__lte=today)

    for mou in expiring_mous:
        send_mail(
            "MOU Expiry Reminder",
            f"Your MOU with ID {mou.id} is expiring soon.",
            "admin@mouapp.com",
            [mou.company.email],
        )

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mou_expiry, "interval", days=1)
    scheduler.start()
