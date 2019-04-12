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
    device_id = serializers.CharField(help_text="UUID of the device concerned")
    event_type = serializers.CharField(help_text="What the event is about")

    class Meta:
        model = models.Provider
        fields = (
            "id",
            "timestamp",
            "device_id",
            "event_type",
        )


class EventRecordViewSet(viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    queryset = models.EventRecord.objects.all()
    lookup_field = "id"
    serializer_class = EventRecordSerializer
