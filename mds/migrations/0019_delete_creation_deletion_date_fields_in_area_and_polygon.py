# Generated by Django 2.1.7 on 2019-04-11 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0018_allow_blank_provider_base_api_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='area',
            name='deletion_date',
        ),
        migrations.RemoveField(
            model_name='polygon',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='polygon',
            name='deletion_date',
        ),
    ]
