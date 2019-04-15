from django.contrib import admin
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from . import enums, export as export_excel
from mds.admin_overload import IncludeNoSelectAction
from mds.apis.prv_api import export_serializers
import pytz


class BaseExportAdmin(IncludeNoSelectAction):
    def export(self, request, queryset):
        # 20k = a bit less than 1.5 GiB
        EXPORT_LIMIT = 20000
        queryset = queryset[:EXPORT_LIMIT]

        def get_default_export_columns(self):
            return [(field, field, None) for field in self.list_display]

        tz = request.GET.get("tz", timezone.get_default_timezone_name())
        tz_object = pytz.timezone(tz)  # Use a shorter alias: Europe/Paris => CET
        tz = timezone.now().astimezone(tz_object).strftime("%Z")
        title = getattr(self, "export_title", "Export")
        export_columns = getattr(
            self, "export_columns", get_default_export_columns(self)
        )
        serializer = getattr(self, "export_serializer", lambda x: x)
        headers = [col[1].format(tz=tz) for col in export_columns]
        template = export_excel.excel_template(headers=headers)

        return export_excel.to_streaming_response(
            title,
            export_columns,
            serializer,
            queryset,
            template,
            tz_object,
            with_time=False,
            batch_size=500,
        )

    export.short_description = "Export"
    export.list_required = False


class ExportDeviceAdmin(BaseExportAdmin, admin.ModelAdmin):
    export_serializer = export_serializers.DeviceSerializer
    export_title = "Devices"
    export_columns = [
        # Headers taken from the frontend and not translated
        ("id", "Vehicle ID", None),
        ("identification_number", "VIN", None),
        ("provider_name", "Provider", None),
        ("category", "Vehicle type", lambda v: getattr(enums.DEVICE_CATEGORY, v).value),
        ("status", "Status", lambda v: getattr(enums.DEVICE_STATUS, v).value),
        ("registration_date", "Registration date ({tz})", parse_datetime),
        ("last_telemetry_date", "Last telemetry date ({tz})", parse_datetime),
        ("battery", "Energy level", lambda v: round(v * 10) * 10),
        ("battery", "Energy range", lambda v: round(v * 200)),  # XXX
    ]


class ExportEventRecordAdmin(BaseExportAdmin, admin.ModelAdmin):
    export_serializer = export_serializers.EventRecordSerializer
    export_title = "EventRecords"
    export_columns = [
        # Headers taken from the frontend and not translated
        ("timestamp", "Timestamp ({tz})", parse_datetime),
        ("provider_name", "Provider", None),
        ("source", "Source", None),
        ("device_id", "Device UUID", None),
        ("device_vin", "Device VIN", None),
        ("event_type", "Event", None),
    ]
