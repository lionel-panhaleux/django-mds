from django.contrib import admin

from . import models, admin_overload


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["name"]


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["id", "provider_name", "identification_number", "category"]
    list_filter = ["provider", "category"]
    search_fields = ["id", "identification_number"]
    list_select_related = ["provider"]

    def provider_name(self, obj):
        return obj.provider.name

    provider_name.short_description = "Provider"


@admin.register(models.EventRecord)
class EventRecordAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "provider", "device_id", "event_type"]
    list_filter = ["device__provider", "event_type"]
    list_select_related = ["device__provider"]
    search_fields = ["device__id", "device__identification_number"]

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super().get_search_results(request, queryset, search_term)
        custom_queryset = admin_overload.get_devices_queryset_search_results(
            self, search_term
        )
        return super().get_search_results(request, custom_queryset, search_term)

    def provider(self, obj):
        return obj.device.provider.name

    def device_id(self, obj):
        return obj.device.id


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "label"]
    ordering = ["label"]


@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ["id", "label"]
    ordering = ["label"]
