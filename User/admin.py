from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *
# Register your models here.


UserAdmin.fieldsets[2][1]['fields'] =(
    'is_active',
    'is_staff',
    'is_superuser',
    'groups',
    
    
    'name',
    
    'phoneNumber',
    
    'Image',
    
    'Address',
    

    'sex',
    
    'City',
    
    'birthday',
    
    'ActiveUser',
    
    'internal',

    'Manager',


    'isForward',

    "robotVoip"

    'isForwardHamkadeh',
    'isForwardSaleHamkadeh',
    'isForward5040',


    
    #hamkadeh
    'isMonitoringHamkadeh',

    'isAddToLineHamkadeh',
    
    'isListeningHamkadeh',
    
    'robotHamkadeh',    

    'statusConsultantHamkadeh',
    
    #sale-hamkadeh
    'isMonitoringSaleHamkadeh',
    'isAddToLineSaleHamkadeh',
    'isListeningSaleHamkadeh',
    "statusSupportHamkadeh",
    
    
    #5040    
    'isMonitoring5040',
    'isAddToLine5040',
    'isListening5040',
    'robot5040',
    'statusUser5040'


)
# UserAdmin.list_display += ('is_author','is_special_user')
admin.site.register(User, UserAdmin)
admin.site.register(Age)



class Users5040Admin(admin.ModelAdmin):
    using = "5040"

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )



class UsersHamkadehAdmin(admin.ModelAdmin):
    using = "hamkadeh"

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )

admin.site.register(Users5040 , Users5040Admin)
# admin.site.register(Users5040)
admin.site.register(UsersHamkadeh , UsersHamkadehAdmin)