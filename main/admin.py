from django.contrib import admin
from .models import Donor,Patient, BloodStock, BloodRequest

admin.site.register(Donor)
admin.site.register(Patient)
admin.site.register(BloodStock)

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient_id',
        'patient_name',
        'blood_group',
        'units',
        'hospital',
        'status',
        'request_date',
    )

    list_filter = ('status', 'blood_group')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description='Approve selected requests')
    def approve_requests(self, request, queryset):
        for blood_request in queryset:
            if blood_request.status == 'Pending':
                stock = BloodStock.objects.get(
                    blood_group=blood_request.blood_group
                )

                if stock.units >= blood_request.units:
                    stock.units -= blood_request.units
                    stock.save()

                    blood_request.status = 'Approved'
                    blood_request.save()

                else:
                    self.message_user(
                        request,
                        f"Not enough {blood_request.blood_group} blood stock.",
                        level='error'
                    )

    @admin.action(description='Reject selected requests')
    def reject_requests(self, request, queryset):
        queryset.filter(status='Pending').update(status='Rejected')