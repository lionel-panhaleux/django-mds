# Generated by Django 2.1.4 on 2019-01-17 00:08

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mds.models
import rest_framework.utils.encoders
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
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deletion_date", models.DateTimeField(null=True)),
                ("label", mds.models.UnboundedCharField(null=True)),
            ],
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
                (
                    "registration_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("identification_number", mds.models.UnboundedCharField()),
                (
                    "category",
                    mds.models.UnboundedCharField(
                        choices=[
                            ("bike", "Bike"),
                            ("scooter", "Scooter"),
                            ("car", "Car"),
                        ]
                    ),
                ),
                ("model", mds.models.UnboundedCharField(default=str)),
                (
                    "propulsion",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=mds.models.UnboundedCharField(
                            choices=[
                                ("electric", "Electric"),
                                ("combustion", "Combustion"),
                            ]
                        ),
                        size=None,
                    ),
                ),
                ("year_manufactured", models.IntegerField(null=True)),
                ("manufacturer", mds.models.UnboundedCharField(default=str)),
                (
                    "dn_gps_point",
                    django.contrib.gis.db.models.fields.PointField(
                        null=True, srid=4326
                    ),
                ),
                ("dn_gps_timestamp", models.DateTimeField(null=True)),
                (
                    "dn_status",
                    mds.models.UnboundedCharField(
                        choices=[
                            ("available", "Available"),
                            ("reserved", "Reserved"),
                            ("unavailable", "Unavailable"),
                            ("removed", "Removed"),
                        ],
                        default="unavailable",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventRecord",
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
                (
                    "saved_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("push", "push"), ("pull", "pull")],
                        default="push",
                        max_length=16,
                    ),
                ),
                (
                    "event_type",
                    mds.models.UnboundedCharField(
                        choices=[
                            ("service_start", "Service start"),
                            ("trip_end", "Trip end"),
                            ("rebalance_drop_off", "Rebalance drop_off"),
                            ("maintenance_drop_off", "Maintenance drop off"),
                            ("cancel_reservation", "Cancel reservation"),
                            ("reserve", "Reserve"),
                            ("trip_start", "Trip start"),
                            ("trip_enter", "Trip enter"),
                            ("trip_leave", "Trip leave"),
                            ("register", "Register"),
                            ("low_battery", "Low battery"),
                            ("maintenance", "Maintenance"),
                            ("service_end", "Service end"),
                            ("rebalance_pick_up", "Rebalance pick up"),
                            ("maintenance_pick_up", "Maintenance pick up"),
                            ("deregister", "Deregister"),
                            ("telemetry", "Received telemetry"),
                        ]
                    ),
                ),
                (
                    "properties",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        default=dict, encoder=rest_framework.utils.encoders.JSONEncoder
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_records",
                        to="mds.Device",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Polygon",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deletion_date", models.DateTimeField(null=True)),
                ("label", mds.models.UnboundedCharField(null=True)),
                ("geom", django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                (
                    "properties",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        default=dict, encoder=rest_framework.utils.encoders.JSONEncoder
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Provider",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", mds.models.UnboundedCharField(default=str)),
                (
                    "logo_b64",
                    mds.models.UnboundedCharField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.AddField(
            model_name="device",
            name="provider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="devices",
                to="mds.Provider",
            ),
        ),
        migrations.AddField(
            model_name="area",
            name="polygons",
            field=models.ManyToManyField(
                blank=True, related_name="areas", to="mds.Polygon"
            ),
        ),
        migrations.AddField(
            model_name="area",
            name="providers",
            field=models.ManyToManyField(
                blank=True, related_name="areas", to="mds.Provider"
            ),
        ),
    ]
