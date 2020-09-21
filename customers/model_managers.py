from django.db import models

from crm_example.querysets import SoftDeleteQuerySet


class BaseCustomers(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class NotDeletedCustomers(models.Manager):

    def get_queryset(self):
        return super(NotDeletedCustomers, self).get_queryset().filter(is_deleted=False)
