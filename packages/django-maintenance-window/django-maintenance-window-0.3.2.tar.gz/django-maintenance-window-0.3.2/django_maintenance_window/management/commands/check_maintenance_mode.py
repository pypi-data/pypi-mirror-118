import pytz
import time
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Enable/Disabled Maintenance Mode if time is passed"

    def handle(self, *args, **options):
        from django_maintenance_window.models import MaintenanceMode
        config = MaintenanceMode.get_solo()
        now = timezone.now()

        if config.maintenance:
            self.disable_maintenance_mode(config, now)
        else:
            self.enable_maintenance_mode(config, now)

    def datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset


    def enable_maintenance_mode(self, config, now):
        if config.maintenance_from and config.maintenance_from < now:
            config.maintenance = True
            config.maintenance_from = None
            config.save()
            # We do not need to check any further. The maintenance should be enabled.
            return

        for schedule in config.schedules.all():
            unaware = datetime.now().replace(hour=schedule.start_time.hour, minute=schedule.start_time.minute, second=schedule.start_time.second, microsecond=0)
            later = datetime.now().replace(hour=schedule.stop_time.hour, minute=schedule.stop_time.minute, second=schedule.stop_time.second, microsecond=0)
            between = schedule.recurrences.between(unaware, later)
            if between:
                scheduled_date = between[0]
                start = datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.start_time.hour,
                    minute=schedule.start_time.minute,
                    second=schedule.start_time.second,
                    tzinfo=pytz.timezone('Europe/Amsterdam')
                )
                tz_now = datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=now.hour,
                    minute=now.minute,
                    second=now.second,
                    tzinfo=pytz.timezone('Europe/Amsterdam')
                )
                if start < self.datetime_from_utc_to_local(now):
                    config.maintenance = True
                    config.save()
                    return

    def disable_maintenance_mode(self, config, now):
        if config.maintenance_until and config.maintenance_until < now:
            config.maintenance = False
            config.maintenance_until = None
            config.save()
            # We do not need to check any further. The maintenance should be disabled.
            return

        for schedule in config.schedules.all():
            unaware = datetime.now().replace(hour=schedule.start_time.hour, minute=schedule.start_time.minute, second=schedule.start_time.second, microsecond=0)
            later = datetime.now().replace(hour=schedule.stop_time.hour, minute=schedule.stop_time.minute, second=schedule.stop_time.second, microsecond=0)
            between = schedule.recurrences.between(unaware, later)
            if between:
                scheduled_date = between[0]
                end = datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.stop_time.hour,
                    minute=schedule.stop_time.minute,
                    second=schedule.stop_time.second,
                )
                if end < self.datetime_from_utc_to_local(now):
                    config.maintenance = True
                    config.save()
                    return
