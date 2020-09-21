from customers import choices as customer_choices
from customers.models import CustomerLog, Customer


class CustomerLogManager:
    
    @staticmethod
    def _create_customer_log(user, customer, log_type, fields_changed=None):
        CustomerLog.objects.create(
            user=user,
            customer=customer,
            log_type=log_type,
            fields_changed=fields_changed
        )

    @classmethod
    def add_creation_log(cls, user, customer, new_data):
        log_type = customer_choices.LOG_CREATION_TYPE
        changed_fields = Customer.get_changed_fields(new_data=new_data)
        cls._create_customer_log(user, customer, log_type, changed_fields)

    @classmethod
    def add_edition_log(cls, user, customer, changed_fields):
        log_type = customer_choices.LOG_EDITION_TYPE
        cls._create_customer_log(user, customer, log_type, changed_fields)

    @classmethod
    def add_deletion_log(cls, user, customer):
        log_type = customer_choices.LOG_DELETION_TYPE
        cls._create_customer_log(user, customer, log_type)
