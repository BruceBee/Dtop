from django.contrib import admin

# Register your models here.

from .models import *

class ItemsAdmin(admin.ModelAdmin):
	list_display = ('items_status','items_title','items_content','items_starter','items_owner','items_relater','create_time','finish_time','finish_info','start_time','end_time',)
	search_fields = ['items_status','items_title','items_content','items_starter','items_owner','items_relater','create_time','finish_time','finish_info','start_time','end_time',]
	list_filter =['items_status','items_title','items_content','items_starter','items_owner','items_relater','create_time','finish_time','finish_info','start_time','end_time',]


class HandleDetailAdmin(admin.ModelAdmin):
	list_display =('items_id','handle_time','handle_user','handle_info',)
	search_fields=['items_id','handle_time','handle_user','handle_info',]
	list_filter=['items_id','handle_time','handle_user','handle_info',]


admin.site.register(Items,ItemsAdmin)
admin.site.register(HandleDetail,HandleDetailAdmin)