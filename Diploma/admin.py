from django.contrib import admin
from Diploma.models import *

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

class PracticeForGroupAdmin(admin.ModelAdmin):
    list_display = ('id_practice','id_group','date_of_sub')
    search_fields = ['id_practice','id_group','date_of_sub']
    list_filer = ['id_practice','id_group','date_of_sub']

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name','id_material','path')

admin.site.register(Theme,ThemeAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(Practice,PracticeAdmin)
admin.site.register(PracticeForGroup,PracticeForGroupAdmin)
admin.site.register(Material,MaterialAdmin)
# Register your models here.
