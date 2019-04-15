from django.contrib import admin
from uuid import UUID


# to use when searching for devices in get_search_results as a relationship to self.model
def get_devices_queryset_search_results(self, search_term):
    def is_uuid(uuid_string, version=4):
        try:
            UUID(uuid_string, version=version)
        except ValueError:
            return False
        return True

    custom_queryset = self.model.objects.select_related("device__provider")
    if is_uuid(search_term):
        return custom_queryset.filter(device_id=search_term)
    else:
        return custom_queryset.filter(device__identification_number=search_term)


class IncludeNoSelectAction(
    admin.ModelAdmin
):  # class to make actions possible without selecting items
    def get_changelist_instance(self, request):
        """
        Return a `ChangeList` instance based on `request`. May raise
        `IncorrectLookupParameters`.
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ["action_checkbox", *list_display]
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
        if "action" in request.POST:
            try:
                # request.POST['action'] returns the name of the action
                # this is a way to retrieve the action itself to access to its attributes
                action = self.get_actions(request)[request.POST["action"]][0]
                # check custom attribute to see if it should perform action even without selecting items in django admin
                action_list_required = action.list_required
            except (KeyError, AttributeError):
                action_list_required = True
            if (not action_list_required) & (
                not request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            ):
                post = request.POST.copy()
                # post.setlist(admin.helpers.ACTION_CHECKBOX_NAME, self.model.objects.values_list('id', flat=True))
                post["select_across"] = 1
                request.POST = post
                return self.response_action(
                    request, queryset=self.get_filtered_queryset(request)
                )

        return admin.ModelAdmin.changelist_view(self, request, extra_context)
