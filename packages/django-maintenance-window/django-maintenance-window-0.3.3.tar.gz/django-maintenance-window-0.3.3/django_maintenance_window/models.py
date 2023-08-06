# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from recurrence.fields import RecurrenceField
from solo.models import SingletonModel

DUMMY_DT = datetime(1970, 1, 1)


class MaintenanceMode(SingletonModel):
    maintenance = models.BooleanField(default=False)
    maintenance_from = models.DateTimeField(null=True, blank=True)
    maintenance_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u"Maintenance Mode"

    class Meta:
        verbose_name = _("Maintenance Mode")

    def clean(self):
        error_message = _('You can not set "maintenance_from" without setting "maintenance_until"')  # noqa
        if self.maintenance_from and not self.maintenance_until:
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Schedule(models.Model):
    mode = models.ForeignKey(MaintenanceMode, on_delete=models.CASCADE, related_name="schedules")
    recurrences = RecurrenceField()
    start_time = models.TimeField(null=True, blank=True)
    stop_time = models.TimeField(null=True, blank=True)

    def clean(self):
        error_message = _('You can not set "start_time" without setting "stop_time"')
        if self.start_time and not self.stop_time:
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def start_dt(self, startdatetime=DUMMY_DT):
        if self.start_time is not None:
            return datetime.combine(startdatetime, self.start_time)
        return None

    def end_dt(self, startdatetime=DUMMY_DT):
        if self.stop_time is not None:
            return datetime.combine(startdatetime, self.stop_time)
        return None

    def get_next_occurrence(self, days_in_future=1):
        """
        Returns the datetime for the next occurrence of this event as
        determined by the recurrences rule and the occurrences.
        :return: Datetime of next occurrence or None if no next occurrence

        :note: I *think* this must use datetime.datetime because TimeFields don't store tz information
        """
        start_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = start_dt + timedelta(days=days_in_future)

        occurrences = []
        for eo in self.occurrences.all():
            for o in eo.recurrences.between(start_dt, end_dt, inc=True):
                hour, minute = (eo.start.hour, eo.start.minute) if eo.start is not None else (0, 0)
                occurrences.append(
                    datetime(o.year, o.month, o.day, hour, minute),
                )
        occurrences.sort()
        return occurrences[0] if occurrences else None
