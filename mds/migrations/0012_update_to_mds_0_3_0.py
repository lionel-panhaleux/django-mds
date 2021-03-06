# Generated by Django 2.2b1 on 2019-03-01 13:16

import django.contrib.postgres.fields
from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0011_added_index_to_polygon_and_area_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='area_type',
            field=mds.models.UnboundedCharField(choices=[('unrestricted', 'Unrestricted'), ('restricted', 'Restricted'), ('preferred_pick_up', 'Preferred pick up'), ('preferred_drop_off', 'Preferred drop off')], default='unrestricted'),
        ),
        migrations.AlterField(
            model_name='device',
            name='dn_status',
            field=mds.models.UnboundedCharField(choices=[('available', 'Available'), ('reserved', 'Reserved'), ('unavailable', 'Unavailable'), ('removed', 'Removed'), ('trip', 'Trip'), ('elsewhere', 'Elsewhere'), ('inactive', 'Inactive'), ('unknown', 'Unknown')], default='unavailable'),
        ),
        migrations.AlterField(
            model_name='device',
            name='propulsion',
            field=django.contrib.postgres.fields.ArrayField(base_field=mds.models.UnboundedCharField(choices=[('human', 'Human'), ('electric_assist', 'Electric Assist'), ('electric', 'Electric'), ('combustion', 'Combustion')]), size=None),
        ),
        migrations.AlterField(
            model_name='eventrecord',
            name='event_type',
            field=mds.models.UnboundedCharField(choices=[('service_start', 'Service start'), ('trip_end', 'Trip end'), ('rebalance_drop_off', 'Rebalance drop off'), ('maintenance_drop_off', 'Maintenance drop off'), ('cancel_reservation', 'Cancel reservation'), ('reserve', 'Reserve'), ('trip_start', 'Trip start'), ('trip_enter', 'Trip enter'), ('trip_leave', 'Trip leave'), ('register', 'Register'), ('low_battery', 'Low battery'), ('maintenance', 'Maintenance'), ('service_end', 'Service end'), ('rebalance_pick_up', 'Rebalance pick up'), ('maintenance_pick_up', 'Maintenance pick up'), ('deregister', 'Deregister'), ('telemetry', 'Received telemetry'), ('battery_ok', 'Battery OK')]),
        ),
    ]
