# Generated by Django 2.1.3 on 2019-04-26 08:07
from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [("mds", "0020_fields_consistency")]

    operations = [
        migrations.AlterField(
            model_name="eventrecord",
            name="source",
            field=mds.models.UnboundedCharField(
                choices=[
                    ("agency_api", "Agency API"),
                    ("provider_api", "Provider API"),
                ],
                default="agency_api",
            ),
        ),
        migrations.RunSQL(
            """
            UPDATE mds_eventrecord SET source='agency_api' WHERE source='push';
            UPDATE mds_eventrecord SET source='provider_api' WHERE source='pull';
            """,
            reverse_sql="""
            UPDATE mds_eventrecord SET source='push' WHERE source='agency_api';
            UPDATE mds_eventrecord SET source='pull' WHERE source='provider_api';
        """,
        ),
    ]
