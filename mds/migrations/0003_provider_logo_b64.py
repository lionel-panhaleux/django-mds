# Generated by Django 2.1.4 on 2019-01-13 21:18

from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0002_update_area_polygons'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='logo_b64',
            field=mds.models.UnboundedCharField(default=None, null=True),
        ),
    ]