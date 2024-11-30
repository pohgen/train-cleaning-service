from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Worker
from cleaning.models import CleaningType, Train, Approval

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "role")
    list_filter = ("role", )
    search_fields = ("first_name", "last_name", "username")
    fieldsets = (
        ("Required", {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (("Role"),{"fields": ("role",),},),
    )
    ordering = ("role", )

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("name", "cleaning_type", "status")
    list_filter = ("name", "cleaning_type", "status")
    search_fields = ("name", "cleaning_type", "status")
    ordering = ("-status", )


admin.site.register(CleaningType)
admin.site.register(Approval)
