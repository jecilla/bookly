from django.contrib import admin


class SoftDeletionAdmin(admin.ModelAdmin):
    """
    Model to ensure all object(including ones considered as deleted by users)
    remain visible by default to admins
    """

    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin
        # to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.hard_delete()
