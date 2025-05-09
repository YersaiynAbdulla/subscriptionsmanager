# Generated by Django 5.2 on 2025-05-04 15:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_subscription_is_paid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='notes',
        ),
        migrations.AddField(
            model_name='subscription',
            name='auto_renew',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='subscription',
            name='last_paid_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='notification_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.category'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
