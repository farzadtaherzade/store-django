# Generated by Django 5.2.1 on 2025-05-23 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('process', 'Process'), ('sucess', 'Sucess'), ('failed', 'Failed')], default='process', max_length=20),
        ),
    ]
