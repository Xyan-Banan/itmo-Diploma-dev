from django.contrib import admin
from Diploma.models import Theme,User,Group,Practice

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

class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name','id_practice')

admin.site.register(Theme,ThemeAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(Practice,PracticeAdmin)
# Register your models here.
