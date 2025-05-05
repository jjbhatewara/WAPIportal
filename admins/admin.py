from django.contrib import admin
from .models import CustomerType, Customer, Department, Executive, AMC,Call

# Register your models here.
admin.site.register(CustomerType)
admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(Executive)

admin.site.register(Call)

@admin.register(AMC)
class AMCAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'amc_name',
        'amc_doc_no',
        'amc_category',
        'renew_status',
        'number_of_services',
        'starting_date',
        'end_date',
    )
    search_fields = ('amc_name', 'amc_doc_no', 'customer__company_customer_name')
    list_filter = ('amc_category', 'renew_status', 'starting_date', 'end_date')
