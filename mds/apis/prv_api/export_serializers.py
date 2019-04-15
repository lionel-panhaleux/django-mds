from rest_framework import serializers

from mds import enums, models
from mds.apis import utils


"""
    Copy here serializers used for export. This file is for detangling views and serializers being created in a single file.
    In the future, this file could be used to list all serializers if we want to dissociate serializers and views from one single file.
"""
class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(help_text="Unique device identifier (UUID)")
    model = serializers.CharField(required=False, help_text="Vehicle model")
    identification_number = serializers.CharField(
        help_text="VIN (Vehicle Identification Number)"
    )
    category = serializers.ChoiceField(
        enums.choices(enums.DEVICE_CATEGORY), help_text="Device type"
    )
    propulsion = serializers.ListField(
        child=serializers.ChoiceField(enums.choices(enums.DEVICE_PROPULSION)),
        help_text="Propulsion type(s)",
    )
    provider_id = serializers.UUIDField(
        source="provider.id", help_text="ID of the service provider of the device"
    )
    provider_name = serializers.CharField(
        source="provider.name", help_text="Name of the service provider of the device"
    )
    registration_date = serializers.DateTimeField(help_text="Device registration date")
    last_telemetry_date = serializers.DateTimeField(
        source="dn_gps_timestamp", help_text="Latest GPS timestamp", allow_null=True
    )
    position = utils.PointSerializer(
        source="dn_gps_point", help_text="Latest GPS position"
    )
    status = serializers.ChoiceField(
        enums.choices(enums.DEVICE_STATUS),
        source="dn_status",
        help_text="Latest status",
        allow_null=True,
    )
    battery = serializers.FloatField(
        source="dn_battery_pct", help_text="Percentage between 0 and 1", allow_null=True
    )

    class Meta:
        model = models.Device
        fields = (
            "id",
            "provider_id",
            "provider_name",
            "model",
            "identification_number",
            "category",
            "propulsion",
            "status",
            "position",
            "registration_date",
            "last_telemetry_date",
            "battery",
        )

class EventRecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=True, help_text="ID of the event"
    )
    timestamp = serializers.DateTimeField(help_text="Timestamp")
    provider_name = serializers.CharField(
        source="device.provider.name", help_text="Name of the service provider of the device"
    ) 
    device_id = serializers.CharField(help_text="UUID of the device concerned")
    device_vin = serializers.CharField(source="device.identification_number", help_text="VIN of the device concerned")
    event_type = serializers.CharField(help_text="What the event is about")
    source = serializers.CharField(help_text="whether it is from agency or provider")

    class Meta:
        model = models.Provider
        fields = (
            "id",
            "timestamp",
            "provider_name",
            "device_id",
            "device_vin",
            "event_type",
            "source"
        )
