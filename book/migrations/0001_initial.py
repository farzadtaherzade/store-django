# Generated by Django 5.2.1 on 2025-05-11 04:05

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('publication_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('edition', models.IntegerField(default=1)),
                ('language', models.CharField()),
                ('cover', models.ImageField(upload_to='books/')),
                ('page_count', models.PositiveBigIntegerField()),
                ('stock', models.PositiveIntegerField(default=0)),
                ('author', models.CharField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
