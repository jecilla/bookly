from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet


class SoftDeletionQuerySet(QuerySet):
    """
    Queryset to handle the bulk deletes that will bypass the
    delete() method of objects ensuring our softdeletes
    are always complied with.

    """

    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone
                                                        .now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeleteManager(models.Manager):
    """
    Manager for softDelete model, ensures that only files the user deems as
    not deleted are made visible to and can be manipulated by the user.

    """

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteModel(models.Model):

    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.is_active = False
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False
        self.is_active = True
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()
