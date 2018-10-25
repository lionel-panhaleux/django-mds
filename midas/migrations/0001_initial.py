# Generated by Django 2.1.2 on 2018-10-25 16:36

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import midas.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "polygons",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("provider", midas.models.UnboundedCharField()),
                ("technical_id", midas.models.UnboundedCharField()),
                ("visible_id", midas.models.UnboundedCharField()),
                ("model", midas.models.UnboundedCharField(default=str)),
                (
                    "status",
                    midas.models.UnboundedCharField(
                        choices=[
                            ("available", "Available"),
                            ("reserved", "Reserved"),
                            ("unavailable", "Unavailable"),
                            ("removed", "Removed"),
                        ]
                    ),
                ),
                (
                    "position",
                    django.contrib.gis.db.models.fields.PointField(
                        null=True, srid=4326
                    ),
                ),
                ("position_timestamp", models.DateTimeField(null=True)),
                (
                    "details",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Query",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("provider", midas.models.UnboundedCharField()),
                ("endpoint", midas.models.UnboundedCharField(default=str)),
                (
                    "method",
                    midas.models.UnboundedCharField(
                        choices=[("POST", "POST"), ("PUT", "PUT"), ("DELETE", "DELETE")]
                    ),
                ),
                (
                    "content",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("provider", midas.models.UnboundedCharField()),
                ("begin_date", models.DateTimeField()),
                ("end_date", models.DateTimeField(null=True)),
                (
                    "details",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="midas.Area"
                    ),
                ),
            ],
        ),
    ]
