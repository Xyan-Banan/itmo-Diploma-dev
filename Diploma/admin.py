from django.contrib import admin
from Diploma.models import Theme,User,Group

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name','path')
    search_fields = ['name','path']

class UserAdmin(admin.ModelAdmin):
    list_display = ('sername','name','patronymic','status','group')
    search_fields = ['sername','name','patronymic']
    list_filer = ['status','group']

class GroupAdmin(admin.ModelAdmin):
    list_display = ('number','teacher')
    list_filer = ['number','teacher']

admin.site.register(Theme,ThemeAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Group,GroupAdmin)
# Register your models here.
