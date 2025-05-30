# Generated by Django 5.2.1 on 2025-05-24 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='ref_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='result',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
