# Generated by Django 2.1.4 on 2018-12-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0002_update_area_polygons'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('added', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
