from django.contrib import admin

from customers.models import Customer


# Register the models that will be shown in Admin
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('full_name', 'id', 'is_deleted', 'email', 'phone')
    list_filter = ('is_deleted', )
    search_fields = ('first_name', 'last_name', 'email', 'phone')


admin.site.register(Customer, CustomerAdmin)
