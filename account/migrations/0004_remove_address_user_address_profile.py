# Generated by Django 5.2.1 on 2025-05-21 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_addres_address_rename_pelac_address_pelak_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.AddField(
            model_name='address',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='accounts.profile'),
            preserve_default=False,
        ),
    ]
