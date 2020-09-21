import datetime
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from customers import model_managers as customer_managers
from customers import choices as customer_choices
from crm_example.models import BaseModel, BaseModelLog


def get_customer_photo_upload_to(instance, filename):
    """
    Function to generate file names for uploaded images
    :param instance:
    :param filename:
    :return:
    """
    path = customer_choices.PATH_TO_UPLOAD_CUSTOMER_PHOTOS
    filename_without_extension, extension = os.path.splitext(filename)  # Extension has already the dot
    upload_datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    full_path = '{path}customer-{upload_datetime}{extension}'.format(
        path=path, upload_datetime=upload_datetime_str, extension=extension)
    return full_path


class Customer(BaseModel):
    """
    Model Customer
    It's not necessary declare a Primary Key, because Django does it by default with the name 'id'
    """

    first_name = models.CharField(max_length=50, verbose_name=_("Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Surname"))
    photo = models.ImageField(upload_to=get_customer_photo_upload_to, null=True, blank=True, verbose_name=_("Photo"))
    phone = models.CharField(max_length=15, default='', verbose_name=_("Phone"))
    email = models.EmailField(max_length=150, default='', verbose_name=_("Email"))

    country = models.CharField(max_length=50, default='', verbose_name=_("Country"))
    postal_code = models.CharField(max_length=15, default='', verbose_name=_("Postal Code"))
    region = models.CharField(max_length=100, default='', verbose_name=_("Region"))
    locality = models.CharField(max_length=100, default='', verbose_name=_("Locality"))
    address = models.CharField(max_length=200, default='', verbose_name=_("Address"))

    created_by = models.ForeignKey(
        'auth.User', null=False, blank=False, on_delete=models.PROTECT, related_name='creator')
    updated_by = models.ForeignKey('auth.User', null=False, blank=False, on_delete=models.PROTECT)

    # Model Managers
    objects = customer_managers.BaseCustomers()
    objects_not_deleted = customer_managers.NotDeletedCustomers()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """
        Main method to show model's representation.
        By default the framework shows them like that: {{ ClassName }} object ({{ id }})
        :return: the full_name of the instance
        """
        return self.full_name
    
    def delete(self, using=None, keep_parents=False):
        """
        We override this method to force the soft delete of this model, when this method is used through the code.
        """
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class CustomerLog(BaseModelLog):

    LOG_TYPE_CHOICES = (
        (customer_choices.LOG_CREATION_TYPE, _("Creation")),
        (customer_choices.LOG_EDITION_TYPE, _("Edition")),
        (customer_choices.LOG_DELETION_TYPE, _("Deletion")),
    )

    log_type = models.CharField(choices=LOG_TYPE_CHOICES, max_length=50)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']
