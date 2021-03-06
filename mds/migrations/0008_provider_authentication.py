# Generated by Django 2.1.5 on 2019-01-29 16:41

import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.jsonb
from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [("mds", "0007_provider_api")]

    operations = [
        migrations.RenameField(
            model_name="provider",
            old_name="authentication",
            new_name="api_authentication",
        ),
        migrations.AlterField(
            model_name="provider",
            name="api_authentication",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=mds.models.provider_api_authentication_default,
                verbose_name="API Authentication",
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="api_configuration",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=mds.models.provider_api_configuration_default,
                verbose_name="API Configuration",
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="oauth2_url",
            field=mds.models.UnboundedCharField(
                default="", verbose_name="OAuth2 URL (if different)"
            ),
        ),
    ]
