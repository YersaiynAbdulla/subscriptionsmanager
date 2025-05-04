from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

PERIOD_CHOICES = [
    ('daily', 'Ежедневно'),
    ('weekly', 'Еженедельно'),
    ('monthly', 'Ежемесячно'),
    ('yearly', 'Ежегодно'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    renewal_period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    paid_date = models.DateField(default=timezone.now)
    due_date = models.DateField(editable=False)
    is_paid = models.BooleanField(default=False)
    auto_renew = models.BooleanField(default=False)
    last_paid_at = models.DateField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def get_period_days(self):
        return {
            'daily': 1,
            'weekly': 7,
            'monthly': 30,
            'yearly': 365,
        }.get(self.renewal_period, 0)

    def save(self, *args, **kwargs):
        self.due_date = self.paid_date + timedelta(days=self.get_period_days())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name