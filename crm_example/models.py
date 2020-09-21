import jsonfield

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


# Here we will declare abstract classes that they will be used through this project
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False, null=False)  # Soft delete

    class Meta:
        abstract = True

    @classmethod
    def get_changed_fields(cls, new_data, instance=None):
        """
        Function to get new and old values in instance.
        :param new_data: dict with new value get from endpoint request
        :param instance: instance (Customer) that has been modified
        :return:
        """
        changed_fields = []

        for field_name in new_data:

            if isinstance(new_data.get(field_name), InMemoryUploadedFile):
                # If the field is an image we can't get its value. Only want to know that the image is new
                field_data = {'name': field_name, 'new_value': '-'}
                changed_fields.append(field_data)
                continue

            else:
                field_data = {'name': field_name, 'new_value': new_data.get(field_name)}

            if instance:

                # If instance value hasn't change, we won't save this information in log
                current_value_in_instance = getattr(instance, field_name)
                if current_value_in_instance == new_data.get(field_name):
                    continue

                field_data.update(
                    {'old_value': current_value_in_instance}
                )

            changed_fields.append(field_data)

        return changed_fields


class BaseModelLog(models.Model):
    """
    An abstract base model to implement logs.

    Usage:

        class MyLog(BaseModelLog):
            TYPE_CHOICES = (
                ('foo', 'bar'),
                ('foo2', 'bar2'),
            )
            type = models.CharField(choices=TYPE_CHOICES, max_length=50)
            something = models.ForeignKey(...)

    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    fields_changed = jsonfield.JSONField(null=True)
    user = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def initialize_user_authorisation(sender, instance=None, created=False, **kwargs):
    """
    This function will create a token for each user that has been created and set staff status
    to allow them to access to admin panel. Then, the user will be able to handle customers
    """
    if created:
        Token.objects.create(user=instance)

        customer_permissions = Permission.objects.filter(content_type__model='customer')
        instance.user_permissions.add(*customer_permissions)
        instance.is_staff = True
        instance.save()
