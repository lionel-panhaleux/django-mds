from django.contrib import admin
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from . import models, enums, export as export_excel
from mds.apis.prv_api import vehicles

import pytz

from uuid import UUID


def is_uuid(uuid_string, version=4):
    try:
        UUID(uuid_string, version=version)
    except ValueError:
        return False
    return True


class ExportAdmin(admin.ModelAdmin): #class needed to overload a few methods
    def export(self, request, queryset): #global action
        def get_default_export_columns(self):
            return [(field, field, None) for field in self.list_display]

        tz = request.GET.get("tz", timezone.get_default_timezone_name())
        tz_object = pytz.timezone(tz) # Use a shorter alias: Europe/Paris => CET
        tz = timezone.now().astimezone(tz_object).strftime("%Z")
        title = getattr(self, 'export_title', 'Export')
        export_columns = getattr(self, 'export_columns', get_default_export_columns(self))
        serializer = getattr(self, 'export_serializer', lambda x: x)
        headers = [col[1].format(tz=tz) for col in export_columns]
        template = export_excel.excel_template(headers=headers)

        return export_excel.to_streaming_response(
            title, export_columns, serializer, queryset, template, tz_object, with_time=False, batch_size=500
        )

    def get_changelist_instance(self, request):
        """
        Return a `ChangeList` instance based on `request`. May raise
        `IncorrectLookupParameters`.
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ['action_checkbox', *list_display]
        sortable_by = self.get_sortable_by(request)
        ChangeList = self.get_changelist(request)
        return ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
            self.get_list_filter(request),
            self.date_hierarchy,
            self.get_search_fields(request),
            self.get_list_select_related(request),
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            sortable_by,
        )

    def get_filtered_queryset(self, request):
        """
        Returns a queryset filtered by the URLs parameters
        """
        cl = self.get_changelist_instance(request)
        return cl.get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST:
            try:
                # request.POST['action'] returns the name of the action
                # this is a way to retrieve the action itself to access to its attributes
                action = self.get_actions(request)[request.POST['action']][0]
                # check custom attribute to see if it should perform action even without selecting items in django admin
                action_list_required = action.list_required
            except (KeyError, AttributeError):
                action_list_required = True
            if (not action_list_required) & (not request.POST.getlist(admin.ACTION_CHECKBOX_NAME)):
                post = request.POST.copy()
                # post.setlist(admin.helpers.ACTION_CHECKBOX_NAME, self.model.objects.values_list('id', flat=True))
                post["select_across"] =  1
                request.POST = post
                return self.response_action(request, queryset=self.get_filtered_queryset(request))

        return admin.ModelAdmin.changelist_view(self, request, extra_context)

@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["name"]

@admin.register(models.Device)
class DeviceAdmin(ExportAdmin, admin.ModelAdmin):
    list_display = ["id", "provider_name", "identification_number", "category"]
    list_filter = ["provider", "category"]
    search_fields = ["id", "identification_number"]
    list_select_related = ("provider",)
    actions = ['export']

    def provider_name(self, obj):
        return obj.provider.name
    provider_name.short_description = "Provider"

    def export(self, request, queryset):
        return ExportAdmin.export(self, request, queryset)
    export.short_description = "Export"
    export.list_required = False

    export_serializer = vehicles.DeviceSerializer
    export_title = "Devices"
    export_columns = [
        # Headers taken from the frontend and not translated
        ("id", "Vehicle ID", None),
        ("identification_number", "VIN", None),
        ("provider_name", "Provider", None),
        (
            "category",
            "Vehicle type",
            lambda v: getattr(enums.DEVICE_CATEGORY, v).value,
        ),
        (
            "status",
            "Status",
            lambda v: getattr(enums.DEVICE_STATUS, v).value,
        ),
        ("registration_date", "Registration date ({tz})", parse_datetime),
        ("last_telemetry_date", "Last telemetry date ({tz})", parse_datetime),
        ("battery", "Energy level", lambda v: round(v * 10) * 10),
        ("battery", "Energy range", lambda v: round(v * 200)),  # XXX
    ]


@admin.register(models.EventRecord)
class EventRecordAdmin(ExportAdmin, admin.ModelAdmin):
    list_display = ["timestamp", "provider", "device_id", "event_type"]
    list_filter = ["device__provider", "event_type"]
    list_select_related = ("device__provider",)
    search_fields = ["device__id", "device__identification_number"]

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super().get_search_results(request, queryset, search_term)
        custom_queryset = get_devices_queryset_search_results(self, search_term)
        return super().get_search_results(request, custom_queryset, search_term)

    def provider(self, obj):
        return obj.device.provider.name

    def device_id(self, obj):
        return obj.device.id
    
    def export(self, request, queryset):
        return ExportAdmin.export(self, request, queryset)
    export.short_description = "Export"
    export.list_required = False

    export_serializer = None
    export_title = "EventRecords"
    export_columns = [
        # Headers taken from the frontend and not translated
        ("timestamp", "Timestamp", None),
        ("provider", "Provider", None),
    ]


# to use when searching for devices in get_search_results as a relationship to self.model
def get_devices_queryset_search_results(self, search_term):
    custom_queryset = self.model.objects.select_related("device__provider")
    if is_uuid(search_term):
        return custom_queryset.filter(device_id=search_term)
    else:
        return custom_queryset.filter(device__identification_number=search_term)


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "label"]
    ordering = ["label"]


@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ["id", "label"]
    ordering = ["label"]
