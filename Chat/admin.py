from django.contrib import admin
from .models import Group,Chat,GroupType,UserProfile
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    search_fields = ['message']
    list_display=['message','group','timestamp']
    list_filter = ['group__name']
    readonly_fields = ['message']

class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name','type']
    list_filter = ['type']
    list_display = ['name','type','member_count']

    def member_count(self,group_name):
        pass
        #return Group.objects.get(name=group_name).members.count()

class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ['type']
    
admin.site.register(Chat,ChatAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(GroupType,GroupTypeAdmin)
admin.site.register(UserProfile)

