# Generated by Django 3.2.7 on 2021-10-29 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='service_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Annual'), (2, 'Minor')], default=2),
        ),
    ]
