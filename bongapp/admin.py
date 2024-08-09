from django.contrib import admin
# Register your models here.
from .models import Profile,Product,Booking,OrderModel,ChatGroup,Groupmessage
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','category','price']
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['product','customer','phone']
admin.site.register(Profile)
admin.site.register(Product,ProductAdmin)
admin.site.register(OrderModel,OrderModelAdmin)
admin.site.register(ChatGroup)
admin.site.register(Groupmessage)
admin.site.register(Booking)