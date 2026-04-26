from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
# from rest_framework_simplejwt import token_blacklist

from api.models import Role,User,Permission

# class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

#     def has_delete_permission(self, *args, **kwargs):
#         return True

# admin.site.unregister(token_blacklist.models.OutstandingToken)
# admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)


class RoleFilter(SimpleListFilter):
    title = 'role'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return Role.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(roles__id__in=[self.value()])

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email','created_at', 'updated_at')
    readonly_fields = ['is_staff']
    search_fields = ['username']
    list_filter = (RoleFilter,)
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','password1', 'password2'),
        }),
    )
    filter_horizontal=[]
    raw_id_fields = ('created_by', 'updated_by')
    
class RoleAdmin(admin.ModelAdmin):
    raw_id_fields = ('created_by', 'updated_by')

admin.site.site_header = 'Game Catalogue'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission)