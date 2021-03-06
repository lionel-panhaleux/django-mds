# Generated by Django 2.1.5 on 2019-01-30 17:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0008_provider_authentication'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='agency_api_authentication',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=mds.models.agency_api_authentication_default, verbose_name='API Agency Authentication'),
        ),
    ]
