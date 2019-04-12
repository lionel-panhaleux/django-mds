from rest_framework import serializers
from rest_framework import viewsets

from mds import models
from mds.access_control.permissions import require_scopes
from mds.access_control.scopes import SCOPE_PRV_API


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


class EventRecordViewSet(viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    queryset = models.EventRecord.objects.prefetch_related("device").all()
    lookup_field = "id"
    serializer_class = EventRecordSerializer
